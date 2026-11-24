"""Builder A: portfolio-level screens from Ken French / AQR pre-sorted portfolios.

Run:  <venv>/bin/python -I screens.py <A-folder> <letter-2025.txt> <float.csv> <leverage_cost.csv>
Writes CSVs to <A-folder>/out/. All rules are those of PRE-REGISTRATION.md.
"""
import sys, re, json, datetime, os
import numpy as np, pandas as pd

A = sys.argv[1]; LETTER = sys.argv[2]; FLOAT = sys.argv[3]; LEVCOST = sys.argv[4]
FR = os.path.join(A, 'data', 'french'); OUT = os.path.join(A, 'out')
START, END = 197601, 202512


def french(name, title_re, daily=False):
    """Return the first block whose title line matches title_re, as a DataFrame in decimals."""
    rows = open(os.path.join(FR, name + '.csv'), encoding='latin-1').read().splitlines()
    n = 8 if daily else 6
    start = None
    if title_re is None:
        start = next(i for i, l in enumerate(rows) if l.startswith(','))
    else:
        for i, l in enumerate(rows):
            if re.search(title_re, l):
                start = i + 1; break
    hdr = [c.strip() for c in rows[start].split(',')][1:]
    idx, data = [], []
    for l in rows[start + 1:]:
        p = [c.strip() for c in l.split(',')]
        if len(p[0]) == n and p[0].isdigit():
            idx.append(int(p[0])); data.append([float(x) for x in p[1:1 + len(hdr)]])
        elif idx:
            break
    df = pd.DataFrame(data, index=idx, columns=hdr)
    df = df.where(df > -99)  # -99.99 / -999 are missing
    return df / 100.0


VW = r'Value Weight(ed)? Returns -- Monthly'
ff = french('F-F_Research_Data_Factors', None)
rf = ff['RF']; mkt = ff['Mkt-RF'] + ff['RF']

beta = french('Portfolios_Formed_on_BETA', VW)
var = french('Portfolios_Formed_on_VAR', VW)
bm = french('Portfolios_Formed_on_BE-ME', VW)
ep = french('Portfolios_Formed_on_E-P', VW)
op = french('Portfolios_Formed_on_OP', VW)
inv = french('Portfolios_Formed_on_INV', VW)
p32 = french('32_Portfolios_ME_BEME_OP_2x4x4', VW)
p32i = french('32_Portfolios_ME_OP_INV_2x4x4', VW)
p25b = french('25_Portfolios_ME_BETA_5x5', VW)
p25 = french('25_Portfolios_BEME_OP_5x5', VW)

CELLS = {
    'A7': ['ME2 BM3 OP3', 'ME2 BM3 OP4', 'ME2 BM4 OP3', 'BIG HiBM HiOP'],
    'A8': ['ME2 OP3 INV1', 'ME2 OP3 INV2', 'BIG HiOP LoINV', 'ME2 OP4 INV2'],
    'A9': ['BIG LoBETA', 'ME5 BETA2'],
    'A13': ['BM4 OP4', 'BM4 OP5', 'BM5 OP4', 'HiBM HiOP'],
}
NAMES = {
    'A1': 'Low beta', 'A2': 'Low variance', 'A3': 'Cheap (B/M)', 'A4': 'Cheap (E/P)',
    'A5': 'Profitable', 'A6': 'Conservative', 'A7': 'Big cheap profitable',
    'A8': 'Big profitable conservative', 'A9': 'Big low beta', 'A10': 'Blend A7+A1',
    'A11': 'Blend cheap+safe+quality', 'A12': 'AQR quality P10', 'A13': 'All-cap cheap profitable',
}
scr = pd.DataFrame(index=ff.index)
scr['A1'] = beta['Lo 20']; scr['A2'] = var['Lo 20']; scr['A3'] = bm['Hi 20']; scr['A4'] = ep['Hi 20']
scr['A5'] = op['Hi 20']; scr['A6'] = inv['Lo 20']
scr['A7'] = p32[CELLS['A7']].mean(axis=1, skipna=False)
scr['A8'] = p32i[CELLS['A8']].mean(axis=1, skipna=False)
scr['A9'] = p25b[CELLS['A9']].mean(axis=1, skipna=False)
scr['A10'] = (scr['A7'] + scr['A1']) / 2
scr['A11'] = (scr['A3'] + scr['A1'] + scr['A5']) / 3
scr['A13'] = p25[CELLS['A13']].mean(axis=1, skipna=False)

