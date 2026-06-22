# Elevate Views

Premium systems & automation agency site. Brand position: **we build the operational systems
businesses run on** (ordering, stock, forecasting, automation), not commodity "AI websites".
Concept: **Slate & Signal** (graphite + signal-blue, Inter Tight + Space Mono, structural grid).

## Stack
Vanilla HTML/CSS/JS, no build step. Deploy: GitHub repo + Vercel (root = this folder).

## Structure
- `index.html` — home (hero, services, **systems gallery**, worked example, process, sectors, FAQ, contact)
- `services/` — 4 service pages + index (each targets its own keyword set)
- `sectors/` — 7 industry verticals + index (each targets sector keywords)
- `resources/` — blog shell (3 placeholder articles, ready for content)
- `css/styles.css`, `js/main.js` — shared across all pages
- `_gen.py` — one-shot generator that stamped services/* and sectors/* from data. Edit data + re-run to update.
- `keyword-map.md` — per-page keyword + difficulty plan and content backlog
- `gen-images.sh` — generates the 4 system-mockup images via mediagen (needs FAL_KEY)
- `sitemap.xml`, `robots.txt`, `favicon.svg`, `vercel.json`

## To do before going live
1. **Formspree:** replace `your-form-id` in every form `action` with a real Formspree ID.
2. **System images:** add FAL_KEY to `_shared/mediagen/.env`, run `bash gen-images.sh`, then swap the
   4 `.gallery__shot` placeholder blocks in `index.html` for `<img>` tags.
3. **Hero images:** the two Picsum images are placeholders; swap for real/branded assets.
4. **Domain:** point elevateviews.co.uk at the Vercel deploy.

## Preview locally
```bash
python -m http.server 8000   # from this folder, then open http://localhost:8000/
```

## Editing service/sector pages
Edit the data dicts in `_gen.py` and re-run `python _gen.py`. Do not hand-edit the generated
`services/*.html` / `sectors/*.html` (they get overwritten). The home, resources and index pages are
hand-maintained.
