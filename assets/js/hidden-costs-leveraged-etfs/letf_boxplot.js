(function() {
  var L = window.LETF;
  var classMap = function(cls) { return ['Country','Currency','Volatility'].indexOf(cls) >= 0 ? 'Other' : cls; };
  var classOrder = ['Equity Index','Equity Sector','Single Stock','Commodity','Fixed Income','Crypto','Other'];

  var container = document.getElementById('letf-boxplot');
  var w = container.clientWidth, h = container.clientHeight;
  var margin = { top: 20, right: 20, bottom: 50, left: 58 };
  var iw = w - margin.left - margin.right;
  var ih = h - margin.top - margin.bottom;

  var svg = d3.select(container).append('svg').attr('width', w).attr('height', h);
  var g = svg.append('g').attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

  // Group funds
  var groups = classOrder.map(function(cls) {
    var funds = L.funds.filter(function(f) { return classMap(f.asset_class) === cls && f.financing_premium != null; });
    var vals = funds.map(function(f) { return f.financing_premium; }).sort(function(a, b) { return a - b; });
    var q1 = d3.quantile(vals, 0.25);
    var med = d3.quantile(vals, 0.5);
    var q3 = d3.quantile(vals, 0.75);
    var iqr = q3 - q1;
    var lo = Math.max(d3.min(vals), q1 - 1.5 * iqr);
    var hi = Math.min(d3.max(vals), q3 + 1.5 * iqr);
    return { cls: cls, funds: funds, vals: vals, q1: q1, med: med, q3: q3, lo: lo, hi: hi };
  }).filter(function(g) { return g.funds.length > 0; });

  // Scales
  var xScale = d3.scaleBand().domain(groups.map(function(g) { return g.cls; })).range([0, iw]).padding(0.35);
  var yMax = Math.min(0.6, d3.max(L.funds, function(f) { return f.financing_premium || 0; }) * 1.05);
  var yScale = d3.scaleLinear().domain([0, yMax]).range([ih, 0]);
  var bw = xScale.bandwidth();

  // Grid
  g.append('g').selectAll('line').data(yScale.ticks(6)).join('line')
    .attr('x1', 0).attr('x2', iw).attr('y1', function(d) { return yScale(d); }).attr('y2', function(d) { return yScale(d); })
    .attr('stroke', '#eee').attr('stroke-width', 0.5);

  // Y axis
  g.append('g')
    .call(d3.axisLeft(yScale).ticks(6).tickFormat(function(d) { return (d * 100).toFixed(0) + '%'; }))
    .call(function(g) { g.select('.domain').attr('stroke', '#ddd'); })
    .call(function(g) { g.selectAll('.tick line').attr('stroke', '#ddd'); })
    .call(function(g) { g.selectAll('.tick text').attr('fill', '#757575').attr('font-size', '11px').attr('font-family', L.FONT); });

  // X axis
  g.append('g').attr('transform', 'translate(0,' + ih + ')')
    .call(d3.axisBottom(xScale).tickSize(0))
    .call(function(g) { g.select('.domain').attr('stroke', '#ddd'); })
    .call(function(g) { g.selectAll('.tick text').attr('fill', '#757575').attr('font-size', '11px').attr('font-family', L.FONT)
      .attr('transform', 'rotate(-25)').attr('text-anchor', 'end').attr('dx', '-4').attr('dy', '6'); });

  // Y axis label
  svg.append('text').attr('transform', 'rotate(-90)').attr('x', -(margin.top + ih / 2)).attr('y', 14)
    .attr('text-anchor', 'middle').attr('fill', '#757575').attr('font-size', '12px').attr('font-family', L.FONT)
    .text('Financing premium s (%)');

  // Draw boxes
  groups.forEach(function(grp) {
    var cx = xScale(grp.cls) + bw / 2;
    var color = L.CLASS_COLORS[grp.cls] || '#999';

    // Whiskers
    g.append('line').attr('x1', cx).attr('x2', cx)
      .attr('y1', yScale(grp.lo)).attr('y2', yScale(grp.hi))
      .attr('stroke', '#292929').attr('stroke-width', 1);
    g.append('line').attr('x1', cx - bw * 0.25).attr('x2', cx + bw * 0.25)
      .attr('y1', yScale(grp.lo)).attr('y2', yScale(grp.lo))
      .attr('stroke', '#292929').attr('stroke-width', 1);
    g.append('line').attr('x1', cx - bw * 0.25).attr('x2', cx + bw * 0.25)
      .attr('y1', yScale(grp.hi)).attr('y2', yScale(grp.hi))
      .attr('stroke', '#292929').attr('stroke-width', 1);

    // Box
    g.append('rect')
      .attr('x', xScale(grp.cls)).attr('y', yScale(grp.q3))
      .attr('width', bw).attr('height', yScale(grp.q1) - yScale(grp.q3))
      .attr('fill', color).attr('fill-opacity', 0.2)
      .attr('stroke', color).attr('stroke-opacity', 0.4).attr('stroke-width', 1);

    // Median
    g.append('line').attr('x1', xScale(grp.cls)).attr('x2', xScale(grp.cls) + bw)
      .attr('y1', yScale(grp.med)).attr('y2', yScale(grp.med))
      .attr('stroke', '#292929').attr('stroke-width', 2);

    // Jittered dots
    var jitter = d3.randomNormal(0, bw * 0.12);
    grp.funds.forEach(function(f) {
      g.append('circle')
        .attr('cx', cx + Math.max(-bw * 0.35, Math.min(bw * 0.35, jitter())))
        .attr('cy', yScale(f.financing_premium))
        .attr('r', 3.5)
        .attr('fill', color).attr('opacity', 0.65)
        .attr('stroke', color).attr('stroke-opacity', 0.3)
        .style('cursor', 'pointer')
        .on('mousemove', function(e) { L.showTooltip(e, f); })
        .on('mouseleave', L.hideTooltip);
    });

  });
})();
