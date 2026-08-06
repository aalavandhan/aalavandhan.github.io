{% raw %}
```javascript
interface IMorpho {
  function flashLoan(
    address token,
    uint256 assets,
    bytes calldata data
  ) external;
}

contract Broker is IConditionalOrder, IERC1271 {
  using SafeERC20 for IERC20;

  bytes4 internal constant MAGIC_VALUE = IERC1271.isValidSignature.selector;

  bytes32 public constant SALT_TOKEN0_IN = keccak256('Broker.token0In');
  bytes32 public constant SALT_TOKEN1_IN = keccak256('Broker.token1In');

  uint32 public constant VALID_TO_BUFFER_SEC = 30 minutes;

  ISwapVault public immutable vault;
  IERC20 public immutable token0;
  IERC20 public immutable token1;

  // … remaining immutables, errors and modifiers elided …

  address private transient _loanToken;
  uint256 private transient _loanAmount;

  constructor(/* … */) {
    // … wiring and standing approvals to the vault and CoW's relayer elided …

    composableCow_.create(
      ConditionalOrderParams({
        handler: IConditionalOrder(address(this)),
        salt: SALT_TOKEN0_IN,
        staticInput: abi.encode(token0_)
      }),
      true
    );
    composableCow_.create(
      ConditionalOrderParams({
        handler: IConditionalOrder(address(this)),
        salt: SALT_TOKEN1_IN,
        staticInput: abi.encode(token1_)
      }),
      true
    );
  }

  // -------------------------------------------------------------------------
  // Pokes — permissionless

  function settleToVault(IERC20 token) public {
    uint256 bal = token.balanceOf(address(this));
    if (bal > 0) token.safeTransfer(address(vault), bal);
  }

  // -------------------------------------------------------------------------
  // Settlement — CoW borrower

  function flashLoanAndCallBack(
    address lender_,
    IERC20 token,
    uint256 amount,
    bytes calldata callBackData
  ) external onlyCowRouter onlyPinnedLender(lender_) whenNoLoanInFlight {
    _loanToken = address(token);
    _loanAmount = amount;

    IMorpho(lender).flashLoan(address(token), amount, callBackData);
    settleToVault(token0);
    settleToVault(token1);

    _loanToken = address(0);
    _loanAmount = 0;
  }

  function onMorphoFlashLoan(
    uint256 assets,
    bytes calldata data
  ) external onlyLender {
    if (assets > _loanAmount) revert UnexpectedLoanAmount();

    ICowFlashLoanRouter(cowRouter).borrowerCallBack(data);
    IERC20(_loanToken).forceApprove(lender, _loanAmount);
  }

  // -------------------------------------------------------------------------
  // Settlement — pre-hook

  function provideInventory(
    IERC20 tokenIn,
    IERC20 tokenOut,
    uint256 tokenInAmt,
    uint256 tokenOutAmt
  ) external onlyTrampoline whenLoanInFlight {
    vault.swap(
      SwapParams({
        tokenIn: tokenIn,
        tokenOut: tokenOut,
        tokenInAmt: tokenInAmt,
        tokenOutAmt: tokenOutAmt
      })
    );
  }

  // -------------------------------------------------------------------------
  // ERC-1271 — authorize the fill

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
  // ComposableCoW handler — discovery

  function getTradeableOrder(
    address /* owner */,
    address /* sender */,
    bytes32 /* ctx */,
    bytes calldata staticInput,
    bytes calldata offchainInput
  ) external view returns (GPv2Order.Data memory order) {
    bytes32 appData = offchainInput.length > 0
      ? abi.decode(offchainInput, (bytes32))
      : bytes32(0);

    order = _buildOrder(appData, _decodeTokenIn(staticInput));

    if (order.sellAmount <= 0 || order.buyAmount <= 0) {
      revert InvalidOrder('no capacity');
    }
  }

  function verify(
    address /* owner */,
    address /* sender */,
    bytes32 /* hash */,
    bytes32 /* domainSeparator */,
    bytes32 /* ctx */,
    bytes calldata staticInput,
    bytes calldata /* offchainInput */,
    GPv2Order.Data calldata order
  ) external view {
    if (order.buyToken != _decodeTokenIn(staticInput)) {
      revert InvalidOrder('direction');
    }

    _checkOrder(order);
  }

  // -------------------------------------------------------------------------
  // Internal

  function _checkOrder(GPv2Order.Data memory order) internal view {
    if (order.receiver != address(this)) revert InvalidOrder('receiver');

    if (order.kind != GPv2Order.KIND_SELL) revert InvalidOrder('kind');
    if (order.partiallyFillable) revert InvalidOrder('partial');
    if (order.feeAmount > 0) revert InvalidOrder('fee');
    if (order.validTo < block.timestamp) revert InvalidOrder('expired');
    if (
      order.sellTokenBalance != GPv2Order.BALANCE_ERC20 ||
      order.buyTokenBalance != GPv2Order.BALANCE_ERC20
    ) revert InvalidOrder('balance');

    // … token-pair check elided …

    if (
      !vault.isAcceptableSwap(
        SwapParams({
          tokenIn: order.buyToken,
          tokenOut: order.sellToken,
          tokenInAmt: order.buyAmount,
          tokenOutAmt: order.sellAmount
        })
      )
    ) {
      revert InvalidOrder('price');
    }
  }

  function _decodeTokenIn(
    bytes calldata staticInput
  ) internal view returns (IERC20 takes) {
    if (staticInput.length != 32) revert InvalidOrder('direction');
    takes = IERC20(abi.decode(staticInput, (address)));
    if (takes != token0 && takes != token1) revert InvalidOrder('direction');
  }

  function _buildOrder(
    bytes32 appData,
    IERC20 takes
  ) internal view returns (GPv2Order.Data memory order) {
    (SwapParams memory token0In, SwapParams memory token1In) = vault
      .swapCapacity();
    SwapParams memory s = takes == token0 ? token0In : token1In;

    order = GPv2Order.Data({
      sellToken: s.tokenOut,
      buyToken: s.tokenIn,
      receiver: address(this),
      sellAmount: s.tokenOutAmt,
      buyAmount: s.tokenInAmt,
      validTo: uint32(block.timestamp + VALID_TO_BUFFER_SEC),
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
