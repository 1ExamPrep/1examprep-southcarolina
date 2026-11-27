#!/usr/bin/env python3
"""Build passyoursouthcarolinacontractorexam.com (design: Palmetto Night).

python3 build.py   -> writes the static site into ./site
Products come from data/products-raw.json (Shopify pull). Copy and facts live in tools/sccopy.py.
"""
import html, json, os, re, shutil, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from sccopy import *  # noqa
from scblog import POSTS, AUTHOR, BSRC
SRC.update(BSRC)

# In the GitHub repo the scripts live in source/ and the site is written to the repo root.
OUT = os.path.dirname(ROOT) if os.path.basename(ROOT) == "source" else os.path.join(ROOT, "site")
MANIFEST = os.path.join(OUT, ".build-manifest.json")
SITE = "https://passyoursouthcarolinacontractorexam.com"
BRAND = "Pass Your South Carolina Contractor Exam"
SHORT = "Pass Your SC Exam"
PHONE = "(877) 775-9400"; TEL = "+18777759400"; EMAIL = "sales@1examprep.com"
FORM_ID = "1jGx4TPpXO5C3XkV5vuq"
LAUNCHED = "2026-11-24"
CART = "https://1examprep.com/cart/{}:1"
REFUND = "https://1examprep.com/policies/refund-policy"
E = html.escape

STOP = {"a", "an", "and", "the", "of", "for", "to", "in", "on", "with", "by", "or", "at", "from", "based", "includes", "&", "+", "-"}


def slugify(s, maxw=8):
    s = s.lower().replace("&", " ").replace("'", "")
    w = [x for x in re.split(r"[^a-z0-9]+", s) if x and x not in STOP]
    return "-".join(w[:maxw])


def money(x):
    x = float(x)
    return f"${x:,.2f}" if x % 1 else f"${x:,.0f}"


def wc(s):
    return len(re.sub(r"<[^>]+>", " ", s).split())


def fit(req, opts, lo=42, hi=58):
    """Opening paragraph: required sentence(s) plus optional ones until 42 to 58 words."""
    out = req
    for o in opts:
        if wc(out) >= lo:
            break
        if wc(out + " " + o) <= hi:
            out += " " + o
    for o in opts:
        if wc(out) >= lo:
            break
        if o not in out and wc(out + " " + o) <= 60:
            out += " " + o
    return out


# ---------------------------------------------------------------- products
BANNED_START = re.compile(r"^(this|that|these|those|it|they|he|she|such|here|above|below|as mentioned|as noted|as discussed|as we saw)\b", re.I)
BAD = re.compile(r"(\(?\d{3}\)?[\s.-]\d{3}-\d{4}|@|https?://|www\.|\.com\b|\.org\b)", re.I)
OTHER = re.compile(r"\b(" + "|".join(re.escape(s) for s in STATES) + r")\b")


def sentences(p):
    t = re.sub(r"\s+", " ", p["description"]).strip()
    title = p["title"].strip()
    if t.startswith(title):
        t = t[len(title):].strip()
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"“])", t)
    out = []
    for s in parts:
        s = s.strip()
        if not s or len(s.split()) > 38 or len(s.split()) < 5:
            continue
        if BAD.search(s) or OTHER.search(s.replace("South Carolina", "")):
            continue
        if s in out:
            continue
        out.append(s)
    return out


def take(sents, start, target):
    """Take sentences from index start until ~target words; first one must not open with a back-reference."""
    i = start
    while i < len(sents) and BANNED_START.match(sents[i]):
        i += 1
    chunk, n = [], 0
    while i < len(sents) and n < target:
        chunk.append(sents[i]); n += len(sents[i].split()); i += 1
    return chunk, i


def short_name(title, lic):
    t = title
    t = re.sub(r"\(Based on the (\d{4}) NEC\)", r"(\1 NEC)", t)
    t = re.sub(r"^South Carolina\s*-\s*", "", t)
    t = t.replace("South Carolina ", "").replace(" South Carolina", "")
    t = re.sub(r":.*$", "", t)
    t = re.sub(r"\s+", " ", t).strip(" -,;")
    return t


def load_products():
    raw = json.load(open(os.path.join(ROOT, "data", "products-raw.json")))
    prods, used = [], set()
    for p in raw:
        lic = classify(p["title"])
        if not lic or lic == "unmatched":
            continue
        typ, rank = ptype(p["title"])
        prices = [float(v["price"]) for v in p["variants"]["nodes"]]
        vid = p["variants"]["nodes"][0]["id"].rsplit("/", 1)[1]
        img = ((p.get("featuredMedia") or {}).get("preview") or {}).get("image") or {}
        year = re.search(r"\b(20\d\d)\b", p["title"])
        year = int(year.group(1)) if year else None
        old = bool(year and lic in ("journeyman-electrician", "master-electrician") and year < 2026) or ("8th edit" in p["title"].lower())
        slug = slugify(re.sub(r"(?i)south carolina", "", p["title"]), 9) or p["handle"]
        base = slug; k = 2
        while slug in used:
            slug = f"{base}-{k}"; k += 1
        used.add(slug)
        prods.append(dict(
            id=p["id"], title=p["title"].strip(), short=short_name(p["title"], lic), lic=lic, type=typ, rank=rank,
            price=min(prices), pmax=max(prices), vid=vid, img=img.get("url"), alt=img.get("altText") or p["title"],
            year=year, old=old, slug=slug, sents=sentences(p), online=typ in ONLINE_TYPES,
        ))
    for p in prods:
        p["url"] = f"/{p['lic']}/{p['slug']}/"
    return prods


# ---------------------------------------------------------------- layout
NAV = [("/licenses/", "Licenses"), ("/how-to-get-licensed/", "How to get licensed"), ("/blog/", "Blog"), ("/faq/", "FAQ"), ("/reviews/", "Reviews"), ("/contact/", "Contact")]


def ld_org():
    return {"@type": "Organization", "@id": SITE + "/#org", "name": BRAND, "url": SITE + "/",
            "logo": SITE + "/assets/img/logo-mark.png", "image": SITE + "/assets/img/og.jpg",
            "telephone": PHONE, "email": EMAIL, "parentOrganization": {"@type": "Organization", "name": "1 Exam Prep", "url": "https://1examprep.com"},
            "contactPoint": {"@type": "ContactPoint", "telephone": TEL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-SC", "availableLanguage": "English"},
            "areaServed": {"@type": "State", "name": "South Carolina"}}


def publisher():
    return {"@type": "Organization", "name": BRAND, "url": SITE + "/", "logo": {"@type": "ImageObject", "url": SITE + "/assets/img/logo-mark.png"}}


def crumbs_ld(crumbs):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (u, n) in enumerate(crumbs)]}


def faq_ld(faq):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faq]}


