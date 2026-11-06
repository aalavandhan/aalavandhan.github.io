// The cost of 1.33× bitcoin, through a perp and through Jr, per dollar of your own money. Two tabs:
// Predicted (weekly, 2021–2025: Binance funding and the landing page's Jr estimate) and
// Live (daily since launch: Hyperliquid funding and Jr's realized cost). A perp at 1.33× pays
// funding on the full notional, so its cost is 1.337 × funding.
(function() {
  var J = window.JPC;
  var V = 1.337;
  var state = { tab: 'predicted' };

  var TABS = {
    predicted: {
      label: 'Predicted, 2021–2025',
      rows: function() {
        var parse = d3.timeParse('%Y-%m-%d'), jr = J.data.jrcost;
        return J.data.binance.map(function(r, i) { return { t: parse(r[0]), p: V * r[1], j: jr[i][1] }; });
      },
      perp: '1.33× via a perp (Binance funding)', jr: '1.33× via Jr (estimated)',
      tick: null, fmt: d3.timeFormat('%b %-d, %Y')
    },
    live: {
      label: 'Live, since launch',
      rows: function() {
        var parse = d3.utcParse('%Y-%m-%d');
        return J.data.month.map(function(d) { return { t: parse(d.t), p: V * d.hyperliquid, j: d.jr, sr: d.sr }; });
      },
      perp: '1.33× via a perp (Hyperliquid funding)', jr: '1.33× via Jr',
      tick: d3.utcFormat('%b %-d'), fmt: d3.utcFormat('%b %-d, %Y')
    }
  };

  function drawTab(body, tab) {
    var T = TABS[tab], rows = T.rows();
    var f = J.frame(body, 320, { top: 16, right: 84, bottom: 30, left: 40 });
    var x = d3.scaleTime().domain(d3.extent(rows, function(d) { return d.t; })).range([0, f.iw]);
    var lo = Math.min(-4, d3.min(rows, function(d) { return d.p; }));
    var hi = d3.max(rows, function(d) { return d.p; }) * 1.05;
    var y = d3.scaleLinear().domain([lo, hi]).nice().range([f.ih, 0]);

    J.gridY(f, y, 5);
    J.xAxis(f, x, f.iw < 420 ? 3 : 5, T.tick);
    J.yAxis(f, y, 5, function(v) { return v + '%'; });
    f.g.append('line').attr('x1', 0).attr('x2', f.iw).attr('y1', y(0)).attr('y2', y(0))
      .style('stroke', J.C.axis).attr('stroke-dasharray', '3,3');

    var X = function(d) { return x(d.t); };
    var spread = f.g.append('path').datum(rows).style('fill', J.C.fillPerp)
      .attr('d', d3.area().x(X).y0(function(d) { return y(d.j); }).y1(function(d) { return y(Math.max(d.p, d.j)); }));
    var pPath = f.g.append('path').datum(rows).style('fill', 'none').style('stroke', J.C.perp).attr('stroke-width', 2)
      .attr('d', d3.line().x(X).y(function(d) { return y(d.p); }));
    var jPath = f.g.append('path').datum(rows).style('fill', 'none').style('stroke', J.C.jr).attr('stroke-width', 2)
      .attr('d', d3.line().x(X).y(function(d) { return y(d.j); }));

    // The point is stability, not level: label each line with its typical range (10th to 90th percentile).
    function band(key) {
      var v = rows.map(function(d) { return d[key]; }).sort(d3.ascending);
      return [d3.quantile(v, 0.1), d3.quantile(v, 0.9), d3.median(v)];
    }
    [[band('p'), 'via a perp'], [band('j'), 'via Jr']].forEach(function(a, i) {
      var yy = Math.min(f.ih - 18, y(a[0][2]) + (i ? 12 : -4));
      f.g.append('text').attr('x', f.iw + 8).attr('y', yy).attr('font-size', 12).style('fill', J.C.text).text(a[1]);
      f.g.append('text').attr('x', f.iw + 8).attr('y', yy + 14).attr('font-size', 11).style('fill', J.C.muted)
        .text(Math.round(a[0][0]) + '–' + Math.round(a[0][1]) + '%');
    });

    var cross = f.g.append('g').style('display', 'none');
    cross.append('line').attr('y1', 0).attr('y2', f.ih).style('stroke', J.C.axis);
    var dotP = cross.append('circle').attr('r', 4).style('fill', J.C.perp).style('stroke', J.C.surface).attr('stroke-width', 2);
    var dotJ = cross.append('circle').attr('r', 4).style('fill', J.C.jr).style('stroke', J.C.surface).attr('stroke-width', 2);
    var bis = d3.bisector(function(d) { return d.t; }).center;
    f.g.append('rect').attr('width', f.iw).attr('height', f.ih).style('fill', 'transparent')
      .on('mousemove', function(e) {
        var d = rows[bis(rows, x.invert(d3.pointer(e)[0]))];
        cross.style('display', null).attr('transform', 'translate(' + x(d.t) + ',0)');
        dotP.attr('cy', y(d.p)); dotJ.attr('cy', y(d.j));
        var tip = [['Via a perp', J.pct(d.p)], ['Via Jr', J.pct(d.j)], ['Spread', J.pct(d.p - d.j)]];
        if (d.sr != null) tip.push(['Sr yield', J.pct(d.sr)]);
        J.showTip(e, T.fmt(d.t), tip);
      })
      .on('mouseleave', function() { cross.style('display', 'none'); J.hideTip(); });

    J.legend(body, [
      { color: J.C.perp, label: T.perp },
      { color: J.C.jr, label: T.jr },
      { color: J.C.fillPerp, label: 'spread', box: true }
    ]);

    // Draw the lines in.
    if (!J.reduced) {
      [pPath, jPath].forEach(function(p) {
        var len = p.node().getTotalLength();
        p.attr('stroke-dasharray', len + ' ' + len).attr('stroke-dashoffset', len)
          .transition().duration(1200).ease(d3.easeCubicOut).attr('stroke-dashoffset', 0)
          .on('end', function() { d3.select(this).attr('stroke-dasharray', null); });
      });
      spread.style('opacity', 0).transition().delay(700).duration(500).style('opacity', 1);
    }
  }

  J.mount('jpc-jrcost', function(root) {
    var row = J.controls(root);
    var body = document.createElement('div');
    root.appendChild(body);
    J.segmented(row, Object.keys(TABS).map(function(k) { return [k, TABS[k].label]; }), state.tab, function(v) {
      state.tab = v; body.innerHTML = ''; drawTab(body, v);
    });
    // Wait for the chart to scroll into view before the first draw-in.
    if (J.reduced) drawTab(body, state.tab);
    else J.onView(root, function() { drawTab(body, state.tab); });
  });
})();