# AQR quality deciles. The sheet says whether returns are excess of T-bills; handled below.
aqr_note = ''
try:
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(A, 'data', 'aqr', 'qmj10.xlsx'), read_only=True, data_only=True)
    ws = wb.worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    aqr_note = ' '.join(str(r[0]) for r in rows[2:8] if r[0])
    h = next(i for i, r in enumerate(rows) if r[0] == 'DATE')
    d = {}
    for r in rows[h + 1:]:
        if not r[0] or r[10] in (None, ''): continue
        dt = r[0] if isinstance(r[0], (datetime.date, datetime.datetime)) else datetime.datetime.strptime(str(r[0]), '%m/%d/%Y')
        d[dt.year * 100 + dt.month] = float(r[10])  # column 10 = P10 (high quality), Long Sample - US
    aq = pd.Series(d)
    excess = 'excess' in aqr_note.lower()
    scr['A12'] = aq.reindex(scr.index) + (rf if excess else 0)
    aqr_note = ('AQR returns treated as EXCESS of T-bills; RF added back. ' if excess else 'AQR returns treated as total returns. ') + aqr_note
except Exception as e:  # noqa
    aqr_note = 'AQR not built: %r' % (e,)
open(os.path.join(OUT, 'aqr_note.txt'), 'w').write(aqr_note + '\n')
ORDER = [k for k in NAMES if k in scr]

# ---------- Berkshire ----------
r = json.load(open(os.path.join(A, 'data', 'brk', 'brk_daily.json')))['chart']['result'][0]
px = {}
for t, c in zip(r['timestamp'], r['indicators']['quote'][0]['close']):
    if c:
        dt = datetime.datetime.fromtimestamp(t, datetime.timezone.utc)
        px[dt.year * 100 + dt.month] = c  # last close in the month wins
px = pd.Series(px).sort_index()
brk_m = (px / px.shift(1) - 1).dropna()  # first value = April 1980
brk_m = brk_m[brk_m.index <= END]
letter = {}
for l in open(LETTER, encoding='utf-8', errors='replace'):
    m = re.match(r'^\s*(19[6-9]\d|20[0-2]\d)\s*(?:\. ?)+\s*(\(?-?[\d,.]+\)?)%?\s+(\(?-?[\d,.]+\)?)%?\s*$', l)
    if m:
        v = m.group(2).replace(',', '')
        letter[int(m.group(1))] = (-float(v.strip('()')) if v.startswith('(') else float(v)) / 100
brk_a = pd.Series(letter).sort_index()
brk_a = brk_a[(brk_a.index >= 1976) & (brk_a.index <= 2025)]
assert len(brk_a) == 50, len(brk_a)

