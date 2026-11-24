"""Vector art for Pass Your South Carolina Contractor Exam (Palmetto Night).
Writes SVG sources to brand/ and rendered images to assets/img/.
Run: python3 tools/art.py
"""
import os, random, subprocess
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BR = os.path.join(ROOT, "brand"); IMG = os.path.join(ROOT, "assets", "img")
os.makedirs(BR, exist_ok=True); os.makedirs(IMG, exist_ok=True)

NAVY = "#0B2545"; NAVY2 = "#13315C"; GREEN = "#2E9E5B"; MINT = "#7BD389"; GOLD = "#F2C14E"


def palmetto(x, y, s=1.0, fill="#061a33"):
    """Palmetto silhouette with its base at (x, y)."""
    g = [f'<g transform="translate({x},{y}) scale({s})" fill="{fill}">']
    # trunk: slight curve, textured with bands
    g.append('<path d="M-9 0 C-6 -120 -2 -240 6 -330 L18 -330 C12 -240 10 -120 11 0 Z"/>')
    # fronds: fan of tapered leaves from the crown
    import math
    cx, cy = 12, -335
    for i, ang in enumerate(range(-170, 15, 13)):
        a = math.radians(ang)
        L = 150 + (25 if i % 2 else 0) - abs(ang + 80) * 0.25
        ex, ey = cx + L * math.cos(a), cy + L * math.sin(a) + (abs(math.cos(a)) * 55)
        mx, my = cx + L * 0.5 * math.cos(a), cy + L * 0.5 * math.sin(a) - 18
        g.append(f'<path d="M{cx} {cy} Q{mx:.1f} {my-10:.1f} {ex:.1f} {ey:.1f} Q{mx+6:.1f} {my+10:.1f} {cx} {cy+6} Z"/>')
    # boots (leaf stems) at crown
    g.append(f'<ellipse cx="{cx}" cy="{cy+6}" rx="20" ry="14"/>')
    g.append('</g>')
    return "".join(g)


def crescent(cx, cy, r, color=GOLD, cut="#0B2545"):
    return (f'<g><circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>'
            f'<circle cx="{cx + r*0.42}" cy="{cy - r*0.18}" r="{r*0.88}" fill="{cut}"/></g>')


def rowhouses(y0, width, seed=4):
    """Charleston Rainbow Row style houses along the bottom."""
    random.seed(seed)
    cols = ["#F4B6A6", "#F7D58B", "#A8D5BA", "#9CC3E6", "#F1A7C1", "#CDB4DB", "#F6E3B4", "#B5E2D4"]
    out = []; x = 40
    while x < width - 40:
        w = random.choice([86, 96, 104, 112]); h = random.choice([150, 170, 185, 200])
        c = random.choice(cols)
        top = y0 - h
        out.append(f'<rect x="{x}" y="{top}" width="{w}" height="{h}" fill="{c}" opacity="0.92"/>')
        # parapet / roof
        if random.random() < 0.5:
            out.append(f'<path d="M{x-4} {top} L{x + w/2} {top-34} L{x+w+4} {top} Z" fill="#3A3F58" opacity="0.9"/>')
        else:
            out.append(f'<rect x="{x-3}" y="{top-12}" width="{w+6}" height="12" fill="#3A3F58" opacity="0.9"/>')
        # windows: lit warm
        for r in range(3):
            for k in range(2):
                wx = x + 16 + k * (w - 46); wy = top + 22 + r * 46
                if wy + 30 > y0 - 8: continue
                lit = random.random() < 0.7
                out.append(f'<rect x="{wx}" y="{wy}" width="16" height="28" rx="2" fill="{"#FFE7A3" if lit else "#56607a"}"/>')
                out.append(f'<rect x="{wx-3}" y="{wy-3}" width="3" height="34" fill="#2c3550" opacity=".5"/>')
        # door
        out.append(f'<rect x="{x + w/2 - 10}" y="{y0-38}" width="20" height="38" fill="#2c3550"/>')
        x += w + 4
    return "".join(out)


