// Moving user co-locations — animated inline SVG.
// Every contact that enters the tracked user's moving radius is counted as a
// co-location. Renders into the #viz SVG embedded in the post.
//
// A red tracked user, labelled T, and 30 numbered contacts move through a street
// network. Who the tracked user actually knows is decided when the page loads —
// between FRIEND_MIN and FRIEND_MAX of the contacts, and nothing marks them out.
// When one of those few enters the radius it heads over, the tracked user pauses
// to let it catch up, and the two walk the same streets shoulder to shoulder for a
// few seconds before it peels off. Every other entry is a stranger passing close
// by, and the counter cannot tell the difference — a contact is red only while it
// is genuinely walking along, which is ground truth the data never contains.
//
// The panel below the map plots the ties that are real: a node appears the first
// time somebody actually walks with the tracked user, and the tie darkens and
// thickens each time it happens again. Two contacts walking along at the same time
// are tied to each other as well. The co-location count in the corner keeps rising
// for everyone who merely passes through, which is the gap between what the data
// says and what the graph below shows.
(() => {
  "use strict";

  const NS = "http://www.w3.org/2000/svg";
  const svg = document.querySelector("#viz");
  const roadLayer = document.querySelector("#roads");
  const fillLayer = document.querySelector("#cellFills");
  const cellLayer = document.querySelector("#cells");
  const siteLayer = document.querySelector("#sites");
  const contactLayer = document.querySelector("#contacts");
  const targetLayer = document.querySelector("#target");
  const hudCurrent = document.querySelector("#hudCurrent");
  const hudTotal = document.querySelector("#hudTotal");
  const netEdgeLayer = document.querySelector("#netEdges");
  const netNodeLayer = document.querySelector("#netNodes");
  const netSummary = document.querySelector("#netSummary");

  const ACCENT = "#d94232";       // the tracked user and anyone walking with them
  const ACCENT_WASH = "#ef4a38";  // cell tint under the tracked user
  const ACCENT_RIM = "#f8d8d3";   // pale ring around the tracked user's dot
  const CONTACT_GREY = "#526773"; // everyone going about their own business
  const LABEL_INK = "#3f5460";    // the number carried by each contact
  const NET_CENTER = [300, 464];  // hub of the network graph below the map
  const NET_BOX = { x0: 32, x1: 568, y0: 404, y1: 524 };
  const NET_CHARGE = 3200;        // node-to-node repulsion
  const NET_HUB_CHARGE = 4200;    // the hub pushes a little harder
  const NET_LINK_DISTANCE = 100;  // preferred length of a tie to the hub
  const NET_PEER_DISTANCE = 62;   // and of a tie between two contacts
  const NET_SPRING = .022;
  const NET_PULL_X = .0010;       // weak sideways gravity, so the graph spreads
  const NET_PULL_Y = .06;         // stronger downward gravity, so it stays flat
  const NET_DECAY = .78;

  const bounds = { x0: 16, y0: 29, x1: 584, y1: 364 };
  const CONTACT_COUNT = 30;
  const COLOCATION_RADIUS = 48;
  const TOGETHER_RADIUS = 15.5;   // the arm's-length circle friends walk inside
  const FRIEND_MIN = 5;           // how many of them actually know the tracked user
  const FRIEND_MAX = 10;          // i.e. 15-33% of the crowd, fixed on load
  const COMPANION_CHANCE = .75;   // chance a friend in range stops to walk along
  const COMPANION_MIN_SECONDS = 3.5;
  const COMPANION_MAX_SECONDS = 6.5;
  const CATCHUP_SPEEDUP = 2.1;    // a friend hurrying over
  const TARGET_WAIT = 2.5;        // how long the tracked user pauses for them
  const CHASE_PATIENCE = 12;      // how long the friend keeps trying after that
  const CHASE_REPLAN = .7;        // how often the friend re-aims at a moving target
  const WAIT_COOLDOWN = 10;       // how long before they are willing to wait again
  const JOIN_DISTANCE = 2.5;      // close enough to have arrived
  const LAG_SETTLE = 9;           // units/sec a follower closes on its walking position
  const WALK_ABREAST = 4.2;       // how far to one side a friend walks
  const TRAIL_LENGTH = 44;        // how far back the tracked user's path is kept
  const MAX_COMPANIONS = 4;       // guard only; there are rarely this many friends
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
  let togetherEntries = 0;
  let network = new Map();
  let peers = new Map();
  let netAlpha = 0;

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
        d: pathD(poly, true), fill: ACCENT_WASH, "fill-opacity": "0", stroke: "none"
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

  // The end of whichever road the point is standing on. Walking there stays on
  // that road, whereas the nearest node overall can sit across a block.
  function nearestRoadNode(x, y) {
    let bestEdge = graph.edges[0];
    let bestD = Infinity;
    let bestT = 0;
    for (const edge of graph.edges) {
      const a = graph.nodes[edge.a];
      const b = graph.nodes[edge.b];
      const dx = b.x - a.x;
      const dy = b.y - a.y;
      const len2 = dx * dx + dy * dy || 1e-9;
      const t = Math.max(0, Math.min(1, ((x - a.x) * dx + (y - a.y) * dy) / len2));
      const d = Math.hypot(x - (a.x + dx * t), y - (a.y + dy * t));
      if (d < bestD) { bestD = d; bestEdge = edge; bestT = t; }
    }
    return bestT < .5 ? bestEdge.a : bestEdge.b;
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

  // Breadcrumbs of where the tracked user has just been, with the distance walked
  // to reach each one. A follower reads its position off this trail, which keeps
  // it on the roads the tracked user actually used — including round corners and
  // across the joins between one trip and the next.
  function recordTrail() {
    const trail = target.trail;
    const last = trail[trail.length - 1];
    if (last) {
      const moved = Math.hypot(target.x - last.x, target.y - last.y);
      if (moved < .35) return; // standing still adds nothing
      target.travelled += moved;
    }
    trail.push({ x: target.x, y: target.y, s: target.travelled });
    while (trail.length > 2 && target.travelled - trail[0].s > TRAIL_LENGTH) trail.shift();
  }

  // How far back along the trail a point already is, so a contact can slot into
  // the trail at its current position rather than snapping to a spot on it.
  function trailLagNear(x, y) {
    let bestLag = 0;
    let bestD = Infinity;
    for (const crumb of target.trail) {
      const d = Math.hypot(crumb.x - x, crumb.y - y);
      if (d < bestD) { bestD = d; bestLag = target.travelled - crumb.s; }
    }
    return bestLag;
  }

  function pointOnTrail(lag) {
    const trail = target.trail;
    if (!trail.length) return [target.x, target.y];
    const want = target.travelled - lag;
    for (let i = trail.length - 1; i > 0; i--) {
      if (trail[i - 1].s <= want) {
        const a = trail[i - 1];
        const b = trail[i];
        const t = (want - a.s) / Math.max(1e-6, b.s - a.s);
        return [a.x + (b.x - a.x) * t, a.y + (b.y - a.y) * t];
      }
    }
    return [trail[0].x, trail[0].y];
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
    agent.mode = "route";
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
    const dot = el("circle", {
      r: String(2.3 + random() * .8), fill: CONTACT_GREY, stroke: "#f5fafb", "stroke-width": "1.05"
    }, group);
    // Everyone carries their number so a dot on the map can be matched to a node
    // in the network below.
    const label = el("text", {
      x: "5", y: "-3.4", "font-size": "4.6", fill: LABEL_INK, "fill-opacity": ".92",
      stroke: "#f2f8f9", "stroke-width": ".9", "paint-order": "stroke", "font-weight": "600"
    }, group);
    label.textContent = String(index + 1);
    const agent = {
      index, group, dot, label, id: index + 1,
      speed: (reducedMotion ? 3.5 : 11.5 + random() * 10.5),
      route: [], routeIndex: 0, fromNode: 0, toNode: 0, progress: 0, pause: 0,
      x: 0, y: 0, inside: false,
      mode: "route", walkLeft: 0, catchupLeft: 0, replanIn: 0,
      followLag: 0, wantedLag: 0, walkSide: 0, sideX: 0, sideY: 0, rejoinNode: 0,
      isFriend: false
    };
    startAlongRoute(agent);
    return agent;
  }

  // Who the tracked user actually knows is decided once, up front, and nothing on
  // the map gives it away. Everybody else can still be co-located with them any
  // number of times without it ever meaning anything.
  function pickFriends() {
    const order = contacts.map(contact => contact.index);
    for (let i = order.length - 1; i > 0; i--) {
      const j = Math.floor(random() * (i + 1));
      const swap = order[i];
      order[i] = order[j];
      order[j] = swap;
    }
    const count = FRIEND_MIN + Math.floor(random() * (FRIEND_MAX - FRIEND_MIN + 1));
    order.slice(0, count).forEach(index => { contacts[index].isFriend = true; });
  }

  function createTarget() {
    const group = el("g", {}, targetLayer);
    // Anyone walking with the tracked user sits inside this one, which is small
    // enough to read as arm's length rather than as a second co-location radius.
    const ring = el("circle", {
      r: TOGETHER_RADIUS, fill: "none", stroke: ACCENT, "stroke-opacity": ".38", "stroke-width": "1"
    }, group);
    const dot = el("circle", {
      r: "5.3", fill: ACCENT, stroke: ACCENT_RIM, "stroke-width": "1.15", filter: "url(#softGlow)"
    }, group);
    const label = el("text", {
      x: "8", y: "-5", "font-size": "5.6", fill: ACCENT, "font-weight": "700",
      stroke: "#f2f8f9", "stroke-width": "1", "paint-order": "stroke"
    }, group);
    label.textContent = "T";
    const agent = {
      group, ring, dot,
      speed: reducedMotion ? 4 : 16.5,
      route: [], routeIndex: 0, fromNode: 0, toNode: 0, progress: 0, pause: 0,
      x: 0, y: 0, activeCount: 0, mode: "route", holdLeft: 0, holdCooldown: 0,
      trail: [], travelled: 0
    };
    startAlongRoute(agent);
    return agent;
  }

  // A contact that decided to meet the tracked user hurries over on the road
  // network. It turns back down the segment it is on if the junction behind it is
  // the better way round, which is the one moment its direction can flip.
  function startCatchup(contact) {
    const from = graph.nodes[contact.fromNode];
    const to = graph.nodes[contact.toNode];
    if (Math.hypot(from.x - target.x, from.y - target.y) <
        Math.hypot(to.x - target.x, to.y - target.y)) {
      const behind = contact.fromNode;
      contact.fromNode = contact.toNode;
      contact.toNode = behind;
      contact.progress = 1 - contact.progress;
    }
    contact.mode = "catchup";
    contact.catchupLeft = CHASE_PATIENCE;
    contact.pause = 0;
    aimAtTarget(contact);
    // The tracked user stands still for a moment to let them arrive, but a second
    // friend setting off does not buy the first one any more waiting time.
    if (target.holdLeft <= 0 && target.holdCooldown <= 0) target.holdLeft = TARGET_WAIT;
  }

  // Re-route towards the junction the tracked user is walking to rather than the
  // one nearest them, so the friend cuts the corner instead of trailing a step
  // behind for ever. The segment the contact is on stays the first leg of the new
  // route, which keeps its position put.
  function aimAtTarget(contact) {
    contact.route = [contact.fromNode, ...findRoute(contact.toNode, target.toNode)];
    contact.routeIndex = 0;
    contact.replanIn = CHASE_REPLAN;
  }

  function chaseTarget(contact, dt) {
    contact.catchupLeft -= dt;
    contact.replanIn -= dt;
    if (Math.hypot(contact.x - target.x, contact.y - target.y) <= JOIN_DISTANCE) {
      joinTarget(contact);
      return;
    }
    // Once the tracked user gives up waiting and walks on, keep re-aiming at them.
    if (contact.replanIn <= 0) aimAtTarget(contact);
    if (atRouteEnd(contact)) {
      // The tracked user is on a road running off this junction, so closing the
      // last few units directly still follows the street.
      stepToward(contact, target.x, target.y, contact.speed * CATCHUP_SPEEDUP * dt);
    } else {
      advanceRoute(contact, dt, CATCHUP_SPEEDUP, true);
    }
    if (contact.catchupLeft <= 0) {
      contact.mode = "rejoin";
      contact.rejoinNode = nearestRoadNode(contact.x, contact.y);
    }
  }

  function atRouteEnd(agent) {
    return agent.routeIndex >= agent.route.length - 2 && agent.progress >= 1;
  }

  function stepToward(agent, x, y, step) {
    const dx = x - agent.x;
    const dy = y - agent.y;
    const distance = Math.hypot(dx, dy);
    if (distance <= step || distance < 1e-6) {
      agent.x = x;
      agent.y = y;
      return true;
    }
    agent.x += dx / distance * step;
    agent.y += dy / distance * step;
    return false;
  }

  // Counted here rather than when the contact sets off, so the tally only covers
  // pairs that actually met up.
  function joinTarget(contact) {
    togetherEntries += 1;
    recordWalk(contact);
    contacts.forEach(other => {
      if (other !== contact && other.mode === "follow") recordPeer(contact, other);
    });
    contact.mode = "follow";
    contact.walkLeft = COMPANION_MIN_SECONDS + random() * (COMPANION_MAX_SECONDS - COMPANION_MIN_SECONDS);
    contact.wantedLag = 2 + random() * 5;                // shoulder to shoulder, half a step back
    contact.walkSide = (random() < .5 ? 1 : -1) * WALK_ABREAST;
    // Start from where it already is, so falling into step is continuous. Capped
    // at the walking lag because a contact that arrives where the tracked user
    // doubled back can sit nearest a much older breadcrumb, and easing in from
    // there would leave it trailing half a block behind.
    contact.followLag = Math.min(trailLagNear(contact.x, contact.y), contact.wantedLag);
    contact.sideX = 0;                                   // ease out to their side of the road
    contact.sideY = 0;
  }

  // Followers walk the tracked user's own path, half a step back and just off to
  // one side, so the two read as a pair on the same street rather than one tailing
  // the other. The lag settles into place over the first stride or two rather than
  // snapping there.
  function followTarget(contact, dt) {
    contact.walkLeft -= dt;
    const drift = LAG_SETTLE * dt;
    contact.followLag += Math.max(-drift, Math.min(drift, contact.wantedLag - contact.followLag));

    const [x, y] = pointOnTrail(contact.followLag);
    const [bx, by] = pointOnTrail(contact.followLag + 6);
    const dx = x - bx;
    const dy = y - by;
    const heading = Math.hypot(dx, dy);
    // Ease which way "beside" points instead of snapping it, so a companion
    // crosses over behind the tracked user when they double back on themselves,
    // and eases out from their shoulder when first falling into step.
    if (heading > 1e-6) {
      const turn = Math.min(1, dt * 5);
      contact.sideX += (-dy / heading - contact.sideX) * turn;
      contact.sideY += (dx / heading - contact.sideY) * turn;
    }
    contact.x = x + contact.sideX * contact.walkSide;
    contact.y = y + contact.sideY * contact.walkSide;

    if (contact.walkLeft <= 0) {
      contact.mode = "rejoin";
      contact.rejoinNode = nearestRoadNode(contact.x, contact.y);
    }
  }

  // Peeling off leaves a contact mid-block, so walk it up to the nearest junction
  // before handing it a fresh route — planning from there directly would snap it
  // across the gap.
  function rejoinRoute(contact, dt) {
    const node = graph.nodes[contact.rejoinNode];
    if (stepToward(contact, node.x, node.y, contact.speed * dt)) {
      planTrip(contact, contact.rejoinNode);
    }
  }

  function advanceAgent(agent, dt) {
    if (agent.mode === "catchup") { chaseTarget(agent, dt); return; }
    if (agent.mode === "follow") { followTarget(agent, dt); return; }
    if (agent.mode === "rejoin") { rejoinRoute(agent, dt); return; }
    advanceRoute(agent, dt, 1);
  }

  function advanceRoute(agent, dt, speedScale, stopAtEnd) {
    if (agent.pause > 0) {
      agent.pause -= dt;
      return;
    }

    const a = graph.nodes[agent.fromNode];
    const b = graph.nodes[agent.toNode];
    const segmentLength = Math.max(1, Math.hypot(b.x - a.x, b.y - a.y));
    agent.progress += agent.speed * speedScale * dt / segmentLength;

    while (agent.progress >= 1) {
      agent.progress -= 1;
      agent.routeIndex += 1;
      if (agent.routeIndex >= agent.route.length - 1) {
        if (stopAtEnd) {
          agent.routeIndex = agent.route.length - 2;
          agent.progress = 1;
          break;
        }
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

  // The social network somebody would infer from this data: one node per contact
  // that has ever been co-located with the tracked user, with the edge thickening
  // each time it happens again. Solid edges are the pairs that genuinely walked
  // together; dashed ones are the false positives the inference cannot separate
  // out, because to the counter they look identical.
  function recordWalk(contact) {
    let member = network.get(contact.index);
    if (!member) {
      member = {
        walks: 0,
        edge: el("line", {
          x1: NET_CENTER[0], y1: NET_CENTER[1], stroke: CONTACT_GREY, "stroke-linecap": "round"
        }, netEdgeLayer),
        node: el("circle", { fill: CONTACT_GREY, stroke: "#eef4f4", "stroke-width": "1" }, netNodeLayer),
        label: el("text", { "text-anchor": "middle", fill: "#fff", "font-weight": "700" }, netNodeLayer)
      };
      member.label.textContent = String(contact.id);
      placeNewNode(member, network.size);
      network.set(contact.index, member);
      reheatNetwork();
    }
    member.walks += 1;
    drawEdge(member);
    updateNetworkSummary();
  }

  // Two contacts walking with the tracked user at the same time are walking with
  // each other as well, so they get a tie of their own.
  function recordPeer(one, two) {
    if (!network.has(one.index) || !network.has(two.index)) return;
    const key = one.index < two.index ? `${one.index}-${two.index}` : `${two.index}-${one.index}`;
    let peer = peers.get(key);
    if (!peer) {
      peer = {
        a: one.index, b: two.index, walks: 0,
        line: el("line", { stroke: CONTACT_GREY, "stroke-linecap": "round" }, netEdgeLayer)
      };
      peers.set(key, peer);
      reheatNetwork();
    }
    peer.walks += 1;
    drawTie(peer.line, peer.walks);
  }

  // A tie darkens and thickens the more often the two are seen walking together.
  function drawTie(line, walks) {
    line.setAttribute("stroke-width", Math.min(3.2, .8 + walks * .45).toFixed(2));
    line.setAttribute("stroke-opacity", Math.min(.88, .3 + walks * .15).toFixed(2));
  }

  function drawEdge(member) {
    drawTie(member.edge, member.walks);
  }

  // Nodes are laid out by the same force model d3-force uses: every pair of nodes
  // carries a charge and repels, every tie behaves like a spring pulling towards a
  // preferred length, and a little gravity keeps the graph around the hub. Adding a
  // node or a tie reheats the simulation (alpha back to 1) and it cools from there,
  // so the graph reorganises itself and settles rather than snapping into place.
  // Gravity is weaker across the panel than down it, which spreads the graph into
  // the available width instead of letting it ball up.
  function placeNewNode(member, index) {
    const angle = index * 2.39996; // golden angle, as d3 seeds its layouts
    member.x = NET_CENTER[0] + Math.cos(angle) * (26 + index * 3);
    member.y = NET_CENTER[1] + Math.sin(angle) * (18 + index * 2);
    member.vx = 0;
    member.vy = 0;
  }

  function reheatNetwork() {
    netAlpha = 1;
    const roomy = network.size <= 6;
    network.forEach(member => {
      member.node.setAttribute("r", roomy ? "7" : "5.6");
      member.label.setAttribute("font-size", roomy ? "6.6" : "5.4");
      member.labelDrop = roomy ? 2.3 : 1.9;
    });
  }

  function stepNetwork() {
    if (netAlpha < .004) return false;
    const nodes = [...network.values()];

    nodes.forEach(node => {
      // the hub is fixed, so it only ever pushes the others away
      applyCharge(node, null, NET_CENTER[0], NET_CENTER[1], NET_HUB_CHARGE);
      spring(node, null, NET_CENTER[0], NET_CENTER[1], NET_LINK_DISTANCE);
      node.vx += (NET_CENTER[0] - node.x) * NET_PULL_X * netAlpha;
      node.vy += (NET_CENTER[1] - node.y) * NET_PULL_Y * netAlpha;
    });

    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        applyCharge(nodes[i], nodes[j], nodes[j].x, nodes[j].y, NET_CHARGE);
      }
    }

    peers.forEach(peer => {
      const a = network.get(peer.a);
      const b = network.get(peer.b);
      if (a && b) spring(a, b, b.x, b.y, NET_PEER_DISTANCE);
    });

    nodes.forEach(node => {
      node.vx *= NET_DECAY;
      node.vy *= NET_DECAY;
      node.x = Math.max(NET_BOX.x0, Math.min(NET_BOX.x1, node.x + node.vx));
      node.y = Math.max(NET_BOX.y0, Math.min(NET_BOX.y1, node.y + node.vy));
    });

    netAlpha += (0 - netAlpha) * .0228; // d3's default cooling schedule
    return true;
  }

  // Pushes `node` away from a point; if `other` is given it takes the equal and
  // opposite share, which is what keeps the graph from drifting.
  function applyCharge(node, other, x, y, strength) {
    const dx = node.x - x;
    const dy = node.y - y;
    const distance = Math.max(6, Math.hypot(dx, dy));
    const push = strength * netAlpha / (distance * distance);
    const ux = dx / distance * push;
    const uy = dy / distance * push;
    node.vx += ux;
    node.vy += uy;
    if (other) {
      other.vx -= ux;
      other.vy -= uy;
    }
  }

  function spring(node, other, x, y, rest) {
    const dx = node.x - x;
    const dy = node.y - y;
    const distance = Math.max(1, Math.hypot(dx, dy));
    const pull = (distance - rest) * NET_SPRING * netAlpha;
    const ux = dx / distance * pull;
    const uy = dy / distance * pull;
    node.vx -= ux;
    node.vy -= uy;
    if (other) {
      other.vx += ux;
      other.vy += uy;
    }
  }

  function paintNetwork() {
    network.forEach(member => {
      member.node.setAttribute("cx", member.x.toFixed(2));
      member.node.setAttribute("cy", member.y.toFixed(2));
      member.label.setAttribute("x", member.x.toFixed(2));
      member.label.setAttribute("y", (member.y + member.labelDrop).toFixed(2));
      member.edge.setAttribute("x2", member.x.toFixed(2));
      member.edge.setAttribute("y2", member.y.toFixed(2));
    });
    peers.forEach(peer => {
      const a = network.get(peer.a);
      const b = network.get(peer.b);
      if (!a || !b) return;
      peer.line.setAttribute("x1", a.x.toFixed(2));
      peer.line.setAttribute("y1", a.y.toFixed(2));
      peer.line.setAttribute("x2", b.x.toFixed(2));
      peer.line.setAttribute("y2", b.y.toFixed(2));
    });
  }

  function updateNetworkSummary() {
    const people = network.size;
    if (!people) {
      netSummary.textContent = "nobody has walked with T yet";
      return;
    }
    let walks = 0;
    network.forEach(member => { walks += member.walks; });
    netSummary.textContent = `${people} ${people === 1 ? "person has" : "people have"} walked with T, `
      + `${walks} time${walks === 1 ? "" : "s"} in all`;
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

    let companionCount = 0;
    let chasing = false;
    contacts.forEach(contact => {
      if (contact.mode === "catchup") { chasing = true; companionCount += 1; }
      else if (contact.mode === "follow") companionCount += 1;
    });

    // Stand still for a moment when a friend sets off to join — but stop as soon
    // as they arrive, and don't do it for every one of them, or the tracked user
    // would spend the whole animation waiting around. Friends who set off during
    // the cooldown catch up with them on the move instead.
    if (target.holdLeft > 0) {
      target.holdLeft -= chasing ? dt : target.holdLeft;
      if (target.holdLeft <= 0) {
        target.holdLeft = 0;
        target.holdCooldown = WAIT_COOLDOWN;
      }
    } else if (target.holdCooldown > 0) {
      target.holdCooldown -= dt;
    }

    if (target.holdLeft <= 0) advanceAgent(target, dt);
    recordTrail();
    target.group.setAttribute("transform", `translate(${target.x.toFixed(2)} ${target.y.toFixed(2)})`);

    let activeCount = 0;
    contacts.forEach(contact => {
      advanceAgent(contact, dt);
      contact.group.setAttribute("transform", `translate(${contact.x.toFixed(2)} ${contact.y.toFixed(2)})`);

      const distance = Math.hypot(contact.x - target.x, contact.y - target.y);
      const inside = distance <= COLOCATION_RADIUS;
      if (inside) activeCount += 1;

      // Only contacts going about their own business start a fresh co-location.
      // A contact that is already meeting the tracked user drifts across the edge
      // of the radius repeatedly, and that is all one encounter, not several.
      if (inside && !contact.inside && contact.mode === "route") {
        totalEntries += 1;
        if (contact.isFriend && companionCount < MAX_COMPANIONS && random() < COMPANION_CHANCE) {
          startCatchup(contact);
          companionCount += 1;
        }
      }
      contact.inside = inside;

      // Red marks the people actually walking with the tracked user. Everyone who
      // merely crosses the radius stays grey, even though the counter logs them
      // exactly the same way.
      const together = contact.mode === "follow";
      contact.dot.setAttribute("fill", together ? ACCENT : CONTACT_GREY);
      contact.dot.setAttribute("r", together ? "3.4" : "2.65");
    });

    target.activeCount = activeCount;
    // Feedback while somebody is on their way over or walking along: the
    // arm's-length circle breathes instead of sitting still.
    const interacting = companionCount > 0;
    const pulse = interacting && !reducedMotion ? Math.sin(now / 250) : 0;
    target.ring.setAttribute("r", (TOGETHER_RADIUS + pulse * 1.5).toFixed(2));
    target.ring.setAttribute("stroke-opacity", interacting ? (.8 + pulse * .12).toFixed(3) : ".38");
    target.ring.setAttribute("stroke-width", interacting ? (1.55 + pulse * .3).toFixed(2) : "1");

    if (stepNetwork()) paintNetwork();

    const targetSite = nearestSite(target.x, target.y);
    updateCellHighlight(targetSite, activeCount);
    hudCurrent.textContent = activeCount === 1 ? "1 IN RANGE" : `${activeCount} IN RANGE`;
    hudTotal.textContent = `${totalEntries} entries · ${togetherEntries} together`;

    requestAnimationFrame(tick);
  }

  function reset() {
    random = makeRandom((Date.now() ^ Math.floor(Math.random() * 0xffffffff)) >>> 0);
    graph = buildRoadGraph();
    drawRoads();
    drawCells();
    clear(contactLayer); clear(targetLayer);
    clear(netEdgeLayer); clear(netNodeLayer);
    network = new Map();
    peers = new Map();
    netAlpha = 0;
    updateNetworkSummary();
    totalEntries = 0;
    togetherEntries = 0;
    activeCell = -1;
    contacts = Array.from({ length: CONTACT_COUNT }, (_, i) => createContact(i));
    pickFriends();
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
