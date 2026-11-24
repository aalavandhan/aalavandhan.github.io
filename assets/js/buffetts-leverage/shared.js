// Shared helpers for the buffetts-leverage charts (adapted from the carry-trade post's helpers). Colors come from CSS custom properties so the
// charts follow the blog's light/dark toggle without redrawing.
window.BLV = (function() {
  var FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif";

  // Series colors (same validated set as the carry-trade post: Berkshire orange, index blue, T-bills aqua), plus neutrals.
  var css = [
    ':root{--blv-brk:#d4581f;--blv-idx:#2a78d6;--blv-tbill:#14946a;--blv-other:#8a8a8a;',
    '--blv-grid:#eeede7;--blv-axis:#dddddd;}',
    ':root[data-theme=dark]{--blv-brk:#e0682e;--blv-idx:#3987e5;--blv-tbill:#199e70;--blv-other:#9a9a9a;',
    '--blv-grid:#26272b;--blv-axis:#3a3b40;}',
    '.blv-viz{position:relative;width:100%;margin:36px 0 40px;font-family:' + FONT + ';color:var(--page-text);}',
    // These charts take their colours from the theme, so on the dark page they sit on the page itself,
    // not on the light panel the site gives charts drawn only for light (_sass/_post.scss).
    ':root[data-theme=dark] .post-content > div.blv-viz[id]:has(svg){background:transparent;}',
    '.blv-viz svg{display:block;overflow:visible;}',
    '.blv-viz text{font-family:' + FONT + ';}',
    '.blv-controls{display:flex;flex-wrap:wrap;gap:8px 20px;align-items:center;margin:0 0 10px;font-size:13px;color:var(--page-muted);}',
    '.blv-controls label{display:flex;align-items:center;gap:8px;}',
    '.blv-seg{display:inline-flex;border:1px solid var(--ui-border);border-radius:6px;overflow:hidden;}',
    '.blv-seg button{font:inherit;font-size:12px;padding:4px 10px;border:0;background:var(--ui-surface);color:var(--page-muted);cursor:pointer;}',
    '.blv-seg button+button{border-left:1px solid var(--ui-border);}',
    '.blv-seg button.on{background:var(--ui-surface-active);color:var(--page-text);}',
    '.blv-legend{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:12px;color:var(--page-muted);margin:6px 0 0;}',
    '.blv-legend span{display:inline-flex;align-items:center;gap:6px;}',
    '.blv-legend i{display:inline-block;width:14px;height:3px;border-radius:2px;}',
    '#blv-tip{position:fixed;pointer-events:none;z-index:1000;opacity:0;background:var(--page-bg);',
    'border:1px solid var(--ui-border);border-radius:4px;padding:8px 12px;font-size:12px;line-height:1.5;',
    'font-family:' + FONT + ';color:var(--page-text);max-width:280px;box-shadow:0 2px 8px rgba(0,0,0,.08);',
    'transition:opacity .2s ease;}',
    '#blv-tip .k{color:var(--page-muted);}',
    '#blv-tip .row{display:flex;justify-content:space-between;gap:16px;}',
    '@media (prefers-reduced-motion: reduce){.blv-viz *{transition:none !important;}}'
  ].join('');
  var style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  var C = {
    brk: 'var(--blv-brk)', idx: 'var(--blv-idx)', tbill: 'var(--blv-tbill)', other: 'var(--blv-other)',
    text: 'var(--page-text)', muted: 'var(--page-muted)', grid: 'var(--blv-grid)', axis: 'var(--blv-axis)',
    surface: 'var(--page-bg)'
  };

  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function pct(v, d) { return v == null || isNaN(v) ? '—' : v.toFixed(d == null ? 1 : d) + '%'; }

  // Tooltip: one shared element. rows = [[label, value], ...]
  var tip;
  function showTip(e, title, rows) {
    if (!tip) { tip = document.createElement('div'); tip.id = 'blv-tip'; }
    // An open modal sits in the browser's top layer, above any z-index, so a tooltip for a chart
    // inside one has to live inside that dialog to be seen.
    var host = (e.target.closest && e.target.closest('dialog[open]')) || document.body;
    if (tip.parentNode !== host) host.appendChild(tip);
    tip.innerHTML = (title ? '<div style="font-weight:600;margin-bottom:2px">' + title + '</div>' : '') +
      (rows || []).map(function(r) {
        return '<div class="row"><span class="k">' + r[0] + '</span><span>' + r[1] + '</span></div>';
      }).join('');
    tip.style.opacity = '1';
    var b = tip.getBoundingClientRect();
    var x = e.clientX + 14, y = e.clientY + 14;
    if (x + b.width > window.innerWidth - 8) x = e.clientX - b.width - 14;
    if (y + b.height > window.innerHeight - 8) y = e.clientY - b.height - 14;
    tip.style.left = x + 'px';
    tip.style.top = y + 'px';
  }
  function hideTip() { if (tip) tip.style.opacity = '0'; }

  // An SVG frame inside a container. Returns {root, svg, g, w, h, iw, ih, m}.
  function frame(root, height, m) {
    m = m || { top: 16, right: 16, bottom: 36, left: 48 };
    var w = Math.max(280, root.clientWidth);
    var svg = d3.select(root).append('svg').attr('width', w).attr('height', height)
      .attr('viewBox', '0 0 ' + w + ' ' + height);
    var g = svg.append('g').attr('transform', 'translate(' + m.left + ',' + m.top + ')');
    return { root: root, svg: svg, g: g, w: w, h: height, m: m, iw: w - m.left - m.right, ih: height - m.top - m.bottom };
  }

  // Recessive axes and grid in the blog's style.
  function styleAxis(sel) {
    sel.select('.domain').style('stroke', C.axis);
    sel.selectAll('.tick line').style('stroke', C.axis);
    sel.selectAll('.tick text').style('fill', C.muted).attr('font-size', 11);
  }
  function xAxis(f, scale, ticks, fmt) {
    var a = f.g.append('g').attr('transform', 'translate(0,' + f.ih + ')')
      .call(d3.axisBottom(scale).ticks(ticks).tickFormat(fmt).tickSizeOuter(0));
    styleAxis(a);
    return a;
  }
  function yAxis(f, scale, ticks, fmt) {
    var a = f.g.append('g').call(d3.axisLeft(scale).ticks(ticks).tickFormat(fmt).tickSizeOuter(0));
    styleAxis(a);
    a.select('.domain').remove();
    return a;
  }
  function gridY(f, scale, ticks) {
    f.g.insert('g', ':first-child').selectAll('line').data(scale.ticks(ticks)).join('line')
      .attr('x1', 0).attr('x2', f.iw).attr('y1', scale).attr('y2', scale)
      .style('stroke', C.grid).attr('stroke-width', 0.7);
  }
  function label(f, x, y, text, opts) {
    opts = opts || {};
    return f.g.append('text').attr('x', x).attr('y', y).text(text)
      .attr('text-anchor', opts.anchor || 'start').attr('font-size', opts.size || 12)
      .attr('font-weight', opts.weight || 400).style('fill', opts.fill || C.muted);
  }

  // Controls row at the top of a chart's root. Call it before frame() so it sits above the SVG.
  // The root is cleared on resize, so keep control state in variables outside draw().
  function controls(root) {
    var row = document.createElement('div');
    row.className = 'blv-controls';
    root.appendChild(row);
    return row;
  }
  function segmented(row, options, value, onChange) {
    var seg = document.createElement('div');
    seg.className = 'blv-seg';
    options.forEach(function(opt) {
      var b = document.createElement('button');
      b.type = 'button'; b.textContent = opt[1];
      if (opt[0] === value) b.className = 'on';
      b.addEventListener('click', function() {
        seg.querySelectorAll('button').forEach(function(x) { x.className = ''; });
        b.className = 'on';
        onChange(opt[0]);
      });
      seg.appendChild(b);
    });
    row.appendChild(seg);
    return seg;
  }
  function legend(root, items) {
    var el = document.createElement('div');
    el.className = 'blv-legend';
    el.innerHTML = items.map(function(it) {
      var mark = it.dash
        ? '<i style="background:repeating-linear-gradient(90deg,' + it.color + ' 0 5px,transparent 5px 8px)"></i>'
        : '<i style="background:' + it.color + (it.box ? ';height:10px;width:10px;border-radius:2px' : '') + '"></i>';
      return '<span>' + mark + it.label + '</span>';
    }).join('');
    root.appendChild(el);
    return el;
  }

  // Run once when the element scrolls into view (animations start there).
  function onView(el, cb) {
    if (!('IntersectionObserver' in window)) { cb(); return; }
    var io = new IntersectionObserver(function(es) {
      if (es[0].isIntersecting) { io.disconnect(); cb(); }
    }, { threshold: 0.3 });
    io.observe(el);
  }

  // Mount a chart: draw(root) builds it; it's redrawn when the width changes.
  function mount(id, draw) {
    function go() {
      var root = document.getElementById(id);
      if (!root || !window.d3) return;
      var last = 0, timer;
      function render() {
        var w = root.clientWidth;
        if (!w || w === last) return;   // hidden (e.g. in a closed modal): draw on the resize that opening fires
        last = w;
        root.innerHTML = '';
        draw(root);
      }
      render();
      // In a modal, draw the moment it opens (see _layouts/post.html).
      var dlg = root.closest('dialog');
      if (dlg) dlg.addEventListener('modal:open', render);
      window.addEventListener('resize', function() { clearTimeout(timer); timer = setTimeout(render, 150); });
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go();
  }

  return {
    FONT: FONT, C: C, reduced: reduced, pct: pct, showTip: showTip, hideTip: hideTip,
    frame: frame, xAxis: xAxis, yAxis: yAxis, gridY: gridY, label: label,
    controls: controls, segmented: segmented, legend: legend, onView: onView, mount: mount,
    data: window.BLV_DATA
  };
})();
