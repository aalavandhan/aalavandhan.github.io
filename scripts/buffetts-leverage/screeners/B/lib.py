"""Shared helpers for builder B. Standard library only. Run with python3 -I."""
import json, os, datetime, math, re, csv

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
OUT = os.path.join(HERE, 'out')
UTC = datetime.timezone.utc


def monday(ts):
    d = datetime.datetime.fromtimestamp(ts, UTC).date()
    return d - datetime.timedelta(days=d.weekday())


def load_bars(ticker, freq='weekly'):
    fn = os.path.join(DATA, 'yahoo_' + freq, ticker.replace('^', '_') + '.json')
    return json.load(open(fn))


def french_block(path, title, annual=False):
    """Return {yyyymm or yyyy or yyyymmdd: {col: decimal return}} for the block under `title` (None = first block)."""
    rows = open(path).read().splitlines()
    out = {}; hdr = None; on = False
    n = 4 if annual else None
    for i, l in enumerate(rows):
        if title is None and hdr is None and l.startswith(','):
            hdr = [c.strip() for c in l.split(',')][1:]; on = True; continue
        if title is not None and hdr is None and re.sub(r'^Average ', '', l.strip()).replace('Weighted', 'Weight') == re.sub(r'^Average ', '', title).replace('Weighted', 'Weight'):
            hdr = [c.strip() for c in rows[i + 1].split(',')][1:]; on = 'skip'; continue
        if on == 'skip':
            on = True; continue
        if on is True:
            p = [c.strip() for c in l.split(',')]
            if p[0].isdigit() and (n is None or len(p[0]) == n):
                if n is None: n = len(p[0])
                out[int(p[0])] = dict(zip(hdr, [float(x) / 100 for x in p[1:]]))
            elif out:
                break
    return out


def french_factors():
    p = os.path.join(DATA, 'french', 'F-F_Research_Data_Factors.csv')
    m = french_block(p, None)
    rows = open(p).read().splitlines()
    a = {}
    for l in rows:
        q = [c.strip() for c in l.split(',')]
        if len(q) == 5 and len(q[0]) == 4 and q[0].isdigit():
            a[int(q[0])] = {'Mkt-RF': float(q[1]) / 100, 'RF': float(q[4]) / 100}
    return m, a


def french_daily():
    p = os.path.join(DATA, 'french', 'F-F_Research_Data_Factors_daily.csv')
    return french_block(p, None)


def brk_letter(path):
    """Annual % change in Berkshire per-share market value and S&P 500 with dividends, from the letter text."""
    out = {}
    num = r'(\(?[\d,]+\.\d\)?)'
    for l in open(path, encoding='utf-8', errors='replace'):
        m = re.match(r'^(\d{4}) [ .]+\s+' + num + r'%?\s+' + num, l)
        if m:
            f = lambda s: (-1 if s.startswith('(') else 1) * float(s.strip('()').replace(',', '')) / 100
            out[int(m.group(1))] = (f(m.group(2)), f(m.group(3)))
    return out


def weekly_series(ticker):
    """{monday date: adjusted close} for one ticker from the weekly file."""
    b = load_bars(ticker)
    return {monday(t): a for t, a in zip(b['t'], b['a']) if a}


def friday(mon):
    return mon + datetime.timedelta(days=4)


def weekly_rf(weeks, ffm):
    """Weekly risk-free return for each Monday-keyed week, so that weeks whose Friday falls in a month compound to that month's RF."""
    cnt = {}
    for w in weeks:
        f = friday(w); k = f.year * 100 + f.month
        cnt[k] = cnt.get(k, 0) + 1
    out = {}
    for w in weeks:
        f = friday(w); k = f.year * 100 + f.month
        rf = ffm.get(k, {}).get('RF')
        out[w] = None if rf is None else (1 + rf) ** (1 / cnt[k]) - 1
    return out


def to_monthly(weeks, r):
    """Compound weekly returns {monday: r} into {yyyymm: r} by the month of the week's Friday. Only complete data weeks are used."""
    out = {}
    for w in weeks:
        if w not in r or r[w] is None: continue
        f = friday(w); k = f.year * 100 + f.month
        out[k] = (1 + out.get(k, 0.0)) * (1 + r[w]) - 1
    return out


def lever_weekly(weeks, r, rf, L, spread, reset='month'):
    """Levered weekly returns. Assets L, debt L-1 per unit equity; debt accrues rf+spread; leverage reset at month-end or year-end weeks."""
    out = {}; A = L; D = L - 1.0
    ws = [w for w in weeks if w in r and r[w] is not None and rf.get(w) is not None]
    for i, w in enumerate(ws):
        E0 = A - D
        A *= 1 + r[w]; D *= 1 + rf[w] + spread / 52.0
        E = A - D
        if E <= 0:
            out[w] = -1.0; A = D = 0.0
            for w2 in ws[i + 1:]: out[w2] = 0.0
            break
        out[w] = E / E0 - 1
        nxt = ws[i + 1] if i + 1 < len(ws) else None
        f = friday(w); fn = friday(nxt) if nxt else None
        last = fn is None or (fn.month != f.month if reset == 'month' else fn.year != f.year)
        if last:
            A = L * E; D = (L - 1) * E
    return out


