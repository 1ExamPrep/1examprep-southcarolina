#!/usr/bin/env python3
"""Grade every built page against 'What every page and post needs to pass'.
python3 tools/check_pages.py [site-dir] [-v]
"""
import json, os, re, sys
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DIR = next((a for a in sys.argv[1:] if not a.startswith("-")), os.path.join(ROOT, "site"))
VERBOSE = "-v" in sys.argv
DOMAIN = "https://passyoursouthcarolinacontractorexam.com"
PHONES = {"8777759400"}; EMAILS = {"sales@1examprep.com"}
COMPETITORS = ["examprep.org", "rocketcert.com", "contractorsintelligence", "atlanticbuilders"]
BAD_OPEN = re.compile(r"^(in today'?s|in this (article|post|guide)|welcome to|we all know|have you ever|when it comes to|it'?s no secret|in the ever|as the industry)", re.I)
BACKREF = re.compile(r"^(this|that|these|those|it|they|he|she|such|here|above|below|as mentioned|as noted|as discussed|as we saw)\b", re.I)
FIG = re.compile(r"(\$[\d,]+(\.\d+)?|\b\d[\d,]*(\.\d+)?\s?(%|percent)?|\b(19|20)\d\d\b)")


def words(t):
    return re.findall(r"[A-Za-z0-9$][\w$,.'%-]*", t)


