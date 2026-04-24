// Shared helpers for LETF blog charts
window.LETF = (function() {
  var FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif";
  var CLASS_COLORS = {
    'Equity Index':'#5b82d7','Equity Sector':'#9b7ad7','Single Stock':'#d09050',
    'Commodity':'#c47070','Fixed Income':'#53baa0','Country':'#e07840',
    'Crypto':'#5ea080','Currency':'#5ba0c0','Volatility':'#8090b0',
    'Factor':'#5090b0','Thematic':'#70b0a8','Other':'#8090b0'
  };
  var pct = function(v) { return v != null ? (v*100).toFixed(2)+'%' : '\u2014'; };
  var dollar = function(v) {
    if (v==null||isNaN(v)) return '\u2014';
    if (v>=1e9) return '$'+(v/1e9).toFixed(1)+'B';
    if (v>=1e6) return '$'+(v/1e6).toFixed(0)+'M';
    return '$'+v.toFixed(0);
  };
  var tooltip = document.getElementById('letf-tooltip');
  function showTooltip(e, f) {
    var cls = function(v) { return v!=null?(v>=0?'pos':'neg'):''; };
    var spotCagr = f.period_spot_cagr!=null?f.period_spot_cagr:f.spot_cagr;
    var rLr1 = (f.letf_cagr!=null&&spotCagr!=null)?f.letf_cagr-spotCagr:null;
    var row = function(l,v,c) { return '<div style="display:flex;justify-content:space-between;gap:16px"><span style="color:#757575">'+l+'</span><span style="color:'+(c==='pos'?'#2d7a4a':c==='neg'?'#b44':'#292929')+'">'+v+'</span></div>'; };
    tooltip.innerHTML = '<div style="font-size:14px;font-weight:700;color:#292929">'+f.ticker+' <span style="color:#757575;font-size:11px;font-weight:400">'+(f.multiplier||'')+'x</span></div>'+
      '<div style="color:#757575;font-size:11px;margin-bottom:4px">'+(f.name||'')+'</div>'+
      row('Asset Class',f.asset_class,'')+row('AUM',dollar(f.aum),'')+
      '<div style="border-top:1px solid #e6e6e6;margin:4px 0"></div>'+
      row('Spot \u03bc',pct(f.spot_mu),cls(f.spot_mu))+row('Spot \u03c3',pct(f.spot_sigma),'')+
      (f.letf_cagr!=null?row('LETF CAGR',pct(f.letf_cagr),cls(f.letf_cagr)):'')+
      (rLr1!=null?row('R(L)\u2212R(1)',pct(rLr1),cls(rLr1)):'')+
      '<div style="border-top:1px solid #e6e6e6;margin:4px 0"></div>'+
      (f.expense_ratio!=null?row('Expense Ratio',pct(f.expense_ratio),'neg'):'')+
      (f.financing_premium!=null?row('Financing Premium (s)',pct(f.financing_premium),f.financing_premium>0?'neg':''):'');
    var wasHidden = tooltip.style.opacity === '0' || tooltip.style.opacity === '';
    if (wasHidden) {
      // Position immediately without transition on first appear
      tooltip.style.transition='none';
      tooltip.style.left=(e.clientX+15)+'px';
      tooltip.style.top=(e.clientY+15)+'px';
      tooltip.offsetHeight; // force reflow
      tooltip.style.transition='opacity 0.25s ease, left 0.15s ease-out, top 0.15s ease-out';
    }
    tooltip.style.opacity='1';
    var r=tooltip.getBoundingClientRect();
    tooltip.style.left=(e.clientX+15+r.width>window.innerWidth?e.clientX-r.width-15:e.clientX+15)+'px';
    tooltip.style.top=(e.clientY+15+r.height>window.innerHeight?e.clientY-r.height-15:e.clientY+15)+'px';
  }
  function hideTooltip() { tooltip.style.opacity='0'; }
  return { FONT: FONT, CLASS_COLORS: CLASS_COLORS, pct: pct, dollar: dollar, showTooltip: showTooltip, hideTooltip: hideTooltip, funds: LETF_FUNDS };
})();