def stats(weeks, r, rf, mkt_m=None, start=None, end=None):
    """Summary statistics of a weekly return series between two dates (inclusive, by Friday)."""
    ws = [w for w in weeks if w in r and r[w] is not None and rf.get(w) is not None
          and (start is None or friday(w) >= start) and (end is None or friday(w) <= end)]
    if len(ws) < 60: return None
    wlt = 1.0; pk = 1.0; dd = 0.0; ddw = None
    for w in ws:
        wlt *= 1 + r[w]; pk = max(pk, wlt)
        if wlt / pk - 1 < dd: dd = wlt / pk - 1; ddw = w
    yrs = (friday(ws[-1]) - friday(ws[0])).days / 365.25 + 7 / 365.25
    cagr = wlt ** (1 / yrs) - 1 if wlt > 0 else -1.0
    rm = to_monthly(ws, r); fm = to_monthly(ws, rf)
    ks = sorted(rm)
    ex = [rm[k] - fm[k] for k in ks]; n = len(ex)
    mu = sum(ex) / n; sd = (sum((x - mu) ** 2 for x in ex) / (n - 1)) ** .5
    beta = None
    if mkt_m:
        kk = [k for k in ks if k in mkt_m]
        if len(kk) > 24:
            xs = [rm[k] - fm[k] for k in kk]; ys = [mkt_m[k] for k in kk]
            mx = sum(xs) / len(xs); my = sum(ys) / len(ys)
            beta = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((y - my) ** 2 for y in ys)
    return dict(start=friday(ws[0]).isoformat(), end=friday(ws[-1]).isoformat(), years=yrs, cagr=cagr, wealth=wlt,
                excess=mu * 12, vol=sd * 12 ** .5, sharpe=(mu * 12) / (sd * 12 ** .5) if sd > 0 else float('nan'),
                maxdd=dd, maxdd_week=ddw.isoformat() if ddw else None, beta=beta)


def cost_rate(year):
    return 0.010 if year <= 1989 else (0.005 if year <= 2004 else 0.001)


def margin_sim(dates, r, rf_per, spread_per, L, maint, policy, cost_fn=cost_rate):
    """Margin account on any-frequency data.
    dates: list of date objects; r, rf_per: dicts keyed by date (period returns); spread_per: financing spread per period.
    policy 'ratchet': re-lever up to L at year-end only, never sell voluntarily. policy 'month': reset to L each month-end.
    maint: equity/assets maintenance requirement or None. On a breach, sell to return to leverage L at that close, paying cost on the amount sold.
    Returns a dict with the equity path and event log."""
    A = L; D = L - 1.0
    eq = {}; calls = []; min_ratio = 1.0; min_date = None; wiped = None; cost_paid = 0.0
    for i, d in enumerate(dates):
        A *= 1 + r[d]; D *= 1 + rf_per[d] + spread_per
        E = A - D
        if E <= 0:
            wiped = d; eq[d] = 0.0
            for d2 in dates[i + 1:]: eq[d2] = 0.0
            break
        ratio = E / A
        if ratio < min_ratio: min_ratio = ratio; min_date = d
        if maint is not None and ratio < maint:
            c = cost_fn(d.year)
            # sell S so that (A-S) = L*(E - c*S)  ->  S = (A - L*E)/(1 - L*c)
            S = (A - L * E) / (1 - L * c)
            A -= S; D -= S * (1 - c); E = A - D
            cost_paid += c * S
            calls.append((d, ratio, S / (A + S)))
        nxt = dates[i + 1] if i + 1 < len(dates) else None
        if nxt is not None:
            if policy == 'ratchet' and nxt.year != d.year and A / E < L:
                A, D = L * E, (L - 1) * E
            elif policy == 'month' and nxt.month != d.month:
                A, D = L * E, (L - 1) * E
        eq[d] = E
    pk = 1.0; dd = 0.0; ddd = None
    for d in dates:
        e = eq[d]; pk = max(pk, e)
        if e / pk - 1 < dd: dd = e / pk - 1; ddd = d
    return dict(eq=eq, calls=calls, min_ratio=min_ratio, min_date=min_date, wiped=wiped, final=eq[dates[-1]], maxdd=dd, maxdd_date=ddd, cost_paid=cost_paid)
