// Two carry trades run through six months of the same generated bitcoin path, as one continuous
// animation: cash and carry (#jpc-rebalance) and the Jr carry (#jpc-jrcarry). Bitcoin's price draws
// forward; the tanks (the long leg, margin), the short's leverage and the running totals follow it.
// When the short's leverage leaves its band, value pours through the pipe to bring it back to target.
// $100k at the start; funding at 10% a year; 0.15% cost per leg.
//
// Cash and carry holds spot against a 5× short, band 3.5×–7.5×.
// The Jr carry runs its short at the same 5×, band 3.5×–7.5×, as in the post's table: $78.9k in Jr,
// which holds a fixed amount of bitcoin against a dollar debt to Sr (1.337× at the start, ~$105k of
// exposure), shorts the same bitcoin, and keeps the other $21.1k as margin. Jr pays Sr ~7.7% a year
// on its debt. Funding is 10% a year for both, matching the table.
(function() {
  var J = window.JPC;
  var JRL_ = 1.337, COST = 0.0015, FUND = 0.10, SR = 0.077, JRL = 1.337, JRW = (1 / JRL_) / (1 / JRL_ + 1 / 5);
  var STEP = 0.1, WINDOW = 4;            // a rebalance pours over 4 days
  // A generated bitcoin path in $k: flat stretches, rallies and drops of different sizes, and a
  // small seeded wiggle on top, so it looks the same on every visit. Illustrative.
  var SEGMENTS = [[14, 0], [10, 10], [10, 0], [10, -10], [12, 0], [14, 14], [8, 0], [12, -8],
                  [10, 6], [12, -12], [10, 0], [14, 12], [10, 0], [10, -7], [14, 0]];   // [days, % move]
  var days = (function() {
    var seed = 5, out = [{ t: 0, p: 100 }], level = 100;
    function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646 - 0.5; }
    SEGMENTS.forEach(function(sg) {
      var end = level * (1 + sg[1] / 100);
      for (var k = 1; k <= sg[0]; k++) {
        var base = level + (end - level) * k / sg[0];
        out.push({ t: out.length, p: base + rnd() * 1.4 * base / 100 });
      }
      level = end;
    });
    return out;
  })();
  var N = days.length - 1;

  function priceAt(t) {
    var i = Math.min(N - 1, Math.floor(t)), f = t - i;
    return days[i].p + (days[i + 1].p - days[i].p) * f;
  }

  // Simulate on a 0.1-day grid, in $k. Each point: the long leg's value, margin, the short's notional
  // and leverage, rebalances so far, slippage and what's kept.
  function simulate(cfg) {
    var p0 = days[0].p, out = [], pour = null, n = 0, cost = 0, kept = 0, marks = [];
    var st = cfg.init(p0);
    for (var k = 0; k <= N / STEP; k++) {
      var t = +(k * STEP).toFixed(1), p = priceAt(t);
      if (k > 0) kept += cfg.step(st, p, priceAt(t - STEP));
      var lev = st.q * p / st.m;
      if (!(pour && t < pour.end) && Math.abs(t - Math.round(t)) < 1e-6 && (lev > cfg.HI || lev < cfg.LO)) {
        var to = cfg.target(st, p), dv = to.long - cfg.long(st, p);   // value moving into the long leg
        pour = { end: t + WINDOW, from: cfg.snapshot(st), to: to, cost: Math.abs(dv) * 2 * COST, dir: dv < 0 ? 1 : -1 };
        n++; cost += pour.cost; kept -= pour.cost; marks.push(t);
      }
      var flowing = pour && t < pour.end;
      if (flowing) cfg.pour(st, pour.from, pour.to, STEP / WINDOW, p, pour.cost * STEP / WINDOW);
      out.push({ t: t, p: p, long: cfg.long(st, p), margin: st.m, notional: st.q * p, lev: st.q * p / st.m,
                 n: n, cost: cost * 1000, kept: kept * 1000, dir: flowing ? pour.dir : 0 });
    }
    out.marks = marks;
    return out;
  }

  // Cash and carry: q bitcoin held, q shorted; margin m.
  var CC = {
    LO: 3.5, HI: 7.5, TARGET: 5, longName: 'Bitcoin', longColor: 'other',
    toMargin: 'Selling spot to top up margin', toLong: 'Buying spot with spare margin',
    init: function(p) { return { q: 83.333 / p, m: 16.667 }; },
    long: function(st, p) { return st.q * p; },
    step: function(st, p, p1) { var f = FUND / 365 * STEP * st.q * p; st.m += -st.q * (p - p1) + f; return f; },
    target: function(st, p) { var tot = st.q * p + st.m; return { long: tot * TARGETW(5), q: tot * TARGETW(5) / p }; },
    snapshot: function(st) { return { q: st.q, m: st.m }; },
    // Each step moves a slice of the bitcoin at today's price, between the long leg and margin.
    pour: function(st, a, b, k, p, c) { var dq = (b.q - a.q) * k; st.q += dq; st.m -= dq * p + c; }
  };
  function TARGETW(L) { return L / (L + 1); }   // share of capital in the long leg at short leverage L

  // The Jr carry: Jr holds Q bitcoin against a dollar debt D to Sr; equity E = Q·p − D. The short is Q too.
  var JC = {
    LO: 3.5, HI: 7.5, TARGET: JRL / (1 - JRW) * JRW, longName: 'Jr', longColor: 'jr',
    toMargin: 'Redeeming Jr to top up margin', toLong: 'Minting Jr with spare margin',
    init: function(p) { var e = 100 * JRW, q = JRL * e / p; return { q: q, d: q * p - e, m: 100 - e }; },
    long: function(st, p) { return st.q * p - st.d; },
    step: function(st, p, p1) {
      var f = FUND / 365 * STEP * st.q * p, c = SR / 365 * STEP * st.d;
      st.m += -st.q * (p - p1) + f; st.d += c;
      return f - c;
    },
    target: function(st, p) {
      var tot = st.q * p - st.d + st.m, e = tot * JRW, q = JRL * e / p;
      return { long: e, q: q, d: q * p - e };
    },
    snapshot: function(st) { return { q: st.q, d: st.d, m: st.m }; },
    // Each step mints or redeems a slice of Jr at today's price; the value moves to or from margin.
    pour: function(st, a, b, k, p, c) {
      var dq = (b.q - a.q) * k, dd = (b.d - a.d) * k;
      st.q += dq; st.d += dd; st.m -= dq * p - dd + c;
    }
  };

  var SECONDS = 45, HOLD = 3;   // six months play in about 45 seconds, slower while a pour runs, then hold

  function build(id, cfg) {
  var sim = simulate(cfg);
  function at(t) { return sim[Math.max(0, Math.min(sim.length - 1, Math.round(t / STEP)))]; }
  var LO = cfg.LO, HI = cfg.HI, TARGET = cfg.TARGET;
  J.mount(id, function(root) {
    var W = root.clientWidth, H = Math.min(W, 560);   // full column width; height capped
    var box = document.createElement('div');
    box.className = 'jpc-story';
    box.style.width = W + 'px'; box.style.height = H + 'px';
    root.appendChild(box);
    var svg = d3.select(box).append('svg').attr('width', W).attr('height', H)
      .style('position', 'absolute').style('left', 0).style('top', 0).style('transition', 'opacity .6s ease');
    var g = svg.append('g');
    var top = 34, bottom = H - 62, pad = 24, split = Math.round(W * 0.62);
    var mid = top + Math.round((bottom - top) * 0.56);

    // Dividers between the three parts: the time series, the tanks, and the stats row.
    g.append('line').attr('x1', split).attr('x2', split).attr('y1', top - 10).attr('y2', H - 36)
      .style('stroke', J.C.axis).attr('stroke-width', 1);
    g.append('line').attr('x1', pad).attr('x2', W - pad).attr('y1', H - 36).attr('y2', H - 36)
      .style('stroke', J.C.axis).attr('stroke-width', 1);

    // Left top: bitcoin's price over the year.
    var px = d3.scaleLinear().domain([0, N]).range([pad + 44, split - 32]);
    var py = d3.scaleLinear().domain(d3.extent(days, function(d) { return d.p; })).nice().range([mid - 22, top + 30]);
    g.append('text').attr('x', pad).attr('y', top + 4).attr('font-size', 12).style('fill', J.C.muted).text('Bitcoin');
    py.ticks(3).forEach(function(v) {
      g.append('line').attr('x1', px(0)).attr('x2', px(N)).attr('y1', py(v)).attr('y2', py(v)).style('stroke', J.C.grid);
      g.append('text').attr('x', px(0) - 6).attr('y', py(v) + 4).attr('text-anchor', 'end').attr('font-size', 10)
        .style('fill', J.C.muted).text('$' + v + 'k');
    });
    [0, 60, 120].forEach(function(d) {
      g.append('text').attr('x', px(d)).attr('y', bottom + 14).attr('text-anchor', d === 0 ? 'start' : 'middle')
        .attr('font-size', 10).style('fill', J.C.muted).text('Day ' + d);
    });
    var clipId = id + '-clip';
    var clip = g.append('clipPath').attr('id', clipId).append('rect').attr('height', H).attr('width', 0);
    var marksG = g.append('g').attr('clip-path', 'url(#' + clipId + ')');
    sim.marks.forEach(function(t) {
      [[top + 26, mid - 12], [mid + 32, bottom - 8]].forEach(function(span) {
        marksG.append('line').attr('x1', px(t)).attr('x2', px(t)).attr('y1', span[0]).attr('y2', span[1])
          .style('stroke', J.C.muted).attr('stroke-width', 1).attr('stroke-dasharray', '2,3');
      });
    });
    // The price line is redrawn each frame up to the current moment, ending exactly at the dot.
    var priceLine = d3.line().x(function(d) { return px(d.t); }).y(function(d) { return py(d.p); });
    var pricePath = g.append('path').attr('fill', 'none').style('stroke', J.C.other).attr('stroke-width', 2)
      .attr('stroke-linejoin', 'round');
    var halo = g.append('circle').attr('r', 4).style('fill', 'none').style('stroke', J.C.text).attr('stroke-width', 1.5).style('opacity', 0);
    var dot = g.append('circle').attr('r', 4).style('fill', J.C.text);

    // Left bottom: the short's leverage, with the 3.5x-7.5x band.
    g.append('line').attr('x1', pad).attr('x2', split - 12).attr('y1', mid + 1).attr('y2', mid + 1)
      .style('stroke', J.C.axis).attr('stroke-width', 1);   // divider between the two time series
    var ly = d3.scaleLinear().domain([0, 10]).range([bottom - 12, mid + 38]);
    g.append('text').attr('x', pad).attr('y', mid + 20).attr('font-size', 12).style('fill', J.C.muted).text('Perp position');
    g.append('rect').attr('x', px(0)).attr('width', px(N) - px(0)).attr('y', ly(HI)).attr('height', ly(LO) - ly(HI)).style('fill', J.C.fill);
    [0, 10].forEach(function(v) {
      g.append('line').attr('x1', px(0)).attr('x2', px(N)).attr('y1', ly(v)).attr('y2', ly(v)).style('stroke', J.C.grid);
      g.append('text').attr('x', px(0) - 6).attr('y', ly(v) + 4).attr('text-anchor', 'end').attr('font-size', 10)
        .style('fill', J.C.muted).text(v + '×');
    });
    g.append('line').attr('x1', px(0)).attr('x2', px(N)).attr('y1', ly(TARGET)).attr('y2', ly(TARGET))
      .style('stroke', J.C.muted).attr('stroke-dasharray', '4,3');
    g.append('text').attr('x', px(0) - 6).attr('y', ly(TARGET) + 4).attr('text-anchor', 'end').attr('font-size', 10)
      .style('fill', J.C.muted).text(+TARGET.toFixed(1) + '×');
    g.append('path').datum(sim).attr('clip-path', 'url(#' + clipId + ')').attr('fill', 'none')
      .style('stroke', J.C.perp).attr('stroke-width', 1.75)
      .attr('d', d3.line().x(function(d) { return px(d.t); }).y(function(d) { return ly(Math.min(10, d.lev)); }));

    // Right: two tanks joined by a pipe; the fluid is bitcoin held and margin.
    var base = bottom - 4, bh = d3.scaleLinear().domain([0, 120]).range([0, (base - (top + 30)) * 0.72]);
    var bw = Math.min(52, (W - split - 120) / 2), x2 = split + 16, x1 = W - pad - bw - 4, tankTop = base - bh(120);
    [x1, x2].forEach(function(x) {
      g.append('rect').attr('x', x - 3).attr('y', tankTop - 3).attr('width', bw + 6).attr('height', base - tankTop + 3)
        .attr('rx', 5).style('fill', 'none').style('stroke', J.C.axis).attr('stroke-width', 1.5);
    });
    var yp = tankTop + 26;   // the pipe runs along the top, just under the 'rebalance' label
    g.append('rect').attr('x', x2 + bw + 3).attr('y', yp - 6).attr('width', x1 - x2 - bw - 6).attr('height', 12)
      .style('fill', 'var(--ui-surface)').style('stroke', J.C.axis).attr('stroke-width', 1.5);
    var pipe = g.append('line').attr('x1', x2 + bw + 3).attr('x2', x1 - 3).attr('y1', yp).attr('y2', yp)
      .attr('stroke-width', 7).attr('stroke-dasharray', '8,6').style('opacity', 0);
    var spot = g.append('rect').attr('x', x1).attr('width', bw).attr('rx', 3).style('fill', J.C[cfg.longColor]);
    var margin = g.append('rect').attr('x', x2).attr('width', bw).attr('rx', 3).style('fill', J.C.perp);
    g.append('text').attr('x', x1 + bw / 2).attr('y', base + 16).attr('text-anchor', 'middle').attr('font-size', 11).style('fill', J.C.muted).text(cfg.longName);
    g.append('text').attr('x', x2 + bw / 2).attr('y', base + 16).attr('text-anchor', 'middle').attr('font-size', 11).style('fill', J.C.muted).text('Margin');
    var spotT = g.append('text').attr('x', x1 + bw / 2).attr('text-anchor', 'middle').attr('font-size', 12).style('fill', J.C.text);
    var marginT = g.append('text').attr('x', x2 + bw / 2).attr('text-anchor', 'middle').attr('font-size', 12).style('fill', J.C.text);
    var target = g.append('line').attr('x1', x2).attr('x2', x2 + bw).style('stroke', J.C.muted).style('opacity', 0.7).attr('stroke-dasharray', '4,3');
    var targetT = g.append('text').attr('x', x2 + bw + 8).attr('font-size', 10).style('fill', J.C.muted).style('opacity', 0.7).text(+TARGET.toFixed(1) + '× target');
    var liq = g.append('line').attr('x1', x2).attr('x2', x2 + bw).style('stroke', J.C.muted).style('opacity', 0.7).attr('stroke-width', 1.5);
    var liqT = g.append('text').attr('x', x2 + bw + 8).attr('font-size', 10).style('fill', J.C.muted).style('opacity', 0.7).text('liquidation');
    // The stats row: each stat in its own fixed column, with fixed-width digits, so a value that
    // gains a digit doesn't push the others along.
    var LABELS = ['Return', 'Rebalances', 'Slippage'];
    var COLS = [0, 0.36, 0.68];   // column starts, as fractions of the row
    var vals = LABELS.map(function(k, i) {
      var t = g.append('text').attr('x', pad + COLS[i] * (W - 2 * pad)).attr('y', H - 14).attr('font-size', 12)
        .style('font-variant-numeric', 'tabular-nums');
      t.append('tspan').text(k + ' ').style('fill', J.C.muted);
      return t.append('tspan').attr('font-weight', 600).style('fill', J.C.text);
    });

    var flowOff = 0, lvl = null;
    var pourT = g.append('text').attr('x', (x2 + bw + x1) / 2).attr('y', tankTop + 12).attr('text-anchor', 'middle')
      .attr('font-size', 10).style('fill', J.C.text).style('opacity', 0).text('rebalance');
    // What the strategy is doing right now, above the tanks.
    var actX = (split + W - pad) / 2;
    g.append('text').attr('x', actX).attr('y', top + 4).attr('text-anchor', 'middle').attr('font-size', 10)
      .style('fill', J.C.muted).style('letter-spacing', '0.06em').text('NOW');
    var actT = g.append('text').attr('x', actX).attr('y', top + 24).attr('text-anchor', 'middle').attr('font-size', 13)
      .attr('font-weight', 600).style('fill', J.C.text);
    function action(d) {
      if (d.dir > 0) return cfg.toMargin;
      if (d.dir < 0) return cfg.toLong;
      if (d.lev > HI - 1) return 'Rally: the short\u2019s margin is draining';
      if (d.lev < LO + 0.5) return 'Sell-off: spare margin piling up';
      return 'Holding the hedge, collecting funding';
    }
    // dt: seconds since the last frame (0 snaps the tanks to the value). The tank levels ease toward
    // the simulated values, slowly in normal moves and quickly while value pours through the pipe.
    function draw(t, dt) {
      var d = at(t);
      var tt = Math.min(t, N - 1e-9), now = { t: t, p: priceAt(tt) };
      pricePath.attr('d', priceLine(days.slice(0, Math.floor(tt) + 1).concat([now])));
      clip.attr('width', px(t));
      dot.attr('cx', px(t)).attr('cy', py(now.p));
      // While a rebalance runs, a ring pulses out from the dot.
      if (d.dir) {
        var ph = (performance.now() / 900) % 1;
        halo.attr('cx', px(t)).attr('cy', py(now.p)).attr('r', 4 + 10 * ph).style('opacity', 0.8 * (1 - ph));
        dot.attr('r', 4 + 1.5 * Math.sin(ph * Math.PI));
      } else {
        halo.style('opacity', 0);
        dot.attr('r', 4);
      }
      if (!lvl || !dt) lvl = { spot: d.long, margin: d.margin, notional: d.notional };
      else {
        var k = 1 - Math.exp(-dt / (d.dir ? 0.12 : 0.7));
        lvl.spot += (d.long - lvl.spot) * k;
        lvl.notional += (d.notional - lvl.notional) * k;
        lvl.margin += (d.margin - lvl.margin) * k;
      }
      spot.attr('y', base - bh(lvl.spot)).attr('height', bh(lvl.spot));
      margin.attr('y', base - bh(lvl.margin)).attr('height', bh(lvl.margin));
      spotT.attr('y', base - bh(lvl.spot) - 6).text('$' + lvl.spot.toFixed(0) + 'k');
      marginT.attr('y', base - bh(lvl.margin) - 6).text('$' + lvl.margin.toFixed(0) + 'k');
      var ty = base - bh(lvl.notional / TARGET), lyy = base - bh(0.03 * lvl.notional);
      target.attr('y1', ty).attr('y2', ty); targetT.attr('y', ty + 3);
      liq.attr('y1', lyy).attr('y2', lyy); liqT.attr('y', lyy + 3);
      var idle = d.lev < LO;
      margin.style('fill', idle ? J.C.margin : J.C.perp);

      pipe.style('opacity', d.dir ? 1 : 0).style('stroke', d.dir > 0 ? J.C[cfg.longColor] : J.C.perp);
      pourT.style('opacity', d.dir ? 1 : 0);
      var a = action(d);
      if (actT.text() !== a) actT.text(a);
      if (d.dir) { flowOff += d.dir * 1.4; pipe.attr('stroke-dashoffset', flowOff); }

      vals[0].text((d.kept < 0 ? '\u2212$' : '+$') + d3.format(',')(Math.abs(Math.round(d.kept))));
      vals[1].text(d.n);
      vals[2].text(d.n ? '\u2212' + (d.cost / 10).toFixed(1) + ' bps' : '0 bps');
    }

    if (J.reduced) { draw(N, 0); return; }

    // Play while on screen; pause off screen; loop with a soft fade.
    var clock = 0, day = 0, last = null, visible = false, fading = false, seen = 0, hold = 0;
    draw(0, 0);
    var timer = d3.timer(function(now) {
      if (!document.body.contains(box)) { timer.stop(); return; }
      var dt = last == null ? 0 : (now - last) / 1000;
      last = now;
      if (!visible || fading) return;
      // A rebalance holds the timeline for a moment before the pour, for emphasis.
      var cur = at(day);
      if (cur.n > seen) { seen = cur.n; hold = 0.8; }
      if (hold > 0) { hold -= dt; draw(day, dt); return; }
      // Time runs at a steady pace, and at a quarter of it while value pours through the pipe.
      clock += dt * (day < N && cur.dir ? 0.25 : 1);
      if (clock >= SECONDS + HOLD) {
        fading = true;
        svg.style('opacity', 0);
        setTimeout(function() { clock = 0; day = 0; seen = 0; draw(0, 0); svg.style('opacity', 1); fading = false; }, 700);
        return;
      }
      day = Math.min(N, N * clock / SECONDS);
      draw(day, dt);
    });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function(es) { visible = es[0].isIntersecting; }, { threshold: 0.4 }).observe(box);
    } else visible = true;
  });
  }

  build('jpc-rebalance', CC);
  build('jpc-jrcarry', JC);
})();
