{% raw %}
```javascript
/// @title IAmm
/// @notice The surface the publisher reads. Any AMM that can answer "what would
///         you trade right now, and what's the worst price you'd accept?" can be
///         published into CoW this way.
/// @dev Deliberately small. The publisher never needs to understand the pricing
///      logic behind these — only that `quote` is the floor the AMM stands
///      behind, and that `swap` will honor it.
interface IAmm {
  /// @notice The two tokens this AMM trades between.
  function tokenA() external view returns (IERC20);

  function tokenB() external view returns (IERC20);

  /// @notice The swap the AMM wants to make right now — the read-side mirror of
  ///         `swap`, and what the published order is built from.
  /// @return sellingTokenA True when the AMM wants to sell `tokenA`.
  /// @return sellAmount Sell-token amount (raw token units); 0 when no swap is
  ///         warranted, which the publisher treats as "nothing to publish".
  /// @return minBuyAmount Buy-token floor for `sellAmount` (raw token units).
  function previewSwap()
    external
    view
    returns (bool sellingTokenA, uint256 sellAmount, uint256 minBuyAmount);

  /// @notice Swaps `amountIn` of `tokenIn` at the AMM's own quote.
  /// @dev Called inside the settlement's pre-hook with the flash-borrowed
  ///      counter-leg. `minAmountOut` is the order's `sellAmount`, so a fill can
  ///      never be sourced for less than it commits to deliver.
  /// @param tokenIn Either `tokenA` or `tokenB`.
  /// @param amountIn Input amount (raw token units).
  /// @param minAmountOut Minimum output accepted (raw token units).
  /// @return amountOut Output delivered (raw token units).
  function swap(
    IERC20 tokenIn,
    uint256 amountIn,
    uint256 minAmountOut
  ) external returns (uint256 amountOut);

  /// @notice The AMM's floor value of `amountIn` of `tokenIn` in the other token
  ///         — unsized; the price-floor reference the order is checked against.
  /// @dev MUST scale with `amountIn`, since the publisher uses it to bound an
  ///      order whose size it did not choose.
  /// @param tokenIn Either `tokenA` or `tokenB`.
  /// @param amountIn Amount of `tokenIn` (raw token units).
  /// @return minOut Floor counter-token amount (raw token units).
  function quote(
    IERC20 tokenIn,
    uint256 amountIn
  ) external view returns (uint256 minOut);
}
```
{% endraw %}