def webpage_ld(path, title, desc, typ="WebPage"):
    return {"@type": typ, "@id": SITE + path + "#page", "url": SITE + path, "name": title, "description": desc,
            "inLanguage": "en-US", "isPartOf": {"@id": SITE + "/#website"}, "publisher": publisher(),
            "datePublished": LAUNCHED, "dateModified": CHECKED, "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + "/assets/img/og.jpg"}}


def head(p):
    title, desc, path = p["title"], p["desc"], p["path"]
    assert 30 <= len(title) <= 60, (len(title), title)
    assert 70 <= len(desc) <= 160, (len(desc), desc)
    lds = "".join(f'\n<script type="application/ld+json">{json.dumps(dict({"@context": "https://schema.org"}, **x), ensure_ascii=False)}</script>' for x in p["ld"])
    img = p.get("ogimg") or SITE + "/assets/img/og.jpg"
    pre = '\n<link rel="preload" as="image" href="/assets/img/hero.webp" type="image/webp">' if p.get("home") else ""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{SITE}{path}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="{'product' if p.get('product') else ('article' if p.get('article') else 'website')}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{E(img)}">
<meta property="og:image:alt" content="{E(p.get('ogalt') or 'Pass Your South Carolina Contractor Exam: Charleston waterfront at night under a crescent moon')}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(desc)}">
<meta name="twitter:image" content="{E(img)}">
<meta name="theme-color" content="#0B2545">
<link rel="icon" type="image/png" href="/assets/img/favicon.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">{pre}
<link rel="stylesheet" href="/assets/site.css?v=5">
<script src="/assets/site.js?v=3" defer></script>{lds}
</head>'''


def header():
    nav = "".join(f'<a href="{u}">{n}</a>' for u, n in NAV)
    return f'''<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap"><span>South Carolina CLB and Residential Builders exam prep</span><span class="tb-contact"><a href="tel:{TEL}">{PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a></span></div></div>
<header class="site-header"><div class="wrap hdr">
<a class="logo" href="/"><img src="/assets/img/logo-nav.png" width="260" height="50" alt="Pass Your SC Exam logo: palmetto, crescent moon and green check"></a>
<nav class="nav" id="nav" aria-label="Main">{nav}</nav>
<a class="btn btn-call" href="tel:{TEL}">Call {PHONE}</a>
<button class="menu" type="button" aria-controls="nav" aria-expanded="false" aria-label="Open menu"><span></span><span></span></button>
</div></header>'''


def footer():
    lic = [l for l in LICENSES if l["group"] in ("commercial", "residential")][:10]
    links = "".join(f'<li><a href="/{l["slug"]}/">{E(l["name"])}</a></li>' for l in lic)
    return f'''<footer class="site-footer"><div class="wrap fgrid">
<div><img src="/assets/img/logo-nav-dark.png" width="240" height="46" alt="Pass Your SC Exam logo on navy" loading="lazy">
<p>Exam prep books, tabs, courses and licensing help for South Carolina contractors. Orders are fulfilled by 1 Exam Prep.</p>
<p class="fcontact"><a href="tel:{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
<div><p class="fh">Popular licenses</p><ul>{links}</ul></div>
<div><p class="fh">Site</p><ul><li><a href="/licenses/">All licenses</a></li><li><a href="/how-to-get-licensed/">How to get licensed</a></li><li><a href="/blog/">Blog</a></li><li><a href="/faq/">FAQ</a></li><li><a href="/reviews/">Customer reviews</a></li><li><a href="/contact/">Contact</a></li><li><a href="/sitemap.xml">Sitemap</a></li></ul>
<p class="fh">Official sources</p><ul><li><a href="https://llr.sc.gov/clb/" rel="noopener">SC Contractor's Licensing Board</a></li><li><a href="https://llr.sc.gov/res/" rel="noopener">SC Residential Builders Commission</a></li></ul></div>
</div><div class="wrap fbase"><p>&copy; 2026 {BRAND}. Not affiliated with SC LLR or PSI. Prices in US dollars.</p></div></footer>
</body>
</html>'''


def breadcrumb(crumbs):
    items = []
    for i, (u, n) in enumerate(crumbs):
        items.append(f'<li><a href="{u}">{E(n)}</a></li>' if i < len(crumbs) - 1 else f'<li aria-current="page">{E(n)}</li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>'


def takeaways_html(items):
    lis = "".join(f"<li>{x}</li>" for x in items)
    return f'<aside class="takeaways"><h2 id="key-takeaways">Key takeaways</h2><ul>{lis}</ul></aside>'


def faq_html(faq):
    items = "".join(f'<div class="qa"><dt>{E(q)}</dt><dd>{a}</dd></div>' for q, a in faq)
    return f'<section class="faq" id="faq"><h2 id="frequently-asked-questions">Frequently asked questions</h2><p>Short answers to the questions South Carolina candidates ask us most, checked against LLR and PSI on {CHECKED_TEXT}.</p><dl>{items}</dl></section>'


def sources_html(keys, note=None):
    lis = "".join(f'<li><a href="{SRC[k][1]}" rel="noopener">{E(SRC[k][0])}</a></li>' for k in keys)
    return f'<section class="sources" id="sources"><h2 id="sources-h">Sources</h2><p>{note or 'Licensing facts on this page come from the South Carolina Department of Labor, Licensing and Regulation and its exam vendor, PSI.'}</p><ul>{lis}</ul></section>'


def help_card():
    return f'''<div class="help"><p class="side-h">Questions before you buy?</p><p>Call or email the 1 Exam Prep team and we will match you with the right books.</p>
<a class="btn btn-gold" href="tel:{TEL}">{PHONE}</a><a class="help-mail" href="mailto:{EMAIL}">{EMAIL}</a><a class="help-link" href="/contact/">Contact page</a></div>'''


def render(p):
    sec = "".join(f'<section id="s-{sid}"><h2 id="{sid}">{E(h)}</h2>{body}</section>' for sid, h, body in p["sections"])
    side = f'<aside class="sidebar">{p.get("side", "")}{help_card()}</aside>' if p.get("sidebar", True) else ""
    updated = f'<p class="updated">Last updated <time datetime="{CHECKED}">{CHECKED_TEXT}</time></p>'
    hero = p.get("hero_html") or f'''<div class="page-hero"><div class="wrap">{breadcrumb(p["crumbs"])}<div class="ph-row">{p.get("hero_img", "")}<div><p class="eyebrow">{E(p.get("eyebrow", "South Carolina"))}</p><h1>{E(p["h1"])}</h1>{p.get("byline", "")}</div></div></div></div>'''
    pre = p.get("pre", "")
    body = f'''{header()}
<main id="main">{hero}
<div class="wrap {'layout' if side else 'single'}"><article class="content">
<p class="lead">{p["lead"]}</p>{updated}
{takeaways_html(p["takeaways"])}{pre}{sec}{faq_html(p["faq"])}{sources_html(p["sources"], p.get("sources_note"))}
</article>{side}</div>{p.get("post", "")}
</main>
{footer()}'''
    return head(p) + "\n" + body


def write(path, s):
    fp = os.path.join(OUT, path.strip("/"), "index.html") if path.endswith("/") else os.path.join(OUT, path.strip("/"))
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w").write(s)


# ---------------------------------------------------------------- shared copy
def exams_for(l):
    b = l["board"]
    if b in ("gc", "mc"):
        return [(f"PSI {l['name']} technical exam" if l["slug"] != "commercial-general-building" else "NASCLA Commercial General Building exam (PSI)", "Trade knowledge, codes, estimating and safety", "Books allowed (open book)"),
                ("Business Management and Law for Commercial Contractors", "50 questions, 125 minutes, 35 correct to pass", "Open book")]
    if b == "alarm":
        return [("PSI Fire Alarm exam", "NFPA 72 and fire alarm practice", "Open book"), ("Alarm Code of Laws exam", "SC Alarm System Business Act", "Open book")]
    if b == "rbc":
        return [(f"PSI {l['name']} exam", "Trade knowledge and the residential code", "Open book"),
                ("Business Management and Law for Residential Builders", "Scale score of 68 to pass", "Open book")]
    if b == "local":
        code = "International Plumbing Code" if "plumb" in l["slug"] else "National Electrical Code"
        return [(f"{l['name']} exam (local)", f"{code} lookups and calculations", "Usually open book")]
    if l["slug"] == "commercial-business-law":
        return [("Business Management and Law for Commercial Contractors", "50 questions, 125 minutes, 35 correct to pass", "Open book")]
    if l["slug"] == "residential-business-law":
        return [("Business Management and Law for Residential Builders", "Scale score of 68 to pass", "Open book")]
    return [("No exam", "Paperwork and business setup", "Not applicable")]


def board_sources(l):
    b = l["board"]
    return {"gc": ["clb", "clb_lic", "abbr", "psi_clb"], "mc": ["clb", "clb_lic", "abbr", "psi_clb"], "alarm": ["alarm", "alarm_act"],
            "rbc": ["rbc", "rbc_exam", "rbc_lic", "psi_rbc"], "local": ["clb", "rbc_lic"], "bl": ["clb_lic", "rbc_exam", "psi_clb", "psi_rbc"],
            "svc": ["clb_lic", "doc165", "rbc"]}[b]


TYPE_NOTE = {
    "The 1 Package": "exam prep, the LLR application service and business setup in one order",
    "Ultimate rental package": "the full rental book set with highlighting, tabs and course access",
    "Books and courses rental": "rented reference books together with the online course",
    "Highlighted and tabbed books": "the reference books, already highlighted and tabbed for fast lookups",
    "Complete book package": "every reference book on the PSI list, new and untabbed",
    "Live virtual training": "live instructor-led classes online plus self-study",
    "Online course": "self-paced online lessons and practice questions",
    "Online practice questions": "online practice questions in the exam format",
    "Pre-printed tabs": "printed tabs you stick into your own books",
    "Complete pass package": "the business and law book with tabs, highlighting and practice",
    "Business and Law book": "the NASCLA business and law reference used on the exam",
    "Study guide": "a study guide with 12 practice exams and 2 final exams",
    "Study guide and flash cards": "the study guide plus flash cards",
    "Study guide and NEC with tabs": "the study guide with the NEC code book and tabs",
    "Study guide, calculations and NEC": "the study guide, the calculations guide and the NEC",
    "Super combo": "study guides, flash cards, the NEC and tabs",
    "Ultimate combo": "every study guide, flash cards, the NEC, tabs and highlighting",
    "Study package with NEC course": "the ultimate combo plus an instructor-led NEC course",
    "Exam prep package": "the code book, tabs and a study guide",
    "Ultimate prep package": "the code book, tabs, study guide and extra practice",
    "Starter course": "a short course that explains the license path step by step",
    "Service": "a done-for-you licensing or business filing service",
    "Ultimate service package": "the license application and business formation together",
    "Jumpstart package": "the starter course, business setup and application help",
    "Book": "a single reference book from the exam list",
}


def delivery(p):
    if p["online"]:
        return "Online access is sent by email after checkout. Nothing ships."
    if "rental" in p["type"].lower():
        return "Rental books ship free by USPS Media Mail inside the United States; course access comes by email."
    return "Ships free by USPS Media Mail to US addresses."


DELIVERY_DAYS = {"@type": "OpeningHoursSpecification", "dayOfWeek": ["https://schema.org/Monday", "https://schema.org/Tuesday", "https://schema.org/Wednesday", "https://schema.org/Thursday", "https://schema.org/Friday"]}


def delivery_time(hmin, hmax, tmin, tmax):
    """ShippingDeliveryTime in business days. Matches the page copy: Media Mail 2 to 8 business days,
    rental / Ultimate / 1 Package orders up to 15, online access by email the same or next business day."""
    return {"@type": "ShippingDeliveryTime", "businessDays": DELIVERY_DAYS,
            "handlingTime": {"@type": "QuantitativeValue", "minValue": hmin, "maxValue": hmax, "unitCode": "DAY"},
            "transitTime": {"@type": "QuantitativeValue", "minValue": tmin, "maxValue": tmax, "unitCode": "DAY"}}


def offer_delivery_time(p):
    if p["online"]:
        return delivery_time(0, 1, 0, 0)
    if re.search(r"\b(rental|ultimate|1 package)\b", p["title"] + " " + p["type"], re.I):
        return delivery_time(0, 7, 2, 8)
    return delivery_time(0, 2, 2, 8)


# ---------------------------------------------------------------- product page
def product_card(p, lic_name=None):
    img = f'<img src="{E(p["img"])}&width=480" alt="{E(p["alt"])}" width="240" height="240" loading="lazy">' if p["img"] else '<img src="/assets/img/cat-services.webp" alt="Exam prep package illustration" width="240" height="240" loading="lazy">'
    tag = '<span class="tag tag-old">Older edition</span>' if p["old"] else f'<span class="tag">{E(p["type"])}</span>'
    price = money(p["price"]) + ("+" if p["pmax"] > p["price"] else "")
    return f'''<li class="card" data-type="{E(p["type"])}"><a class="card-img" href="{p["url"]}">{img}</a><div class="card-b">{tag}
<p class="card-t"><a href="{p["url"]}">{E(p["short"])}</a></p><p class="price">{price}</p>
<div class="card-cta"><a class="btn btn-sm btn-green" href="{CART.format(p["vid"])}" rel="nofollow">Buy now</a><a class="more" href="{p["url"]}">Details</a></div></div></li>'''


def ptitle(p, lic, taken):
    sfx = " | SC Exam Prep"
    tt = " ".join(w if w in ("and", "with") else w[:1].upper() + w[1:] for w in p["type"].split())
    cands = [p["short"], f'SC {lic["name"]} Exam: {tt}', f'{lic["name"]} Exam: {tt}', f'SC {lic["name"]} {tt}']
    yr = f' {p["year"]}' if p["year"] else ""
    for c in cands:
        for t in (c + sfx, c, c + yr):
            t = re.sub(r"\s+", " ", t).strip()
            if 30 <= len(t) <= 60 and t not in taken:
                taken.add(t); return t
    base = f'SC {lic["name"]} {p["type"]}'[:44]
    t = f'{base} {money(p["price"])}'
    if len(t) < 30:
        t = t + " | SC Exam Prep"
    t = t[:60]; k = 2
    while t in taken:
        t = t[:56] + f" #{k}"; k += 1
    taken.add(t); return t


def pdesc(p, lic):
    d = f'{p["short"]} for the South Carolina {lic["name"]} exam: {TYPE_NOTE.get(p["type"], "exam prep")}. {money(p["price"])}.'
    if len(d) > 158:
        d = f'{p["type"]} for the South Carolina {lic["name"]} exam: {TYPE_NOTE.get(p["type"], "exam prep")}. {money(p["price"])}.'
    if len(d) > 158:
        d = d[:155].rsplit(" ", 1)[0] + "."
    if len(d) < 75:
        d += " Free shipping on books."
    return d


def product_page(p, lic, siblings, taken):
    path = p["url"]
    title = ptitle(p, lic, taken)
    desc = pdesc(p, lic)
    s = p["sents"]
    c1, i = take(s, 0, 150)
    c2, i = take(s, i, 120)
    if not c1:
        c1 = [f"The {p['short']} is {TYPE_NOTE.get(p['type'], 'exam prep')} for South Carolina {lic['name']} candidates."]
    req = f'The {E(p["short"])} costs {money(p["price"])} and gives South Carolina {E(lic["name"])} candidates {E(TYPE_NOTE.get(p["type"], "exam prep"))}.'
    if wc(req) > 40:
        req = f'This {E(p["type"].lower())} costs {money(p["price"])} and gives South Carolina {E(lic["name"])} candidates {E(TYPE_NOTE.get(p["type"], "exam prep"))}.'.replace("This ", "The ", 1)
    lead = fit(req, [E(delivery(p)), f"Buy it below or call {PHONE} with questions.", "Orders are fulfilled by 1 Exam Prep.",
                     f"PSI runs the {E(lic['name'])} exams as open-book tests, so tabbed books save time." if lic["board"] not in ("local", "svc") else "Most local code exams allow the code book in the room.",
                     "All sales are final, so ask before you order."])
    exams = exams_for(lic)
    sib = sorted([x for x in siblings if x["id"] != p["id"]], key=lambda x: (x["old"], x["rank"], x["price"]))[:8]
    sib_rows = "".join(f'<tr><td><a href="{x["url"]}">{E(x["short"])}</a></td><td>{E(x["type"])}</td><td>{money(x["price"])}</td></tr>' for x in sib)
    cmp_tbl = f'<table><thead><tr><th>Package</th><th>Type</th><th>Price</th></tr></thead><tbody><tr class="hl"><td>{E(p["short"])} (this page)</td><td>{E(p["type"])}</td><td>{money(p["price"])}</td></tr>{sib_rows}</tbody></table>'
    exam_list = "".join(f"<li><strong>{E(a)}</strong>: {E(b)} ({E(c)})</li>" for a, b, c in exams)
    old_note = f" This listing is an older edition ({p['year'] or 'previous'}); check which code edition your exam uses before you buy." if p["old"] else ""
    sections = [
        ("whats-included", f"What is in the {p['short']}?", "<p>" + E(" ".join(c1)) + "</p>" + f'<ul class="facts"><li>Package type: {E(p["type"])}</li><li>Price: {money(p["price"])}{" to " + money(p["pmax"]) if p["pmax"] > p["price"] else ""}</li><li>Delivery: {E(delivery(p))}</li><li>License: <a href="/{lic["slug"]}/">South Carolina {E(lic["name"])}</a></li></ul>'),
        ("fit", f"How does it fit the South Carolina {lic['name']} exam?", f"<p>{E(lic['scope'])} {E(lic['note'])}{E(old_note)}</p><p>Candidates for this license sit {len(exams)} exam{'s' if len(exams) > 1 else ''}:</p><ul>{exam_list}</ul>"),
    ]
    if c2:
        sections.append(("study", "What will you study with it?", "<p>" + E(" ".join(c2)) + "</p>"))
    sections.append(("compare", f"How does it compare with other {lic['name']} packages?",
                     f"<p>South Carolina {E(lic['name'])} prep comes in {len(siblings)} options on this site, from {money(min(x['price'] for x in siblings))} to {money(max(x['price'] for x in siblings))}. The table lists the closest alternatives so you can trade price against how much is done for you.</p>{cmp_tbl}"))
    faq = [
        (f"How much does the {p['short']} cost?", f"The price is {money(p['price'])} in US dollars{', and some options cost up to ' + money(p['pmax']) if p['pmax'] > p['price'] else ''}. Checkout runs through the 1 Exam Prep store, which takes major cards."),
        ("How is the order delivered?", delivery(p) + " Shipping is US only, and tracking comes by email once the order leaves the warehouse."),
        ("Can I return it?", f'All sales are final under the 1 Exam Prep <a href="{REFUND}" rel="noopener">refund policy</a>, so call {PHONE} before ordering if you are unsure which package fits your exam.'),
        (f"Which exams does the South Carolina {lic['name']} license need?", " ".join(f"{a}: {b}." for a, b, c in exams)),
        ("Are the South Carolina exams open book?", "Yes. PSI runs the CLB and Residential Builders Commission exams as open-book tests, so tabbed and highlighted books save real time during the exam."),
        ("Who do I contact with questions?", f'Call the 1 Exam Prep team at <a href="tel:{TEL}">{PHONE}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>. You can also use the <a href="/contact/">contact form</a>.'),
    ]
    take_items = [f"Price: {money(p['price'])}, {E(p['type']).lower()}.", E(delivery(p)), f"For the South Carolina {E(lic['name'])} license ({E(BOARDS[lic['board']])}).",
                  f"{len(siblings)} {E(lic['name'])} packages on this site, from {money(min(x['price'] for x in siblings))}."]
    crumbs = [("/", "Home"), ("/licenses/", "Licenses"), (f"/{lic['slug']}/", lic["name"]), (path, p["short"])]
    img_url = (p["img"] or SITE + "/assets/img/og.jpg")
    shipping = {"@type": "OfferShippingDetails", "shippingRate": {"@type": "MonetaryAmount", "value": 0, "currency": "USD"},
                "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "US"},
                "deliveryTime": offer_delivery_time(p)}
    if p["online"]:
        shipping["shippingLabel"] = "Online access by email, nothing shipped"
    else:
        shipping["shippingLabel"] = "Free USPS (Media Mail)"
    offer = {"@type": "Offer", "url": SITE + path, "priceCurrency": "USD", "price": f"{p['price']:.2f}", "availability": "https://schema.org/InStock",
             "itemCondition": "https://schema.org/NewCondition", "seller": {"@type": "Organization", "name": "1 Exam Prep"},
             "priceValidUntil": "2027-12-31", "shippingDetails": shipping,
             "hasMerchantReturnPolicy": {"@type": "MerchantReturnPolicy", "applicableCountry": "US", "returnPolicyCategory": "https://schema.org/MerchantReturnNotPermitted", "merchantReturnLink": REFUND}}
    if p["pmax"] > p["price"]:
        offer = dict(offer, **{"@type": "AggregateOffer", "lowPrice": f"{p['price']:.2f}", "highPrice": f"{p['pmax']:.2f}", "offerCount": 2}); offer.pop("price")
    prod_ld = {"@type": "Product", "@id": SITE + path + "#product", "name": p["title"], "description": " ".join(c1)[:500] or desc,
               "image": [img_url], "sku": p["vid"], "url": SITE + path, "brand": {"@type": "Brand", "name": "1 Exam Prep"},
               "category": f"South Carolina {lic['name']} exam prep", "offers": offer}
    imgtag = f'<img src="{E(p["img"])}&width=720" alt="{E(p["alt"])}" width="360" height="360">' if p["img"] else '<img src="/assets/img/cat-services.webp" alt="Exam prep package illustration" width="360" height="360">'
    buybox = f'''<div class="buy"><div class="buy-img">{imgtag}</div><div class="buy-b"><span class="tag">{E(p["type"])}</span><p class="buy-price">{money(p["price"])}</p>
<p>{E(delivery(p))}</p><a class="btn btn-green btn-lg" href="{CART.format(p["vid"])}" rel="nofollow">Buy now</a><p class="small">Secure checkout at 1examprep.com. All sales are final.</p></div></div>'''
    side = f'<div class="side-box"><p class="side-h">{E(lic["name"])}</p><p class="side-price">{money(p["price"])}</p><a class="btn btn-green" href="{CART.format(p["vid"])}" rel="nofollow">Buy now</a><a class="help-link" href="/{lic["slug"]}/">All {E(lic["name"])} packages</a></div>'
    pg = dict(path=path, title=title, desc=desc, h1=p["title"], lead=lead, takeaways=take_items, sections=sections, faq=faq,
              sources=board_sources(lic), crumbs=crumbs, eyebrow=f"South Carolina {lic['name']}", pre=buybox, side=side, product=True,
              ogimg=p["img"] or None, ogalt=p["alt"],
              ld=[prod_ld, webpage_ld(path, title, desc, "ItemPage"), crumbs_ld(crumbs), faq_ld(faq)])
    return pg


# ---------------------------------------------------------------- license page
def license_page(l, items):
    path = f"/{l['slug']}/"
    items = sorted(items, key=lambda x: (x["old"], x["rank"], x["price"]))
    lo, hi = min(x["price"] for x in items), max(x["price"] for x in items)
    n = len(items)
    title = f"South Carolina {l['name']} Exam Prep"
    if len(title) > 60:
        title = f"SC {l['name']} Exam Prep"
    if len(title) < 30:
        title += " | Books and Courses"
    if len(title) > 60:
        title = title[:60]
    desc = f"South Carolina {l['name']} exam prep: {n} package{'s' if n > 1 else ''} from {money(lo)} to {money(hi)}. Books, tabs and courses, with exam facts from LLR and PSI."
    if len(desc) > 160:
        desc = f"SC {l['name']} exam prep: {n} packages from {money(lo)}. Books, tabs and courses with exam facts from LLR and PSI."
    exams = exams_for(l)
    req = f"{E(l['scope'])} We carry {n} South Carolina {E(l['name'])} package{'s' if n > 1 else ''}, priced from {money(lo)} to {money(hi)}."
    if wc(req) > 46:
        req = f"We carry {n} South Carolina {E(l['name'])} exam prep package{'s' if n > 1 else ''}, priced from {money(lo)} to {money(hi)}, for the {E(BOARDS[l['board']])}."
    lead = fit(req, [f"They cover {'the ' + str(len(exams)) + ' exams' if len(exams) > 1 else 'the exam'} you need, from reference books to courses.".replace("They cover", "The packages cover"),
                     "Every book ships free by USPS Media Mail.", "Online courses arrive by email right after checkout.", f"Call {PHONE} for help choosing."])
    types = defaultdict(list)
    for x in items:
        types[x["type"]].append(x)
    chips = '<div class="chips" role="group" aria-label="Filter packages"><button type="button" class="chip on" data-filter="all">All</button>' + "".join(
        f'<button type="button" class="chip" data-filter="{E(t)}">{E(t)}</button>' for t in sorted(types, key=lambda t: types[t][0]["rank"])) + "</div>" if len(types) > 2 else ""
    grid = f'<section class="pkgs" id="packages"><h2 id="packages-h">South Carolina {E(l["name"])} packages</h2><p>{n} package{"s" if n > 1 else ""} for this license, sorted with the most complete options first. Prices are in US dollars and books ship free.</p>{chips}<ul class="cards">{"".join(product_card(x) for x in items)}</ul></section>'
    exam_rows = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td></tr>" for a, b, c in exams)
    sections = [
        ("what-it-covers", f"What does the South Carolina {l['name']} license cover?",
         f"<p>{E(l['scope'])} {E(l['note'])}</p>" + (f"<p>On a CLB license the classification shows as a 2-letter code followed by a group number, so {E(l['abbr'].split(' / ')[0])}3 means {E(l['name'])} work up to $1,000,000 per job. A license is needed once regulated commercial work costs more than $10,000.</p>" if l["board"] in ("gc", "mc") else "")),
        ("exams", f"Which exams do {l['name']} candidates take?",
         f"<p>{'PSI gives every South Carolina contractor exam at its test centers.' if l['board'] != 'local' else 'Local credentials use exams chosen by the city or county.'} The table lists what this license needs, based on the current LLR pages and PSI bulletins.</p><table><thead><tr><th>Exam</th><th>What it covers</th><th>Format</th></tr></thead><tbody>{exam_rows}</tbody></table>"),
    ]
    if l["board"] in ("gc", "mc"):
        g = GC_GROUPS if l["board"] == "gc" else MC_GROUPS
        if l["slug"] == "limited-building":
            g = g[:3]
        rows = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in g)
        sections.append(("job-limits", "How much work can you bid with the license?",
                         f"<p>South Carolina {'general' if l['board'] == 'gc' else 'mechanical'} contractor licenses come in groups set by your financial statement or surety bond. The group caps the value of any single job or bid. The initial license fee is $350, and {'general' if l['board'] == 'gc' else 'mechanical'} licenses expire on October 31 of {'even' if l['board'] == 'gc' else 'odd'}-numbered years.</p><table><thead><tr><th>Group</th><th>Limit per job</th></tr></thead><tbody>{rows}</tbody></table>"))
    elif l["board"] == "rbc":
        sections.append(("process", f"How do you get the {l['name']} license?",
                         "<ol><li>Apply to the Residential Builders Commission first and pay the application fee.</li><li>Wait for the Exam Eligibility letter by email or mail; eligibility lasts 1 year.</li><li>Schedule both exams with PSI and pay PSI directly.</li><li>Pass the trade exam and Business Management and Law (scale score 68) within the 12 months.</li><li>Send proof of insurance or bonding as the Commission asks, then receive the license.</li></ol>"))
    elif l["board"] == "local":
        sections.append(("local", "Who issues the license in South Carolina?",
                         f"<p>South Carolina does not issue a statewide {E(l['name'].lower())} card. Cities and counties do, and most use a PSI or ICC exam built on a recent code edition. Ask the building department where you work which edition it tests, then pick the matching study guide. The {n} packages here include current and older editions, clearly labelled.</p>"))
    tl = sorted(types, key=lambda t: types[t][0]["rank"])
    type_list = "".join(f"<li><strong>{E(t)}</strong> ({len(types[t])}, from {money(min(x['price'] for x in types[t]))}): {E(TYPE_NOTE.get(t, 'exam prep'))}.</li>" for t in tl)
    sections.append(("choose", f"Which {l['name']} package should you choose?",
                     f"<p>Pick by how much time you have and how much of the setup you want done for you. Candidates with 6 weeks or less usually choose highlighted and tabbed books or a course, because the exams are open book and speed matters.</p><ul>{type_list}</ul>"))
    best = items[0]
    cheap = min(items, key=lambda x: x["price"])
    faq = [
        (f"How much does South Carolina {l['name']} exam prep cost?", f"Packages on this site run from {money(lo)} to {money(hi)}. The lowest-priced option is the {E(cheap['short'])} at {money(cheap['price'])}."),
        (f"Which exams do I need for the {l['name']} license?", " ".join(f"{a}: {b}." for a, b, c in exams)),
        ("Are South Carolina contractor exams open book?", "Yes. PSI allows the approved reference books in the testing room for the CLB and Residential Builders Commission exams, so tabbed and highlighted books are worth having."),
        ("Do I need approval before scheduling the exam?", "Not for Contractor's Licensing Board exams: you schedule with PSI directly and apply after you pass. Residential Builders Commission candidates apply first and wait for the Exam Eligibility letter." if l["board"] != "local" else "Local exams follow the rules of the city or county that issues the card. Most require an application and proof of experience before you can sit the exam."),
        ("Do the books ship free?", "Yes. Physical books and tabs ship free by USPS Media Mail inside the United States, and online courses arrive by email right after checkout."),
        ("Which package is the most complete?", f"The most complete option for this license is the {E(best['short'])} at {money(best['price'])}. Call {PHONE} if you want help comparing it with the cheaper choices."),
        ("How do I get help choosing?", f'Call <a href="tel:{TEL}">{PHONE}</a>, email <a href="mailto:{EMAIL}">{EMAIL}</a> or use the <a href="/contact/">contact page</a>. Tell us the license and your exam date.'),
    ]
    take_items = [f"{n} package{'s' if n > 1 else ''} from {money(lo)} to {money(hi)}.", f"Issued by: {E(BOARDS[l['board']])}.",
                  " ".join(f"{E(a)}: {E(b)}." for a, b, c in exams[:2])]
    if l["board"] in ("gc", "mc"):
        take_items.append("A license is required for regulated commercial work over $10,000.")
    elif l["board"] == "rbc":
        take_items.append("Apply to the Commission first; eligibility lasts 1 year.")
    crumbs = [("/", "Home"), ("/licenses/", "Licenses"), (path, l["name"])]
    item_list = {"@type": "ItemList", "name": f"South Carolina {l['name']} exam prep packages", "numberOfItems": n,
                 "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + x["url"], "name": x["title"]} for i, x in enumerate(items)]}
    coll = webpage_ld(path, title, desc, "CollectionPage"); coll["mainEntity"] = {"@id": SITE + path + "#list"}; item_list["@id"] = SITE + path + "#list"
    icon = {"commercial": "commercial", "mechanical": "mechanical", "residential": "residential", "local": "local", "business": "business", "services": "services"}[l["group"]]
    side = f'''<div class="side-box"><p class="side-h">Exam facts</p><ul class="side-facts"><li><span>Issued by</span>{E(BOARDS[l["board"]])}</li>{"".join(f"<li><span>Exam</span>{E(a)}</li>" for a, b, c in exams)}<li><span>Packages</span>{n}, from {money(lo)}</li></ul><a class="btn btn-green" href="#packages">See packages</a></div>'''
    return dict(path=path, title=title, desc=desc, h1=f"South Carolina {l['name']} Exam Prep", lead=lead, takeaways=take_items, pre=grid,
                sections=sections, faq=faq, sources=board_sources(l), crumbs=crumbs, eyebrow=dict((g[0], g[1]) for g in GROUPS)[l["group"]],
                hero_img=f'<img class="ph-icon" src="/assets/img/cat-{icon}.webp" alt="{E(l["name"])} license illustration" width="96" height="96">',
                side=side, ld=[coll, item_list, crumbs_ld(crumbs), faq_ld(faq)])


# ---------------------------------------------------------------- static pages
def license_tiles(counts, prices, heads=True):
    out = []
    for gk, gname, gdesc, icon in GROUPS:
        ls = [l for l in LICENSES if l["group"] == gk]
        lis = "".join(f'<li data-name="{E(l["name"].lower())}"><a href="/{l["slug"]}/"><span>{E(l["name"])}</span><small>{counts[l["slug"]]} package{"s" if counts[l["slug"]] != 1 else ""} · from {money(prices[l["slug"]])}</small></a></li>' for l in ls)
        out.append(f'<div class="group" id="g-{gk}"><div class="g-head"><img src="/assets/img/cat-{icon}.webp" alt="{E(gname)} illustration" width="72" height="72" loading="lazy"><div>{f'<h3 id="h-{gk}">{E(gname)}</h3>' if heads else f'<p class="g-title">{E(gname)}</p>'}<p>{E(gdesc)}</p></div></div><ul class="lic-list">{lis}</ul></div>')
    return "".join(out)


def home_page(counts, prices, nprod):
    path = "/"
    title = "Pass Your South Carolina Contractor Exam | SC Exam Prep"
    desc = f"South Carolina contractor exam prep for {len(LICENSES)} CLB, Residential Builders and trade licenses. {nprod} books, tabs and courses with free shipping."
    lead = (f"Passing the South Carolina contractor exam takes the right open-book references and a plan. We stock {nprod} study packages for {len(LICENSES)} licenses, "
            f"from the $10,000 CLB commercial threshold to Residential Builder, with tabbed books, online courses and live classes. Call {PHONE} for help choosing.")
    hero = f'''<section class="hero"><picture><source type="image/webp" srcset="/assets/img/hero-800.webp 800w, /assets/img/hero.webp 1600w" sizes="100vw"><img class="hero-bg" src="/assets/img/hero.jpg" alt="Charleston waterfront at night under a crescent moon, with the Ravenel Bridge, historic homes, a church steeple and palmetto trees" width="1600" height="900"></picture>
<div class="wrap hero-in"><p class="eyebrow">South Carolina contractor exam prep</p><h1>Pass your South Carolina contractor exam. <span>First try.</span></h1>
<p class="hero-sub">Books, tabs, courses and licensing help for {len(LICENSES)} CLB, Residential Builders and trade licenses.</p>
<div class="hero-cta"><a class="btn btn-gold btn-lg" href="#find">Find my exam</a><a class="btn btn-ghost btn-lg" href="tel:{TEL}">Call {PHONE}</a></div>
<ul class="hero-stats"><li><b>{nprod}</b><span>study packages</span></li><li><b>{len(LICENSES)}</b><span>licenses covered</span></li><li><b>$0</b><span>shipping on books</span></li></ul></div></section>'''
    finder = f'''<section class="finder" id="find"><div class="wrap"><h2 id="find-your-license">Find your South Carolina license</h2><p class="sub">Type a trade or pick a board. Every license page lists the exams, the job limits and every package we carry.</p>
<label class="search"><span class="sr">Search licenses</span><input id="lic-search" type="search" placeholder="Roofing, HVAC, residential builder" autocomplete="off"></label>
<div class="groups">{license_tiles(counts, prices)}</div></div></section>'''
    gc_rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for (a, b), (_, c) in zip(GC_GROUPS, MC_GROUPS))
    sections = [
        ("which-board", "Which South Carolina board licenses you?",
         "<p>South Carolina splits contractor licensing between two boards inside the Department of Labor, Licensing and Regulation (LLR). The Contractor's Licensing Board (CLB) covers commercial general and mechanical contractors, alarm businesses and boiler work. The Residential Builders Commission (RBC) covers homes. Electrician and plumber cards for individual workers are handled locally.</p>"
         "<table><thead><tr><th>Board</th><th>Who needs it</th><th>Exams</th></tr></thead><tbody><tr><td>Contractor's Licensing Board</td><td>Regulated commercial work over $10,000</td><td>Trade exam plus Commercial Business and Law</td></tr><tr><td>Residential Builders Commission</td><td>Residential builders and residential specialty trades</td><td>Trade exam plus Residential Business and Law</td></tr><tr><td>City or county</td><td>Journeyman and master electricians, plumbers</td><td>Local code exam</td></tr></tbody></table>"),
        ("how-it-works", "How do you pass with 1 Exam Prep?",
         "<ol class='steps'><li><b>Pick your license.</b> Each license page lists the exams and every package we carry.</li><li><b>Choose how you study.</b> Tabbed books, online courses, live virtual classes or a complete rental.</li><li><b>Study the books you take in.</b> South Carolina exams are open book, so practice finding answers fast.</li><li><b>Book with PSI and pass.</b> CLB candidates schedule directly; RBC candidates wait for the Exam Eligibility letter.</li></ol>"
         "<p>Most candidates study for 4 to 8 weeks. Highlighted and tabbed books cut lookup time on a 125-minute business exam where you need 35 of 50 right.</p>"),
        ("job-limits", "How much can a South Carolina contractor bid?",
         f"<p>CLB licenses carry a group number that caps each job. The group comes from your financial statement or surety bond, and the license fee is $350. The limits below are from the LLR group table.</p><table><thead><tr><th>Group</th><th>General contractor</th><th>Mechanical contractor</th></tr></thead><tbody>{gc_rows}</tbody></table>"),
        ("why-us", "Why do South Carolina contractors study with us?",
         f"<ul><li><b>Every book on the PSI list</b>, new or rented, with tabs placed where the answers are.</li><li><b>Free USPS Media Mail shipping</b> on books and tabs inside the US.</li><li><b>Courses for {sum(1 for l in LICENSES if l['board'] in ('gc', 'mc'))} CLB classifications</b>, plus Residential Builder and the three residential trades.</li><li><b>Licensing help</b>: the LLR application service and LLC setup, or all of it in The 1 Package.</li><li><b>People who answer the phone</b> at {PHONE} and {EMAIL}.</li></ul>"),
    ]
    faq = [
        ("Do I need a contractor license in South Carolina?", "You need a CLB general or mechanical contractor license for regulated commercial work over $10,000, and a Residential Builders Commission license for residential building and specialty trade work."),
        ("Are South Carolina contractor exams open book?", "Yes. PSI runs the CLB and RBC trade exams and both Business and Law exams as open-book tests with the approved references."),
        ("How many questions are on the Commercial Business and Law exam?", "The Business Management and Law for Commercial Contractors exam has 50 questions and a 125-minute limit. You need 35 correct answers to pass."),
        ("What score passes the Residential Business and Law exam?", "The Residential Builders Commission requires a scale score of 68 on the Business Management and Law exam."),
        ("Can I skip the Residential Builder trade exam?", "Yes, if you hold a current SC General Contractor license or passed the NASCLA exam in the last 3 years. The Business and Law exam still applies."),
        ("How long does a CLB license last?", "General contractor licenses expire October 31 in even-numbered years and mechanical contractor licenses on October 31 in odd-numbered years."),
        ("Do you ship outside South Carolina?", "Books ship free by USPS Media Mail anywhere in the United States. Online courses are delivered by email, so you can study from anywhere."),
        ("How do I contact you?", f'Call <a href="tel:{TEL}">{PHONE}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>. The <a href="/contact/">contact page</a> has a form as well.'),
    ]
    take = [f"{nprod} study packages for {len(LICENSES)} South Carolina licenses.", "CLB license needed for regulated commercial work over $10,000.",
            "Commercial Business and Law: 50 questions, 125 minutes, 35 to pass.", "Residential Business and Law: scale score 68.", f"Help by phone at {PHONE}."]
    contact_band = f'''<section class="band" id="contact-band"><div class="wrap band-in"><div><p class="band-h">Not sure which package fits your exam?</p><p>Talk to a person who knows the South Carolina exams.</p></div><div class="band-cta"><a class="btn btn-gold btn-lg" href="tel:{TEL}">{PHONE}</a><a class="btn btn-ghost btn-lg" href="mailto:{EMAIL}">{EMAIL}</a></div></div></section>'''
    website = {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": BRAND, "publisher": {"@id": SITE + "/#org"}, "inLanguage": "en-US"}
    return dict(path=path, title=title, desc=desc, h1="", lead=lead, takeaways=take, sections=sections, faq=faq, sources=["clb", "clb_faq", "rbc_exam", "psi_clb", "psi_rbc"],
                crumbs=[("/", "Home")], hero_html=hero + finder, home=True, sidebar=False, post=contact_band,
                ld=[ld_org(), website, webpage_ld(path, title, desc), faq_ld(faq)])


def licenses_index(counts, prices, nprod):
    path = "/licenses/"
    title = "South Carolina Contractor Licenses: Exam Prep by Trade"
    desc = f"All {len(LICENSES)} South Carolina contractor licenses we cover, grouped by board, with package counts and starting prices. CLB, RBC, local and business exams."
    lead = (f"South Carolina contractor licenses fall into six groups on this site: {len(LICENSES)} licenses in all, with {nprod} study packages between them. "
            "Pick a license to see its exams, job limits and every book, tab and course we carry for it, or call us for a recommendation.")
    sections = [("all-licenses", "Which licenses does the site cover?", f'<p>The list below groups every license by the board that issues it. Counts and starting prices update each time the catalog is synced from the 1 Exam Prep store.</p><label class="search"><span class="sr">Search licenses</span><input id="lic-search" type="search" placeholder="Search {len(LICENSES)} licenses" autocomplete="off"></label><div class="groups">{license_tiles(counts, prices, False)}</div>'),
                ("how-to-choose", "How do you know which license you need?",
                 "<p>Start with the work and its value. Commercial work in a regulated classification over $10,000 needs a CLB license. Homes need an RBC license. Individual electricians and plumbers need a local card. The <a href='/how-to-get-licensed/'>licensing guide</a> walks through each path step by step.</p>")]
    faq = [
        ("How many South Carolina contractor licenses are there?", f"The CLB lists dozens of classifications and subclassifications. This site covers {len(LICENSES)} of them, including every one we stock prep material for."),
        ("What is the difference between CLB and RBC?", "The Contractor's Licensing Board licenses commercial general and mechanical contractors. The Residential Builders Commission licenses residential builders and residential specialty contractors."),
        ("Can I hold more than one classification?", "Yes. A CLB license can carry several classifications. You pass the technical exam for each one and the Business and Law exam once."),
        ("Is there a statewide electrician license?", "Not for individual journeymen. South Carolina electrician cards are local, while electrical contracting businesses hold a CLB or RBC license."),
        ("Do all licenses need the Business and Law exam?", "Every CLB and RBC license needs the matching Business Management and Law exam. Local electrician and plumber cards do not."),
        ("Where do I schedule the exams?", "PSI runs the South Carolina contractor exams. CLB candidates schedule directly with PSI; RBC candidates wait for the Exam Eligibility letter first."),
    ]
    take = [f"{len(LICENSES)} licenses, {nprod} packages.", "CLB: commercial work over $10,000.", "RBC: residential builders and trades.", "Local: journeyman and master cards."]
    crumbs = [("/", "Home"), (path, "Licenses")]
    il = {"@type": "ItemList", "name": "South Carolina contractor licenses", "numberOfItems": len(LICENSES),
          "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/{l['slug']}/", "name": l["name"]} for i, l in enumerate(LICENSES)]}
    return dict(path=path, title=title, desc=desc, h1="South Carolina Contractor Licenses", lead=lead, takeaways=take, sections=sections, faq=faq,
                sources=["clb", "abbr", "rbc_lic"], crumbs=crumbs, eyebrow="All licenses", sidebar=False,
                ld=[webpage_ld(path, title, desc, "CollectionPage"), il, crumbs_ld(crumbs), faq_ld(faq)])


def guide_page():
    path = "/how-to-get-licensed/"
    title = "How to Get a South Carolina Contractor License (2026)"
    desc = "Step-by-step guide to a South Carolina contractor license: CLB vs RBC, PSI exams, Business and Law, job limits, fees and renewal dates. Updated November 2026."
    lead = ("To get a South Carolina contractor license, decide whether the CLB or the Residential Builders Commission covers your work, pass the PSI trade exam and the "
            "Business Management and Law exam, then apply to LLR with your financials. Commercial work over $10,000 needs a CLB license, and the fee is $350.")
    steps = [
        ("Pick the board", "Commercial general or mechanical work over $10,000 goes to the Contractor's Licensing Board. Residential building and residential trades go to the Residential Builders Commission."),
        ("Choose the classification", "Match your work to a classification such as Building, Roofing, Plumbing or Residential Builder."),
        ("Pass the PSI exams", "Take the trade exam and the matching Business Management and Law exam. Both are open book."),
        ("Prepare financials", "CLB applicants submit a financial statement or surety bond, which sets the license group."),
        ("Apply to LLR", "Send the application, exam pass sheets and the $350 fee for a CLB license."),
    ]
    steps_html = "<ol class='steps'>" + "".join(f"<li><b>{E(a)}.</b> {E(b)}</li>" for a, b in steps) + "</ol>"
    gc_rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for (a, b), (_, c) in zip(GC_GROUPS, MC_GROUPS))
    sections = [
        ("steps", "What are the steps to a South Carolina contractor license?", steps_html + "<p>Most candidates finish the exams within 4 to 8 weeks of starting to study. The LLR review then takes a few weeks, depending on how complete the application is.</p>"),
        ("clb-or-rbc", "Do you need a CLB or an RBC license?",
         "<p>The Contractor's Licensing Board regulates general and mechanical contractors under Title 40, Chapter 11 of the SC Code. A CLB license is required once regulated commercial work costs more than $10,000, and it also allows residential work. "
         "The Residential Builders Commission licenses builders and specialty contractors who only work on homes. Burglar and fire alarm businesses are licensed by the CLB under the Alarm System Business Act.</p>"
         "<p>Pick by your biggest likely job. A remodeler doing kitchens and baths needs the Residential Builder license. A company bidding a $250,000 retail fit-out needs a CLB Building license in Group 2 or above.</p>"),
        ("exams", "Which exams will you take?",
         "<table><thead><tr><th>Exam</th><th>Who takes it</th><th>Key facts</th></tr></thead><tbody>"
         "<tr><td>Business Management and Law for Commercial Contractors</td><td>Every CLB applicant, plus pool and alarm qualifiers</td><td>50 questions, 125 minutes, 35 to pass, open book</td></tr>"
         "<tr><td>Business Management and Law for Residential Builders</td><td>Every RBC applicant</td><td>Scale score 68, open book</td></tr>"
         "<tr><td>CLB technical exam</td><td>One per classification</td><td>PSI, open book; NASCLA accepted for Unlimited Building</td></tr>"
         "<tr><td>RBC technical exam</td><td>Residential Builder, Electrical, HVAC, Plumbing</td><td>PSI, open book; waivers in some cases</td></tr></tbody></table>"
         "<p>CLB candidates do not need approval to book a PSI exam. RBC candidates apply first and receive an Exam Eligibility letter valid for 1 year.</p>"),
        ("groups", "How do license groups and job limits work?",
         f"<p>Each CLB license carries a group from 1 to 5. The group sets the most you can bid or contract on one job. Groups 1 and 2 can use an owner-prepared financial statement or a surety bond; higher groups need reviewed or audited statements.</p><table><thead><tr><th>Group</th><th>General contractor</th><th>Mechanical contractor</th></tr></thead><tbody>{gc_rows}</tbody></table>"),
        ("waivers", "Can you skip a South Carolina exam?",
         "<p>Sometimes. The CLB has waiver agreements with several states for technical exams, but every waiver applicant still passes the South Carolina Business Management and Law exam. "
         "For Residential Builder, a current SC General Contractor or a NASCLA pass from the last 3 years waives the trade exam. Residential electrical and plumbing waivers exist with North Carolina and Mississippi.</p>"),
        ("renewal", "When does a South Carolina license expire?",
         "<p>General contractor licenses expire on October 31 of even-numbered years. Mechanical contractor licenses expire on October 31 of odd-numbered years. Burglar and fire alarm licenses for 2026 to 2028 had a renewal deadline of October 29, 2026.</p>"),
        ("study", "How should you study for an open-book exam?",
         "<ul><li>Get the exact edition of every book on the PSI reference list.</li><li>Tab and highlight the sections that answer most questions, or buy them pre-tabbed.</li><li>Time yourself: the commercial business exam allows about 2.5 minutes per question.</li><li>Take full practice exams in the last 2 weeks.</li></ul><p>Browse the <a href='/licenses/'>license list</a> to find the books for your classification, or read the <a href='/faq/'>FAQ</a>.</p>"),
    ]
    faq = [
        ("How long does it take to get a South Carolina contractor license?", "Most candidates study 4 to 8 weeks, then wait a few weeks for LLR to review the application. RBC candidates also wait for the Exam Eligibility letter before testing."),
        ("How much does a CLB license cost?", "The CLB licensure fee is $350, plus PSI exam fees paid to PSI and the cost of a surety bond or financial statement for your group."),
        ("Is the South Carolina exam hard?", "The exams are open book but timed, so the challenge is finding answers quickly. Tabbed books and practice exams make the biggest difference."),
        ("Do I need experience?", "Yes. Both boards ask for documented experience in the trade; the application lists what counts and who can verify it."),
        ("Can a company hold the license?", "Yes. A CLB license is issued to the business entity, with a qualifying party who passed the exams."),
        ("What is the NASCLA exam?", "The NASCLA Accredited Examination for Commercial General Building is a national exam that South Carolina accepts for an Unlimited Building license."),
        ("Do I need a license for work under $10,000?", "Not a CLB license for commercial work at or under $10,000, but residential work and local rules can still apply. Check with LLR before you bid."),
    ]
    take = ["CLB license required for regulated commercial work over $10,000.", "CLB fee: $350.", "Commercial Business and Law: 50 questions, 125 minutes, 35 to pass.",
            "RBC eligibility letter lasts 1 year.", "GC licenses expire October 31 in even years; MC in odd years."]
    crumbs = [("/", "Home"), (path, "How to get licensed")]
    howto = {"@type": "HowTo", "name": "How to get a South Carolina contractor license", "totalTime": "P8W",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": a, "text": b} for i, (a, b) in enumerate(steps)]}
    return dict(path=path, title=title, desc=desc, h1="How to Get a South Carolina Contractor License", lead=lead, takeaways=take, sections=sections, faq=faq,
                sources=["clb", "clb_lic", "clb_faq", "doc165", "rbc", "rbc_exam", "rbc_lic", "alarm", "code"], crumbs=crumbs, eyebrow="Licensing guide",
                side='<div class="side-box"><p class="side-h">On this page</p><ul class="toc">' + "".join(f'<li><a href="#{sid}">{E(h)}</a></li>' for sid, h, _ in sections) + "</ul></div>",
                ld=[webpage_ld(path, title, desc), howto, crumbs_ld(crumbs), faq_ld(faq)])


def faq_page():
    path = "/faq/"
    title = "South Carolina Contractor Exam FAQ | SC Exam Prep"
    desc = "Answers on South Carolina contractor exams: open book rules, question counts, passing scores, waivers, job limits, shipping and how to order exam prep."
    lead = ("South Carolina contractor exams are open-book PSI tests: the Commercial Business and Law exam has 50 questions in 125 minutes and needs 35 correct, "
            "while the residential version needs a scale score of 68. The answers below cover exams, licenses and ordering from us.")
    sections = [
        ("about-the-exams", "What should you know about the exams?", "<ul><li>PSI gives every CLB and RBC exam at test centers across the state.</li><li>Approved references are allowed in the room, so book editions matter.</li><li>CLB candidates book without pre-approval; RBC candidates need the Exam Eligibility letter.</li><li>RBC candidates get 12 months to pass both parts.</li></ul>"),
        ("about-orders", "How do orders work?", f"<ul><li>Checkout runs on the 1 Exam Prep store.</li><li>Books and tabs ship free by USPS Media Mail inside the US.</li><li>Online courses and services are delivered by email.</li><li>All sales are final, so call {PHONE} if you are unsure.</li></ul>"),
        ("which-license", "Which license do you need?",
         "<p>The value and type of the work decide it. Regulated commercial work over $10,000 needs a Contractor's Licensing Board license in the right classification, such as Building, Roofing or Plumbing. "
         "Work on homes needs a Residential Builders Commission license: Residential Builder for general building and remodeling, or Residential Electrical, HVAC or Plumbing for those trades. "
         "Individual journeyman and master electricians and journeyman plumbers get their cards from the city or county where they work. "
         "Alarm businesses are licensed by the CLB under the Alarm System Business Act, with a Fire Alarm exam and an Alarm Code of Laws exam. "
         "The <a href='/licenses/'>license list</a> groups all 33 licenses we cover by board.</p>"),
        ("study-time", "How long should you study?",
         "<p>Most candidates need 4 to 8 weeks. Plan for more if you work full time or if you are taking a trade exam and Business and Law in the same month. "
         "A good split is 2 weeks learning the layout of each reference book, 2 to 4 weeks of practice questions, and a final 1 to 2 weeks of timed full-length exams. "
         "Because every South Carolina contractor exam is open book, the goal is fast lookups rather than memorizing. "
         "On the commercial Business and Law exam you have about 2.5 minutes per question, which is why pre-printed tabs and highlighted books are popular. "
         "Read the <a href='/how-to-get-licensed/'>licensing guide</a> for the full process.</p>"),
        ("still-stuck", "Can't find your answer?", f"<p>Call <a href='tel:{TEL}'>{PHONE}</a> or email <a href='mailto:{EMAIL}'>{EMAIL}</a>. You can also browse the <a href='/licenses/'>license pages</a> or the <a href='/how-to-get-licensed/'>licensing guide</a>.</p>"),
    ]
    faq = [
        ("Are South Carolina contractor exams open book?", "Yes. The CLB and RBC trade exams and both Business and Law exams allow the approved reference books."),
        ("How many questions are on the Commercial Business and Law exam?", "50 questions with a 125-minute limit; 35 correct answers pass."),
        ("What score passes the Residential Business and Law exam?", "A scale score of 68 is required."),
        ("Who needs a CLB license?", "Anyone performing regulated commercial general or mechanical work where the total cost is over $10,000."),
        ("How long is the RBC Exam Eligibility letter valid?", "1 year from the date it is issued. You must pass both exam parts within that time or reapply."),
        ("Does South Carolina accept the NASCLA exam?", "Yes, for the Unlimited Building classification, and a NASCLA pass within 3 years waives the Residential Builder trade exam."),
        ("How much is shipping?", "Free for books and tabs by USPS Media Mail to US addresses."),
        ("Can I return books?", f'No. All sales are final under the <a href="{REFUND}" rel="noopener">1 Exam Prep refund policy</a>.'),
        ("Do you help with the LLR application?", "Yes. The License Application Service and The 1 Package include application help and business formation."),
        ("How do I reach a person?", f'Call <a href="tel:{TEL}">{PHONE}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>.'),
    ]
    take = ["All CLB and RBC exams are open book.", "Commercial Business and Law: 50 questions, 125 minutes, 35 to pass.", "Residential Business and Law: scale score 68.", "Free USPS Media Mail on books."]
    crumbs = [("/", "Home"), (path, "FAQ")]
    return dict(path=path, title=title, desc=desc, h1="South Carolina Contractor Exam FAQ", lead=lead, takeaways=take, sections=sections, faq=faq,
                sources=["clb_lic", "rbc_exam", "psi_clb", "psi_rbc", "clb_faq"], crumbs=crumbs, eyebrow="FAQ",
                ld=[webpage_ld(path, title, desc), crumbs_ld(crumbs), faq_ld(faq)])


def contact_page():
    path = "/contact/"
    title = "Contact Pass Your SC Exam | Call (877) 775-9400"
    desc = "Call (877) 775-9400 or email sales@1examprep.com for help choosing South Carolina contractor exam books, courses and licensing services."
    lead = (f"The fastest way to reach us is by phone at {PHONE}. You can also email {EMAIL} or send the form below. Tell us your South Carolina license, "
            "your exam date and how you like to study, and we will point you to the right package, usually the same business day.")
    form = f'''<div class="form-wrap" id="contact-form" data-form="{FORM_ID}" data-source="passyoursouthcarolinacontractorexam.com"><p>The contact form loads here. If it does not appear, call <a href="tel:{TEL}">{PHONE}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>'''
    cards = f'''<div class="contact-cards"><a class="cc" href="tel:{TEL}"><span>Call</span><b>{PHONE}</b></a><a class="cc" href="mailto:{EMAIL}"><span>Email</span><b>{EMAIL}</b></a><a class="cc" href="/licenses/"><span>Browse</span><b>All licenses</b></a></div>'''
    sections = [
        ("reach-us", "How can you reach us?", cards + f"<p>Phone and email reach the same 1 Exam Prep team that ships the books. Calls get the quickest answer, and email works well when you want a written list of what to buy.</p>"),
        ("form", "Send a message", form),
        ("what-to-include", "What should you include in your message?", "<ul><li>The license or classification you are going for, for example Roofing or Residential Builder.</li><li>Your exam date, or how many weeks you have to study.</li><li>Whether you already own any of the reference books.</li><li>If you want help with the LLR application or forming an LLC.</li></ul><p>With those 4 details we can usually recommend one package and tell you what it costs.</p>"),
        ("orders", "Need help with an order?", f"<p>Include your order number and the email used at checkout. Books ship free by USPS Media Mail, which usually takes 2 to 8 business days. Online courses arrive by email after checkout, so check your spam folder before calling.</p>"),
        ("what-we-help-with", "What can the team help you with?",
         "<p>Most calls fall into one of five areas. Bring any of them to the phone or put them in an email.</p><ul>"
         "<li><b>Choosing books.</b> We match your classification to the PSI reference list, including the exact editions allowed in the testing room.</li>"
         "<li><b>Tabs and highlighting.</b> We explain what the pre-printed tabs cover and when a highlighted and tabbed set is worth the extra cost.</li>"
         "<li><b>Courses and live classes.</b> We compare the online course, the live virtual training and the rental packages for your schedule.</li>"
         "<li><b>The LLR application.</b> The License Application Service and the LLC setup take the paperwork off your hands.</li>"
         "<li><b>Company orders.</b> We quote books for several qualifiers or several classifications at once.</li></ul>"),
        ("before-you-call", "What happens after you get in touch?",
         f"<p>A member of the 1 Exam Prep team reads every message and replies by phone or email, whichever you prefer. "
         f"For product questions we usually send a short list: the package we recommend, its price and what is in the box. "
         f"When you are ready, the Buy now button on any product page opens checkout with that item already in the cart. "
         f"Licensing questions about eligibility or experience are decided by LLR, so we point you to the right board page when that is the real question. "
         f"Exam scheduling is handled by PSI. You can see both boards' official pages in the sources list below.</p>"),
    ]
    faq = [
        ("What is your phone number?", f"Call {PHONE}. The same number handles product questions and order help."),
        ("What is your email address?", f"Email {EMAIL} for quotes, product lists and order questions."),
        ("How fast do you reply?", "Most emails and form messages get a reply the same business day."),
        ("Can you tell me which books my exam needs?", "Yes. Give us the license and we will match it to the PSI reference list."),
        ("Do you offer group or company orders?", "Yes. Contact us with the number of candidates and licenses, and we will put together a quote."),
        ("Are you part of LLR or PSI?", "No. We are an independent exam prep provider. Licensing decisions are made by LLR, and PSI runs the exams."),
    ]
    take = [f"Phone: {PHONE}.", f"Email: {EMAIL}.", "Most messages answered the same business day.", "Include your license and exam date."]
    crumbs = [("/", "Home"), (path, "Contact")]
    cp = webpage_ld(path, title, desc, "ContactPage"); cp["mainEntity"] = {"@id": SITE + "/#org"}
    return dict(path=path, title=title, desc=desc, h1="Contact Us", lead=lead, takeaways=take, sections=sections, faq=faq,
                sources=["clb", "rbc"], crumbs=crumbs, eyebrow="Contact",
                ld=[cp, ld_org(), crumbs_ld(crumbs), faq_ld(faq)])


def reviews_page():
    sys.path.insert(0, os.path.join(ROOT, "tools")); import reviewskit as rk
    c = rk.content(BRAND, "South Carolina contractor exam", PHONE, TEL, EMAIL)
    for k, (name, url) in zip(("rev_sa", "rev_gpolicy"), c["sources"]):
        SRC[k] = (name, url)
    path = rk.PATH
    crumbs = [("/", "Home"), (path, "Reviews")]
    return dict(path=path, title=c["title"], desc=c["desc"], h1=c["h1"], lead=c["lead"], takeaways=c["takeaways"], sections=c["sections"],
                faq=c["faq"], sources=["rev_sa", "rev_gpolicy"], sources_note="Review sources and the rules they follow.", crumbs=crumbs, eyebrow="Reviews",
                ld=[rk.page_ld(SITE, c["title"], c["desc"], CHECKED, SITE + "/#org"), crumbs_ld(crumbs), faq_ld(c["faq"])])


# ---------------------------------------------------------------- blog
def nice_date(d):
    import datetime
    return datetime.date.fromisoformat(d).strftime("%B %-d, %Y")


def post_page(post):
    path = f"/blog/{post['slug']}/"
    crumbs = [("/", "Home"), ("/blog/", "Blog"), (path, post["title"])]
    byline = (f'<div class="post-meta">By <span class="author">{AUTHOR}</span> · Published <time datetime="{post["date"]}">{nice_date(post["date"])}</time>'
              f' · Updated <time datetime="{post["updated"]}">{nice_date(post["updated"])}</time></div>')
    words = sum(wc(b) for _, _, b in post["sections"])
    art = {"@type": "BlogPosting", "@id": SITE + path + "#post", "headline": post["title"], "url": SITE + path, "mainEntityOfPage": SITE + path,
           "description": post["meta_desc"], "image": SITE + "/assets/img/og.jpg", "datePublished": post["date"], "dateModified": post["updated"],
           "author": {"@type": "Person", "name": AUTHOR}, "publisher": publisher(), "inLanguage": "en-US", "keywords": ", ".join(post["tags"]),
           "articleSection": "South Carolina contractor licensing", "wordCount": words, "isPartOf": {"@id": SITE + "/blog/#blog"}}
    others = [x for x in POSTS if x is not post]
    related = "".join(f'<li><a href="/blog/{x["slug"]}/">{E(x["title"])}</a></li>' for x in others)
    side = ('<div class="side-box"><p class="side-h">In this post</p><ul class="toc">' + "".join(f'<li><a href="#{sid}">{E(h)}</a></li>' for sid, h, _ in post["sections"]) + "</ul></div>"
            + (f'<div class="side-box"><p class="side-h">More from the blog</p><ul class="toc">{related}</ul></div>' if related else ""))
    return dict(path=path, title=post["meta_title"], desc=post["meta_desc"], h1=post["title"], lead=E(post["lead"]), takeaways=post["takeaways"],
                sections=post["sections"], faq=post["faq"], sources=post["sources"], crumbs=crumbs, eyebrow="Blog · " + post["tags"][0],
                byline=byline, side=side, article=True, ld=[art, crumbs_ld(crumbs), faq_ld(post["faq"])])


def post_card(x):
    return (f'<li class="post-card"><p class="post-tag">{E(x["tags"][0])}</p><h3 id="post-{x["slug"]}"><a href="/blog/{x["slug"]}/">{E(x["title"])}</a></h3>'
            f'<p>{E(x["excerpt"])}</p><p class="post-by">By {AUTHOR} · <time datetime="{x["date"]}">{nice_date(x["date"])}</time></p>'
            f'<a class="more" href="/blog/{x["slug"]}/">Read the answers</a></li>')


def blog_index():
    path = "/blog/"
    title = "South Carolina Contractor Exam Blog | Pass Your SC Exam"
    desc = "Plain-English guides to South Carolina contractor licensing: CLB and Residential Builders rules, PSI exams, study plans and costs. Checked against LLR."
    lead = ("The Pass Your SC Exam blog answers the questions South Carolina contractors ask before they test: which board licenses them, what the PSI exams cover, "
            "how long to study and what it costs. Every post is checked against LLR and PSI and dated, so you know the facts are current.")
    cards = "".join(post_card(x) for x in POSTS)
    latest = POSTS[0]
    n = len(POSTS)
    sections = [
        ("latest-posts", "What are the latest posts?", f'<p>{n} post{"s" if n != 1 else ""} so far, newest first. Each one opens with a short answer, then goes question by question with tables, a FAQ and a list of official sources.</p><ul class="post-list">{cards}</ul>'),
        ("start-here", "Where should a new candidate start?",
         "<p>Start with the board, because everything else follows from it. Commercial work over $10,000 means the Contractor's Licensing Board. Home building over $5,000 means the Residential Builders Commission. "
         f"Then read <a href='/blog/{latest['slug']}/'>{E(latest['title'])}</a> for the 15 questions most people ask, and the <a href='/how-to-get-licensed/'>licensing guide</a> for the step-by-step process. "
         "When you know your classification, its <a href='/licenses/'>license page</a> lists the exams, the job limits and every book and course we carry for it.</p>"
         "<ol><li>Decide between CLB and RBC by the type and value of your work.</li><li>Pick the classification, such as Roofing or Residential Builder.</li>"
         "<li>Check the PSI bulletin for the book list and editions.</li><li>Get the books 4 to 8 weeks before your exam date.</li><li>Tab, practice and take 2 timed exams before test day.</li></ol>"),
        ("topics", "What does the blog cover?",
         "<ul><li><b>Licensing rules:</b> the $10,000 CLB threshold, the $5,000 and $500 residential thresholds, license groups and renewal dates.</li>"
         "<li><b>The exams:</b> the Commercial Business and Law exam (50 questions, 125 minutes, 35 to pass), the residential version (scale score 68) and the trade exams.</li>"
         "<li><b>Studying:</b> how to tab and highlight books for an open-book test, and how long to plan for.</li>"
         "<li><b>Costs:</b> the $350 CLB fee, PSI exam fees, bonds and study materials.</li>"
         "<li><b>After the exam:</b> applications, financial statements, business setup and renewals.</li></ul>"),
        ("how-we-check", "How are the facts checked?",
         "<p>Every number in a post comes from an official source: the LLR pages for the Contractor's Licensing Board and the Residential Builders Commission, the PSI candidate bulletins, "
         "or the South Carolina Code of Laws, Title 40 Chapters 11 and 59. Each post links its sources at the bottom and shows the date it was last updated. "
         "When the rules change, such as the 2023 move of the CLB threshold from $5,000 to $10,000 or the 2025 Nonstructural Renovation exam, the affected posts are updated and re-dated. "
         f"Spot something out of date? Email {EMAIL} and we will fix it.</p>"),
        ("who-writes", "Who writes the posts?",
         f"<p>Posts are written by {AUTHOR} for 1 Exam Prep, which supplies exam prep books, tabs and courses to contractors across the country. "
         f"The team behind the blog also answers the phone at {PHONE}, so the questions in each post are the ones contractors actually ask us. "
         "Posts stay practical: what the rule is, what it means for your next job, and what to study. Licensing decisions belong to LLR, and the posts say so when a question needs an official answer.</p>"),
        ("study-plan", "How long should you study for a South Carolina exam?",
         "<p>Most candidates need 4 to 8 weeks. A simple plan that works for both CLB and RBC exams:</p>"
         "<table><thead><tr><th>Week</th><th>Focus</th></tr></thead><tbody><tr><td>1 to 2</td><td>Learn the layout of each reference book; place tabs.</td></tr>"
         "<tr><td>3 to 5</td><td>Practice questions by topic; highlight the answers you look up.</td></tr><tr><td>6</td><td>Business and Law practice: about 2.5 minutes per question.</td></tr>"
         "<tr><td>7 to 8</td><td>2 or more full timed practice exams, then review misses.</td></tr></tbody></table>"
         "<p>Candidates with less time often choose highlighted and tabbed book sets or a live virtual class to shorten weeks 1 and 2.</p>"),
        ("recent-changes", "What changed in South Carolina licensing recently?",
         "<ul><li><b>May 2022:</b> the residential specialty registration threshold rose from $200 to $500 per job.</li>"
         "<li><b>May 19, 2023:</b> the CLB commercial threshold rose from $5,000 to $10,000 under Act 69.</li>"
         "<li><b>January 1, 2025:</b> the Nonstructural Renovation classification began requiring a PSI technical exam.</li>"
         "<li><b>October 29, 2026:</b> the renewal deadline for 2026 to 2028 burglar and fire alarm contractor licenses.</li></ul>"
         "<p>Changes like these are why every post carries an updated date. Before you bid near a limit or book an exam, check the date on the post and the linked LLR page.</p>"),
        ("popular-licenses", "Which licenses do readers ask about most?",
         "<p>Five licenses account for most of the questions we get from South Carolina contractors. Each link goes to the license page with its exams, limits and study packages.</p><ul>"
         + "".join(f"<li><a href='/{l}/'>{E(BY_SLUG[l]['name'])}</a>: {E(BY_SLUG[l]['scope'])}</li>" for l in ("residential-builder", "commercial-general-building", "roofing", "commercial-business-law", "residential-hvac"))
         + "</ul>"),
    ]
    faq = [
        ("How often is the blog updated?", "Posts are reviewed when LLR or PSI changes a rule, fee or exam, and each post shows its last updated date."),
        ("Who is the author?", f"Posts are written by {AUTHOR} for 1 Exam Prep and checked against LLR and PSI sources."),
        ("Can I suggest a topic?", f"Yes. Email {EMAIL} with your question and it may become the next post."),
        ("Is the blog official licensing advice?", "No. The blog explains the rules in plain English. LLR makes licensing decisions, and PSI runs the exams."),
        ("Where are the exam books?", "Every license page lists the books, tabs and courses for that exam, with free USPS Media Mail shipping on books."),
        ("How do I get help choosing a package?", f"Call {PHONE} or use the contact page, and tell us your license and exam date."),
    ]
    take = [f"{n} post{'s' if n != 1 else ''}, written by {AUTHOR} and checked against LLR and PSI.", "Start with the board: CLB for commercial work over $10,000, RBC for homes.",
            "Most candidates study 4 to 8 weeks.", "Every post lists its official sources and update date."]
    crumbs = [("/", "Home"), (path, "Blog")]
    blog_ld = {"@type": "Blog", "@id": SITE + "/blog/#blog", "url": SITE + path, "name": "Pass Your SC Exam blog", "description": desc, "publisher": publisher(), "inLanguage": "en-US",
               "blogPost": [{"@type": "BlogPosting", "headline": x["title"], "url": f"{SITE}/blog/{x['slug']}/", "datePublished": x["date"], "dateModified": x["updated"],
                             "author": {"@type": "Person", "name": AUTHOR}} for x in POSTS]}
    il = {"@type": "ItemList", "name": "Blog posts", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/blog/{x['slug']}/", "name": x["title"]} for i, x in enumerate(POSTS)]}
    pop = ("residential-builder", "commercial-general-building", "roofing", "commercial-business-law", "residential-hvac")
    side = '<div class="side-box"><p class="side-h">Popular licenses</p><ul class="toc">' + "".join(f'<li><a href="/{l}/">{E(BY_SLUG[l]["name"])}</a></li>' for l in pop) + "</ul></div>"
    return dict(path=path, title=title, desc=desc, h1="South Carolina Contractor Exam Blog", lead=lead, takeaways=take, sections=sections, faq=faq,
                sources=["clb", "rbc", "rbc_exam", "psi_clb", "psi_rbc", "code11", "code59"], crumbs=crumbs, eyebrow="Blog", side=side,
                ld=[blog_ld, webpage_ld(path, title, desc, "CollectionPage"), il, crumbs_ld(crumbs), faq_ld(faq)])


# ---------------------------------------------------------------- build
def main():
    # remove only what the last build wrote, never the source or .git
    if os.path.exists(MANIFEST):
        for f in json.load(open(MANIFEST)):
            fp = os.path.join(OUT, f)
            if os.path.isfile(fp):
                os.remove(fp)
    os.makedirs(OUT, exist_ok=True)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"), dirs_exist_ok=True)
    prods = load_products()
    by = defaultdict(list)
    for p in prods:
        by[p["lic"]].append(p)
    counts = {l["slug"]: len(by[l["slug"]]) for l in LICENSES}
    prices = {l["slug"]: min(x["price"] for x in by[l["slug"]]) for l in LICENSES}
    pages = [home_page(counts, prices, len(prods)), licenses_index(counts, prices, len(prods)), guide_page(), faq_page(), contact_page(), reviews_page(), blog_index()] + [post_page(x) for x in POSTS]
    for l in LICENSES:
        pages.append(license_page(l, by[l["slug"]]))
    taken = set(p["title"] for p in pages)
    for l in LICENSES:
        for p in by[l["slug"]]:
            pages.append(product_page(p, l, by[l["slug"]], taken))
    for pg in pages:
        write(pg["path"], render(pg))
    # 404
    nf = dict(path="/404.html", title="Page Not Found | Pass Your SC Exam", desc="That page moved or never existed. Browse South Carolina contractor licenses or call (877) 775-9400 for help.",
              ld=[], h1="Page not found")
    write("/404.html", head(nf).replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">') + header() +
          f'<main id="main" class="wrap single nf"><h1>Page not found</h1><p class="lead">That page moved or never existed. Try the <a href="/licenses/">license list</a>, the <a href="/faq/">FAQ</a> or call <a href="tel:{TEL}">{PHONE}</a>.</p></main>' + footer())
    # sitemap, robots, llms, agents
    urls = "".join(f"<url><loc>{SITE}{pg['path']}</loc><lastmod>{CHECKED}</lastmod></url>" for pg in pages)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    open(os.path.join(OUT, "robots.txt"), "w").write(
        "User-agent: *\nAllow: /\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in ("GPTBot", "ClaudeBot", "Google-Extended", "PerplexityBot", "Bingbot")) + f"Sitemap: {SITE}/sitemap.xml\n")
    lic_lines = "\n".join(f"- [{l['name']}]({SITE}/{l['slug']}/): {counts[l['slug']]} packages from {money(prices[l['slug']])}. {l['scope']}" for l in LICENSES)
    blog_lines = "\n".join(f"- [{x['title']}]({SITE}/blog/{x['slug']}/): {x['excerpt']}" for x in POSTS)
    llms = f"""# {BRAND}

> Exam prep books, pre-printed tabs, online courses, live classes and licensing services for South Carolina contractor exams (Contractor's Licensing Board, Residential Builders Commission and local electrician and plumber cards). {len(prods)} products for {len(LICENSES)} licenses, fulfilled by 1 Exam Prep. Contact: {PHONE}, {EMAIL}.

## Key facts (checked {CHECKED_TEXT})
- CLB license required for regulated commercial work over $10,000; fee $350.
- Commercial Business and Law exam: 50 questions, 125 minutes, 35 correct to pass, open book.
- Residential Business and Law exam: scale score 68.
- RBC Exam Eligibility letter valid 1 year.
- Books ship free by USPS Media Mail (US only). All sales final.

## Main pages
- [Home]({SITE}/)
- [All licenses]({SITE}/licenses/)
- [How to get a South Carolina contractor license]({SITE}/how-to-get-licensed/)
- [FAQ]({SITE}/faq/)
- [Contact]({SITE}/contact/)
- [Customer reviews]({SITE}/reviews/)
- [Blog]({SITE}/blog/)
{blog_lines}

## Licenses
{lic_lines}
"""
    open(os.path.join(OUT, "llms.txt"), "w").write(llms)
    open(os.path.join(OUT, "agents.md"), "w").write(llms.replace(f"# {BRAND}", f"# {BRAND}: agent guide") + f"\n## Buying\nEach product page has a Buy now link to {CART.format('<variant-id>')} on the 1 Exam Prep store. Product pages carry Product JSON-LD with price, availability, shipping and return policy.\n")
    open(os.path.join(OUT, "CNAME"), "w").write("passyoursouthcarolinacontractorexam.com\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    made = []
    for d, dirs, fs in os.walk(OUT):
        dirs[:] = [x for x in dirs if x not in (".git", "source")]
        for f in fs:
            r = os.path.relpath(os.path.join(d, f), OUT)
            if r not in (".build-manifest.json", "README.md"):
                made.append(r)
    json.dump(sorted(made), open(MANIFEST, "w"), indent=0)
    print(f"built {len(pages)} pages ({len(prods)} products, {len(LICENSES)} licenses) into {OUT}")


if __name__ == "__main__":
    main()