def hero_svg(W=1600, H=900):
    random.seed(7)
    stars = "".join(f'<circle cx="{random.randint(0,W)}" cy="{random.randint(0,int(H*0.55))}" r="{random.choice([1,1,1.4,1.8])}" fill="#fff" opacity="{random.uniform(.35,.9):.2f}"/>' for _ in range(140))
    ground = H - 120
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#071a33"/><stop offset=".55" stop-color="{NAVY}"/><stop offset=".82" stop-color="#2b3f6b"/><stop offset="1" stop-color="#e3a56a"/></linearGradient>
<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b3258"/><stop offset="1" stop-color="#071a33"/></linearGradient>
<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{GOLD}" stop-opacity=".35"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
</defs>
<rect width="{W}" height="{H}" fill="url(#sky)"/>
{stars}
<circle cx="1250" cy="190" r="190" fill="url(#glow)"/>
<mask id="moon"><rect x="-100" y="-100" width="200" height="200" fill="#fff"/><circle cx="34" cy="-14" r="70" fill="#000"/></mask>
<g transform="translate(1250 190)"><circle r="78" fill="{GOLD}" mask="url(#moon)"/></g>
<rect x="0" y="{ground}" width="{W}" height="{H-ground}" fill="url(#water)"/>
<g opacity=".95">{rowhouses(ground, W)}</g>
<g opacity=".22" transform="translate(0 {2*ground}) scale(1 -1)">{rowhouses(ground, W)}</g>
<rect x="0" y="{ground}" width="{W}" height="3" fill="{GOLD}" opacity=".5"/>
{palmetto(1420, ground+6, 1.25)}
{palmetto(1530, ground+6, 0.95)}
{palmetto(90, ground+6, 1.05)}
<path d="M120 {ground+70} C 480 {ground+20}, 760 {ground+110}, 1080 {ground+50} S 1400 {ground+30}, 1560 {ground+60}" fill="none" stroke="{MINT}" stroke-width="6" stroke-dasharray="2 18" stroke-linecap="round"/>
<g transform="translate(1080 {ground+50})"><circle r="20" fill="{GREEN}"/><path d="M-9 0 l6 7 l12 -14" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
</svg>'''


def icon_svg(kind, S=480):
    """Category illustrations on a soft rounded tile."""
    bg = {"commercial": "#E8EEF7", "mechanical": "#E6F4EA", "residential": "#FFF4D6", "business": "#EEE9F7", "local": "#E1F1F6", "services": "#F7ECE6"}[kind]
    body = {
        "commercial": f'''<rect x="150" y="170" width="120" height="210" rx="6" fill="{NAVY}"/>
<rect x="280" y="230" width="80" height="150" rx="6" fill="{NAVY2}"/>
{''.join(f'<rect x="{168+c*34}" y="{190+r*36}" width="20" height="22" rx="3" fill="{GOLD}"/>' for r in range(5) for c in range(3))}
{''.join(f'<rect x="{294+c*30}" y="{248+r*34}" width="18" height="20" rx="3" fill="{MINT}"/>' for r in range(4) for c in range(2))}
<path d="M110 120 L370 120 M330 120 L330 380 M330 120 L300 92 L360 92 Z" stroke="{GREEN}" stroke-width="10" fill="none" stroke-linecap="round"/>
<path d="M140 120 L140 175" stroke="{GREEN}" stroke-width="5"/><rect x="128" y="175" width="24" height="18" fill="{GOLD}"/>''',
        "mechanical": f'''<rect x="120" y="190" width="240" height="160" rx="18" fill="{NAVY}"/>
