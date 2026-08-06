{% raw %}
```javascript
/// @notice One swap, from the vault's side of the trade: it takes `tokenInAmt`
///         of `tokenIn` and pays out `tokenOutAmt` of `tokenOut`.
struct SwapParams {
  // token the vault takes in
  IERC20 tokenIn;
  // token the vault pays out
  IERC20 tokenOut;
  // `tokenIn` handed to the vault (raw token units)
  uint256 tokenInAmt;
  // `tokenOut` it pays out for that (raw token units)
  uint256 tokenOutAmt;
}

/// @title ISwapVault
/// @notice A vault that swaps between two tokens with a whitelisted
///         counterparty: it quotes a size in each direction, judges a price,
///         and settles at the price the caller names.
interface ISwapVault {
  /// @notice Returns the two tokens the vault swaps between, ascending by
  ///         address.
  /// @return token0 The lower-addressed of the pair.
  /// @return token1 The higher-addressed one.
  function swapTokens() external view returns (IERC20 token0, IERC20 token1);

  /// @notice Sizes the swap the vault would settle now in each direction — the
  ///         read-side mirror of `swap`. Sides follow `swapTokens`.
  /// @return token0In What the vault takes `token0` in for, paying `token1` out.
  /// @return token1In The reverse: `token1` in, `token0` out.
  function swapCapacity()
    external
    view
    returns (SwapParams memory token0In, SwapParams memory token1In);

  /// @notice Swaps `s.tokenInAmt` of `s.tokenIn` for exactly `s.tokenOutAmt` of
  ///         `s.tokenOut`.
  /// @param s The swap to settle, from the vault's side of the trade.
  function swap(SwapParams calldata s) external;

  /// @notice Whether the vault will part with `s.tokenOutAmt` of `s.tokenOut`
  ///         for `s.tokenInAmt` of `s.tokenIn`, judged on rate alone.
  /// @param s The swap to price, from the vault's side of the trade.
  function isAcceptableSwap(SwapParams calldata s) external view returns (bool);
}
```
{% endraw %}
