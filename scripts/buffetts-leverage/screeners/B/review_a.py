"""Independent recomputation of agent A's headline numbers and stress tests of them. Run: python3 -I review_a.py <letter 2025 text>
Uses my own downloads of the French files (B/data/french) and my own parser. Writes out/review_a.txt."""
import sys, os, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
D = datetime.date
out = open(os.path.join(OUT, 'review_a.txt'), 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s); out.write(s + '\n')
FR = os.path.join(DATA, 'french')
ffm, ffa = french_factors()
VW = 'Value Weight Returns -- Monthly'
bm = french_block(os.path.join(FR, 'Portfolios_Formed_on_BE-ME.csv'), VW)
be = french_block(os.path.join(FR, 'Portfolios_Formed_on_BETA.csv'), VW)
op = french_block(os.path.join(FR, 'Portfolios_Formed_on_OP.csv'), VW)
p25 = french_block(os.path.join(FR, '25_Portfolios_BEME_OP_5x5.csv'), VW)
p32 = french_block(os.path.join(FR, '32_Portfolios_ME_BEME_OP_2x4x4.csv'), VW)
nf = french_block(os.path.join(FR, '25_Portfolios_BEME_OP_5x5.csv'), 'Number of Firms in Portfolios')
mc = french_block(os.path.join(FR, '25_Portfolios_BEME_OP_5x5.csv'), 'Average Market Cap')
months = [m for m in sorted(ffm) if 197601 <= m <= 202512]
letter = {y: v[0] for y, v in brk_letter(sys.argv[1]).items()}
C13 = ['BM4 OP4', 'BM4 OP5', 'BM5 OP4', 'HiBM HiOP']
C7 = ['ME2 BM3 OP3', 'ME2 BM3 OP4', 'ME2 BM4 OP3', 'BIG HiBM HiOP']
SCR = {
 'Market': {m: ffm[m]['Mkt-RF'] + ffm[m]['RF'] for m in months},
 'A11': {m: (bm[m]['Hi 20'] + be[m]['Lo 20'] + op[m]['Hi 20']) / 3 for m in months},
 'A10': {m: 0.5 * sum(p32[m][c] for c in C7) / 4 + 0.5 * be[m]['Lo 20'] for m in months},
 'A13 (equal weight across 4 cells, as A)': {m: sum(p25[m][c] for c in C13) / 4 for m in months},
 'A13 weighted by cell market value': {m: sum(p25[m][c] * nf[m][c] * mc[m][c] for c in C13) / sum(nf[m][c] * mc[m][c] for c in C13) for m in months},
 'A13 weighted by number of firms': {m: sum(p25[m][c] * nf[m][c] for c in C13) / sum(nf[m][c] for c in C13) for m in months},
 'A3 cheap quintile alone': {m: bm[m]['Hi 20'] for m in months},
}
def lev(r, L=1.6, sp=0.01, hair=0.005):
    return {m: L * (r[m] - hair / 12) - (L - 1) * (ffm[m]['RF'] + sp / 12) for m in r}
def grow(r, y0, y1):
    w = 1.0
    for m in sorted(r):
        if y0 <= m // 100 <= y1: w *= 1 + r[m]
    return w, w ** (1 / (y1 - y0 + 1)) - 1
def bk(y0, y1):
    w = 1.0
    for y in range(y0, y1 + 1): w *= 1 + letter[y]
    return w, w ** (1 / (y1 - y0 + 1)) - 1
say('== 1. Recomputation of A headline: 1.6x, T-bill + 1%, 0.5% haircut, monthly reset. $1 grows to / CAGR.')
say('%-42s %22s %14s %14s %14s %14s' % ('', '1976-2025', '1976-1998', '1999-2025', '1976-2011', '2012-2025'))
P = [(1976, 2025), (1976, 1998), (1999, 2025), (1976, 2011), (2012, 2025)]
say('%-42s %22s' % ('Berkshire (letter)', '$%.0f  %.1f%%' % (bk(1976, 2025)[0], 100 * bk(1976, 2025)[1])) + ''.join('%14s' % ('%.1f%%' % (100 * bk(*p)[1])) for p in P[1:]))
for k, r in SCR.items():
    l = lev(r)
    say('%-42s %22s' % (k, '$%.0f  %.1f%%' % (grow(l, 1976, 2025)[0], 100 * grow(l, 1976, 2025)[1])) + ''.join('%14s' % ('%.1f%%' % (100 * grow(l, *p)[1])) for p in P[1:]))
say('A13 cells: median number of firms', {c: sorted(nf[m][c] * 100 for m in months)[len(months) // 2] for c in C13}, 'minimum', {c: min(nf[m][c] * 100 for m in months) for c in C13})
say('A13 cells: median share of the four cells\' combined market value', {c: round(sorted(nf[m][c] * mc[m][c] / sum(nf[m][x] * mc[m][x] for x in C13) for m in months)[len(months) // 2], 2) for c in C13})

say('\n== 2. Never-sell account on A\'s screens, month-end checks only (understates stress). 0.5% haircut, T-bill + 1%, borrow back up to target each December, sell only on a call.')
say('%-42s %4s | %-24s | %-22s | %-32s' % ('', 'L', 'lowest month-end equity', 'no rule: $1 to', '30% rule: calls (months), $1 to'))
dates = [D(m // 100, m % 100, 28) for m in months]
for k, r in SCR.items():
    rr = {d: r[m] - 0.005 / 12 for d, m in zip(dates, months)}; rf = {d: ffm[m]['RF'] for d, m in zip(dates, months)}
    for L in (1.6, 2.0):
        n = margin_sim(dates, rr, rf, 0.01 / 12, L, None, 'ratchet'); c = margin_sim(dates, rr, rf, 0.01 / 12, L, 0.30, 'ratchet')
        say('%-42s %4.1f | %-24s | %-22s | %-32s' % (k, L, '%.2f in %s' % (n['min_ratio'], n['min_date'].strftime('%Y-%m')), ('wiped ' + n['wiped'].strftime('%Y-%m')) if n['wiped'] else '%.0f' % n['final'],
            '%d (%s), %.0f' % (len(c['calls']), ' '.join(x[0].strftime('%Y-%m') for x in c['calls']), c['final'])))
