# Finiteck website

The official static website for [Finiteck](https://finiteck.com), a personal money-saving assistant for iPhone and iPad. Hosted on GitHub Pages using the existing `CNAME` and `main` branch.

## Local preview

No framework, package manager, or installation is required.

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Open `http://127.0.0.1:4173`. Serve the repository root; shared links and assets use root-relative paths.

## Editing and validation

Edit HTML directly. Edit styles in `css/style.css`, then regenerate the checked-in browser bundle:

```sh
python3 scripts/build_css.py
python3 scripts/build_sitemap.py
python3 scripts/check_site.py
node --check js/site.js
```

The site checker uses only Python's standard library. It validates all content pages, internal assets and links, fragment destinations, heading/main structure, image alt attributes, metadata, JSON-LD, and sitemap destinations. Node is needed only for the optional JavaScript syntax check.

The visual and product decisions are documented in `DESIGN.md` and `PRODUCT.md`. The redesign and verification record is in `docs/REDESIGN-2026-10-09.md`.

## Structure

- `index.html`: product introduction, real app screenshots, screen selector, recurring-cost calculator, pricing, resources, and FAQ.
- `guides.html`: French practical-guide library.
- `guide-*.html`: existing guides with readable article layout and desktop contents navigation.
- `blog/index.html`: French journal, including accent-insensitive search and category filters.
- `blog/*.html`: existing articles; public URLs are preserved.
- `support.html`: support answers and a direct email link.
- `privacy.html`, `terms.html`, `risk.html`: existing legal content with the shared visual system.
- `404.html`: branded GitHub Pages error page.
- `css/style.css`, `css/style.min.css`: source stylesheet and generated bundle.
- `js/site.js`: progressive enhancements; no dependencies.
- `fonts/`: locally served Manrope files and SIL Open Font License.
- `images/`: original branding and screenshots from the public App Store listing. See `images/SOURCES.md`.

## Behaviour and privacy

Navigation, article content, FAQ, pricing, and App Store links work without JavaScript. The app screen selector and calculator are enabled when JavaScript loads. Journal search is revealed only when available; otherwise all articles remain visible.

Calculator inputs and journal searches stay in memory in the browser. They are not submitted, stored in cookies or local storage, or sent to analytics. The pre-existing Plausible script remains on the pages that already used it. Fonts and all product/editorial images are served locally. Existing article illustrations were copied from their published sources and optimized as WebP; provenance is recorded in `images/articles/sources.json`.

## Search and media

`sitemap.xml` includes 35 canonical pages and 79 image references. `scripts/build_sitemap.py` regenerates it from canonical HTML and image references, including the app screen selector, while preserving known `lastmod` dates. Update a page's `lastmod` when its content or structured data changes substantially. The 404 and redirect pages are excluded. `robots.txt` declares the sitemap and permits page/image crawling.

Every content page includes canonical, Open Graph, Twitter, and large-image-preview metadata. Article images have intrinsic dimensions and lazy loading. Structured data describes the real publisher, articles, breadcrumbs, app, and visible FAQs; no reviews or ratings are fabricated. There is currently no video, so there is no video sitemap or VideoObject markup.

## Product facts

The App Store destination is `https://apps.apple.com/app/finiteck/id6758164183`. Prices and compatibility were checked against the French listing on 2026-10-09. Check Apple before changing prices, availability, or trial wording. Published screenshots contain sample data and are labelled accordingly.

Describe privacy accurately: local storage and on-device analysis are distinct from optional consent-based cloud AI and web search. Do not introduce blanket claims that data can never leave a device.

## Publishing

The existing GitHub Pages configuration remains in place. `.nojekyll` serves the checked-in static files directly without generating HTML copies of internal Markdown documents. Review the changes and run the checks before pushing to the configured publishing branch. Keep the domain-verification files, `.well-known`, `CNAME`, robots.txt, and existing article URLs intact.

All rights reserved. The website content and branding are proprietary to Finiteck; the font retains its own included license.
