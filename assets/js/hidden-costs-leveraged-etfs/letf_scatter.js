(function() {
  var L = window.LETF;
  var funds = L.funds.filter(function(f) { return f.spot_sigma != null && f.financing_premium != null; });
  var container = document.getElementById('letf-scatter');
  var w = container.clientWidth, h = container.clientHeight;
  var margin = { top: 20, right: 20, bottom: 44, left: 58 };
  var iw = w - margin.left - margin.right;
  var ih = h - margin.top - margin.bottom;

  var svg = d3.select(container).append('svg').attr('width', w).attr('height', h);
  var g = svg.append('g').attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

  var xMax = Math.min(1.0, d3.max(funds, function(f) { return f.spot_sigma; }) * 1.05);
  var xScale = d3.scaleLinear().domain([0, xMax]).range([0, iw]);
  var yMax = Math.min(0.6, d3.max(funds, function(f) { return f.financing_premium; }) * 1.05);
  var yScale = d3.scaleLinear().domain([0, yMax]).range([ih, 0]);
  var rScale = d3.scaleSqrt().domain([0, d3.max(funds, function(f) { return f.aum || 0; })]).range([3, 24]);

  // Grid
  g.append('g').selectAll('line').data(yScale.ticks(6)).join('line')
    .attr('x1', 0).attr('x2', iw).attr('y1', function(d) { return yScale(d); }).attr('y2', function(d) { return yScale(d); })
    .attr('stroke', '#eee').attr('stroke-width', 0.5);

  // Axes
  g.append('g').attr('transform', 'translate(0,' + ih + ')')
    .call(d3.axisBottom(xScale).ticks(8).tickFormat(function(d) { return (d * 100).toFixed(0) + '%'; }))
    .call(function(g) { g.select('.domain').attr('stroke', '#ddd'); })
    .call(function(g) { g.selectAll('.tick line').attr('stroke', '#ddd'); })
    .call(function(g) { g.selectAll('.tick text').attr('fill', '#757575').attr('font-size', '11px').attr('font-family', L.FONT); });

  g.append('g')
    .call(d3.axisLeft(yScale).ticks(6).tickFormat(function(d) { return (d * 100).toFixed(0) + '%'; }))
    .call(function(g) { g.select('.domain').attr('stroke', '#ddd'); })
    .call(function(g) { g.selectAll('.tick line').attr('stroke', '#ddd'); })
    .call(function(g) { g.selectAll('.tick text').attr('fill', '#757575').attr('font-size', '11px').attr('font-family', L.FONT); });

  // Axis labels
  svg.append('text').attr('x', margin.left + iw / 2).attr('y', h - 4)
    .attr('text-anchor', 'middle').attr('fill', '#757575').attr('font-size', '12px').attr('font-family', L.FONT)
    .text('Underlying annualized volatility (\u03c3)');
  svg.append('text').attr('transform', 'rotate(-90)').attr('x', -(margin.top + ih / 2)).attr('y', 14)
    .attr('text-anchor', 'middle').attr('fill', '#757575').attr('font-size', '12px').attr('font-family', L.FONT)
    .text('Financing premium s (%)');

  // Bubbles
  var sorted = funds.slice().sort(function(a, b) { return (b.aum || 0) - (a.aum || 0); });
  g.selectAll('circle').data(sorted).join('circle')
    .attr('cx', function(d) { return xScale(d.spot_sigma); })
    .attr('cy', function(d) { return yScale(d.financing_premium); })
    .attr('r', function(d) { return rScale(d.aum || 0); })
    .attr('fill', function(d) { return L.CLASS_COLORS[d.asset_class] || '#999'; })
    .attr('opacity', 0.7)
    .attr('stroke', function(d) { return L.CLASS_COLORS[d.asset_class] || '#999'; })
    .attr('stroke-opacity', 0.3)
    .style('cursor', 'pointer')
    .on('mousemove', function(e, d) { L.showTooltip(e, d); })
    .on('mouseleave', L.hideTooltip);

  // Legend
  var classes = ['Equity Index', 'Equity Sector', 'Single Stock', 'Commodity', 'Fixed Income', 'Crypto', 'Other'];
  var lg = svg.append('g').attr('transform', 'translate(' + (margin.left + 8) + ',' + (margin.top + 6) + ')');
  classes.forEach(function(cls, i) {
    var col = i < 4 ? 0 : 1;
    var row = i < 4 ? i : i - 4;
    var lx = col * 120, ly = row * 14;
    lg.append('circle').attr('cx', lx + 4).attr('cy', ly).attr('r', 4).attr('fill', L.CLASS_COLORS[cls] || '#999').attr('opacity', 0.7);
    lg.append('text').attr('x', lx + 12).attr('y', ly + 3.5).attr('fill', '#757575').attr('font-size', '10px').attr('font-family', L.FONT).text(cls);
  });
})();
