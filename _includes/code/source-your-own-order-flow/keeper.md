{% raw %}
```typescript
/**
 * Keeper: polls the AMM, builds the order the swapper would sign, and posts it
 * to CoW's orderbook with the recipe a solver needs to settle it.
 *
 * The swapper holds no working capital: its sell side is created inside the
 * settlement, when the pre-hook draws the flash-borrowed counter-leg and hands
 * it to the AMM. Direction, `sellAmount` and the price floor all come off the
 * AMM's own `previewSwap` / `quote`, so what we post matches what the contract
 * would sign.
 *
 * Every field a solver could vary is bounded on-chain: the borrower pins the
 * lender, and the swapper's ERC-1271 pins the receiver, the pair and the price
 * floor. The preflight below runs that same `isValidSignature` before posting,
 * because the orderbook's rate limit is strict and a rejection is deterministic.
 */

const SETTLEMENT = '0x9008D19f58AAbD9eD0D60971565AA8510560ab41';
/// Morpho Blue — zero flash-loan premium, so repayment equals the principal.
const MORPHO = '0xBBBBBbbBBb9cC5e90e3b3Af64bdAF62C37EEFFCb';

const API = 'https://api.cow.fi/mainnet/api/v1';

/// GPv2Order.Data in EIP-712 field order — the ERC-1271 signature payload.
const ORDER_TUPLE =
  'tuple(address sellToken,address buyToken,address receiver,uint256 sellAmount,uint256 buyAmount,uint32 validTo,bytes32 appData,uint256 feeAmount,bytes32 kind,bool partiallyFillable,bytes32 sellTokenBalance,bytes32 buyTokenBalance)';

// Direction decides the pair: the AMM pays out the token the order sells and
// pulls the other one, which is the leg the loan funds.
const [sellingTokenA, sellAmount]: [boolean, bigint] = await amm.previewSwap();
if (sellAmount === 0n) throw new Error('AMM advertises no capacity');

const [sellTokenAddr, buyTokenAddr] = sellingTokenA
  ? [tokenAAddr, tokenBAddr]
  : [tokenBAddr, tokenAAddr];

// `buyAmount` is the swapper's own ERC-1271 floor. Quoting below it is rejected
// by `_checkOrder`, so it is read straight off the AMM.
const buyAmount: bigint = await amm.quote(sellTokenAddr, sellAmount);

// The draw is the flash-borrowed counter-leg the pre-hook hands the AMM,
// denominated in the buy token. The AMM swap must return at least `sellAmount`
// from it, and the fill must return at least the draw to repay the lender — so
// the draw sits between the two, and where exactly depends on the AMM leg's own
// loss, which differs by direction.
const loanAmount: bigint = args.loan ? BigInt(args.loan) : buyAmount;

// The pre-hook that sources the inventory, run by the solver inside the batch.
const hooks = {
  pre: [
    {
      target: swapperAddr,
      callData: swapper.interface.encodeFunctionData('provideInventory', [
        loanAmount,
        sellAmount,
        sellingTokenA,
      ]),
      gasLimit: '400000',
    },
  ],
  post: [],
};

// The execution recipe: which lender to draw from, which contract adapts the
// callback, and the hooks to run. CIP-66 lets a solver pick this up natively.
const appDataDoc = {
  version: '1.3.0',
  appCode: 'amm-cow-swapper',
  metadata: {
    flashloan: {
      liquidityProvider: MORPHO,
      protocolAdapter: borrowerAddr,
      receiver: borrowerAddr,
      token: buyTokenAddr,
      amount: loanAmount.toString(),
    },
    hooks,
  },
};
const appDataStr = JSON.stringify(appDataDoc);
const appDataHash = keccak256(toUtf8Bytes(appDataStr));

const order = {
  sellToken: sellTokenAddr,
  buyToken: buyTokenAddr,
  receiver: borrowerAddr,
  sellAmount: sellAmount.toString(),
  buyAmount: buyAmount.toString(),
  validTo,
  appData: appDataHash,
  feeAmount: '0',
  kind: 'sell',
  partiallyFillable: false,
  sellTokenBalance: 'erc20',
  buyTokenBalance: 'erc20',
};

const digest = TypedDataEncoder.hash(DOMAIN, ORDER_TYPE, order);

// ERC-1271: the swapper decodes this ABI-encoded order in isValidSignature.
// There is no private key anywhere — the contract IS the signer.
const signature = AbiCoder.defaultAbiCoder().encode(
  [ORDER_TUPLE],
  [
    [
      sellTokenAddr,
      buyTokenAddr,
      borrowerAddr,
      sellAmount,
      buyAmount,
      validTo,
      appDataHash,
      0n,
      keccak256(toUtf8Bytes('sell')),
      false,
      keccak256(toUtf8Bytes('erc20')),
      keccak256(toUtf8Bytes('erc20')),
    ],
  ]
);

// … preflight: borrower allowlists the swapper, floor covers the principal, the
//     AMM still offers this direction and size, relayer allowance stands, and
//     the swapper's own ERC-1271 accepts this exact order …

// POST /orders registers the appData document itself when `appData` carries the
// full JSON, so a separate PUT /app_data is redundant.
const res = await fetch(`${API}/orders`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    ...order,
    signingScheme: 'eip1271',
    signature,
    from: swapperAddr,
    appData: appDataStr,
    appDataHash,
  }),
});
```
{% endraw %}