<circle cx="200" cy="270" r="52" fill="none" stroke="{MINT}" stroke-width="10"/>
{''.join(f'<path d="M200 270 l{40*__import__("math").cos(a*1.2566):.1f} {40*__import__("math").sin(a*1.2566):.1f}" stroke="{MINT}" stroke-width="12" stroke-linecap="round"/>' for a in range(5))}
<rect x="275" y="225" width="60" height="12" rx="6" fill="{GOLD}"/><rect x="275" y="255" width="60" height="12" rx="6" fill="{GOLD}"/><rect x="275" y="285" width="60" height="12" rx="6" fill="{GOLD}"/>
<path d="M150 350 L150 400 L330 400 L330 350" stroke="{GREEN}" stroke-width="14" fill="none"/>
<path d="M300 130 l-30 52 h28 l-18 46 l50 -64 h-30 l20 -34 z" fill="{GOLD}"/>''',
        "residential": f'''<path d="M110 250 L240 140 L370 250 Z" fill="{NAVY}"/>
<rect x="140" y="245" width="200" height="140" fill="#fff" stroke="{NAVY}" stroke-width="6"/>
<rect x="215" y="300" width="50" height="85" fill="{GREEN}"/>
<rect x="160" y="275" width="40" height="40" fill="{GOLD}"/><rect x="282" y="275" width="40" height="40" fill="{GOLD}"/>
<rect x="300" y="160" width="26" height="60" fill="{NAVY2}"/>
<circle cx="380" cy="150" r="28" fill="{MINT}"/><path d="M366 150 l10 11 l18 -22" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round"/>''',
        "business": f'''<path d="M240 120 L240 360" stroke="{NAVY}" stroke-width="12" stroke-linecap="round"/>
<path d="M130 160 L350 160" stroke="{NAVY}" stroke-width="10" stroke-linecap="round"/>
<path d="M130 160 L95 255 h70 Z M350 160 L315 255 h70 Z" fill="none" stroke="{NAVY2}" stroke-width="5"/>
<path d="M90 255 a40 22 0 0 0 80 0 Z" fill="{GOLD}"/><path d="M310 255 a40 22 0 0 0 80 0 Z" fill="{GOLD}"/>
<rect x="180" y="355" width="120" height="22" rx="8" fill="{GREEN}"/><circle cx="240" cy="120" r="16" fill="{GOLD}"/>''',
        "local": f'''<rect x="150" y="120" width="180" height="250" rx="16" fill="{NAVY}"/>
<rect x="172" y="145" width="136" height="70" rx="8" fill="#0d2f57"/><text x="240" y="193" font-family="Poppins" font-weight="600" font-size="40" fill="{MINT}" text-anchor="middle">240V</text>
<circle cx="205" cy="280" r="28" fill="{GOLD}"/><circle cx="275" cy="280" r="28" fill="{MINT}"/>
<path d="M205 330 C 205 390, 120 380, 120 420 M275 330 C 275 390, 360 380, 360 420" stroke="{GREEN}" stroke-width="10" fill="none" stroke-linecap="round"/>''',
        "services": f'''<rect x="140" y="110" width="200" height="260" rx="14" fill="#fff" stroke="{NAVY}" stroke-width="8"/>
{''.join(f'<rect x="170" y="{160+i*46}" width="{140 - (i%2)*40}" height="14" rx="7" fill="{NAVY2}" opacity=".85"/>' for i in range(4))}
<circle cx="320" cy="350" r="50" fill="{GREEN}"/><path d="M296 350 l16 18 l30 -36" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="200" y="92" width="80" height="34" rx="10" fill="{GOLD}"/>''',
    }[kind]
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 480 480"><rect width="480" height="480" rx="48" fill="{bg}"/>{body}</svg>'


