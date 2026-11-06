// Chart 6: the leverage landscape as a table. Each way to get levered bitcoin, with its leverage range,
// cost at 2× per dollar of your own money, liquidation risk and whether it needs active management. Jr's row is highlighted.
(function() {
  var J = window.JPC;
  // Costs at 2×, per dollar of your own money.
  var LOAN_LO = 7, LOAN_HI = 13, L = 2;
  var range = function(lo, hi, d) { return lo.toFixed(d) + '–' + hi.toFixed(d) + '%'; };

  var INSTR = [
    // Option leverage (delta × spot / premium) depends on strike: deep in the money ~1.5–2×, at the money ~5×, out of the money 20×+.
    { key: 'calls', name: 'Options', color: 'other', lev: '1.5–20×', liq: 'No', upkeep: 'Yes',
      cost: '14–24%' },
    { key: 'letf', name: 'LETF', color: 'other', lev: '2–3×', liq: 'No', upkeep: 'No',
      // Supplement: crypto LETF premiums s = 11–17%; cost at 2× = r_f (3.5%) + s + expense ratio (~0.9–1.9%).
      cost: '15–22%' },
    { key: 'perp', name: 'Perp long', color: 'perp', lev: '1–125×', liq: 'Yes', upkeep: 'Yes',
      // Funding on the full 2× notional, from ~5% (Binance's 2025 average) to 9.1% (Hyperliquid, month one).
      cost: range(L * 5, L * 9.1, 0) },
    { key: 'loan', name: 'Margin loan', color: 'margin', lev: '1–2×', liq: 'Yes', upkeep: 'Yes',
      cost: range((L - 1) * LOAN_LO, (L - 1) * LOAN_HI, 0) },
    { key: 'jr', name: '2factor Jr', color: 'jr', lev: '1–3×', liq: 'No', upkeep: 'No',
      // At 2× Jr borrows $1 of Sr per dollar, so it pays Sr's yield: ~5% by design (supplement), ~7.7% in month one.
      cost: '5–8%' }
  ];

  J.mount('jpc-landscape', function(root) {
    // Each row spans the grid as a subgrid, so Jr's row can carry its own box.
    var table = document.createElement('div');
    table.style.cssText = 'display:grid;grid-template-columns:1.2fr 1.1fr .9fr .7fr 1.2fr;column-gap:12px;row-gap:2px;font-size:13px;';
    root.appendChild(table);
    var ROW = 'grid-column:1/-1;display:grid;grid-template-columns:subgrid;padding:5px 8px;border:1px solid transparent;border-radius:6px;';
    var head = '<div style="' + ROW + 'color:var(--page-muted);border-bottom:1px solid var(--ui-border);border-radius:0">' +
      ['Instrument', 'Leverage', 'Cost at 2×', 'Liquidation', 'Active management'].map(function(h) { return '<div>' + h + '</div>'; }).join('') + '</div>';
    table.innerHTML = head + INSTR.map(function(i) {
      var box = i.key === 'jr' ? 'background:color-mix(in srgb, ' + J.C.jr + ' 10%, transparent);border-color:color-mix(in srgb, ' + J.C.jr + ' 45%, transparent);font-weight:600;' : i.key === 'perp' ? 'font-weight:600;' : '';   // Jr boxed; perps, the section's subject, in bold
      return '<div style="' + ROW + box + '"><div><i style="display:inline-block;width:8px;height:8px;border-radius:2px;margin-right:6px;background:' + J.C[i.color] + '"></i>' + i.name + '</div>' +
        '<div style="color:var(--page-muted)">' + i.lev + '</div>' +
        '<div style="font-variant-numeric:tabular-nums' + (i.muted ? ';color:var(--page-muted)' : '') + '">' + i.cost + '</div>' +
        '<div>' + i.liq + '</div><div>' + i.upkeep + '</div></div>';
    }).join('');
  });
})();
