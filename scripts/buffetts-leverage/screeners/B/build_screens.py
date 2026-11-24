"""Build the pre-registered stock-level screens from weekly Yahoo bars. Run: python3 -I build_screens.py
Outputs out/screens_weekly.csv (weekly gross and net returns per screen), out/holdings.json, out/build_log.txt."""
import sys, os, json, datetime, math, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

FIRST_YEAR, LAST_YEAR = 1976, 2025
ticks = open(os.path.join(DATA, 'tickers_sp1500_today.txt')).read().split()
log = open(os.path.join(OUT, 'build_log.txt'), 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s); log.write(s + '\n')

# master weekly calendar from the S&P 500 price index
g = load_bars('^GSPC')
gs = {monday(t): c for t, c in zip(g['t'], g['c']) if c}
weeks = sorted(w for w in gs if friday(w) <= datetime.date(LAST_YEAR, 12, 31))
widx = {w: i for i, w in enumerate(weeks)}
NW = len(weeks)
spx = [gs[w] for w in weeks]

P = {}; C = {}; V = {}; DIV = {}
missing = []
for t in ticks:
    try: b = load_bars(t)
    except Exception: missing.append(t); continue
    a = [None] * NW; c = [None] * NW; v = [0.0] * NW
    for ts, aa, cc, vv in zip(b['t'], b['a'], b['c'], b['v']):
        i = widx.get(monday(ts))
        if i is None or not aa or not cc or aa <= 0 or cc <= 0: continue
        a[i] = aa; c[i] = cc; v[i] = float(vv or 0)
    if sum(1 for x in a if x) < 60: continue
    P[t] = a; C[t] = c; V[t] = v
    DIV[t] = sorted((datetime.datetime.fromtimestamp(int(k), UTC).date(), x) for k, x in b['d'].items() if x)
say('tickers loaded', len(P), 'missing files', len(missing), missing[:20])

def sel_index(year):
    """Index of the last week whose Friday is on or before 31 December of `year`."""
    lim = datetime.date(year, 12, 31)
    i = max(k for k, w in enumerate(weeks) if friday(w) <= lim)
    return i

# weekly returns with gaps filled: return placed in the week the price reappears
R = {}
bad = []
for t, a in P.items():
    r = [None] * NW; last = None
    for i in range(NW):
        if a[i] is None: continue
        if last is not None:
            r[i] = a[i] / a[last] - 1
            if abs(r[i]) > 1.0 and i - last == 1: bad.append((t, weeks[i].isoformat(), round(r[i], 2)))
        last = i
    R[t] = r
say('weekly returns above +100% or below -100% (possible bad ticks):', len(bad), bad[:40])

def ttm_div(t, asof):
    lo = asof - datetime.timedelta(days=365)
    return sum(x for d, x in DIV[t] if lo < d <= asof)

def measures(t, e):
    """Trailing measures at selection index e, or None if not eligible (needs 156 weekly returns, at most 6 missing, and a price at e)."""
    a = P[t]
    if a[e] is None or e < 157: return None
    rr = R[t][e - 155:e + 1]
    if a[e - 156] is None: return None
    xs = [x for x in rr if x is not None]
    if len(xs) < 150: return None
    mu = sum(xs) / len(xs); vol = (sum((x - mu) ** 2 for x in xs) / (len(xs) - 1)) ** .5
    pairs = [(rr[k], spx[e - 155 + k] / spx[e - 156 + k] - 1) for k in range(156) if rr[k] is not None]
    mx = sum(p[0] for p in pairs) / len(pairs); my = sum(p[1] for p in pairs) / len(pairs)
    beta = sum((x - mx) * (y - my) for x, y in pairs) / sum((y - my) ** 2 for x, y in pairs)
    dv = sum((C[t][k] or 0) * V[t][k] for k in range(e - 51, e + 1))
    asof = friday(weeks[e])
    dy = ttm_div(t, asof) / C[t][e]
    return dict(vol=vol, beta=beta, dv=dv, dy=dy)

