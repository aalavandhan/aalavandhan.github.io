// Moving user co-locations — animated inline SVG.
// A red tracked user and 28 contacts move through a street network; contacts
// turn red when they enter the tracked user's moving radius, and each entry is
// counted as a co-location. Renders into the #viz SVG embedded in the post.
(() => {
  "use strict";

  const NS = "http://www.w3.org/2000/svg";
  const svg = document.querySelector("#viz");
  const roadLayer = document.querySelector("#roads");
  const fillLayer = document.querySelector("#cellFills");
  const cellLayer = document.querySelector("#cells");
  const siteLayer = document.querySelector("#sites");
  const linkLayer = document.querySelector("#links");
  const contactLayer = document.querySelector("#contacts");
  const targetLayer = document.querySelector("#target");
  const burstLayer = document.querySelector("#entryBursts");
  const hudCurrent = document.querySelector("#hudCurrent");
  const hudTotal = document.querySelector("#hudTotal");

  const bounds = { x0: 16, y0: 29, x1: 584, y1: 364 };
  const CONTACT_COUNT = 28;
  const COLOCATION_RADIUS = 48;
  const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

  let random = makeRandom((Date.now() ^ 0x5f3759df) >>> 0);
  let graph = null;
  let contacts = [];
  let target = null;
  let cellFills = [];
  let activeCell = -1;
  let playing = false; // flipped on by updateRunState() once reset() runs
  let lastFrame = performance.now();
  let totalEntries = 0;

  const sites = [
    [30, 61], [142, 72], [263, 70], [349, 69], [459, 58], [560, 62],
    [110, 167], [200, 147], [292, 145], [400, 146], [519, 146],
    [46, 233], [154, 232], [263, 259], [350, 247], [458, 234], [575, 222],
    [117, 324], [207, 323], [294, 322], [395, 340], [518, 307]
  ];

  function el(name, attrs = {}, parent) {
    const node = document.createElementNS(NS, name);
    for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
    if (parent) parent.appendChild(node);
    return node;
  }

  function clear(node) { while (node.firstChild) node.removeChild(node.firstChild); }

  function makeRandom(seed) {
    return function rand() {
      seed |= 0;
      seed = seed + 0x6D2B79F5 | 0;
      let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }

  function pathD(points, close = false) {
    return points.map((p, i) => `${i ? "L" : "M"}${p[0].toFixed(2)},${p[1].toFixed(2)}`).join(" ") + (close ? " Z" : "");
  }

  function clipHalfPlane(poly, nx, ny, c) {
    const out = [];
    for (let i = 0; i < poly.length; i++) {
      const a = poly[i];
      const b = poly[(i + 1) % poly.length];
      const da = nx * a[0] + ny * a[1] - c;
      const db = nx * b[0] + ny * b[1] - c;
      const aInside = da <= 1e-7;
      const bInside = db <= 1e-7;
      if (aInside) out.push(a);
      if (aInside !== bInside) {
        const t = da / (da - db);
        out.push([a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t]);
      }
    }
    return out;
  }

  function voronoiCell(index) {
    const s = sites[index];
    let poly = [[14, 10], [586, 10], [586, 366], [14, 366]];
    for (let j = 0; j < sites.length && poly.length; j++) {
      if (j === index) continue;
      const q = sites[j];
      const nx = q[0] - s[0];
      const ny = q[1] - s[1];
      const c = (q[0] * q[0] + q[1] * q[1] - s[0] * s[0] - s[1] * s[1]) / 2;
      poly = clipHalfPlane(poly, nx, ny, c);
    }
    return poly;
  }

  function nearestSite(x, y) {
    let best = 0;
    let bestD = Infinity;
    for (let i = 0; i < sites.length; i++) {
      const dx = x - sites[i][0];
      const dy = y - sites[i][1];
      const d = dx * dx + dy * dy;
      if (d < bestD) { bestD = d; best = i; }
    }
    return best;
  }

  function drawCells() {
    clear(fillLayer); clear(cellLayer); clear(siteLayer);
    cellFills = [];
    sites.forEach((site, i) => {
      const poly = voronoiCell(i);
      cellFills[i] = el("path", {
        d: pathD(poly, true), fill: "#ef4a38", "fill-opacity": "0", stroke: "none"
      }, fillLayer);
      el("path", {
        d: pathD(poly, true), fill: "none", stroke: "#111c23", "stroke-opacity": ".93",
        "stroke-width": "2", "stroke-linejoin": "round", "vector-effect": "non-scaling-stroke"
      }, cellLayer);
      el("circle", {
        cx: site[0], cy: site[1], r: "2.2", fill: "#edf6f7", stroke: "#4c5c65", "stroke-width": "1.3"
      }, siteLayer);
    });
  }

  function buildRoadGraph() {
    const cols = 10;
    const rows = 7;
    const nodes = [];
    const byRC = [];
    const xStep = (bounds.x1 - bounds.x0 - 34) / (cols - 1);
    const yStep = (bounds.y1 - bounds.y0 - 24) / (rows - 1);

    for (let r = 0; r < rows; r++) {
      byRC[r] = [];
      for (let c = 0; c < cols; c++) {
        const edgeX = c === 0 || c === cols - 1;
        const edgeY = r === 0 || r === rows - 1;
        const x = bounds.x0 + 17 + c * xStep + (edgeX ? 0 : (random() - .5) * 22);
        const y = bounds.y0 + 12 + r * yStep + (edgeY ? 0 : (random() - .5) * 19);
        const id = nodes.length;
        nodes.push({ id, x, y, neighbors: [] });
        byRC[r][c] = id;
      }
    }

    const edges = [];
    const edgeSet = new Set();
    const addEdge = (a, b, kind = "minor") => {
      if (a === b) return;
      const key = a < b ? `${a}-${b}` : `${b}-${a}`;
      if (edgeSet.has(key)) return;
      edgeSet.add(key);
      const na = nodes[a], nb = nodes[b];
      const edge = { id: edges.length, a, b, length: Math.hypot(nb.x - na.x, nb.y - na.y), kind };
      edges.push(edge);
      na.neighbors.push({ node: b, edge: edge.id });
      nb.neighbors.push({ node: a, edge: edge.id });
    };

    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        if (c + 1 < cols) addEdge(byRC[r][c], byRC[r][c + 1], r === 2 || r === 5 ? "major" : "minor");
        if (r + 1 < rows) addEdge(byRC[r][c], byRC[r + 1][c], c === 2 || c === 6 || c === 8 ? "major" : "minor");
        if (r + 1 < rows && c + 1 < cols && random() < .16) addEdge(byRC[r][c], byRC[r + 1][c + 1], "minor");
        if (r + 1 < rows && c > 0 && random() < .12) addEdge(byRC[r][c], byRC[r + 1][c - 1], "minor");
      }
    }

    return { nodes, edges };
  }

  function drawRoads() {
    clear(roadLayer);
    graph.edges.forEach(edge => {
      const a = graph.nodes[edge.a], b = graph.nodes[edge.b];
      const major = edge.kind === "major";
      el("path", {
        d: `M${a.x.toFixed(2)},${a.y.toFixed(2)} L${b.x.toFixed(2)},${b.y.toFixed(2)}`,
        fill: "none", stroke: "#f8fcfd", "stroke-opacity": major ? ".74" : ".48",
        "stroke-width": major ? "3.1" : "1.55", "stroke-linecap": "round"
      }, roadLayer);
      if (major) {
        el("path", {
          d: `M${a.x.toFixed(2)},${a.y.toFixed(2)} L${b.x.toFixed(2)},${b.y.toFixed(2)}`,
          fill: "none", stroke: "#d3e3e7", "stroke-opacity": ".72",
          "stroke-width": "1", "stroke-linecap": "round"
        }, roadLayer);
      }
    });
  }

  function randomDestination(from) {
    let candidate = from;
    for (let tries = 0; tries < 30; tries++) {
      candidate = Math.floor(random() * graph.nodes.length);
      const a = graph.nodes[from], b = graph.nodes[candidate];
      if (Math.hypot(a.x - b.x, a.y - b.y) > 150) return candidate;
    }
    return candidate;
  }

  function findRoute(start, goal) {
    const n = graph.nodes.length;
    const dist = new Float64Array(n);
    const prev = new Int16Array(n);
    const visited = new Uint8Array(n);
    dist.fill(Infinity); prev.fill(-1); dist[start] = 0;
    const routeNoise = graph.edges.map(() => .82 + random() * .42);

    for (let step = 0; step < n; step++) {
      let u = -1, best = Infinity;
      for (let i = 0; i < n; i++) {
        if (!visited[i] && dist[i] < best) { best = dist[i]; u = i; }
      }
      if (u < 0 || u === goal) break;
      visited[u] = 1;
      for (const item of graph.nodes[u].neighbors) {
        const edge = graph.edges[item.edge];
        const alt = dist[u] + edge.length * routeNoise[edge.id];
        if (alt < dist[item.node]) { dist[item.node] = alt; prev[item.node] = u; }
      }
    }

    const path = [];
    let cursor = goal;
    while (cursor >= 0) {
      path.push(cursor);
      if (cursor === start) break;
      cursor = prev[cursor];
    }
    path.reverse();
    return path.length > 1 ? path : [start, graph.nodes[start].neighbors[0].node];
  }

  function planTrip(agent, fromNode) {
    const destination = randomDestination(fromNode);
    const path = findRoute(fromNode, destination);
    agent.route = path;
    agent.routeIndex = 0;
    agent.fromNode = path[0];
    agent.toNode = path[1];
    agent.progress = 0;
    agent.pause = random() < .18 ? random() * .55 : 0;
  }

  function startAlongRoute(agent) {
    const start = Math.floor(random() * graph.nodes.length);
    planTrip(agent, start);
    agent.progress = random() * .9;
    const a = graph.nodes[agent.fromNode], b = graph.nodes[agent.toNode];
    agent.x = a.x + (b.x - a.x) * agent.progress;
    agent.y = a.y + (b.y - a.y) * agent.progress;
  }

  function createContact(index) {
    const group = el("g", {}, contactLayer);
    const halo = el("circle", {
      r: "7", fill: "#d94232", "fill-opacity": ".10", stroke: "#d94232", "stroke-width": "1.1", opacity: "0"
    }, group);
    const dot = el("circle", {
      r: String(2.3 + random() * .8), fill: "#526773", stroke: "#f5fafb", "stroke-width": "1.05"
    }, group);
    const link = el("line", {
      stroke: "#d94232", "stroke-width": "1", "stroke-dasharray": "2 3", opacity: "0"
    }, linkLayer);
    const agent = {
      index, group, halo, dot, link,
      speed: (reducedMotion ? 3.5 : 11.5 + random() * 10.5),
      route: [], routeIndex: 0, fromNode: 0, toNode: 0, progress: 0, pause: 0,
      x: 0, y: 0, inside: false
    };
    startAlongRoute(agent);
    return agent;
  }

  function createTarget() {
    const group = el("g", {}, targetLayer);
    const radius = el("circle", {
      r: COLOCATION_RADIUS, fill: "#d94232", "fill-opacity": ".035", stroke: "#d94232",
      "stroke-opacity": ".62", "stroke-width": "1.15", "stroke-dasharray": "4 4"
    }, group);
    const pulses = Array.from({ length: 3 }, (_, i) => el("circle", {
      r: String(9 + i * 8), fill: "none", stroke: "#d94232", "stroke-width": "1.7", opacity: ".22"
    }, group));
    const halo = el("circle", {
      r: "11", fill: "#e54b38", "fill-opacity": ".13", stroke: "#d94232", "stroke-width": "1.2"
    }, group);
    const dot = el("circle", {
      r: "5.3", fill: "#d94232", stroke: "#f8d8d3", "stroke-width": "1.15", filter: "url(#softGlow)"
    }, group);
    const agent = {
      group, radius, pulses, halo, dot,
      speed: reducedMotion ? 4 : 16.5,
      route: [], routeIndex: 0, fromNode: 0, toNode: 0, progress: 0, pause: 0,
      x: 0, y: 0, activeCount: 0
    };
    startAlongRoute(agent);
    return agent;
  }

  function advanceAgent(agent, dt) {
    if (agent.pause > 0) {
      agent.pause -= dt;
      return;
    }

    const a = graph.nodes[agent.fromNode];
    const b = graph.nodes[agent.toNode];
    const segmentLength = Math.max(1, Math.hypot(b.x - a.x, b.y - a.y));
    agent.progress += agent.speed * dt / segmentLength;

    while (agent.progress >= 1) {
      agent.progress -= 1;
      agent.routeIndex += 1;
      if (agent.routeIndex >= agent.route.length - 1) {
        planTrip(agent, agent.toNode);
        if (agent.pause > 0) return;
      } else {
        agent.fromNode = agent.route[agent.routeIndex];
        agent.toNode = agent.route[agent.routeIndex + 1];
      }
    }

    const from = graph.nodes[agent.fromNode];
    const to = graph.nodes[agent.toNode];
    const t = agent.progress;
    agent.x = from.x + (to.x - from.x) * t;
    agent.y = from.y + (to.y - from.y) * t;
  }

  function burstAt(x, y) {
    const circle = el("circle", {
      cx: x.toFixed(2), cy: y.toFixed(2), r: "5", fill: "none", stroke: "#d94232", "stroke-width": "1.6", opacity: ".9"
    }, burstLayer);
    const start = performance.now();
    function animate(now) {
      const p = Math.min(1, (now - start) / 650);
      circle.setAttribute("r", (5 + p * 18).toFixed(2));
      circle.setAttribute("opacity", ((1 - p) * .9).toFixed(3));
      if (p < 1) requestAnimationFrame(animate); else circle.remove();
    }
    requestAnimationFrame(animate);
  }

  function updateCellHighlight(site, activeCount) {
    if (site === activeCell) {
      const opacity = activeCount ? .065 : .018;
      cellFills[site].setAttribute("fill-opacity", opacity.toFixed(3));
      return;
    }
    if (activeCell >= 0) cellFills[activeCell].setAttribute("fill-opacity", "0");
    activeCell = site;
    cellFills[activeCell].setAttribute("fill-opacity", activeCount ? ".065" : ".018");
  }

  function tick(now) {
    if (!playing) return;
    const dt = Math.min(.05, Math.max(0, (now - lastFrame) / 1000));
    lastFrame = now;

    advanceAgent(target, dt);
    target.group.setAttribute("transform", `translate(${target.x.toFixed(2)} ${target.y.toFixed(2)})`);

    let activeCount = 0;
    contacts.forEach(contact => {
      advanceAgent(contact, dt);
      contact.group.setAttribute("transform", `translate(${contact.x.toFixed(2)} ${contact.y.toFixed(2)})`);

      const distance = Math.hypot(contact.x - target.x, contact.y - target.y);
      const inside = distance <= COLOCATION_RADIUS;
      if (inside) activeCount += 1;

      if (inside && !contact.inside) {
        totalEntries += 1;
        burstAt(contact.x, contact.y);
      }
      contact.inside = inside;

      contact.dot.setAttribute("fill", inside ? "#d94232" : "#526773");
      contact.dot.setAttribute("r", inside ? "3.25" : "2.65");
      contact.halo.setAttribute("opacity", inside ? ".82" : "0");
      contact.halo.setAttribute("r", inside ? (7.6 + Math.sin(now / 130 + contact.index) * 1.2).toFixed(2) : "7");

      contact.link.setAttribute("x1", target.x.toFixed(2));
      contact.link.setAttribute("y1", target.y.toFixed(2));
      contact.link.setAttribute("x2", contact.x.toFixed(2));
      contact.link.setAttribute("y2", contact.y.toFixed(2));
      contact.link.setAttribute("opacity", inside ? Math.max(.18, .62 - distance / 120).toFixed(3) : "0");
    });

    target.activeCount = activeCount;
    const pulseStrength = activeCount ? 1 : .35;
    target.pulses.forEach((circle, i) => {
      const phase = ((now / (activeCount ? 900 : 1650)) + i / target.pulses.length) % 1;
      circle.setAttribute("r", (8 + phase * (activeCount ? 37 : 25)).toFixed(2));
      circle.setAttribute("opacity", ((1 - phase) * pulseStrength * .9).toFixed(3));
      circle.setAttribute("stroke-width", (1.9 - phase * .7).toFixed(2));
    });
    target.halo.setAttribute("r", (11 + activeCount * .8 + Math.sin(now / 160) * .7).toFixed(2));
    target.radius.setAttribute("fill-opacity", activeCount ? ".075" : ".035");
    target.radius.setAttribute("stroke-width", activeCount ? "1.55" : "1.15");

    const targetSite = nearestSite(target.x, target.y);
    updateCellHighlight(targetSite, activeCount);
    hudCurrent.textContent = activeCount === 1 ? "1 IN RANGE" : `${activeCount} IN RANGE`;
    hudTotal.textContent = totalEntries === 1 ? "1 co-location entry" : `${totalEntries} co-location entries`;

    requestAnimationFrame(tick);
  }

  function reset() {
    random = makeRandom((Date.now() ^ Math.floor(Math.random() * 0xffffffff)) >>> 0);
    graph = buildRoadGraph();
    drawRoads();
    drawCells();
    clear(linkLayer); clear(contactLayer); clear(targetLayer); clear(burstLayer);
    totalEntries = 0;
    activeCell = -1;
    contacts = Array.from({ length: CONTACT_COUNT }, (_, i) => createContact(i));
    target = createTarget();
    lastFrame = performance.now();
    updateRunState();
  }

  // The animation is a continuous requestAnimationFrame loop. Run it only while
  // the figure is on-screen, and let a click pause/resume it, so it never burns
  // cycles when the reader has scrolled past. (The original demo also bound
  // Space/R on window; that's dropped here — Space must still scroll the page.)
  let userPaused = false;
  let onScreen = true;

  function updateRunState() {
    const shouldRun = onScreen && !userPaused;
    if (shouldRun && !playing) {
      playing = true;
      lastFrame = performance.now();
      requestAnimationFrame(tick);
    } else if (!shouldRun) {
      playing = false;
    }
  }

  svg.addEventListener("click", () => { userPaused = !userPaused; updateRunState(); });

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(entries => {
      onScreen = entries.some(entry => entry.isIntersecting);
      updateRunState();
    }, { threshold: 0.08 }).observe(svg);
  }

  reset();
})();
