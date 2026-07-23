{% raw %}
```javascript
/// @title IMorpho
/// @notice The Morpho Blue flash-loan surface.
/// @dev Morpho pushes `assets` to the caller, invokes `onMorphoFlashLoan`, then
///      pulls `assets` back by `transferFrom` — the caller must hold `assets` and
///      have approved Morpho by the time the callback returns. No premium:
///      `assets` in equals `assets` out.
interface IMorpho {
  /// @notice Flash-borrows `assets` of `token` to the caller.
  function flashLoan(
    address token,
    uint256 assets,
    bytes calldata data
  ) external;
}

/// @title MorphoFlashLoanRouter
/// @notice Sources Morpho Blue liquidity for a CoW settlement, lending it to an
///         allowlisted receiver for the duration and repaying itself.
/// @dev CoW's Borrower role for one lender (each lender's callback differs). What
///      makes it usable by a third party: completing the loan needs no
///      solver-authored settlement interactions — Morpho pushes the loan to its
///      caller, and the CoW order names this contract as `receiver`, so proceeds
///      land where Morpho is already approved to pull from.
/// @dev INVARIANT: holds no balance of the borrowed token between txs. It transits
///      within one settlement and any surplus is swept to the receiver that took
///      it. Not custody.
contract MorphoFlashLoanRouter is Ownable {
  using SafeERC20 for IERC20;

  /// @notice CoW flash-loan router, the only address that may borrow through us.
  address public immutable cowRouter;
  /// @notice Morpho Blue, the only lender this borrower accepts.
  address public immutable lender;

  /// @notice Contracts permitted to borrow through this router.
  mapping(address => bool) public isReceiver;

  /// @notice Token borrowed in the settlement currently in flight.
  /// @dev Transient: Morpho's callback reports `assets` but not the token.
  address private transient loanToken;
  /// @notice Receiver that took the loan in the settlement currently in flight.
  /// @dev Transient, and the sweep's destination. Written only by `takeLoan`, so
  ///      it can only ever name an allowlisted contract.
  address private transient activeReceiver;

  // … constructor, errors, events and `setReceiver` elided …

  /// @notice Takes a Morpho flash loan and hands control back to the CoW router.
  /// @dev `lender_`, `token` and `amount` come from the order's appData and are
  ///      solver-influenced. Pinning `lender_` keeps a solver from pointing this
  ///      contract at a lender of their choosing; an `amount` the settlement can't
  ///      return fails Morpho's pull and reverts, so it needs no bound. One loan
  ///      per settlement: the CoW router borrows a multi-loan array by nesting
  ///      each callback inside the last, which would overwrite the token and
  ///      receiver this one still needs on the way out.
  function flashLoanAndCallBack(
    address lender_,
    IERC20 token,
    uint256 amount,
    bytes calldata callBackData
  ) external {
    if (msg.sender != cowRouter) revert UnauthorizedCall();
    if (lender_ != lender) revert UnauthorizedCall();
    if (loanToken != address(0)) revert LoanInProgress();

    loanToken = address(token);
    IMorpho(lender_).flashLoan(address(token), amount, callBackData);
  }

  /// @notice Lends `amount` of the in-flight loan to the calling receiver.
  /// @dev Callable by an allowlisted receiver from its CoW pre-hook, the one frame
  ///      in a settlement where a receiver is `msg.sender`. The caller becomes the
  ///      sweep's destination; a second, different receiver is rejected so the
  ///      destination can't change mid-settlement.
  function takeLoan(uint256 amount) external {
    if (!isReceiver[msg.sender]) revert UnauthorizedCall();

    if (activeReceiver == address(0)) activeReceiver = msg.sender;
    else if (activeReceiver != msg.sender) revert UnauthorizedCall();

    IERC20(loanToken).safeTransfer(msg.sender, amount);
  }

  /// @notice Morpho's callback: runs the settlement, sweeps the surplus, then
  ///         authorizes repayment.
  /// @dev The settlement runs inside this call, so the receiver draws the loan and
  ///      the proceeds arrive before it returns. Reverts `LoanNotTaken` when
  ///      nothing drew the loan, since the surplus would then have no owner and no
  ///      way out. Morpho pulls immediately after, so an unreturned loan reverts
  ///      the transaction.
  function onMorphoFlashLoan(uint256 assets, bytes calldata data) external {
    if (msg.sender != lender) revert UnauthorizedCall();

    ICowFlashLoanRouter(cowRouter).borrowerCallBack(data);

    address dest = activeReceiver;
    if (dest == address(0)) revert LoanNotTaken();

    IERC20 token = IERC20(loanToken);
    uint256 held = token.balanceOf(address(this));
    if (held > assets) token.safeTransfer(dest, held - assets);

    token.forceApprove(lender, assets);
  }
}
```
{% endraw %}