# ---------- financing ----------
fl = pd.read_csv(FLOAT).set_index('year')['cost_of_float_pct']
fl = pd.to_numeric(fl, errors='coerce').fillna(0.0) / 100  # "less than zero" with no figure -> 0
lc = pd.read_csv(LEVCOST).set_index('year')['blend_pct'].dropna() / 100
months = [m for m in ff.index if START <= m <= END]
yr = pd.Series([m // 100 for m in months], index=months)
FIN = {
    'F0 Tbill': rf.loc[months],
    'F1 Tbill+1': rf.loc[months] + 0.01 / 12,
    'F2 Tbill+2': rf.loc[months] + 0.02 / 12,
    'F4 BRK float': yr.map(fl) / 12,
    'F5 BRK blend': yr.map(lambda y: lc[y] if y in lc.index else fl[y]) / 12,
}
fedp = os.path.join(A, 'data', 'fred', 'FEDFUNDS.csv')
if os.path.exists(fedp) and os.path.getsize(fedp) > 1000:
    fd = pd.read_csv(fedp); fd.columns = ['d', 'v']
    fd.index = [int(x[:4]) * 100 + int(x[5:7]) for x in fd['d']]
    FIN['F3 FedFunds+0.5'] = (fd['v'].reindex(months) / 100 + 0.005) / 12

S = scr.loc[months, ORDER].copy()
RF = rf.loc[months]; MKT = mkt.loc[months]
assert not S.drop(columns=[c for c in ['A12'] if c in S]).isna().any().any(), S.isna().sum()

base = pd.DataFrame({'rf': RF, 'market': MKT, 'berkshire': brk_m.reindex(months)})
for k in ORDER: base[k] = S[k]
base.index.name = 'yyyymm'
base.to_csv(os.path.join(OUT, 'monthly_unlevered.csv'), float_format='%.6f')
brk_a.rename('berkshire_letter_annual').to_csv(os.path.join(OUT, 'berkshire_annual_letter.csv'), index_label='year')


def lever(ra, L, rb, hair=0.0):
    return L * (ra - hair / 12) - (L - 1) * rb


def annual(s):
    return (1 + s).groupby(s.index // 100).prod() - 1


def mstats(s, a, b):
    s = s[(s.index >= a) & (s.index <= b)].dropna()
    ex = s - RF.loc[s.index]; mk = (MKT - RF).loc[s.index]
    w = (1 + s).cumprod(); n = len(s)
    dd = (w / w.cummax().clip(lower=1.0) - 1).min()
    r12 = ((1 + s).rolling(12).apply(np.prod, raw=True) - 1).min()
    return dict(first=s.index[0], last=s.index[-1], excess=ex.mean() * 12, vol=ex.std() * 12 ** .5,
                sharpe=ex.mean() / ex.std() * 12 ** .5, beta=np.cov(ex, mk)[0, 1] / mk.var(),
                cagr=w.iloc[-1] ** (12 / n) - 1, growth=w.iloc[-1], maxdd=dd, worst12m=r12, worst1m=s.min())


def astats(a, y0, y1):
    a = a[(a.index >= y0) & (a.index <= y1)]
    w = (1 + a).prod()
    return dict(cagr_a=w ** (1 / len(a)) - 1, growth_a=w, worst_year=a.min(), vol_a=a.std())


WIN = {'1976-2025': (197601, 202512), '1976-2011': (197601, 201112), '2012-2025': (201201, 202512),
       '1980.04-2025': (198004, 202512), '1980.04-2011': (198004, 201112)}
rows = []
series = {'Market': MKT}
for k in ORDER: series[k] = S[k]
for name, ra in series.items():
    for L in [1.0, 1.3, 1.6, 2.0]:
        for fn, rb in FIN.items():
            if L == 1.0 and fn != 'F0 Tbill': continue
            for hair in [0.0, 0.005, 0.01]:
                if name == 'Market' and hair > 0: continue
                s = lever(ra, L, rb, hair)
                an = annual(s.dropna())
                for wn, (a, b) in WIN.items():
                    if s[(s.index >= a) & (s.index <= b)].isna().any(): continue
                    d = dict(screen=name, name=NAMES.get(name, 'US market'), L=L, fin=fn, haircut=hair, window=wn)
                    d.update(mstats(s, a, b)); d.update(astats(an, a // 100 + (1 if a % 100 > 1 else 0), b // 100))
                    yb0, yb1 = a // 100 + (1 if a % 100 > 1 else 0), b // 100
                    bw = (1 + brk_a[(brk_a.index >= yb0) & (brk_a.index <= yb1)]).prod()
                    d['brk_cagr_a'] = bw ** (1 / (yb1 - yb0 + 1)) - 1
                    d['gap_cagr_a'] = d['cagr_a'] - d['brk_cagr_a']
                    d['wealth_ratio_vs_brk'] = d['growth_a'] / bw
                    rows.append(d)
st = pd.DataFrame(rows)
st.to_csv(os.path.join(OUT, 'stats_all.csv'), index=False, float_format='%.5f')

# Berkshire rows
brows = []
for wn, (a, b) in WIN.items():
    y0, y1 = a // 100 + (1 if a % 100 > 1 else 0), b // 100
    d = dict(window=wn); d.update(astats(brk_a, y0, y1))
    rfa = annual(RF); ma = annual(MKT)
    ex = (brk_a - rfa)[(brk_a.index >= y0) & (brk_a.index <= y1)]; mx = (ma - rfa).loc[ex.index]
    d.update(excess_a=ex.mean(), sharpe_a=ex.mean() / ex.std(), beta_a=np.cov(ex, mx)[0, 1] / mx.var())
    if a >= 198004: d.update(mstats(brk_m, a, b))
    brows.append(d)
pd.DataFrame(brows).to_csv(os.path.join(OUT, 'stats_berkshire.csv'), index=False, float_format='%.5f')
# annual-frequency Sharpe/beta for screens too (like-for-like with Berkshire annual)
arows = []
rfa = annual(RF); ma = annual(MKT)
for name, ra in series.items():
    for L, fn, hair in [(1.0, 'F0 Tbill', 0.0), (1.6, 'F0 Tbill', 0.0), (1.6, 'F1 Tbill+1', 0.005)]:
        an = annual(lever(ra, L, FIN[fn], hair).dropna())
        for wn, (y0, y1) in {'1976-2025': (1976, 2025), '1976-2011': (1976, 2011), '2012-2025': (2012, 2025)}.items():
            if y0 < an.index[0]: continue
            ex = (an - rfa).loc[y0:y1]; mx = (ma - rfa).loc[y0:y1]
            arows.append(dict(screen=name, L=L, fin=fn, haircut=hair, window=wn, excess_a=ex.mean(), vol_a=ex.std(),
                              sharpe_a=ex.mean() / ex.std(), beta_a=np.cov(ex, mx)[0, 1] / mx.var()))
pd.DataFrame(arows).to_csv(os.path.join(OUT, 'stats_annual_freq.csv'), index=False, float_format='%.5f')
# annual returns table
ann = pd.DataFrame({'berkshire': brk_a, 'market': annual(MKT), 'rf': annual(RF)})
for k in ORDER:
    ann[k] = annual(S[k].dropna()).reindex(ann.index)
    ann[k + '_1.6x_F1_h0.5'] = annual(lever(S[k], 1.6, FIN['F1 Tbill+1'], 0.005).dropna()).reindex(ann.index)
ann.to_csv(os.path.join(OUT, 'annual_returns.csv'), index_label='year', float_format='%.5f')


# ---------- margin rules ----------
def margin_sim(ra, rb, L, maint, reset_flags):
    """Annual-reset leverage. ra, rb arrays per period; reset_flags[i] True if period i is the last of a year.
    Returns equity return per period and list of trigger positions. maint=None -> no margin rule."""
    E = 1.0; Aa = L; D = L - 1; out = []; trig = []; called = False; minratio = 1.0
    for i in range(len(ra)):
        E0 = E
        Aa *= 1 + ra[i]; D *= 1 + rb[i]; E = Aa - D
        ratio = E / Aa if Aa > 0 else 0
        if not called: minratio = min(minratio, ratio)
        if maint is not None and not called and D > 0 and ratio < maint:
            Aa = E; D = 0.0; called = True; trig.append(i)
        out.append(E / E0 - 1)
        if reset_flags[i]:
            Aa = L * E; D = (L - 1) * E; called = False
    return np.array(out), trig, minratio


mrows = []
dec = np.array([m % 100 == 12 for m in months])
for name, ra in series.items():
    if ra.isna().any(): continue
    for L in [1.6, 2.0]:
        for fn in ['F0 Tbill', 'F1 Tbill+1']:
            rav = (ra - 0.005 / 12).values if name != 'Market' else ra.values
            rbv = FIN[fn].values
            # M-A: constant leverage monthly rebalance; ratio after one month
            ratio = (L * (1 + rav) - (L - 1) * (1 + rbv)) / (L * (1 + rav))
            const = pd.Series(L * rav - (L - 1) * rbv, index=months)
            base_r, _, minr = margin_sim(rav, rbv, L, None, dec)
            d = dict(screen=name, L=L, fin=fn, MA_min_ratio=ratio.min(), MA_triggers30=int((ratio < .30).sum()),
                     const_cagr=(1 + const).prod() ** (1 / 50) - 1, const_growth=(1 + const).prod(),
                     annreset_cagr=(1 + base_r).prod() ** (1 / 50) - 1, annreset_growth=(1 + base_r).prod(),
                     annreset_min_ratio=minr,
                     annreset_maxdd=((1 + pd.Series(base_r)).cumprod() / (1 + pd.Series(base_r)).cumprod().cummax() - 1).min())
            for mt in [0.30, 0.40]:
                r_, trig, _ = margin_sim(rav, rbv, L, mt, dec)
                tag = 'MB%d' % int(mt * 100)
                d[tag + '_n'] = len(trig); d[tag + '_dates'] = ' '.join(str(months[i]) for i in trig)
                d[tag + '_cagr'] = (1 + r_).prod() ** (1 / 50) - 1; d[tag + '_growth'] = (1 + r_).prod()
            mrows.append(d)
pd.DataFrame(mrows).to_csv(os.path.join(OUT, 'margin_monthly.csv'), index=False, float_format='%.5f')

# M-D: daily check
ffd = french('F-F_Research_Data_Factors_daily', None, daily=True)
bmd = french('Portfolios_Formed_on_BE-ME_Daily', r'Value Weight(ed)? Returns -- Daily', daily=True)
opd = french('Portfolios_Formed_on_OP_Daily', r'Value Weight(ed)? Returns -- Daily', daily=True)
dsel = ffd[(ffd.index >= 19760101) & (ffd.index <= 20251231)]
dser = {'Market': dsel['Mkt-RF'] + dsel['RF'], 'A3': bmd['Hi 20'].reindex(dsel.index), 'A5': opd['Hi 20'].reindex(dsel.index)}
dser['A3+A5 half each'] = (dser['A3'] + dser['A5']) / 2
dyr = np.array([d // 10000 for d in dsel.index]); dreset = np.append(dyr[1:] != dyr[:-1], True)
dym = np.array([d // 100 for d in dsel.index]); mend = np.append(dym[1:] != dym[:-1], True)
drows = []
for name, ra in dser.items():
    assert not ra.isna().any(), name
    for L in [1.6, 2.0]:
        for sp in [0.0, 0.01]:
            rav = ra.values - (0.005 / 252 if name != 'Market' else 0); rbv = dsel['RF'].values + sp / 252
            base_r, _, minr = margin_sim(rav, rbv, L, None, dreset)
            d = dict(screen=name, L=L, spread=sp, noMargin_growth=(1 + base_r).prod(), min_ratio_daily=minr)
            for mt in [0.30, 0.40]:
                r_, trig, _ = margin_sim(rav, rbv, L, mt, dreset)
                tag = 'daily%d' % int(mt * 100)
                d[tag + '_n'] = len(trig); d[tag + '_dates'] = ' '.join(str(dsel.index[i]) for i in trig)
                d[tag + '_growth'] = (1 + r_).prod()
                # same rule, but only checked at month ends
                E = 1.0; Aa = L; D = L - 1; called = False; n = 0; dates = []
                for i in range(len(rav)):
                    Aa *= 1 + rav[i]; D *= 1 + rbv[i]; E = Aa - D
                    if mend[i] and not called and D > 0 and E / Aa < mt:
                        Aa = E; D = 0; called = True; n += 1; dates.append(str(dsel.index[i]))
                    if dreset[i]: Aa = L * E; D = (L - 1) * E; called = False
                d['monthend%d_n' % int(mt * 100)] = n; d['monthend%d_dates' % int(mt * 100)] = ' '.join(dates)
                d['monthend%d_growth' % int(mt * 100)] = E
            drows.append(d)
    # constant leverage rebalanced monthly: worst intra-month equity/assets ratio, daily path
    for L in [1.6, 2.0]:
        Aa = L; D = L - 1; worst = 1; wd = None
        for i in range(len(ra)):
            Aa *= 1 + ra.values[i]; D *= 1 + dsel['RF'].values[i]
            if (Aa - D) / Aa < worst: worst = (Aa - D) / Aa; wd = dsel.index[i]
            if mend[i]: E = Aa - D; Aa = L * E; D = (L - 1) * E
        drows.append(dict(screen=name, L=L, spread=0.0, const_monthly_rebal_worst_intramonth_ratio=worst, worst_date=wd))
pd.DataFrame(drows).to_csv(os.path.join(OUT, 'margin_daily.csv'), index=False, float_format='%.5f')

# sanity: letter annual vs Yahoo year-end to year-end
ya = annual(brk_m[brk_m.index >= 198101])
chk = pd.DataFrame({'letter': brk_a, 'yahoo': ya}).dropna()
chk['diff'] = chk['letter'] - chk['yahoo']
chk.to_csv(os.path.join(OUT, 'berkshire_letter_vs_yahoo.csv'), index_label='year', float_format='%.4f')
print('done', len(st), 'rows;', 'max |letter-yahoo| annual diff', chk['diff'].abs().max())
print(aqr_note[:400])
