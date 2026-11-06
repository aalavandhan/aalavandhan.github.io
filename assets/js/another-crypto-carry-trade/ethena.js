// Viz 4: Ethena's size, and the yield it pays stakers, on one time axis (two stacked panels).
(function() {
  var J = window.JPC;
  var parse = d3.timeParse('%Y-%m-%d');
  var fmtDate = d3.timeFormat('%b %-d, %Y');
  var fmtMonth = d3.timeFormat('%b %Y');
  var rows = function(k) { return J.data[k].map(function(r) { return { t: parse(r[0]), v: r[1] }; }); };
  var yld = rows('susde');
  var start = yld[0].t, end = yld[yld.length - 1].t;
  var size = rows('usde').filter(function(d) { return d.t >= start && d.t <= end; });

  function near(arr, t) {
    if (!arr.length || t < arr[0].t || t > arr[arr.length - 1].t) return null;
    return arr[d3.bisector(function(d) { return d.t; }).center(arr, t)];
  }
  function max(arr) { return arr.reduce(function(a, b) { return b.v > a.v ? b : a; }); }

  J.mount('jpc-ethena', function(root) {
    var f = J.frame(root, 370, { top: 16, right: 20, bottom: 28, left: 44 });
    var topH = 136, gapH = 66, botTop = topH + gapH, botH = f.ih - botTop;
    var x = d3.scaleTime().domain([start, end]).range([0, f.iw]);
    var yS = d3.scaleLinear().domain([0, 16]).range([topH, 0]);
    var yY = d3.scaleLinear().domain([0, 60]).range([botTop + botH, botTop]);

    [[yS, 3, function(d) { return '$' + d + 'B'; }], [yY, 2, function(d) { return d + '%'; }]].forEach(function(a) {
      f.g.append('g').selectAll('line').data(a[0].ticks(a[1])).join('line').attr('x1', 0).attr('x2', f.iw)
        .attr('y1', a[0]).attr('y2', a[0]).style('stroke', J.C.grid).attr('stroke-width', 0.7);
      var ax = f.g.append('g').call(d3.axisLeft(a[0]).ticks(a[1]).tickFormat(a[2]).tickSizeOuter(0));
      ax.select('.domain').remove();
      ax.selectAll('.tick line').style('stroke', J.C.axis);
      ax.selectAll('.tick text').style('fill', J.C.muted).attr('font-size', 11);
    });
    var xa = f.g.append('g').attr('transform', 'translate(0,' + f.ih + ')')
      .call(d3.axisBottom(x).ticks(f.iw < 420 ? 3 : 6).tickSizeOuter(0));
    xa.select('.domain').style('stroke', J.C.axis);
    xa.selectAll('.tick line').style('stroke', J.C.axis);
    xa.selectAll('.tick text').style('fill', J.C.muted).attr('font-size', 11);

    J.label(f, 4, -2, 'Ethena size', { size: 11 });
    J.label(f, 4, botTop - 4, 'Yield', { size: 11 });

    var clipId = 'jpc-ethena-clip';
    var clip = f.svg.append('defs').append('clipPath').attr('id', clipId).append('rect')
      .attr('x', -2).attr('y', -10).attr('height', f.ih + 20).attr('width', f.iw + 40);
    var plot = f.g.append('g').attr('clip-path', 'url(#' + clipId + ')');

    plot.append('path').datum(size).style('fill', J.C.margin).style('fill-opacity', 0.18)
      .attr('d', d3.area().x(function(d) { return x(d.t); }).y0(yS(0)).y1(function(d) { return yS(d.v); }));
    plot.append('path').datum(size).style('fill', 'none').style('stroke', J.C.margin).attr('stroke-width', 2)
      .attr('d', d3.line().x(function(d) { return x(d.t); }).y(function(d) { return yS(d.v); }));
    plot.append('path').datum(yld).style('fill', 'none').style('stroke', J.C.perp).attr('stroke-width', 2)
      .attr('d', d3.line().curve(d3.curveMonotoneX).x(function(d) { return x(d.t); }).y(function(d) { return yY(d.v); }));

    // Direct labels: both peaks, and where each stands now.
    var ann = plot.append('g');
    function dot(px, py, color) {
      ann.append('circle').attr('cx', px).attr('cy', py).attr('r', 3.5).style('fill', color)
        .style('stroke', J.C.surface).attr('stroke-width', 1.5);
    }
    function text(px, py, s, anchor) {
      ann.append('text').attr('x', px).attr('y', py).attr('text-anchor', anchor || 'start')
        .attr('font-size', 11).style('fill', J.C.text).text(s);
    }
    var sp = max(size), yp = max(yld), sl = size[size.length - 1], yl = yld[yld.length - 1];
    dot(x(sp.t), yS(sp.v), J.C.margin);
    text(x(sp.t) - 8, yS(sp.v) + 4, '$' + sp.v.toFixed(1) + 'B, ' + fmtMonth(sp.t), 'end');
    text(x(sl.t), yS(sl.v) - 8, '$' + sl.v.toFixed(1) + 'B', 'end');
    dot(x(yp.t), yY(yp.v), J.C.perp);
    text(x(yp.t) + 8, yY(yp.v) + 4, Math.round(yp.v) + '%, ' + fmtMonth(yp.t));
    text(x(yl.t), yY(yl.v) - 8, J.pct(yl.v), 'end');

    var cross = f.g.append('line').attr('y1', 0).attr('y2', f.ih).style('stroke', J.C.muted).style('opacity', 0);
    f.g.append('rect').attr('width', f.iw).attr('height', f.ih).style('fill', 'transparent')
      .on('mousemove', function(e) {
        var t = x.invert(d3.pointer(e)[0]);
        var y = near(yld, t), s = near(size, t);
        cross.attr('x1', x(y.t)).attr('x2', x(y.t)).style('opacity', 1);
        J.showTip(e, fmtDate(y.t), [['Ethena size', s ? '$' + s.v.toFixed(1) + 'B' : '—'], ['Yield', J.pct(y.v)]]);
      })
      .on('mouseleave', function() { cross.style('opacity', 0); J.hideTip(); });

    J.legend(root, [
      { color: J.C.margin, label: 'Ethena size' },
      { color: J.C.perp, label: 'Yield (weekly avg)' }
    ]);

    if (!J.reduced) {
      clip.attr('width', 0);
      J.onView(root, function() { clip.transition().duration(1600).ease(d3.easeCubicOut).attr('width', f.iw + 40); });
    }
  });
})();
