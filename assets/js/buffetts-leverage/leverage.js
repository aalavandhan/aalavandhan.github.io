// Two views, switched by tabs:
//   Leverage: (assets - cash and T-bills) / equity, at market value, by year.
//   Estimated yearly returns: the change each year in the share price and in the market value of assets per share.
(function() {
  var J = window.BLV;
  var rows = J.data.leverage.map(function(r) { return { y: r[0], lev: r[1], cost: r[2], tb: r[3] }; });
  var avg = d3.mean(rows.filter(function(d) { return d.y >= 1996; }), function(d) { return d.lev; });
  // yearly change, %: share price and assets per share. Before 1996 the asset figure is an estimate (build_post_data.py).
  var stock = J.data.stock.map(function(r) { return { y: r[0], pc: r[1], ac: r[2], est: !!r[3] }; });
  var mode = 'lev';   // kept outside the draw so a resize redraws the tab that was open

  J.mount('blv-leverage', function(root) {
    var row = J.controls(root);
    J.segmented(row, [['lev', 'Leverage'], ['stock', 'Estimated yearly returns']], mode, function(v) { mode = v; render(); });
    var box = document.createElement('div');
    root.appendChild(box);
    function render() {
      box.innerHTML = '';
      if (mode === 'lev') drawLeverage(box); else drawStock(box);
    }
    // Draw each tab once to measure it, and hold the box at the taller height so switching tabs doesn't move the page.
    var tall = 0, keep = mode;
    ['stock', 'lev'].forEach(function(v) { mode = v; render(); tall = Math.max(tall, box.offsetHeight); });
    box.style.minHeight = tall + 'px';
    mode = keep;
    render();
  });

  function drawStock(root) {
    var data = stock;
    var f = J.frame(root, 260, { top: 16, right: 16, bottom: 30, left: 44 });
    var x = d3.scaleLinear().domain(d3.extent(data, function(d) { return d.y; })).range([0, f.iw]);
    var y = d3.scaleLinear().domain([-40, 120]).range([f.ih, 0]);
    J.gridY(f, y, 8);
    J.xAxis(f, x, f.iw < 420 ? 5 : 10, d3.format('d')).select('.domain').remove();
    J.yAxis(f, y, 8, function(d) { return (d > 0 ? '+' : '') + d + '%'; });
    f.g.append('line').attr('x1', 0).attr('x2', f.iw).attr('y1', y(0)).attr('y2', y(0))
      .style('stroke', J.C.axis).attr('stroke-width', 1);

    function draw(key, color) {
      var line = d3.line().x(function(d) { return x(d.y); }).y(function(d) { return y(d[key]); });
      return f.g.append('path').datum(data).attr('d', line).attr('fill', 'none')
        .style('stroke', color).attr('stroke-width', 2).attr('stroke-linejoin', 'round').attr('stroke-linecap', 'round');
    }
    var paths = [draw('ac', J.C.idx), draw('pc', J.C.brk)];
    J.legend(root, [
      { label: 'Share price', color: J.C.brk },
      { label: 'Assets per share, at market value', color: J.C.idx }
    ]);

    var cross = f.g.append('line').attr('y1', 0).attr('y2', f.ih).style('stroke', J.C.muted).attr('stroke-width', 1).style('opacity', 0);
    var dots = [J.C.idx, J.C.brk].map(function(c) {
      return f.g.append('circle').attr('r', 4).style('fill', c).style('stroke', J.C.surface).attr('stroke-width', 2).style('opacity', 0);
    });
    function chg(v) { return (v > 0 ? '+' : '') + v.toFixed(0) + '%'; }
    f.g.append('rect').attr('width', f.iw).attr('height', f.ih).style('fill', 'transparent')
      .on('mousemove', function(e) {
        var yr = Math.round(x.invert(d3.pointer(e)[0]));
        var d = data[Math.max(0, Math.min(data.length - 1, yr - data[0].y))];
        cross.attr('x1', x(d.y)).attr('x2', x(d.y)).style('opacity', 1);
        dots[0].attr('cx', x(d.y)).attr('cy', y(d.ac)).style('opacity', 1);
        dots[1].attr('cx', x(d.y)).attr('cy', y(d.pc)).style('opacity', 1);
        J.showTip(e, String(d.y), [['Share price', chg(d.pc)], ['Assets per share', chg(d.ac)]]);
      })
      .on('mouseleave', function() {
        cross.style('opacity', 0); dots.forEach(function(c) { c.style('opacity', 0); }); J.hideTip();
      });

    if (!J.reduced) {
      var id = 'blv-stock-clip', clip = f.g.append('clipPath').attr('id', id).append('rect')
        .attr('x', -4).attr('y', -10).attr('height', f.ih + 20).attr('width', 0);
      paths.forEach(function(p) { p.attr('clip-path', 'url(#' + id + ')'); });
      clip.transition().duration(1000).ease(d3.easeCubicOut).attr('width', f.iw + 8);
    }
  }

  function drawLeverage(root) {
    var f = J.frame(root, 260, { top: 16, right: 84, bottom: 30, left: 40 });
    var x = d3.scaleLinear().domain(d3.extent(rows, function(d) { return d.y; })).range([0, f.iw]);
    var y = d3.scaleLinear().domain([1, 2.2]).range([f.ih, 0]);
    J.gridY(f, y, 5);
    J.xAxis(f, x, f.iw < 420 ? 4 : 7, d3.format('d')).select('.domain').remove();
    J.yAxis(f, y, 5, function(d) { return d.toFixed(1) + '×'; });

    f.g.append('line').attr('x1', 0).attr('x2', f.iw).attr('y1', y(avg)).attr('y2', y(avg))
      .style('stroke', J.C.text).attr('stroke-width', 1).attr('stroke-dasharray', '4,3');
    J.label(f, f.iw + 6, y(avg) + 4, 'average ' + avg.toFixed(1) + '×', { fill: J.C.text, size: 11 });

    var line = d3.line().x(function(d) { return x(d.y); }).y(function(d) { return y(d.lev); }).curve(d3.curveMonotoneX);
    var path = f.g.append('path').datum(rows).attr('d', line).attr('fill', 'none')
      .style('stroke', J.C.brk).attr('stroke-width', 2).attr('stroke-linejoin', 'round');
    var last = rows[rows.length - 1];
    var dot = f.g.append('circle').attr('cx', x(last.y)).attr('cy', y(last.lev)).attr('r', 4)
      .style('fill', J.C.brk).style('stroke', J.C.surface).attr('stroke-width', 2);
    var end = J.label(f, f.iw + 6, y(last.lev) + 4, last.lev.toFixed(2) + '× in ' + last.y, { fill: J.C.brk, size: 11 });

    var cross = f.g.append('line').attr('y1', 0).attr('y2', f.ih).style('stroke', J.C.muted).attr('stroke-width', 1).style('opacity', 0);
    f.g.append('rect').attr('width', f.iw).attr('height', f.ih).style('fill', 'transparent')
      .on('mousemove', function(e) {
        var yr = Math.round(x.invert(d3.pointer(e)[0]));
        var d = rows[Math.max(0, Math.min(rows.length - 1, yr - rows[0].y))];
        cross.attr('x1', x(d.y)).attr('x2', x(d.y)).style('opacity', 1);
        J.showTip(e, 'End of ' + d.y, [
          ['Leverage', d.lev.toFixed(2) + '×'],
          ['Cost of borrowing', d.cost == null ? 'n/a' : J.pct(d.cost)],
          ['T-bill rate', J.pct(d.tb)]
        ]);
      })
      .on('mouseleave', function() { cross.style('opacity', 0); J.hideTip(); });

    if (!J.reduced) {
      var len = path.node().getTotalLength();
      path.attr('stroke-dasharray', len + ' ' + len).attr('stroke-dashoffset', len);
      dot.style('opacity', 0); end.style('opacity', 0);
      J.onView(root, function() {
        path.transition().duration(1400).ease(d3.easeCubicOut).attr('stroke-dashoffset', 0)
          .on('end', function() { path.attr('stroke-dasharray', null); });
        dot.transition().delay(1300).duration(300).style('opacity', 1);
        end.transition().delay(1300).duration(300).style('opacity', 1);
      });
    }
  }
})();
