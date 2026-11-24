# Pass Your South Carolina Contractor Exam

Static site for https://passyoursouthcarolinacontractorexam.com, served by GitHub Pages from `main`, `/ (root)`.

- `source/` holds the generator. Everything else at the root is build output.
- Rebuild: `cd source && python3 build.py` (writes the pages into the repo root and deletes only what the last build wrote, listed in `.build-manifest.json`).
- Check: `python3 tools/check_pages.py ..` grades every page against the SEO checklist.
- Products: `source/data/products-raw.json`, pulled from Shopify (titles containing "South Carolina").
- Copy, licenses and facts: `source/tools/sccopy.py`. Hero image: `source/assets/img/hero.*`.

Contact on the site: (877) 775-9400, sales@1examprep.com.
