(function() {
  var L = window.LETF;
  var container = document.getElementById('letf-bubble-viz');
  var w = container.clientWidth, h = container.clientHeight;

  var svg = d3.select(container).append('svg').attr('width', w).attr('height', h);
  var funds = L.funds.filter(function(f) { return f.aum != null && f.aum > 0; });

  var excessReturn = function(f) {
    var spot = f.period_spot_cagr != null ? f.period_spot_cagr : (f.spot_cagr != null ? f.spot_cagr : null);
    return (f.letf_cagr != null && spot != null) ? f.letf_cagr - spot : null;
  };

  var radiusScale = d3.scaleSqrt().domain([0, d3.max(funds, function(f) { return f.aum; })]).range([4, 45]);
  var colorScale = d3.scaleLinear().domain([-0.15, 0, 0.15]).range(['#e8a0a0', '#ccc', '#8fc5a8']).clamp(true);

  var nodes = funds.map(function(f) {
    return {
      fund: f, r: radiusScale(f.aum), excess: excessReturn(f),
      color: colorScale(excessReturn(f) || 0),
      x: w / 2 + (Math.random() - 0.5) * 100, y: h / 2 + (Math.random() - 0.5) * 100
    };
  });

  var classes = Array.from(new Set(funds.map(function(f) { return f.asset_class; })));
  var classCenters = {};
  var angleStep = (2 * Math.PI) / classes.length;
  classes.forEach(function(cls, i) {
    classCenters[cls] = {
      x: w / 2 + Math.cos(i * angleStep) * Math.min(w, h) * 0.22,
      y: h / 2 + Math.sin(i * angleStep) * Math.min(w, h) * 0.22
    };
  });

  d3.forceSimulation(nodes)
    .force('charge', d3.forceManyBody().strength(1))
    .force('center', d3.forceCenter(w / 2, h / 2).strength(0.02))
    .force('collision', d3.forceCollide(function(d) { return d.r + 1.5; }).strength(0.8))
    .force('cluster', d3.forceX(function(d) { return (classCenters[d.fund.asset_class] || {}).x || w / 2; }).strength(0.15))
    .force('clusterY', d3.forceY(function(d) { return (classCenters[d.fund.asset_class] || {}).y || h / 2; }).strength(0.15))
    .alphaDecay(0.02)
    .on('tick', function() {
      circles.attr('cx', function(d) { return d.x; }).attr('cy', function(d) { return d.y; });
      labels.attr('x', function(d) { return d.x; }).attr('y', function(d) { return d.y; });
    });

  var gBubbles = svg.append('g');
  var circles = gBubbles.selectAll('circle').data(nodes).join('circle')
    .attr('r', function(d) { return d.r; }).attr('fill', function(d) { return d.color; })
    .attr('stroke', function(d) { return d.fund.letf_beats_spot ? 'rgba(80,140,100,.3)' : 'rgba(180,100,100,.2)'; })
    .attr('stroke-width', 1).attr('opacity', 0.9).style('cursor', 'pointer')
    .on('mousemove', function(e, d) { L.showTooltip(e, d.fund); })
    .on('mouseleave', L.hideTooltip);

  var labels = gBubbles.selectAll('text').data(nodes.filter(function(d) { return d.r > 14; })).join('text')
    .attr('text-anchor', 'middle').attr('dominant-baseline', 'central')
    .attr('fill', function(d) { var ex = d.excess || 0; return Math.abs(ex) < 0.03 ? '#555' : '#fff'; })
    .attr('font-size', function(d) { return Math.max(7, d.r * 0.45) + 'px'; })
    .attr('pointer-events', 'none').attr('font-family', L.FONT).attr('font-weight', '600')
    .text(function(d) { return d.fund.ticker; });

  // Color legend
  var lg = svg.append('g').attr('transform', 'translate(' + (w - 170) + ',' + (h - 32) + ')');
  var defs = svg.append('defs');
  var grad = defs.append('linearGradient').attr('id', 'bgrad');
  grad.append('stop').attr('offset', '0%').attr('stop-color', '#e8a0a0');
  grad.append('stop').attr('offset', '50%').attr('stop-color', '#ccc');
  grad.append('stop').attr('offset', '100%').attr('stop-color', '#8fc5a8');
  lg.append('rect').attr('width', 130).attr('height', 5).attr('rx', 2.5).attr('fill', 'url(#bgrad)');
  lg.append('text').attr('x', 0).attr('y', 16).attr('fill', '#757575').attr('font-size', '10px').attr('font-family', L.FONT).text('Lags spot');
  lg.append('text').attr('x', 94).attr('y', 16).attr('fill', '#757575').attr('font-size', '10px').attr('font-family', L.FONT).text('Beats spot');
})();