def check(path):
    s = open(path, encoding="utf-8").read()
    soup = BeautifulSoup(s, "html.parser")
    rel = "/" + os.path.relpath(path, SITE_DIR).replace("index.html", "")
    must, opp = [], []
    # --- schema
    types = set(); lds = []
    for sc in soup.find_all("script", type="application/ld+json"):
        try:
            d = json.loads(sc.string); lds.append(d)
            t = d.get("@type"); types.update(t if isinstance(t, list) else [t])
        except Exception as e:
            must.append(f"JSON-LD does not parse: {e}")
    if not lds:
        must.append("no JSON-LD")
    if "Product" in types or "/product/" in rel:
        ptype, target, fail = "product", 300, 180
    elif "CollectionPage" in types or "ItemList" in types and "/collection" in rel:
        ptype, target, fail = "collection", 200, 120
    elif any(t in types for t in ("Article", "BlogPosting", "NewsArticle")) or "/blog/" in rel:
        ptype, target, fail = "article", 1200, 720
    else:
        ptype, target, fail = "page", 700, 420
    expect = {"product": {"Product"}, "collection": {"CollectionPage", "ItemList"}, "article": {"Article", "BlogPosting", "NewsArticle"}, "page": {"WebPage", "Article", "Service", "FAQPage", "ContactPage", "ItemPage", "CollectionPage"}}[ptype]
    if not types & expect:
        opp.append(f"schema type does not match {ptype}")
    # --- head
    title = (soup.title.string or "").strip() if soup.title else ""
    if not title: must.append("no title")
    elif not 30 <= len(title) <= 60: opp.append(f"title length {len(title)}")
    md = soup.find("meta", attrs={"name": "description"})
    if not md: must.append("no meta description")
    elif not 70 <= len(md["content"]) <= 160: opp.append(f"description length {len(md['content'])}")
    can = soup.find("link", rel="canonical")
    if not can: must.append("no canonical")
    elif can["href"] != DOMAIN + rel: opp.append(f"canonical {can['href']} != {DOMAIN + rel}")
    if not soup.find("meta", property="og:title") or not soup.find("meta", property="og:image"): opp.append("og tags")
    rob = soup.find("meta", attrs={"name": "robots"})
    if rob and "noindex" in rob["content"]: must.append("noindex")
    if not soup.html.get("lang"): opp.append("no html lang")
    # --- body
    main = soup.find("main")
    body = soup.body
    h1s = body.find_all("h1")
    if len(h1s) != 1: must.append(f"{len(h1s)} H1")
    text = main.get_text(" ", strip=True)
    n = len(words(text))
    if n < fail: must.append(f"{n} words (< {fail} for {ptype})")
    elif n < target: opp.append(f"{n} words (< {target} for {ptype})")
    if n < 150: must.append("under 150 words of text in HTML")
    # opening paragraph
    lead = main.find("p", class_="lead") or main.find("p")
    lw = len(words(lead.get_text(" ", strip=True))) if lead else 0
    if not lead or BAD_OPEN.match(lead.get_text(strip=True)): must.append("opening paragraph warm-up or missing")
    elif not 40 <= lw <= 60:
        (must if lw < 40 else opp).append(f"opening paragraph {lw} words")
    # headings
    hs = main.find_all(re.compile("^h[1-6]$"))
    h2 = [h for h in hs if h.name == "h2"]
    if n > 300 and len(h2) < 3: must.append(f"only {len(h2)} H2")
    last = 1
    for h in hs:
        lv = int(h.name[1])
        if lv > last + 1: must.append(f"skipped heading level {h.name} after h{last}: {h.get_text(strip=True)[:40]}")
        last = lv
    q = [h for h in hs if h.get_text(strip=True).endswith("?")]
    if len(hs) >= 2 and len(q) < 2: opp.append(f"{len(q)} question headings")
    h23 = [h for h in hs if h.name in ("h2", "h3")]
    if h23 and sum(1 for h in h23 if h.get("id")) / len(h23) < .7: opp.append("ids on < 70% of H2/H3")
    # sections: text between consecutive headings
    secs = []
    for i, h in enumerate(hs):
        if h.name == "h1": continue
        chunk = []
        for el in h.next_elements:
            if el is not h and getattr(el, "name", None) and re.match("^h[1-6]$", el.name): break
            if isinstance(el, str) and el.parent is not h and not el.parent.name == "script": chunk.append(el)
        t = " ".join(x.strip() for x in chunk if x.strip())
        secs.append((h.get_text(strip=True), t))
        if BACKREF.match(t): must.append(f"section opens with back-reference: {h.get_text(strip=True)[:40]} -> {t[:30]}")
    wcs = [len(words(t)) for _, t in secs]
    long = [(a, w) for (a, _), w in zip(secs, wcs) if w > 400]
    for a, w in long: opp.append(f"section over 400 words: {a[:40]} ({w})")
    thin = [w for w in wcs if w < 40]
    if secs and len(thin) > len(secs) / 2: must.append(f"{len(thin)} of {len(secs)} sections under 40 words")
    # sentences
    sents = [x for x in re.split(r"(?<=[.!?])\s+", text) if len(x.split()) > 2]
    if sents and sum(len(x.split()) for x in sents) / len(sents) >= 26: opp.append("average sentence >= 26 words")
    # figures
    if n >= 200 and len(FIG.findall(text)) < n / 100: opp.append(f"figures {len(FIG.findall(text))} for {n} words")
    if not main.find(["ul", "ol", "table", "dl"]): opp.append("no list or table")
    faqdl = main.select(".faq dt")
    if not (6 <= len(faqdl) <= 10): must.append(f"FAQ has {len(faqdl)} questions")
    if faqdl and "FAQPage" not in types: opp.append("FAQ not in FAQPage schema")
    if not ("dateModified" in s or main.find(class_="updated")): opp.append("no date")
    # links
    links = body.find_all("a")
    internal = [a for a in links if a.get("href", "").startswith("/") or a.get("href", "").startswith(DOMAIN)]
    outbound = [a for a in main.find_all("a") if a.get("href", "").startswith("http") and DOMAIN not in a["href"] and "1examprep.com" not in a["href"]]
    if len(internal) < 3: opp.append("fewer than 3 internal links")
    if n > 300 and not outbound: opp.append("no outbound citation")
    for a in links:
        h = a.get("href")
        if h is None or h.strip() in ("", "#") or h.startswith("javascript:"): must.append(f"dead or js link: {a}")
        if any(c in (h or "") for c in COMPETITORS): must.append(f"competitor link {h}")
    for im in soup.find_all("img"):
        if not im.get("alt"): opp.append(f"img without alt {im.get('src')}")
    # pre-publish blockers
    if re.search(r"\{\{|\[INSERT|\[YOUR|\[TODO|\bTODO\b|FIXME|\bXXX\b|lorem ipsum|your business name|company name here", text, re.I): must.append("placeholder text")
    if re.search(r"(^|\s)(#{2,} |\*\*\w)", text): must.append("raw markdown")
    for sc in body.find_all("script"): must.append("script tag in body")
    if re.search(r"\son[a-z]+=", str(body)): must.append("inline handler")
    if body.find("iframe"): must.append("iframe")
    for m in re.findall(r"\(?\b(\d{3})\)?[\s.-]?(\d{3})-(\d{4})\b", body.get_text(" ")):
        if "".join(m) not in PHONES: must.append(f"phone {''.join(m)}")
    for m in [x.rstrip(".") for x in re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", body.get_text(" "))]:
        if m not in EMAILS: must.append(f"email {m}")
    return rel, ptype, n, must, opp


def main():
    res = []
    for d, _, fs in os.walk(SITE_DIR):
        for f in fs:
            if f == "index.html":
                res.append(check(os.path.join(d, f)))
    bad = [r for r in res if r[3]]
    opps = [r for r in res if r[4]]
    for rel, t, n, must, opp in sorted(res):
        if must or (VERBOSE and opp):
            print(f"{rel} [{t}, {n} words]")
            for m in must: print("   MUST:", m)
            for o in opp: print("   opp: ", o)
    from collections import Counter
    c = Counter(re.sub(r"[\d:].*", "", o) for r in res for o in r[4])
    print(f"\n{len(res)} pages, {len(res) - len(bad)} pass every must-have, {len(opps)} with opportunities")
    if c: print("opportunity counts:", dict(c))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