def div_grower(t, e, year):
    """Trailing-12-month dividend at the last 11 year-ends: never down year on year, and up over the decade."""
    if e < 52 * 11 + 2 or P[t][e - 52 * 11] is None: return False
    d = [ttm_div(t, datetime.date(year - k, 12, 31)) for k in range(11)]   # d[0] latest
    if d[10] <= 0: return False
    return all(d[k] >= d[k + 1] for k in range(10)) and d[0] > d[10]

SCREENS = ['C0', 'C1', 'B1', 'B2', 'B3', 'B4', 'B5']
holdings = {s: {} for s in SCREENS}
wk = {s: {} for s in SCREENS}       # gross weekly returns keyed by week
wkn = {s: {} for s in SCREENS}      # net of reconstitution cost
turn = {s: {} for s in SCREENS}
prev_w = {s: {} for s in SCREENS}   # drifted end-of-year weights
b4_started = False
for Y in range(FIRST_YEAR, LAST_YEAR + 1):
    e = sel_index(Y - 1); e2 = sel_index(Y)
    M = {t: m for t in P if (m := measures(t, e))}
    elig = sorted(M)
    ranked = sorted(elig, key=lambda t: -M[t]['dv'])
    large = ranked[:len(ranked) // 2]
    n50 = min(50, max(1, round(len(large) / 5)))
    pick = {}
    pick['C0'] = elig
    pick['C1'] = large
    pick['B1'] = sorted(large, key=lambda t: M[t]['vol'])[:n50]
    pick['B2'] = sorted(large, key=lambda t: M[t]['beta'])[:n50]
    hy = sorted(large, key=lambda t: -M[t]['dy'])[:len(large) // 2]
    pick['B3'] = sorted(hy, key=lambda t: M[t]['vol'])[:n50]
    grow = [t for t in elig if div_grower(t, e, Y - 1)]
    if len(grow) >= 20: b4_started = True
    pick['B4'] = grow if b4_started else []
    top100 = ranked[:100]
    pick['B5'] = sorted(top100, key=lambda t: -M[t]['dy'])[:30]
    say(Y, 'selection week', weeks[e], 'eligible', len(elig), 'large half', len(large), 'n50', n50,
        'zero-volume eligible', sum(1 for t in elig if M[t]['dv'] <= 0), 'growers', len(grow))
    for s in SCREENS:
        names = pick[s]
        holdings[s][Y] = names
        if not names: continue
        w0 = {t: 1.0 / len(names) for t in names}
        old = prev_w[s]
        to = sum(abs(w0.get(t, 0) - old.get(t, 0)) for t in set(w0) | set(old))
        turn[s][Y] = to
        val = dict(w0); tot = 1.0
        for i in range(e + 1, e2 + 1):
            new = 0.0
            for t in names:
                r = R[t][i]
                if r is not None: val[t] *= 1 + r
                new += val[t]
            ret = new / tot - 1; tot = new
            wk[s][weeks[i]] = ret
            wkn[s][weeks[i]] = (1 + ret) * (1 - cost_rate(Y) * to) - 1 if i == e + 1 else ret
        prev_w[s] = {t: val[t] / tot for t in names}

with open(os.path.join(OUT, 'screens_weekly.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['week_monday'] + [s + '_gross' for s in SCREENS] + [s + '_net' for s in SCREENS])
    for d in weeks:
        if d not in wk['C0']: continue
        w.writerow([d.isoformat()] + [('%.6f' % wk[s][d]) if d in wk[s] else '' for s in SCREENS]
                   + [('%.6f' % wkn[s][d]) if d in wkn[s] else '' for s in SCREENS])
json.dump({'holdings': holdings, 'turnover': turn}, open(os.path.join(OUT, 'holdings.json'), 'w'))
for s in SCREENS:
    ys = sorted(turn[s])
    if ys: say(s, 'first year', ys[0], 'mean names', round(sum(len(holdings[s][y]) for y in ys) / len(ys), 1),
               'mean annual turnover (sum of absolute weight changes, after first year)', round(sum(turn[s][y] for y in ys[1:]) / max(1, len(ys) - 1), 2))
for s in ['B1', 'B2', 'B3', 'B5']:
    say(s, 'holdings 1976:', ' '.join(holdings[s][1976]))
    say(s, 'holdings 2008:', ' '.join(holdings[s][2008][:50]))
