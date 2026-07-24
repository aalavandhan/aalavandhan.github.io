{% raw %}
```javascript
/// @title IMorpho
/// @notice The Morpho Blue flash-loan surface.
/// @dev Morpho pushes `assets` to the caller, invokes `onMorphoFlashLoan`, then
///      pulls `assets` back — the caller must hold and have approved `assets` by
///      the time the callback returns. No premium: in equals out.
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
///         allowlisted receiver for the settlement and repaying itself.
/// @dev CoW's Borrower role for one lender. Usable by a third party because
///      completing the loan needs no solver-authored interactions: Morpho pushes
///      the loan to its caller, and the CoW order names this contract as
///      `receiver`, so proceeds land where Morpho is already approved to pull.
/// @dev INVARIANT: never holds the borrowed token between txs — it transits one
///      settlement and any surplus is swept to the receiver. Not custody.
contract MorphoFlashLoanRouter is Ownable {
  using SafeERC20 for IERC20;

  /// @notice CoW flash-loan router, the only address that may borrow through us.
  address public immutable cowRouter;
  /// @notice Morpho Blue, the only lender this borrower accepts.
  address public immutable lender;

  /// @notice Contracts permitted to borrow through this router.
  mapping(address => bool) public isReceiver;

  /// @notice Token borrowed in the in-flight settlement.
  /// @dev Transient: Morpho's callback reports `assets` but not the token.
  address private transient loanToken;
  /// @notice Receiver that took the in-flight loan, and the sweep's destination.
  /// @dev Transient. Written only by `takeLoan`, so it can only ever name an
  ///      allowlisted contract.
  address private transient activeReceiver;

  // … constructor, errors, events and `setReceiver` elided …

  /// @notice Takes a Morpho flash loan and hands control back to the CoW router.
  /// @dev `lender_`, `token` and `amount` come from the order's appData and are
  ///      solver-influenced. Pinning `lender_` stops a solver from pointing us at
  ///      their own lender; an `amount` the settlement can't repay fails Morpho's
  ///      pull, so it needs no bound. One loan per settlement — nested callbacks
  ///      would overwrite the token and receiver this one still needs on exit.
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
  /// @dev Callable by an allowlisted receiver from its CoW pre-hook — the one
  ///      frame where a receiver is `msg.sender`. The caller becomes the sweep's
  ///      destination; a different second receiver is rejected so it can't change
  ///      mid-settlement.
  function takeLoan(uint256 amount) external {
    if (!isReceiver[msg.sender]) revert UnauthorizedCall();

    if (activeReceiver == address(0)) activeReceiver = msg.sender;
    else if (activeReceiver != msg.sender) revert UnauthorizedCall();

    IERC20(loanToken).safeTransfer(msg.sender, amount);
  }

  /// @notice Morpho's callback: runs the settlement, sweeps the surplus, then
  ///         authorizes repayment.
  /// @dev The settlement runs inside this call, so the receiver draws the loan and
  ///      the proceeds arrive before it returns. Reverts `LoanNotTaken` if nothing
  ///      drew the loan (the surplus would have no owner). Morpho pulls right
  ///      after, so an unreturned loan reverts the tx.
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
