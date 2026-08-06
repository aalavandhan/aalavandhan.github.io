{% raw %}
```typescript
const SETTLEMENT = '0x9008D19f58AAbD9eD0D60971565AA8510560ab41';
const RELAYER = '0xC92E8bdf79f0507f65a392b0ab4667716BFE0110';
const MORPHO = '0xBBBBBbbBBb9cC5e90e3b3Af64bdAF62C37EEFFCb';

const API = 'https://api.cow.fi/mainnet/api/v1';

// The one contract you deploy for this vault. It is its own CoW Borrower, so it
// is also the order's receiver.
const brokerAddr = '0x…';

const ORDER_TUPLE =
  'tuple(address sellToken,address buyToken,address receiver,uint256 sellAmount,uint256 buyAmount,uint32 validTo,bytes32 appData,uint256 feeAmount,bytes32 kind,bool partiallyFillable,bytes32 sellTokenBalance,bytes32 buyTokenBalance)';

// The vault sizes at most one direction, and which one moves with its target, so
// read it live rather than assuming. It pays out what the order sells and takes
// in what the order buys — the leg the loan funds.
const [token0In, token1In] = await vault.swapCapacity();
const capacity = token0In.tokenOutAmt > 0n ? token0In : token1In;
const sellTokenAddr = getAddress(capacity.tokenOut);
const buyTokenAddr = getAddress(capacity.tokenIn);
const fullSell: bigint = capacity.tokenOutAmt;
const fullDraw: bigint = capacity.tokenInAmt;
if (fullSell === 0n) throw new Error('vault advertises no capacity');

// Orders are fill-or-kill — the loan is drawn in full in the pre-hook, so a
// partial fill couldn't repay it. Cap the slice to work a large rebalance as
// several self-contained orders.
let sellAmount = fullSell;
if (args.maxSell) {
  const cap = BigInt(args.maxSell);
  if (cap < sellAmount) sellAmount = cap;
}

// Mirrors `_buildOrder`: the order buys back the counter-leg the vault takes in,
// pro-rated when the slice is capped, so the fill covers the draw rather than
// only clearing the ERC-1271 gate.
const buyAmount: bigint = (fullDraw * sellAmount) / fullSell;

// The draw the pre-hook hands the vault — the same figure, so the fill repays it.
const loanAmount: bigint = args.loan ? BigInt(args.loan) : buyAmount;

// The pre-hook that sources the inventory, run by the solver inside the batch.
const hooks = {
  pre: [
    {
      target: brokerAddr,
      callData: broker.interface.encodeFunctionData('provideInventory', [
        buyTokenAddr,
        sellTokenAddr,
        loanAmount,
        sellAmount,
      ]),
      gasLimit: '400000',
    },
  ],
  post: [],
};

// The execution recipe: the lender to draw from, the borrower that adapts its
// callback and receives the funds, and the hooks. CIP-66 lets a solver pick
// this up natively.
const appDataDoc = {
  version: '1.3.0',
  appCode: 'amm-cow-broker',
  metadata: {
    flashloan: {
      liquidityProvider: MORPHO,
      protocolAdapter: brokerAddr,
      receiver: brokerAddr,
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
  receiver: brokerAddr,
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

// ERC-1271: the broker decodes this ABI-encoded order in isValidSignature.
// There's no private key anywhere — the contract IS the signer.
const signature = AbiCoder.defaultAbiCoder().encode(
  [ORDER_TUPLE],
  [
    [
      sellTokenAddr,
      buyTokenAddr,
      brokerAddr,
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

// … preflight: the broker is pinned to the lender named in appData, the buy
//     side clears `isAcceptableSwap`, the fill repays the draw, the vault still
//     offers this direction and size, the relayer allowance stands, and the
//     broker's ERC-1271 accepts this exact order …

// POST /orders registers the appData document itself when `appData` carries the
// full JSON, so a separate PUT /app_data is redundant.
const res = await fetch(`${API}/orders`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    ...order,
    signingScheme: 'eip1271',
    signature,
    from: brokerAddr,
    appData: appDataStr,
    appDataHash,
  }),
});
```
{% endraw %}
