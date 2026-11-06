// Viz: perpetual tranching as the hero's river, seen from above. A choppy river (the asset) runs in
// from the left and splits at a weir. The top branch is a wide run of rapids (Jr, levered): fast,
// scattered foam. The bottom branch is a narrow stone-lined canal (Sr, stable): slow, even streaks.
(function() {
  var J = window.JPC;

  J.mount('jpc-tranche', function(root) {
    var W = Math.max(300, root.clientWidth), H = 240, narrow = W < 520;
    var svg = d3.select(root).append('svg').attr('width', W).attr('height', H).attr('viewBox', '0 0 ' + W + ' ' + H);
    var g = svg.append('g');

    var cy = H / 2, forkX = Math.round(W * (narrow ? 0.34 : 0.36)), x1 = W - (narrow ? 60 : 118);
    var yJr = cy - 62, ySr = cy + 64;
    var wIn = 34, wJr = 42, wSr = 16;

    // Centre lines. The incoming river wanders, like a price; the branches ease off the weir.
    var inPts = d3.range(0, forkX + 1, 4).map(function(x) {
      var fade = Math.min(1, (forkX - x) / 40);
      return [x, cy + fade * (7 * Math.sin(x / 31) + 3 * Math.sin(x / 11 + 1))];
    });
    var line = d3.line().curve(d3.curveBasis);
    var dIn = line(inPts);
    var bend = Math.min(130, (x1 - forkX) * 0.35);
    var dJr = 'M' + forkX + ',' + cy + 'C' + (forkX + bend * 0.5) + ',' + cy + ' ' + (forkX + bend * 0.5) + ',' + yJr + ' ' + (forkX + bend) + ',' + yJr + 'L' + x1 + ',' + yJr;
    var dSr = 'M' + forkX + ',' + cy + 'C' + (forkX + bend * 0.5) + ',' + cy + ' ' + (forkX + bend * 0.5) + ',' + ySr + ' ' + (forkX + bend) + ',' + ySr + 'L' + x1 + ',' + ySr;

    // Water, drawn as thick strokes over slightly thicker banks.
    function river(d, w, color, op, bank) {
      g.append('path').attr('d', d).style('fill', 'none').style('stroke', bank).attr('stroke-width', w + 5)
        .attr('stroke-linejoin', 'round');
      // An opaque base so the bank doesn't show through the translucent water.
      g.append('path').attr('d', d).style('fill', 'none').style('stroke', J.C.surface).attr('stroke-width', w)
        .attr('stroke-linejoin', 'round');
      return g.append('path').attr('d', d).style('fill', 'none').style('stroke', color).style('stroke-opacity', op)
        .attr('stroke-width', w).attr('stroke-linejoin', 'round');
    }
    var bank = 'var(--ui-border)';
    river(dJr, wJr, J.C.jr, 0.32, bank);
    river(dSr, wSr, J.C.margin, 0.3, J.C.other);          // stone-lined: a harder edge
    river(dIn, wIn, J.C.other, 0.3, bank);

    // The weir: a line of stones across the river where it splits.
    d3.range(-wIn / 2 + 2, wIn / 2 - 1, 4).forEach(function(dy) {
      g.append('rect').attr('x', forkX - 2).attr('y', cy + dy).attr('width', 4).attr('height', 3).attr('rx', 1)
        .style('fill', J.C.muted);
    });
    // Rocks breaking the rapids.
    [[0.45, -0.25], [0.6, 0.3], [0.72, -0.1], [0.86, 0.22]].forEach(function(r) {
      g.append('ellipse').attr('cx', forkX + bend + (x1 - forkX - bend) * r[0]).attr('cy', yJr + r[1] * wJr)
        .attr('rx', 4).attr('ry', 3).style('fill', J.C.muted).style('opacity', 0.7);
    });

    // Scenery, drawn under the water: grass, reeds, trees, boulders, a cottage on the island and a
    // footbridge over the canal. Spots are tested against the river shapes so nothing lands in the
    // water or on a label. Muted and translucent so the water stays the subject.
    var scene = g.insert('g', ':first-child'), over = g.append('g');
    var probe = g.append('g').style('visibility', 'hidden');
    function zone(pad) {
      return [dIn, dJr, dSr].map(function(d, i) {
        return probe.append('path').attr('d', d).style('fill', 'none').style('stroke', '#000')
          .attr('stroke-width', [wIn, wJr, wSr][i] + pad).node();
      });
    }
    var wet = zone(10), nearBank = zone(34), clear = zone(48);
    var inAny = function(ps, x, y) {
      var pt = new DOMPoint(x, y);
      return ps.some(function(p) { return p.isPointInStroke(pt); });
    };
    var labels = [[0, cy - wIn / 2 - 44, 100, 40], [x1 + 4, yJr - 18, W - x1, 40], [x1 + 4, ySr - 18, W - x1, 40]];
    var onLabel = function(x, y, r) {
      return labels.some(function(b) { return x + r > b[0] && x - r < b[0] + b[2] && y + r > b[1] && y - r < b[1] + b[3]; });
    };
    var srand = d3.randomLcg(42), rnd = function(a, b) { return a + (b - a) * srand(); };
    var GREEN = '#5f8a4e', DARK = '#3f6a35', STONE = '#9a958a';

    // Grass: faint patches of land, then tufts and reeds along the banks.
    for (var i = 0; i < 26; i++) {
      var px_ = rnd(0, W), py_ = rnd(4, H - 4);
      if (!inAny(clear, px_, py_)) continue;
      scene.append('ellipse').attr('cx', px_).attr('cy', py_).attr('rx', rnd(30, 70)).attr('ry', rnd(10, 22))
        .style('fill', GREEN).style('opacity', 0.07);
    }
    for (i = 0; i < 260; i++) {
      var tx = rnd(0, W), ty = rnd(2, H - 2);
      if (!inAny(nearBank, tx, ty) || inAny(wet, tx, ty) || onLabel(tx, ty, 2)) continue;
      var hgt = rnd(3, 6), lean = rnd(-1.5, 1.5);
      scene.append('path').attr('d', 'M' + tx + ',' + ty + 'l' + lean + ',' + (-hgt) + 'M' + tx + ',' + ty + 'l' + (lean + 2) + ',' + (-hgt + 1.5))
        .style('stroke', i % 3 ? GREEN : DARK).style('stroke-opacity', 0.55).attr('stroke-width', 1.1).attr('stroke-linecap', 'round');
    }
    // Trees, seen from above: a shadow, a canopy and a highlight.
    var placed = 0;
    for (i = 0; i < 400 && placed < (narrow ? 9 : 16); i++) {
      var cx_ = rnd(6, W - 6), cy_ = rnd(8, H - 8), r = rnd(7, 13);
      if (inAny(clear, cx_, cy_) || inAny(nearBank, cx_ + r, cy_) || inAny(nearBank, cx_ - r, cy_) ||
          inAny(nearBank, cx_, cy_ + r) || inAny(nearBank, cx_, cy_ - r) || onLabel(cx_, cy_, r)) continue;
      scene.append('circle').attr('cx', cx_ + 2).attr('cy', cy_ + 2).attr('r', r).style('fill', DARK).style('opacity', 0.14);
      scene.append('circle').attr('cx', cx_).attr('cy', cy_).attr('r', r).style('fill', GREEN).style('opacity', 0.32);
      scene.append('circle').attr('cx', cx_ - r / 3).attr('cy', cy_ - r / 3).attr('r', r / 2.6).style('fill', GREEN).style('opacity', 0.3);
      placed++;
    }
    // Boulders on the rapids' banks.
    for (i = 0; i < 120 && placed < 999; i++) {
      var bx = rnd(forkX + bend * 0.6, x1), by = yJr + (srand() < 0.5 ? -1 : 1) * (wJr / 2 + rnd(5, 9));
      if (inAny(wet, bx, by) || onLabel(bx, by, 4)) continue;
      scene.append('ellipse').attr('cx', bx).attr('cy', by).attr('rx', rnd(2.5, 4.5)).attr('ry', rnd(2, 3.2))
        .style('fill', STONE).style('opacity', 0.55);
      if (i > 60) break;
    }
    // Stones lining the canal's straight run.
    for (var sx = forkX + bend + 4; sx < x1 - 4; sx += 9) {
      [-1, 1].forEach(function(sd) {
        scene.append('rect').attr('x', sx).attr('y', ySr + sd * (wSr / 2 + 4) - 1.5).attr('width', 6).attr('height', 3).attr('rx', 1)
          .style('fill', STONE).style('opacity', 0.45);
      });
    }
    // A cottage on the island between the branches, with a path down to a footbridge over the canal.
    var hx = forkX + bend + (x1 - forkX - bend) * 0.32, hy = cy + 4;
    if (!narrow) {
      scene.append('path').attr('d', 'M' + (hx + 10) + ',' + (hy + 8) + 'Q' + (hx + 18) + ',' + (hy + 26) + ' ' + (hx + 34) + ',' + (ySr - wSr / 2 - 6))
        .style('fill', 'none').style('stroke', STONE).style('stroke-opacity', 0.45).attr('stroke-width', 3).attr('stroke-linecap', 'round');
      scene.append('rect').attr('x', hx - 11).attr('y', hy - 8).attr('width', 24).attr('height', 17).attr('rx', 1.5)
        .style('fill', '#a0704a').style('opacity', 0.55);
      scene.append('rect').attr('x', hx - 11).attr('y', hy - 1).attr('width', 24).attr('height', 2).style('fill', '#7a5233').style('opacity', 0.55);
      scene.append('rect').attr('x', hx + 6).attr('y', hy - 13).attr('width', 4).attr('height', 5).style('fill', STONE).style('opacity', 0.6);
      var fb = hx + 34;
      for (var k = 0; k < 4; k++) {
        over.append('rect').attr('x', fb - 6).attr('y', ySr - wSr / 2 - 5 + k * ((wSr + 10) / 4)).attr('width', 12).attr('height', (wSr + 10) / 4 - 1)
          .style('fill', '#a0704a').style('opacity', 0.6);
      }
    }
    probe.remove();

    // Labels.
    var lab = function(x, y, a, b) {
      var t = g.append('text').attr('x', x).attr('y', y).attr('font-size', 12).style('fill', J.C.text);
      t.append('tspan').attr('font-weight', 600).text(a);
      if (b) t.append('tspan').attr('x', x).attr('dy', 14).attr('font-size', 11).style('fill', J.C.muted).text(b);
    };
    lab(6, cy - wIn / 2 - 26, 'Bitcoin');
    lab(x1 + 10, yJr - 2, 'BTC Jr', narrow ? 'levered' : 'rapids: levered');
    lab(x1 + 10, ySr - 2, 'BTC Sr', narrow ? 'stable' : 'calm canal: stable');

    // Flow: particles along each centre line, offset across the stream.
    var paths = {
      in: g.append('path').attr('d', dIn).style('display', 'none').node(),
      jr: g.append('path').attr('d', dJr).style('display', 'none').node(),
      sr: g.append('path').attr('d', dSr).style('display', 'none').node()
    };
    var rng = d3.randomLcg(7);
    function flow(key, n, w, speed, kind) {
      var len = paths[key].getTotalLength();
      return d3.range(n).map(function(i) {
        return { key: key, len: len, w: w, speed: speed * (kind === 'foam' ? 0.8 + 0.5 * rng() : 1),
          s0: len * i / n + rng() * len / n, off: (rng() - 0.5) * w * (kind === 'streak' ? 0.15 : 0.8),
          ph: rng() * 6.28, kind: kind };
      });
    }
    var parts = flow('in', narrow ? 26 : 40, wIn, 55, 'chop')
      .concat(flow('jr', narrow ? 55 : 90, wJr, 105, 'foam'))
      .concat(flow('sr', narrow ? 6 : 9, wSr, 40, 'streak'));
    var fg = g.append('g');
    var marks = fg.selectAll('line').data(parts).join('line')
      .style('stroke', function(d) { return d.kind === 'streak' ? J.C.margin : d.kind === 'foam' ? '#fff' : J.C.other; })
      .style('stroke-opacity', function(d) { return d.kind === 'foam' ? 0.9 : 0.75; })
      .attr('stroke-width', function(d) { return d.kind === 'foam' ? 2 : 1.6; })
      .attr('stroke-linecap', 'round');

    function at(p, s) {
      var a = p.getPointAtLength(Math.max(0, s - 1)), b = p.getPointAtLength(s + 1);
      var dx = b.x - a.x, dy = b.y - a.y, n = Math.hypot(dx, dy) || 1;
      return { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2, tx: dx / n, ty: dy / n };
    }
    function draw(t) {
      marks.each(function(d) {
        var s = (d.s0 + t * d.speed) % d.len, p = at(paths[d.key], s);
        // Chop and foam wobble across the stream; the canal's streaks hold their line.
        var wob = d.kind === 'streak' ? 0 : Math.sin(t * (d.kind === 'foam' ? 9 : 4) + d.ph) * d.w * (d.kind === 'foam' ? 0.12 : 0.08);
        var o = d.off + wob, x = p.x - p.ty * o, y = p.y + p.tx * o;
        var L = d.kind === 'streak' ? 14 : d.kind === 'foam' ? 2.5 : 5;
        d3.select(this).attr('x1', x - p.tx * L / 2).attr('y1', y - p.ty * L / 2).attr('x2', x + p.tx * L / 2).attr('y2', y + p.ty * L / 2);
      });
    }

    if (J.reduced) { draw(4); return; }
    draw(0);
    var t = 0, last = null, visible = false;
    var timer = d3.timer(function(now) {
      if (!document.body.contains(root)) { timer.stop(); return; }
      var dt = last == null ? 0 : (now - last) / 1000; last = now;
      if (!visible) return;
      t += dt;
      draw(t);
    });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function(es) { visible = es[0].isIntersecting; }, { threshold: 0.2 }).observe(root);
    } else visible = true;
  });
})();
