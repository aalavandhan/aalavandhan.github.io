// Growth of $1 from the end of 1975: Berkshire, the US market, and a synthetic Berkshire: a mechanical
// cheap + safe + quality stock screen held at 2.2x. Log scale. Berkshire is year-end only for 1976-79, monthly after.
(function() {
  var J = window.BLV;
  var parse = d3.timeParse('%Y-%m');
  var cols = J.data.race_cols;
  var rows = J.data.race.map(function(r) {
    var o = { t: parse(r[0]) };
    cols.forEach(function(c, i) { o[c] = r[i + 1]; });
    return o;
  });
  var LEV = 'w_a11_22x_tbill';   // the screen at 2.2x, borrowing at the T-bill rate, no trading costs
  var fmtDate = d3.timeFormat('%b %Y');
  function money(v) { return v == null ? '—' : '$' + (v >= 100 ? d3.format(',.0f')(v) : v.toFixed(2)); }

  var view = 'chart';   // kept outside the draw so a resize redraws the tab that was open

  J.mount('blv-race', function(root) {
    var row = J.controls(root);
    J.segmented(row, [['chart', 'Growth of $1'], ['table', 'Summary']], view, function(v) { view = v; render(); });
    var box = document.createElement('div');
    root.appendChild(box);
    function render() {
      box.innerHTML = '';
      if (view === 'chart') drawChart(box); else drawTable(box);
      // the table is shorter than the chart: centre it in the held space
      box.style.cssText += ';display:' + (view === 'table' ? 'flex' : 'block') + ';flex-direction:column;justify-content:center';
    }
    // Draw each tab once to measure it, and hold the box at the taller height so switching tabs doesn't move the page.
    var tall = 0, keep = view;
    ['table', 'chart'].forEach(function(v) { view = v; render(); tall = Math.max(tall, box.offsetHeight); });
    box.style.minHeight = tall + 'px';
    view = keep;
    render();
  });

  // The same three portfolios as a table. Values come from build_post_data.py.
  function drawTable(root) {
    var color = { w_berkshire: J.C.brk, w_a11_22x_tbill: J.C.idx, w_a11: J.C.idx, w_market: J.C.other };
    function pct(v, d) { return (v < 0 ? '\u2212' : '') + Math.abs(v).toFixed(d) + '%'; }
    var head = ['', 'Return a year', '$1 becomes', 'Volatility', 'Sharpe', 'Drawdown'];
    var html = '<table style="font-variant-numeric:tabular-nums;width:100%;font-size:14.5px"><thead><tr>' + head.map(function(h, i) {
      return '<th style="text-align:' + (i ? 'right' : 'left') + '">' + h + '</th>';
    }).join('') + '</tr></thead><tbody>' + J.data.metrics.map(function(m) {
      var cells = [pct(m[2], 1), '$' + d3.format(',')(m[3]), pct(m[4], 1), m[5].toFixed(2), pct(m[6], 0)];
      // the row the chart is about gets a tint of its own line colour
      var hl = m[1] === 'w_a11_22x_tbill' ? ' style="background:color-mix(in srgb,' + color[m[1]] + ' 13%,transparent)"' : '';
      return '<tr' + hl + '><td style="white-space:nowrap"><i style="display:inline-block;box-sizing:border-box;width:10px;height:10px;border-radius:2px;margin-right:8px;border:2px solid '
        + color[m[1]] + ';background:' + (m[1] === 'w_a11' ? 'transparent' : color[m[1]]) + '"></i><strong>' + m[0] + '</strong></td>'
        + cells.map(function(c) { return '<td style="text-align:right">' + c + '</td>'; }).join('') + '</tr>';
    }).join('') + '</tbody></table>';
    var wrap = document.createElement('div');
    wrap.style.overflowX = 'auto';
    wrap.innerHTML = html;
    root.appendChild(wrap);
  }

  function drawChart(root) {
    var narrow = root.clientWidth < 520;
    var f = J.frame(root, narrow ? 340 : 400, { top: 14, right: narrow ? 112 : 150, bottom: 30, left: 52 });
    var x = d3.scaleTime().domain(d3.extent(rows, function(d) { return d.t; })).range([0, f.iw]);
    var y = d3.scaleLog().domain([0.8, 30000]).range([f.ih, 0]);
    var ticks = [1, 10, 100, 1000, 10000];

    f.g.append('g').selectAll('line').data(ticks).join('line').attr('x1', 0).attr('x2', f.iw).attr('y1', y).attr('y2', y)
      .style('stroke', J.C.grid).attr('stroke-width', 0.7);
    J.xAxis(f, x, narrow ? 4 : 7, d3.timeFormat('%Y')).select('.domain').remove();
    var ya = f.g.append('g').call(d3.axisLeft(y).tickValues(ticks).tickFormat(function(d) { return '$' + d3.format(',')(d); }).tickSizeOuter(0));
    ya.select('.domain').remove();
    ya.selectAll('.tick line').style('stroke', J.C.axis);
    ya.selectAll('.tick text').style('fill', J.C.muted).attr('font-size', 11);

    var SERIES = [
      { key: 'w_market', name: 'US market', color: J.C.other, w: 1.5 },
      { key: 'w_a11', name: 'Synthetic at 1×', short: 'At 1×', color: J.C.idx, w: 1.5, dash: '2,3' },
      { key: 'lev', name: 'Synthetic at 2.2×', short: 'Synthetic', color: J.C.idx, w: 2.2 },
      { key: 'w_berkshire', name: 'Berkshire', color: J.C.brk, w: 2.2 }
    ];
    function val(d, s) { return s.key === 'lev' ? d[LEV] : d[s.key]; }
    function pathFor(s) {
      var pts = rows.filter(function(d) { return val(d, s) != null; });
      return d3.line().x(function(d) { return x(d.t); }).y(function(d) { return y(val(d, s)); })(pts);
    }
    var last = rows[rows.length - 1];
    SERIES.forEach(function(s) {
      s.path = f.g.append('path').attr('fill', 'none').style('stroke', s.color).attr('stroke-width', s.w)
        .attr('stroke-linejoin', 'round').attr('stroke-dasharray', s.dash || null).attr('d', pathFor(s));
      s.label = f.g.append('text').attr('x', f.iw + 8).attr('font-size', 11.5).style('fill', J.C.text);
      s.label.append('tspan').attr('font-weight', 600).attr('class', 'n');
      s.label.append('tspan').attr('class', 'v').style('fill', J.C.muted);
    });
    function place() {
      // direct labels at the right edge, nudged apart so they never overlap
      var items = SERIES.map(function(s) { return { s: s, y: y(val(last, s)) }; }).sort(function(a, b) { return a.y - b.y; });
      for (var i = 1; i < items.length; i++) if (items[i].y - items[i - 1].y < 15) items[i].y = items[i - 1].y + 15;
      items.forEach(function(it) {
        it.s.label.attr('y', it.y + 4);
        it.s.label.select('.n').text(narrow && it.s.short ? it.s.short : it.s.name);
        it.s.label.select('.v').text('  ' + money(val(last, it.s)));
      });
    }
    place();

    var cross = f.g.append('line').attr('y1', 0).attr('y2', f.ih).style('stroke', J.C.muted).attr('stroke-width', 1).style('opacity', 0);
    var bis = d3.bisector(function(d) { return d.t; }).center;
    f.g.append('rect').attr('width', f.iw).attr('height', f.ih).style('fill', 'transparent')
      .on('mousemove', function(e) {
        var d = rows[bis(rows, x.invert(d3.pointer(e)[0]))];
        cross.attr('x1', x(d.t)).attr('x2', x(d.t)).style('opacity', 1);
        J.showTip(e, fmtDate(d.t) + ': $1 from 1975 is worth', SERIES.slice().reverse().map(function(s) {
          var v = val(d, s);
          return [s.name, v == null ? 'year-end only before 1980' : money(v)];
        }));
      })
      .on('mouseleave', function() { cross.style('opacity', 0); J.hideTip(); });

    if (!J.reduced) {
      SERIES.forEach(function(s) {
        s.label.style('opacity', 0);
        if (s.dash) { s.path.style('opacity', 0); return; }
        var len = s.path.node().getTotalLength();
        s.path.attr('stroke-dasharray', len + ' ' + len).attr('stroke-dashoffset', len);
        s.label.style('opacity', 0);
      });
      J.onView(root, function() {
        SERIES.forEach(function(s) {
          if (s.dash) { s.path.transition().delay(1700).duration(400).style('opacity', 1); }
          else {
            s.path.transition().duration(2200).ease(d3.easeCubicInOut).attr('stroke-dashoffset', 0)
              .on('end', function() { s.path.attr('stroke-dasharray', null); });
          }
          s.label.transition().delay(2100).duration(400).style('opacity', 1);
        });
      });
    }
  }
})();
