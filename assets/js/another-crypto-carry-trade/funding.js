// Viz 2: weekly bitcoin funding, annualized. Above zero, longs pay shorts.
(function() {
  var J = window.JPC;
  var SRC = { name: 'Binance', note: '30-day average', rows: J.data.binance };
  var parse = d3.timeParse('%Y-%m-%d');
  var fmtDate = d3.timeFormat('%b %-d, %Y');

  J.mount('jpc-funding', function(root) {
    var f = J.frame(root, 300, { top: 14, right: 64, bottom: 30, left: 40 });
    var x = d3.scaleTime().range([0, f.iw]);
    var y = d3.scaleLinear().range([f.ih, 0]);
    var gridG = f.g.append('g'), xG = f.g.append('g'), yG = f.g.append('g');
    var bars = f.g.append('g');
    var zero = f.g.append('line').style('stroke', J.C.muted).attr('stroke-width', 1);
    var avgLine = f.g.append('line').style('stroke', J.C.text).attr('stroke-width', 1).attr('stroke-dasharray', '4,3');
    var avgText = f.g.append('text').attr('font-size', 11).style('fill', J.C.text);
    var cross = f.g.append('line').attr('y1', 0).attr('y2', f.ih).style('stroke', J.C.muted)
      .attr('stroke-width', 1).style('opacity', 0);
    var first = true;

    function update(animate) {
      var src = SRC;
      var data = src.rows.map(function(r) { return { t: parse(r[0]), v: r[1] }; });
      var avg = d3.mean(data, function(d) { return d.v; });
      x.domain(d3.extent(data, function(d) { return d.t; }));
      var lo = Math.min(-5, d3.min(data, function(d) { return d.v; }));
      var hi = Math.max(20, d3.max(data, function(d) { return d.v; }));
      y.domain([lo, hi]).nice();

      gridG.selectAll('*').remove(); xG.selectAll('*').remove(); yG.selectAll('*').remove();
      gridG.selectAll('line').data(y.ticks(5)).join('line').attr('x1', 0).attr('x2', f.iw)
        .attr('y1', y).attr('y2', y).style('stroke', J.C.grid).attr('stroke-width', 0.7);
      xG.attr('transform', 'translate(0,' + f.ih + ')')
        .call(d3.axisBottom(x).ticks(f.iw < 420 ? 3 : 6).tickSizeOuter(0));
      yG.call(d3.axisLeft(y).ticks(5).tickFormat(function(d) { return d + '%'; }).tickSizeOuter(0));
      [xG, yG].forEach(function(a) {
        a.select('.domain').remove();
        a.selectAll('.tick line').style('stroke', J.C.axis);
        a.selectAll('.tick text').style('fill', J.C.muted).attr('font-size', 11);
      });

      var bw = Math.max(1, f.iw / data.length - 1);
      var sel = bars.selectAll('rect').data(data, function(d) { return +d.t; });
      sel.exit().remove();
      var merged = sel.enter().append('rect').attr('y', y(0)).attr('height', 0).merge(sel)
        .attr('x', function(d) { return x(d.t) - bw / 2; }).attr('width', bw)
        .style('fill', function(d) { return d.v >= 0 ? J.C.perp : J.C.jr; });
      var target = function(s) {
        s.attr('y', function(d) { return y(Math.max(0, d.v)); })
          .attr('height', function(d) { return Math.abs(y(d.v) - y(0)); });
      };
      if (animate && !J.reduced) target(merged.transition().duration(first ? 900 : 500).delay(function(d, i) { return first ? i * 3 : 0; }));
      else target(merged);
      first = false;

      zero.attr('x1', 0).attr('x2', f.iw).attr('y1', y(0)).attr('y2', y(0));
      avgLine.attr('x1', 0).attr('x2', f.iw).attr('y1', y(avg)).attr('y2', y(avg));
      avgText.attr('x', f.iw + 6).attr('y', y(avg) + 4).text('avg ' + J.pct(avg));

      var pos = d3.mean(data, function(d) { return d.v > 0 ? 1 : 0; });
      overlay.on('mousemove', function(e) {
        var mx = d3.pointer(e)[0];
        var i = d3.bisector(function(d) { return d.t; }).center(data, x.invert(mx));
        var d = data[i];
        cross.attr('x1', x(d.t)).attr('x2', x(d.t)).style('opacity', 1);
        J.showTip(e, fmtDate(d.t), [
          [src.name + ', ' + src.note, J.pct(d.v)],
          [d.v >= 0 ? 'Longs pay shorts' : 'Shorts pay longs', ''],
          ['Positive weeks, whole period', Math.round(pos * 100) + '%']
        ]);
      });
    }

    var overlay = f.g.append('rect').attr('width', f.iw).attr('height', f.ih).style('fill', 'transparent')
      .on('mouseleave', function() { cross.style('opacity', 0); J.hideTip(); });

    J.legend(root, [
      { color: J.C.perp, label: 'Longs pay', box: true },
      { color: J.C.jr, label: 'Shorts pay', box: true },
      { color: J.C.text, label: 'Average over the period', dash: true }
    ]);

    if (J.reduced) update(false);
    else {
      update(false);
      bars.selectAll('rect').attr('y', y(0)).attr('height', 0);
      first = true;
      J.onView(root, function() { update(true); });
    }
  });
})();
