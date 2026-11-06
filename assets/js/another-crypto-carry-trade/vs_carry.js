// Jr carry vs plain cash and carry: yield on capital as perp funding varies.
(function() {
  var J = window.JPC;
  var V = 1.337;
  // s: Sr's yield. Jr pays it on what it borrows, (V − 1) per dollar of Jr, so Jr's cost is s·(V − 1).
  var state = { s: 7.7, lv: 5 };
  function cost() { return state.s * (V - 1); }
  var MARKS = [[7.9, 'month avg'], [11.1, 'month end']];

  function cc(f) { return f / (1 + 1 / state.lv); }
  function jr(f) { return (f - cost() / V) / (1 / V + 1 / state.lv); }
  function breakEven() { return cost() * (1 + 1 / state.lv) / (V - 1); }

  J.mount('jpc-vs-carry', function(root) {
    var row = J.controls(root);
    J.slider(row, { label: 'Sr yield', min: 2, max: 12, step: 0.1, value: state.s,
      format: function(v) { return v.toFixed(1) + '% \u00b7 Jr cost ' + (v * (V - 1)).toFixed(1) + '%'; }, onInput: function(v) { state.s = v; update(); } });
    J.slider(row, { label: 'Venue leverage', min: 2, max: 8, step: 0.5, value: state.lv,
      format: function(v) { return v.toFixed(1) + '×'; }, onInput: function(v) { state.lv = v; update(); } });

    var narrow = root.clientWidth < 460;
    var f = J.frame(root, 340, { top: 16, right: narrow ? 72 : 110, bottom: 38, left: 40 });
    var x = d3.scaleLinear().domain([0, 16]).range([0, f.iw]);
    var y = d3.scaleLinear().domain([-6, 20]).range([f.ih, 0]);
    var pct = function(v) { return v + '%'; };
    J.gridY(f, y, 6);
    J.xAxis(f, x, narrow ? 4 : 8, pct);
    J.yAxis(f, y, 6, pct);
    J.label(f, f.iw / 2, f.ih + 32, 'Perp funding, annualized', { anchor: 'middle', size: 11 });
    f.g.append('line').attr('x1', 0).attr('x2', f.iw).attr('y1', y(0)).attr('y2', y(0))
      .style('stroke', J.C.axis).attr('stroke-dasharray', '3,3');

    var win = f.g.append('rect').attr('y', 0).attr('height', f.ih).style('fill', J.C.fill);
    var winLab = J.label(f, 0, 14, 'Jr wins', { size: 11 });

    MARKS.forEach(function(m) {
      f.g.append('line').attr('x1', x(m[0])).attr('x2', x(m[0])).attr('y1', 0).attr('y2', f.ih)
        .style('stroke', J.C.muted).attr('stroke-dasharray', '2,3').attr('stroke-width', 1);
      J.label(f, x(m[0]) + 4, f.ih - 6, m[1], { size: 10 });
    });

    var fs = d3.range(0, 16.01, 0.1);
    var line = function(fn) { return d3.line().x(function(v) { return x(v); }).y(function(v) { return y(fn(v)); })(fs); };
    var ccPath = f.g.append('path').style('fill', 'none').style('stroke', J.C.other).attr('stroke-width', 2);
    var jrPath = f.g.append('path').style('fill', 'none').style('stroke', J.C.jr).attr('stroke-width', 2);
    var ccLab = f.g.append('text').attr('font-size', 12).style('fill', J.C.text);
    var jrLab = f.g.append('text').attr('font-size', 12).style('fill', J.C.text);
    var be = f.g.append('circle').attr('r', 5).style('fill', J.C.surface).style('stroke', J.C.text).attr('stroke-width', 1.5);
    var beLab = f.g.append('text').attr('font-size', 11).style('fill', J.C.text);

    var cross = f.g.append('g').style('display', 'none');
    cross.append('line').attr('y1', 0).attr('y2', f.ih).style('stroke', J.C.axis);
    var dC = cross.append('circle').attr('r', 4).style('fill', J.C.other).style('stroke', J.C.surface).attr('stroke-width', 2);
    var dJ = cross.append('circle').attr('r', 4).style('fill', J.C.jr).style('stroke', J.C.surface).attr('stroke-width', 2);
    f.g.append('rect').attr('width', f.iw).attr('height', f.ih).style('fill', 'transparent')
      .on('mousemove', function(e) {
        var v = Math.max(0, Math.min(16, x.invert(d3.pointer(e)[0])));
        cross.style('display', null).attr('transform', 'translate(' + x(v) + ',0)');
        dC.attr('cy', y(cc(v)));
        dJ.attr('cy', y(jr(v)));
        J.showTip(e, 'Funding ' + J.pct(v), [
          ['Basis trade', J.pct(cc(v))],
          ['Jr carry', J.pct(jr(v))],
          ['Jr advantage', (jr(v) - cc(v) >= 0 ? '+' : '') + J.pct(jr(v) - cc(v))]
        ]);
      })
      .on('mouseleave', function() { cross.style('display', 'none'); J.hideTip(); });

    function update() {
      ccPath.attr('d', line(cc));
      jrPath.attr('d', line(jr));
      var yc = y(cc(16)), yj = y(jr(16));
      // Keep the two end labels apart.
      var gap = 14;
      if (Math.abs(yc - yj) < gap) {
        var mid = (yc + yj) / 2, up = yj <= yc;
        yj = up ? mid - gap / 2 : mid + gap / 2;
        yc = up ? mid + gap / 2 : mid - gap / 2;
      }
      ccLab.attr('x', f.iw + 8).attr('y', yc + 4).text(narrow ? 'Basis' : 'Basis trade');
      jrLab.attr('x', f.iw + 8).attr('y', yj + 4).text(narrow ? 'Jr' : 'Jr carry');
      var b = breakEven();
      if (b <= 16) {
        be.style('display', null).attr('cx', x(b)).attr('cy', y(cc(b)));
        var right = x(b) > f.iw - 90;
        beLab.style('display', null).attr('x', x(b) + (right ? -10 : 10)).attr('y', y(cc(b)) + 18)
          .attr('text-anchor', right ? 'end' : 'start').text('break-even ' + J.pct(b));
        win.style('display', null).attr('x', x(b)).attr('width', f.iw - x(b));
        winLab.style('display', null).attr('x', Math.min(x(b) + 6, f.iw - 44));
      } else {
        be.style('display', 'none'); beLab.style('display', 'none');
        win.style('display', 'none'); winLab.style('display', 'none');
      }
    }
    update();

    if (!J.reduced && !root.dataset.drawn) {
      [ccPath, jrPath].forEach(function(p) {
        var len = p.node().getTotalLength();
        p.attr('stroke-dasharray', len + ' ' + len).attr('stroke-dashoffset', len);
      });
      J.onView(root, function() {
        root.dataset.drawn = '1';
        [ccPath, jrPath].forEach(function(p) {
          p.transition().duration(1200).ease(d3.easeCubicOut).attr('stroke-dashoffset', 0)
            .on('end', function() { d3.select(this).attr('stroke-dasharray', null); });
        });
      });
    }

    J.legend(root, [
      { color: J.C.other, label: 'Basis trade: long spot, short perp' },
      { color: J.C.jr, label: 'Jr carry: long Jr, short perp' }
    ]);
  });
})();
