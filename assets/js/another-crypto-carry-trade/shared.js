// Shared helpers for the another-crypto-carry-trade charts. Colors come from CSS custom properties so the
// charts follow the blog's light/dark toggle without redrawing.
window.JPC = (function() {
  var FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif";

  // Series colors (validated as a set: Jr blue, perp orange, margin aqua), plus neutrals.
  var css = [
    ':root{--jpc-jr:#2a78d6;--jpc-perp:#d4581f;--jpc-margin:#14946a;--jpc-other:#8a8a8a;',
    '--jpc-grid:#eeede7;--jpc-axis:#dddddd;--jpc-fill:rgba(42,120,214,0.10);--jpc-fill-perp:rgba(212,88,31,0.10);}',
    ':root[data-theme=dark]{--jpc-jr:#3987e5;--jpc-perp:#e0682e;--jpc-margin:#199e70;--jpc-other:#9a9a9a;',
    '--jpc-grid:#26272b;--jpc-axis:#3a3b40;--jpc-fill:rgba(57,135,229,0.16);--jpc-fill-perp:rgba(224,104,46,0.16);}',
    '.jpc-viz{position:relative;width:100%;margin:36px 0 40px;font-family:' + FONT + ';color:var(--page-text);}',
    '.jpc-viz svg{display:block;overflow:visible;}',
    '.jpc-viz text{font-family:' + FONT + ';}',
    '.jpc-controls{display:flex;flex-wrap:wrap;gap:8px 20px;align-items:center;margin:0 0 10px;font-size:13px;color:var(--page-muted);}',
    '.jpc-controls label{display:flex;align-items:center;gap:8px;}',
    '.jpc-controls input[type=range]{width:140px;accent-color:var(--jpc-jr);}',
    '.jpc-controls output{min-width:44px;color:var(--page-text);font-variant-numeric:tabular-nums;}',
    '.jpc-seg{display:inline-flex;border:1px solid var(--ui-border);border-radius:6px;overflow:hidden;}',
    '.jpc-seg button{font:inherit;font-size:12px;padding:4px 10px;border:0;background:var(--ui-surface);color:var(--page-muted);cursor:pointer;}',
    '.jpc-seg button+button{border-left:1px solid var(--ui-border);}',
    '.jpc-seg button.on{background:var(--ui-surface-active);color:var(--page-text);}',
    '.jpc-btn{font:inherit;font-size:12px;padding:4px 12px;border:1px solid var(--ui-border);border-radius:6px;background:var(--ui-surface);color:var(--page-text);cursor:pointer;}',
    '.jpc-legend{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:12px;color:var(--page-muted);margin:6px 0 0;}',
    '.jpc-legend span{display:inline-flex;align-items:center;gap:6px;}',
    '.jpc-legend i{display:inline-block;width:14px;height:3px;border-radius:2px;}',
    '#jpc-tip{position:fixed;pointer-events:none;z-index:1000;opacity:0;background:var(--page-bg);',
    'border:1px solid var(--ui-border);border-radius:4px;padding:8px 12px;font-size:12px;line-height:1.5;',
    'font-family:' + FONT + ';color:var(--page-text);max-width:280px;box-shadow:0 2px 8px rgba(0,0,0,.08);',
    'transition:opacity .2s ease;}',
    '#jpc-tip .k{color:var(--page-muted);}',
    '#jpc-tip .row{display:flex;justify-content:space-between;gap:16px;}',
    '@media (prefers-reduced-motion: reduce){.jpc-viz *{transition:none !important;}}'
  ].join('');
  var style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  var C = {
    jr: 'var(--jpc-jr)', perp: 'var(--jpc-perp)', margin: 'var(--jpc-margin)', other: 'var(--jpc-other)',
    text: 'var(--page-text)', muted: 'var(--page-muted)', grid: 'var(--jpc-grid)', axis: 'var(--jpc-axis)',
    surface: 'var(--page-bg)', fill: 'var(--jpc-fill)', fillPerp: 'var(--jpc-fill-perp)'
  };

  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function pct(v, d) { return v == null || isNaN(v) ? '—' : v.toFixed(d == null ? 1 : d) + '%'; }
  function usd(v, d) { return '$' + v.toFixed(d == null ? 0 : d); }

  // Tooltip: one shared element. rows = [[label, value], ...]
  var tip;
  function showTip(e, title, rows) {
    if (!tip) { tip = document.createElement('div'); tip.id = 'jpc-tip'; }
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
    row.className = 'jpc-controls';
    root.appendChild(row);
    return row;
  }
  function slider(row, o) {
    var lab = document.createElement('label');
    lab.innerHTML = '<span>' + o.label + '</span>';
    var input = document.createElement('input');
    input.type = 'range'; input.min = o.min; input.max = o.max; input.step = o.step; input.value = o.value;
    var out = document.createElement('output');
    out.textContent = o.format(+o.value);
    input.addEventListener('input', function() { out.textContent = o.format(+input.value); o.onInput(+input.value); });
    lab.appendChild(input); lab.appendChild(out); row.appendChild(lab);
    return input;
  }
  function segmented(row, options, value, onChange) {
    var seg = document.createElement('div');
    seg.className = 'jpc-seg';
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
    el.className = 'jpc-legend';
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

  // A square, auto-advancing explainer. scenes = [{ text, show: function(ctx, dur) }].
  // build(ctx) draws the static parts once; each scene's show() morphs elements to its state
  // with transitions of length dur (0 when jumping or when motion is reduced). Advances while
  // the frame is on screen and holds when it is not.
  var storyCss = document.createElement('style');
  storyCss.textContent =
    '.jpc-story{position:relative;margin:0 auto;border:1px solid var(--ui-border);border-radius:10px;background:var(--ui-surface);overflow:hidden;}' +
    '.jpc-story .cap{position:absolute;left:28px;right:28px;bottom:22px;min-height:42px;display:flex;align-items:flex-end;justify-content:center;text-align:center;font-size:14px;line-height:1.5;color:var(--page-muted);transition:opacity .45s ease;}' +
    '.jpc-story .bar{position:absolute;left:0;bottom:0;height:2px;background:var(--page-muted);opacity:.35;width:0;}';
  document.head.appendChild(storyCss);

  function story(root, o) {
    var S = Math.min(root.clientWidth, o.max || 560);
    var box = document.createElement('div');
    box.className = 'jpc-story';
    box.style.width = S + 'px'; box.style.height = S + 'px';
    root.appendChild(box);
    var cap = document.createElement('div'); cap.className = 'cap'; box.appendChild(cap);
    var svg = d3.select(box).append('svg').attr('width', S).attr('height', S).style('position', 'absolute').style('left', 0).style('top', 0);
    var bar = document.createElement('div'); bar.className = 'bar'; box.appendChild(bar);
    var ctx = { svg: svg, g: svg.append('g'), S: S, box: box };
    if (o.build) o.build(ctx);

    // Plays on its own while the frame is on screen, and holds when it isn't.
    var st = o.state || (o.state = { i: 0 });
    var timer = null, visible = false, every = o.every || 5200;

    function sync() {
      if (timer) { clearTimeout(timer); timer = null; }
      bar.style.transition = 'none'; bar.style.width = '0';
      if (visible) {
        bar.offsetWidth;
        bar.style.transition = 'width ' + every + 'ms linear'; bar.style.width = '100%';
        timer = setTimeout(function() { go(st.i + 1, true); }, every);
      }
    }
    function go(k, animate) {
      st.i = (k + o.scenes.length) % o.scenes.length;
      var sc = o.scenes[st.i], dur = animate && !reduced ? 900 : 0;
      cap.style.opacity = dur ? '0' : '1';
      setTimeout(function() { cap.innerHTML = sc.text; cap.style.opacity = '1'; }, dur ? 380 : 0);
      sc.show(ctx, dur);
      sync();
    }
    go(st.i, false);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function(es) { visible = es[0].isIntersecting; sync(); }, { threshold: 0.6 }).observe(box);
    } else { visible = true; sync(); }
    return ctx;
  }

  return {
    story: story,
    FONT: FONT, C: C, reduced: reduced, pct: pct, usd: usd, showTip: showTip, hideTip: hideTip,
    frame: frame, xAxis: xAxis, yAxis: yAxis, gridY: gridY, label: label,
    controls: controls, slider: slider, segmented: segmented, legend: legend, onView: onView, mount: mount,
    data: window.JPC_DATA
  };
})();
