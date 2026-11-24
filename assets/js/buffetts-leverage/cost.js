// Berkshire's blended cost of borrowing by year, against the 3-month T-bill rate.
// Blended cost = (interest paid + underwriting loss) / (debt + float + deferred taxes), from leverage_cost.csv.
// Measured from 1996. Before that, and for 1999-2001, it is an estimate (see build_post_data.py) and is drawn the same way; the caption says so.
(function() {
  var J = window.BLV;
  var rows = J.data.cost.map(function(r) { return { y: r[0], cost: r[1], tb: r[2], est: !!r[3] }; });

  J.mount('blv-cost', function(root) {
    var f = J.frame(root, 280, { top: 16, right: 92, bottom: 30, left: 40 });
    var x = d3.scaleLinear().domain(d3.extent(rows, function(d) { return d.y; })).range([0, f.iw]);
    var y = d3.scaleLinear().domain([-3, 15]).range([f.ih, 0]);
    J.gridY(f, y, 6);
    J.xAxis(f, x, f.iw < 420 ? 4 : 7, d3.format('d')).select('.domain').remove();
    J.yAxis(f, y, 6, function(d) { return d + '%'; });
    f.g.append('line').attr('x1', 0).attr('x2', f.iw).attr('y1', y(0)).attr('y2', y(0))
      .style('stroke', J.C.axis).attr('stroke-width', 1);

    function draw(key, color, solidOnly) {
      var line = d3.line().defined(function(d) { return !solidOnly || !d.est; })
        .x(function(d) { return x(d.y); }).y(function(d) { return y(d[key]); });
      return f.g.append('path').datum(rows).attr('d', line).attr('fill', 'none')
        .style('stroke', color).attr('stroke-width', 2).attr('stroke-linejoin', 'round').attr('stroke-linecap', 'round');
    }
    var pT = draw('tb', J.C.tbill), pB = draw('cost', J.C.brk);
    var last = rows[rows.length - 1];
    var ends = f.g.append('g');
    [['tb', J.C.tbill, 'T-bills'], ['cost', J.C.brk, 'Berkshire']].forEach(function(s) {
      ends.append('circle').attr('cx', x(last.y)).attr('cy', y(last[s[0]])).attr('r', 4)
        .style('fill', s[1]).style('stroke', J.C.surface).attr('stroke-width', 2);
      J.label(f, f.iw + 8, y(last[s[0]]) + 4, s[2] + ' ' + last[s[0]].toFixed(1) + '%', { fill: J.C.text, size: 11 }).attr('class', 'end');
    });
    var endLabels = f.g.selectAll('text.end');

    var cross = f.g.append('line').attr('y1', 0).attr('y2', f.ih).style('stroke', J.C.muted).attr('stroke-width', 1).style('opacity', 0);
    f.g.append('rect').attr('width', f.iw).attr('height', f.ih).style('fill', 'transparent')
      .on('mousemove', function(e) {
        var yr = Math.round(x.invert(d3.pointer(e)[0]));
        var d = rows[Math.max(0, Math.min(rows.length - 1, yr - rows[0].y))];
        cross.attr('x1', x(d.y)).attr('x2', x(d.y)).style('opacity', 1);
        J.showTip(e, String(d.y), [
          ['Berkshire\u2019s cost of borrowing', J.pct(d.cost)],
          ['T-bill rate', J.pct(d.tb)]
        ]);
      })
      .on('mouseleave', function() { cross.style('opacity', 0); J.hideTip(); });

    if (!J.reduced) {
      // a clip that widens left to right, so the gap in Berkshire's line survives the draw-in
      var id = 'blv-cost-clip', clip = f.g.append('clipPath').attr('id', id).append('rect')
        .attr('x', -4).attr('y', -10).attr('height', f.ih + 20).attr('width', 0);
      [pT, pB].forEach(function(p) { p.attr('clip-path', 'url(#' + id + ')'); });
      ends.style('opacity', 0); endLabels.style('opacity', 0);
      J.onView(root, function() {
        clip.transition().duration(1400).ease(d3.easeCubicOut).attr('width', f.iw + 8);
        ends.transition().delay(1300).duration(300).style('opacity', 1);
        endLabels.transition().delay(1300).duration(300).style('opacity', 1);
      });
    }
  });
})();
