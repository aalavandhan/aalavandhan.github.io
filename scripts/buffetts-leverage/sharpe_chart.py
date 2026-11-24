"""Draw the opening illustration: where Berkshire sits among long-lived stocks.

Illustrative, not a data plot. The curve is a stylised bell; only the three
labelled numbers are real (from sharpes.json, built by sharpe.py):
the median company, the S&P 500, and Berkshire, 1976-2025.

Output: _includes/buffetts-leverage/sharpe-distribution.svg
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / "_includes" / "buffetts-leverage" / "sharpe-distribution.svg"
d = json.load(open(HERE / "sharpes.json"))["1976-2025"]
vals = sorted(d["stocks"].values())
med, brk, sp = vals[len(vals) // 2], d["berkshire"], d["sp500"]

W, H = 720, 380
X0, X1, YB = 40, 690, 300
S0, S1 = 0.05, 0.80
x = lambda s: X0 + (s - S0) / (S1 - S0) * (X1 - X0)

TEXT = "var(--page-text, #292929)"
MUTED = "var(--page-muted, #757575)"
ACCENT = "#d9642b"
o = []
a = o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="sd-t sd-d" '
  f'style="width:100%;height:auto;font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,Helvetica,Arial,sans-serif">')
a('<title id="sd-t">Berkshire Hathaway against every other long-lived stock</title>')
a(f'<desc id="sd-d">Illustration. A bell curve of risk-adjusted returns for long-lived US companies, centred near {med:.2f}, '
  f'with the S&amp;P 500 at {sp:.2f} on its right shoulder. Berkshire Hathaway stands alone beyond the end of the curve at {brk:.2f}.</desc>')
a('''<defs><linearGradient id="sd-g" x1="0" x2="0" y1="0" y2="1">
<stop offset="0" stop-color="#8f9aa6" stop-opacity=".55"/><stop offset="1" stop-color="#8f9aa6" stop-opacity=".08"/></linearGradient></defs>
<style>
.sd-head{transform-box:fill-box;transform-origin:50% 100%;animation:sd-bob 2.4s ease-in-out infinite}
@keyframes sd-bob{0%,100%{transform:rotate(-5deg)}50%{transform:rotate(5deg)}}
@media (prefers-reduced-motion:reduce){.sd-head{animation:none}}
</style>''')

# stylised bell: peak at the median, thin right tail ending short of Berkshire
PEAK, SL, SR, TOP = med, 0.085, 0.075, 205
dens = lambda s: math.exp(-0.5 * ((s - PEAK) / (SL if s < PEAK else SR)) ** 2)
pts = [(x(S0 + i * (0.63 - S0) / 120), YB - TOP * dens(S0 + i * (0.63 - S0) / 120)) for i in range(121)]
line = "M" + "L".join(f"{px:.1f} {py:.1f}" for px, py in pts)
a('<g>')
a(f'<path d="{line}L{pts[-1][0]:.1f} {YB}L{pts[0][0]:.1f} {YB}Z" fill="url(#sd-g)"/>')
a(f'<path d="{line}" fill="none" stroke="#8f9aa6" stroke-width="2" stroke-linejoin="round"/>')
a('</g>')
# baseline with arrow
a(f'<path d="M{X0} {YB}H{X1}" stroke="{MUTED}" stroke-width="1.2"/><path d="M{X1} {YB}l-7 -4v8z" fill="{MUTED}"/>')
a(f'<text x="{(X0+X1)/2}" y="{YB+46}" text-anchor="middle" font-size="12.5" fill="{MUTED}">Sharpe ratio, 1976–2025</text>')

def tick(s, label, num, ytop, delay, anchor="middle"):
    px = x(s)
    a(f'<g>')
    a(f'<path d="M{px:.1f} {YB}V{ytop}" stroke="{TEXT}" stroke-width="1.2" stroke-dasharray="3 4"/>')
    a(f'<text x="{px:.1f}" y="{ytop-8}" text-anchor="{anchor}" font-size="13" fill="{TEXT}">{label}</text>')
    a(f'<text x="{px:.1f}" y="{YB+18}" text-anchor="middle" font-size="12" fill="{MUTED}">{num:.2f}</text>')
    a('</g>')

tick(med, "Typical company", med, YB - TOP - 12, 0.9)
tick(sp, "S&amp;P 500", sp, YB - TOP * dens(sp) - 34, 1.3)
a('<g>')
a(f'<text x="{x(0.15):.1f}" y="{YB-62}" text-anchor="middle" font-size="12.5" fill="{MUTED}">Large US stocks that</text>')
a(f'<text x="{x(0.15):.1f}" y="{YB-46}" text-anchor="middle" font-size="12.5" fill="{MUTED}">lasted 50 years</text>')
a('</g>')

def bobble(cx, base_y, scale):
    """Buffett bobblehead after the classic vinyl figure: boxy oversized head,
    white cap of hair, drooping white brows over black browline glasses, broad
    nose, small smile, grey suit with arms folded, black name base.
    Base bottom sits at (cx, base_y)."""
    skin, shade, ink = "#f6c7b1", "#dba088", "#141517"
    suit, suit_d = "#8c8e93", "#606267"
    g = [f'<g transform="translate({cx:.1f} {base_y:.1f}) scale({scale})">']
    g.append(f'''<defs>
<radialGradient id="sd-skin" cx=".36" cy=".3" r=".85"><stop offset="0" stop-color="#fbdcc8"/><stop offset=".6" stop-color="{skin}"/><stop offset="1" stop-color="#e3ae93"/></radialGradient>
<linearGradient id="sd-hair" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e4e3de"/></linearGradient>
<linearGradient id="sd-suit" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#a3a5aa"/><stop offset=".55" stop-color="#8c8e93"/><stop offset="1" stop-color="#74767b"/></linearGradient>
<linearGradient id="sd-base" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#34363b"/><stop offset=".5" stop-color="{ink}"/><stop offset="1" stop-color="#26272b"/></linearGradient>
</defs>''')
    # base
    g.append(f'<ellipse cx="0" cy="-5" rx="37" ry="7" fill="{ink}"/><rect x="-37" y="-17" width="74" height="12" fill="url(#sd-base)"/>'
             '<ellipse cx="0" cy="-17" rx="37" ry="7" fill="#3a3c42"/><ellipse cx="0" cy="-17" rx="31" ry="5" fill="#25262a"/>'
             '<path d="M-33 -19Q-20 -24.5 0 -24.5" fill="none" stroke="#fff" stroke-width="1.2" stroke-linecap="round" opacity=".35"/>'
             '<rect x="-30" y="-15" width="5" height="9" rx="2.5" fill="#fff" opacity=".12"/>')
    g.append('<text x="0" y="-3.6" text-anchor="middle" font-size="5.8" font-weight="700" letter-spacing=".6" fill="#fff">WARREN BUFFETT</text>')
    # legs: two columns with a seam, a little flared at the foot
    g.append(f'<path d="M-18 -17Q-19 -30 -17 -42H-1.5V-17Q-9 -14 -18 -17ZM18 -17Q19 -30 17 -42H1.5V-17Q9 -14 18 -17Z" fill="url(#sd-suit)" stroke="{suit_d}" stroke-width=".8"/>')
    # jacket
    g.append(f'<path d="M-23 -38L-26 -60Q-26 -76 0 -76Q26 -76 26 -60L23 -38Q0 -32 -23 -38Z" fill="url(#sd-suit)" stroke="{suit_d}" stroke-width=".8"/>')
    g.append('<path d="M-9 -76L0 -60L9 -76Z" fill="#fff"/><path d="M-2.8 -75h5.6l2 9L0 -59l-4.8 -7z" fill="#e0492f"/>')
    g.append(f'<path d="M-9 -76L0 -60L-12 -65Z" fill="{suit_d}"/><path d="M9 -76L0 -60L12 -65Z" fill="{suit_d}"/>')
    # folded arms, elbows out, pale hand at the centre
    g.append(f'<path d="M25 -66Q33 -57 25 -51L-9 -47" fill="none" stroke="{suit_d}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
             f'<path d="M25 -66Q33 -57 25 -51L-9 -47" fill="none" stroke="{suit}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>')
    g.append(f'<path d="M-25 -66Q-33 -58 -25 -53L9 -55" fill="none" stroke="{suit_d}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
             f'<path d="M-25 -66Q-33 -58 -25 -53L9 -55" fill="none" stroke="#9a9ca1" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>')
    g.append(f'<ellipse cx="-7" cy="-48.5" rx="6.2" ry="5" fill="#f9dccb" stroke="{shade}" stroke-width=".8"/>'
             f'<path d="M-10 -49.5q3 -1.5 6 0M-10 -47q3 -1.5 6 0" fill="none" stroke="{shade}" stroke-width=".7" stroke-linecap="round"/>')
    # gloss on shoulders and sleeves
    g.append('<path d="M-22 -68Q-14 -74 -6 -74M-27 -60Q-28 -56 -25 -54" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" opacity=".35"/>')
    g.append('<ellipse cx="0" cy="-74" rx="15" ry="3" fill="#000" opacity=".16"/>')
    # head
    g.append('<g transform="translate(0 -19)"><g class="sd-head">')
    g.append('<path d="M-44 -116Q-44 -144 -22 -145H22Q44 -144 44 -116V-86Q44 -66 31 -59Q22 -54.5 14 -56Q8 -51 0 -51Q-8 -51 -14 -56Q-22 -54.5 -31 -59Q-44 -66 -44 -86Z" fill="url(#sd-skin)"/>')
    g.append(f'<path d="M-42 -80Q-42 -66 -31 -59.5Q-22 -55 -14 -56.5Q-8 -51.5 0 -51.5Q8 -51.5 14 -56.5Q22 -55 31 -59.5Q42 -66 42 -80Q34 -64 20 -62Q10 -57 0 -57Q-10 -57 -20 -62Q-34 -64 -42 -80Z" fill="{shade}" opacity=".3"/>')
    g.append('<ellipse cx="-20" cy="-124" rx="13" ry="5" fill="#fff" opacity=".35"/>')
    # hair: a sculpted white mop, parted on the viewer's left, with a fringe swept across the forehead
    g.append('<path d="M-46 -106C-49 -120 -48 -136 -40 -145C-34 -153 -22 -156 -10 -155C-2 -160 14 -159 24 -154C36 -151 46 -142 47 -128C48 -120 47 -112 46 -106'
             'C44 -114 41 -120 35 -123C26 -119 14 -121 4 -127C-4 -131 -14 -132 -22 -130C-30 -128 -37 -123 -41 -117C-44 -113 -45 -110 -46 -106Z" '
             'fill="url(#sd-hair)" stroke="#c9c8c2" stroke-width="1" stroke-linejoin="round"/>')
    g.append('<path d="M-36 -139C-22 -150 14 -151 38 -136" fill="none" stroke="#e2e1db" stroke-width="5" stroke-linecap="round" opacity=".7"/>')
    g.append('<path d="M-22 -131C-12 -141 12 -143 34 -131M-24 -136C-12 -149 18 -150 42 -134M-23 -131C-31 -133 -39 -127 -43 -116M4 -127C12 -131 24 -131 35 -124" fill="none" stroke="#cfcec8" stroke-width="1.2" stroke-linecap="round"/>')
    g.append(f'<path d="M35 -123C26 -119 14 -121 4 -127C-4 -131 -14 -132 -22 -130C-30 -128 -37 -123 -41 -117" fill="none" stroke="{shade}" stroke-width="1.4" opacity=".4" stroke-linecap="round"/>')
    # brows: big fluffy white tufts resting just above the frames
    g.append('<path d="M-38 -111C-36 -121 -17 -124 -8 -116C-9 -112 -15 -111 -21 -112C-28 -113 -33 -112 -38 -111Z" fill="#fff" stroke="#c9c8c2" stroke-width="1" stroke-linejoin="round"/>'
             '<path d="M38 -111C36 -121 17 -124 8 -116C9 -112 15 -111 21 -112C28 -113 33 -112 38 -111Z" fill="#fff" stroke="#c9c8c2" stroke-width="1" stroke-linejoin="round"/>')
    # glasses: black frames, large lenses, wider than the face
    g.append(f'<rect x="-38" y="-109" width="32" height="23" rx="8" fill="#fff" fill-opacity=".18" stroke="{ink}" stroke-width="1.6"/>'
             f'<rect x="6" y="-109" width="32" height="23" rx="8" fill="#fff" fill-opacity=".18" stroke="{ink}" stroke-width="1.6"/>')
    g.append(f'<path d="M-38 -102q0 -7 8 -7h16q8 0 8 7M6 -102q0 -7 8 -7h16q8 0 8 7" fill="none" stroke="{ink}" stroke-width="3.2" stroke-linecap="round"/>')
    g.append(f'<path d="M-6 -103q6 -3 12 0" fill="none" stroke="{ink}" stroke-width="2.4" stroke-linecap="round"/>'
             f'<path d="M-38 -104l-9 1M38 -104l9 1" stroke="{ink}" stroke-width="2.4" stroke-linecap="round"/>')
    # eyes: small round, a soft lid above and a bag below
    g.append(f'<circle cx="-20" cy="-98" r="2.9" fill="{ink}"/><circle cx="20" cy="-98" r="2.9" fill="{ink}"/>'
             '<circle cx="-19.1" cy="-99" r=".8" fill="#fff"/><circle cx="20.9" cy="-99" r=".8" fill="#fff"/>')
    g.append(f'<path d="M-25 -101.4q5 -2.6 10 0M15 -101.4q5 -2.6 10 0" fill="none" stroke="{shade}" stroke-width="1.4" stroke-linecap="round"/>'
             f'<path d="M-25 -93q5 2 10 0M15 -93q5 2 10 0" fill="none" stroke="{shade}" stroke-width="1" stroke-linecap="round" opacity=".7"/>')
    # nose: big and broad, with a round tip and two nostril wings
    g.append(f'<path d="M-3 -101C-4 -94 -6 -90 -9 -86M3 -101C4 -94 6 -90 9 -86" fill="none" stroke="{shade}" stroke-width="1.1" stroke-linecap="round" opacity=".55"/>')
    g.append('<ellipse cx="-8.5" cy="-81" rx="4.6" ry="3.8" fill="#eeb39a"/><ellipse cx="8.5" cy="-81" rx="4.6" ry="3.8" fill="#eeb39a"/>')
    g.append('<ellipse cx="0" cy="-84" rx="8.8" ry="7.4" fill="#f3bfa7"/><ellipse cx="-2.4" cy="-87" rx="3.2" ry="2.4" fill="#fff" opacity=".6"/>')
    g.append(f'<path d="M-12.5 -80C-11.5 -76.5 -7 -76 -4.5 -77.5M12.5 -80C11.5 -76.5 7 -76 4.5 -77.5" fill="none" stroke="{shade}" stroke-width="1.4" stroke-linecap="round"/>')
    g.append('<path d="M-5.5 -78.2q1.6 1 3 0M2.5 -78.2q1.6 1 3 0" fill="none" stroke="#b9826c" stroke-width="1.2" stroke-linecap="round"/>')
    # raised cheeks and folds that wrap from the nose wings around the corners of a broad grin
    g.append('<ellipse cx="-25" cy="-78" rx="8" ry="5.5" fill="#f0a08c" opacity=".28"/><ellipse cx="25" cy="-78" rx="8" ry="5.5" fill="#f0a08c" opacity=".28"/>')
    g.append(f'<path d="M-12.5 -83C-19.5 -80.5 -22.5 -74.5 -19.5 -68.5M12.5 -83C19.5 -80.5 22.5 -74.5 19.5 -68.5" fill="none" stroke="{shade}" stroke-width="1.4" stroke-linecap="round" opacity=".85"/>')
    # mouth: wide open-lipped smile showing the upper teeth, thin lips, corners pulled up and back
    g.append('<path d="M-16.5 -71.5Q0 -67.2 16.5 -71.5Q9 -60.5 0 -60.5Q-9 -60.5 -16.5 -71.5Z" fill="#7d3a32" stroke="#a65f4e" stroke-width="1.5" stroke-linejoin="round"/>')
    g.append('<path d="M-14.2 -70.6Q0 -66.8 14.2 -70.6Q7.5 -64.6 0 -64.6Q-7.5 -64.6 -14.2 -70.6Z" fill="#fffdf8"/>')
    g.append('<path d="M-7 -68.6v3.4M0 -67.9v3.3M7 -68.6v3.4" stroke="#e3ddd4" stroke-width=".7"/>')
    g.append('<path d="M-16.5 -71.5q-1.8 -.3 -2.6 -1.8M16.5 -71.5q1.8 -.3 2.6 -1.8" fill="none" stroke="#a65f4e" stroke-width="1.3" stroke-linecap="round"/>')
    # lower lip and a small round chin
    g.append('<path d="M-8 -59.2Q0 -57.2 8 -59.2" fill="none" stroke="#e9a893" stroke-width="2" stroke-linecap="round" opacity=".75"/>')
    g.append('<ellipse cx="0" cy="-55" rx="7" ry="2.8" fill="#fde2d2" opacity=".7"/>')
    g.append('<ellipse cx="-27" cy="-84" rx="7" ry="10" fill="#fff" opacity=".22"/><path d="M-40 -146Q-30 -153 -14 -154" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".7"/>')
    g.append('</g></g></g>')
    return "".join(g)

xb = x(brk)
SC = 0.52
a(f'<g>')
a(bobble(xb, YB + 3, SC))
a('</g>')
a('<g>')
a(f'<text x="{xb:.1f}" y="{YB-103}" text-anchor="middle" font-size="15" font-weight="600" fill="{TEXT}">Berkshire Hathaway</text>')
a(f'<text x="{xb:.1f}" y="{YB+22}" text-anchor="middle" font-size="12" font-weight="600" fill="{TEXT}">{brk:.2f}</text>')
a('</g>')
a('</svg>')
OUT.write_text("\n".join(o) + "\n")
print("wrote", OUT, round(med, 2), round(sp, 2), round(brk, 2))
