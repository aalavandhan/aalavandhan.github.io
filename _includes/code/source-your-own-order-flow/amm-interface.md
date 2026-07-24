{% raw %}
```javascript
/// @title IAmm
/// @notice The surface the publisher reads. Any AMM that can answer "what would
///         you trade right now, and what's the worst price you'd accept?" can be
///         published into CoW this way.
/// @dev Deliberately small: the publisher never touches the pricing logic, only
///      trusts that `quote` is a floor the AMM stands behind and `swap` honors.
///      All amounts are raw token units.
interface IAmm {
  /// @notice The two tokens this AMM trades between.
  function tokenA() external view returns (IERC20);

  function tokenB() external view returns (IERC20);

  /// @notice The swap the AMM wants right now — the read-side mirror of `swap`,
  ///         and what the published order is built from.
  /// @return sellingTokenA True when the AMM wants to sell `tokenA`.
  /// @return sellAmount Sell-token amount; 0 means nothing to publish.
  /// @return minBuyAmount Buy-token floor for `sellAmount`.
  function previewSwap()
    external
    view
    returns (bool sellingTokenA, uint256 sellAmount, uint256 minBuyAmount);

  /// @notice Swaps `amountIn` of `tokenIn` at the AMM's own quote.
  /// @dev Called in the settlement pre-hook with the flash-borrowed counter-leg.
  ///      `minAmountOut` is the order's `sellAmount`, so a fill can never be
  ///      sourced for less than it commits to deliver.
  function swap(
    IERC20 tokenIn,
    uint256 amountIn,
    uint256 minAmountOut
  ) external returns (uint256 amountOut);

  /// @notice The AMM's floor value of `amountIn` of `tokenIn` in the other token
  ///         — the unsized price reference the order is checked against.
  /// @dev MUST scale with `amountIn`: the publisher uses it to bound an order
  ///      whose size it did not choose.
  function quote(
    IERC20 tokenIn,
    uint256 amountIn
  ) external view returns (uint256 minOut);
}
```
{% endraw %}
