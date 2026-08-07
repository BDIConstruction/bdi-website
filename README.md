# BDI Construction

The website for BDI Construction — a Miami-based general contractor,
founded 1994, second-generation family-owned, working statewide across
Florida.

*Solid People. Solid Work. Solid Relationships.*

## About this repo

A static HTML/CSS site, hosted on GitHub Pages. No CMS, no build step, no
dependencies — the `.html` files in the repo root are the site. It replaces
the previous WordPress site.

| File | Page |
|---|---|
| `index.html` | Homepage |
| `history.html` | About Us → History |
| `culture.html` | About Us → Culture |
| `community.html` | About Us → Community |
| `expertise.html` | Expertise |
| `work-with-us.html` | Work With Us — subcontractor prequalification |
| `contact.html` | Contact Us |
| `images/` | Project photography |

Each page carries its own CSS in a `<style>` block. There is no shared
stylesheet, so shared elements like the nav and footer must be edited in
all seven files.

## Running it locally

```
python3 -m http.server 8000
```

Open http://localhost:8000/. Links and asset paths are all relative, so
opening the files directly in a browser works too.

## Design

- **Headlines:** Archivo · **Body:** Inter — both from Google Fonts
- **Navy:** `#0B1D2C` `#173352` `#28516B` · **Accent:** `#4FA8D8` ·
  **Off-white:** `#FAF9F5`
- Sections deliberately alternate light and dark

## Status

Seven pages are built and represent the approved design. Still to come:

- **Projects page** — 58 projects need migrating off the old WordPress site
- **Subcontractor form** — currently front-end only; needs a form backend
- **Custom domain** — `bdiconstruction.com` not yet pointed at GitHub Pages
- **Real logo** — pages currently use a text wordmark placeholder
- Contact page map and community gallery are placeholders

See `CLAUDE.md` for full detail, content accuracy rules, and open questions.
