// A coin-toss knockout: 1,024 contestants as dots, half go home each round, one is left after ten.
// Eliminations come in lines, stripes and blocks, chosen at random, and it loops while on screen.
// No text inside the visual.
(function() {
  var J = window.BLV;
  var N = 1024;
  var run = 0;   // bumped on every (re)start so stale timers from an earlier run stop
  var io = null; // one observer at a time; a redraw on resize replaces it

  // Contestants still in the game are green: an emerald that holds up on the light and the dark page.
  var css = document.createElement('style');
  css.textContent = ':root{--blv-alive:#1fa971;}:root[data-theme=dark]{--blv-alive:#34d08c;}';
  document.head.appendChild(css);
  var ALIVE = 'var(--blv-alive)';

  J.mount('blv-knockout', function(root) {
    run++;   // a redraw cancels whatever the previous drawing was doing
    var w = Math.max(280, root.clientWidth);
    var COLS = w < 500 ? 32 : 64, ROWS = N / COLS;   // 64 x 16 on a wide screen, 32 x 32 on a phone
    var cell = w / COLS, r = cell * 0.425;
    var W = COLS * cell, H = ROWS * cell;
    var svg = d3.select(root).append('svg').attr('width', W).attr('height', H).attr('viewBox', '0 0 ' + W + ' ' + H)
      .style('display', 'block').style('overflow', 'visible')
      .attr('role', 'img').attr('aria-label', '1,024 dots. Half are removed in each of ten rounds until one is left.');
    var data = d3.range(N).map(function(i) {
      return { i: i, c: i % COLS, r: Math.floor(i / COLS), x: (i % COLS + 0.5) * cell, y: (Math.floor(i / COLS) + 0.5) * cell };
    });
    function log2(n) { return Math.round(Math.log(n) / Math.LN2); }
    var dots = svg.selectAll('circle.d').data(data).join('circle').attr('class', 'd')
      .attr('cx', function(d) { return d.x; }).attr('cy', function(d) { return d.y; }).attr('r', r);
    // CSS transitions, not d3 ones: a dot's state is always set outright, so nothing is left half-way
    // if a frame is skipped or the tab is in the background.
    function ease(on) { dots.style('transition', on ? 'opacity .4s ease, fill .4s ease' : 'none'); }
    var ring = svg.append('circle').attr('fill', 'none').style('stroke', J.C.brk).attr('stroke-width', 1.5).style('opacity', 0);

    function reset() {
      ease(false);
      dots.attr('r', r).style('fill', ALIVE).style('opacity', 0.9);
      ring.style('transition', 'none').style('opacity', 0);
    }
    function crown(d, animate) {
      dots.filter(function(x) { return x.i === d.i; }).raise()
        .attr('r', r * 2.1).style('fill', J.C.brk).style('opacity', 1);
      ring.attr('cx', d.x).attr('cy', d.y).attr('r', r * 4.2)
        .style('transition', animate ? 'opacity .8s ease' : 'none').style('opacity', 0.6);
    }
    function play(animate) {
      var me = ++run;
      idle = false;
      reset();
      var alive = data.slice();
      // Each round takes one binary digit of the column or row number and drops everyone on one side
      // of it: a low digit gives alternating stripes, a high digit gives bands or half the floor.
      // Ten digits, ten rounds, one left.
      var cuts = [];
      d3.range(log2(COLS)).forEach(function(b) { cuts.push({ dim: 'c', bit: b }); });
      d3.range(log2(ROWS)).forEach(function(b) { cuts.push({ dim: 'r', bit: b }); });
      cuts = d3.shuffle(cuts);
      if (animate) requestAnimationFrame(function() { if (me === run) ease(true); });
      function step() {
        if (me !== run || !document.body.contains(root)) return;
        if (alive.length === 1) {
          crown(alive[0], animate);
          // hold on the winner, then start over; wait if the chart has scrolled out of view
          if (animate) setTimeout(function() { if (me !== run) return; idle = true; if (visible) play(true); }, 3000);
          return;
        }
        var cut = cuts.pop(), side = Math.random() < 0.5 ? 0 : 1;
        var gone = function(d) { return ((d[cut.dim] >> cut.bit) & 1) === side; };
        var out = {};
        alive.forEach(function(d) { if (gone(d)) out[d.i] = 1; });
        alive = alive.filter(function(d) { return !gone(d); });
        var losers = dots.filter(function(d) { return out[d.i]; });
        if (!animate) losers.style('fill', J.C.other).style('opacity', 0.16);
        else {
          // the fade runs along each line like a wave: one timer per row (or column)
          var key = cut.dim === 'c' ? 'r' : 'c', gap = cut.dim === 'c' ? 22 : 7;
          d3.range(cut.dim === 'c' ? ROWS : COLS).forEach(function(k) {
            setTimeout(function() {
              if (me !== run) return;
              losers.filter(function(d) { return d[key] === k; }).style('fill', J.C.other).style('opacity', 0.16);
            }, k * gap);
          });
        }
        if (animate) setTimeout(step, 1250); else step();
      }
      if (animate) setTimeout(step, 1000); else step();
    }

    var visible = false, idle = true;
    if (J.reduced) { play(false); return; }
    reset();
    if ('IntersectionObserver' in window) {
      if (io) io.disconnect();
      io = new IntersectionObserver(function(es) {
        visible = es[0].isIntersecting;
        if (visible && idle) play(true);
      }, { threshold: 0.4 });
      io.observe(root);
    } else { visible = true; play(true); }
  });
})();
