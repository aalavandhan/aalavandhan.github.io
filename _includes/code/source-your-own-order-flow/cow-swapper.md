{% raw %}
```javascript
/// @title AmmCowPublisher
/// @notice Publishes an AMM's own intent to trade into CoW Protocol: signs
///         fill-or-kill orders via ERC-1271, sources the sell inventory from the
///         AMM against a flash-borrowed counter-leg, and returns what it captures.
/// @dev Holds no working capital — the counter-leg is borrowed per settlement and
///      the fill repays it in the same tx; an unrepayable draw reverts the batch.
/// @dev The price floor (`_checkOrder`) only prevents a drain: it caps a
///      solver-authored fill at the AMM's own `quote`. It never captures surplus
///      — this contract reads the AMM, not the market, so routing surplus is the
///      batch auction's job.
contract AmmCowPublisher is IConditionalOrder, IERC1271, Ownable {
  /// @notice ERC-1271 "signature valid" magic value.
  bytes4 internal constant MAGIC_VALUE = IERC1271.isValidSignature.selector;

  /// @notice Fixed salt for the one ComposableCoW registration.
  bytes32 public constant SALT = keccak256('AmmCowPublisher');

  /// @notice The AMM being published.
  IAmm public amm;

  /// @notice Borrower the pre-hook draws the counter-leg from, and the order's
  ///         `receiver`. Must have allowlisted this contract via `setReceiver`,
  ///         since that is where the lender pulls repayment from.
  FlashLoanRouter public flashRouter;

  // … remaining storage, errors and modifiers elided …

  constructor(/* … */) Ownable(msg.sender) {
    // … wiring and standing relayer approvals elided …

    // Register the order once. From here it is discoverable by the orderbook —
    // no listing, no connector, no approval.
    composableCow_.create(
      ConditionalOrderParams({
        handler: IConditionalOrder(address(this)),
        salt: SALT,
        staticInput: ''
      }),
      true
    );
  }

  // -------------------------------------------------------------------------
  // ComposableCoW handler — discovery

  /// @inheritdoc IConditionalOrder
  /// @dev Builds the order from `amm.previewSwap()`, stamping `appData` from
  ///      `offchainInput`. Reverts `InvalidOrder` when no swap is warranted.
  function getTradeableOrder(
    address /* owner */,
    address /* sender */,
    bytes32 /* ctx */,
    bytes calldata /* staticInput */,
    bytes calldata offchainInput
  ) external view returns (GPv2Order.Data memory order) {
    bytes32 appData = offchainInput.length > 0
      ? abi.decode(offchainInput, (bytes32))
      : bytes32(0);

    order = _buildOrder(appData);

    if (order.sellAmount <= 0 || order.buyAmount <= 0) {
      revert InvalidOrder('no capacity');
    }
  }

  // -------------------------------------------------------------------------
  // Settlement participation — pre-hook

  /// @notice Pre-hook: draws the flash-borrowed counter-leg and sources the
  ///         order's `sellAmount` of inventory from the AMM against it.
  /// @dev Trampoline-only. Every arg is solver-supplied but bounded: the AMM swap
  ///      gates `inputAmount` by direction, capacity and min-out, and the lender
  ///      reverts a draw the fill can't repay.
  /// @dev Returns prior settlements' surplus to the AMM first (`_settleToAmm`), so
  ///      only this settlement's inventory is left to pull. MUST precede
  ///      `takeLoan`, or the sweep would take the borrowed counter-leg.
  function provideInventory(
    uint256 inputAmount,
    uint256 sellAmount,
    bool sellingTokenA
  ) external onlyTrampoline {
    _settleToAmm();

    flashRouter.takeLoan(inputAmount);

    IERC20 tokenIn = sellingTokenA ? amm.tokenB() : amm.tokenA();
    tokenIn.forceApprove(address(amm), inputAmount);
    amm.swap(tokenIn, inputAmount, sellAmount);
  }

  // -------------------------------------------------------------------------
  // ERC-1271 — authorize the fill

  /// @inheritdoc IERC1271
  /// @dev `signature` is the ABI-encoded order, bound to `hash` so no other order
  ///      can be authorized, then gated by `_checkOrder`.
  function isValidSignature(
    bytes32 hash,
    bytes calldata signature
  ) external view returns (bytes4) {
    GPv2Order.Data memory order = abi.decode(signature, (GPv2Order.Data));
    if (GPv2Order.hash(order, settlement.domainSeparator()) != hash) {
      revert InvalidOrder('hash');
    }
    _checkOrder(order);
    return MAGIC_VALUE;
  }

  // -------------------------------------------------------------------------
  // Internal

  /// @dev Pins every solver-variable order field. Structural: receiver, fill-or-
  ///      kill sell, zero fee, unexpired, plain ERC20 balances, the AMM pair.
  ///      Price: `buyAmount` at or above the AMM's `quote` for `sellAmount`.
  /// @dev The floor is the only on-chain price gate. The signature isn't bound to
  ///      what the keeper posted, so without it a solver could self-author a
  ///      `buyAmount ≈ 0` order and drain the sourced inventory; `quote` scales
  ///      the floor with `sellAmount`, capping the worst fill at the AMM's rate.
  /// @dev Reads only the order and `block.timestamp`, never settlement state, so
  ///      the orderbook's submission `eth_call` accepts a well-formed order and it
  ///      stays acceptable until it expires.
  function _checkOrder(GPv2Order.Data memory order) internal view {
    if (order.receiver != address(flashRouter)) revert InvalidOrder('receiver');

    if (order.kind != GPv2Order.KIND_SELL) revert InvalidOrder('kind');
    if (order.partiallyFillable) revert InvalidOrder('partial');
    if (order.feeAmount > 0) revert InvalidOrder('fee');
    if (order.validTo < block.timestamp) revert InvalidOrder('expired');

    // … token-pair and balance-kind checks elided …

    if (order.buyAmount < amm.quote(order.sellToken, order.sellAmount)) {
      revert InvalidOrder('price');
    }
  }

  /// @dev Fill-or-kill sell, sized and floored by `amm.previewSwap()`. It enters
  ///      the batch as a market order with the AMM's quote as its floor: a solver
  ///      may fill it better, never worse.
  function _buildOrder(
    bytes32 appData
  ) internal view returns (GPv2Order.Data memory order) {
    (bool sellingTokenA, uint256 sellAmount, uint256 buyAmount) = amm
      .previewSwap();

    (IERC20 sellToken, IERC20 buyToken) = sellingTokenA
      ? (amm.tokenA(), amm.tokenB())
      : (amm.tokenB(), amm.tokenA());

    order = GPv2Order.Data({
      sellToken: sellToken,
      buyToken: buyToken,
      receiver: address(flashRouter),
      sellAmount: sellAmount,
      buyAmount: buyAmount,
      validTo: uint32(block.timestamp + validToBufferSec),
      appData: appData,
      feeAmount: 0,
      kind: GPv2Order.KIND_SELL,
      partiallyFillable: false,
      sellTokenBalance: GPv2Order.BALANCE_ERC20,
      buyTokenBalance: GPv2Order.BALANCE_ERC20
    });
  }
}
```
{% endraw %}