def mark_svg(S=512, bg=True):
    """Logo mark: navy rounded square, gold crescent, palmetto, green exam-path check."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 512 512">
{'<rect width="512" height="512" rx="112" fill="'+NAVY+'"/>' if bg else ''}
<g transform="translate(150 150)"><circle r="62" fill="{GOLD}"/><circle cx="26" cy="-12" r="56" fill="{NAVY}"/></g>
{palmetto(300, 430, 0.92, fill="#ffffff")}
<g transform="translate(372 392)"><circle r="58" fill="{GREEN}" stroke="{NAVY}" stroke-width="12"/><path d="M-26 2 l18 20 l36 -42" stroke="#fff" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
</svg>'''


def wordmark_svg(dark=False):
    c1 = "#fff" if dark else NAVY
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1560" height="300" viewBox="0 0 1560 300">
<g transform="scale(0.5859)">{mark_svg(512).split('>',1)[1].rsplit('</svg>',1)[0]}</g>
<text x="340" y="140" font-family="Poppins" font-weight="600" font-size="104" fill="{c1}" letter-spacing="-2">Pass Your <tspan fill="{GREEN if not dark else MINT}">SC</tspan> Exam</text>
<text x="344" y="226" font-family="Poppins" font-weight="400" font-size="52" fill="{'#cfd8e3' if dark else '#5b6b80'}">South Carolina contractor exam prep</text>
</svg>'''


def og_svg():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
<defs><clipPath id="c"><rect width="1200" height="630"/></clipPath></defs>
<g clip-path="url(#c)"><g transform="scale(0.75) translate(0 -60)">{hero_svg().split('>',1)[1].rsplit('</svg>',1)[0]}</g></g>
<rect width="1200" height="630" fill="#071a33" opacity=".45"/>
<g transform="translate(70 70) scale(0.28)">{mark_svg(512).split('>',1)[1].rsplit('</svg>',1)[0]}</g>
<text x="70" y="290" font-family="Poppins" font-weight="600" font-size="68" fill="#fff" letter-spacing="-1.5">Pass your South Carolina</text>
<text x="70" y="370" font-family="Poppins" font-weight="600" font-size="68" fill="{MINT}" letter-spacing="-1.5">contractor exam.</text>
<text x="70" y="440" font-family="Poppins" font-size="30" fill="#dbe4ee">CLB, Residential Builders and trade exams. Books, tabs and courses.</text>
<text x="70" y="540" font-family="Poppins" font-weight="500" font-size="30" fill="{GOLD}">passyoursouthcarolinacontractorexam.com</text>
</svg>'''


def render(svg, name, w, h=None, fmts=("png",)):
    src = os.path.join(BR, name + ".svg"); open(src, "w").write(svg)
    png = os.path.join(IMG, name + ".png")
    cmd = ["rsvg-convert", "-w", str(w)] + (["-h", str(h)] if h else []) + ["-o", png, src]
    subprocess.run(cmd, check=True)
    im = Image.open(png)
    if "webp" in fmts: im.save(os.path.join(IMG, name + ".webp"), quality=82)
    if "jpg" in fmts: im.convert("RGB").save(os.path.join(IMG, name + ".jpg"), quality=84, optimize=True, progressive=True)
    if "png" not in fmts: os.remove(png)


if __name__ == "__main__":
    h = hero_svg()
    render(h, "hero", 1600, 900, ("webp", "jpg"))
    open(os.path.join(BR, "hero.svg"), "w").write(h)
    subprocess.run(["rsvg-convert", "-w", "800", "-o", os.path.join(IMG, "hero-800.png"), os.path.join(BR, "hero.svg")], check=True)
    im = Image.open(os.path.join(IMG, "hero-800.png")); im.save(os.path.join(IMG, "hero-800.webp"), quality=80); os.remove(os.path.join(IMG, "hero-800.png"))
    for k in ("commercial", "mechanical", "residential", "business", "local", "services"):
        render(icon_svg(k), "cat-" + k, 480, 480, ("webp", "png"))
    render(mark_svg(), "logo-mark", 512, 512, ("png",))
    render(mark_svg(), "favicon", 64, 64, ("png",))
    render(mark_svg(), "apple-touch-icon", 180, 180, ("png",))
    render(wordmark_svg(), "logo-nav", 520, 100, ("png",))
    render(wordmark_svg(True), "logo-nav-dark", 520, 100, ("png",))
    render(og_svg(), "og", 1200, 630, ("jpg", "png"))
    print("art done:", sorted(os.listdir(IMG)))
