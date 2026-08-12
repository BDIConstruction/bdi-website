# BDI Construction

The website for BDI Construction — a Miami-based general contractor,
founded 1994, second-generation family-owned, working statewide across
Florida.

*Solid People. Solid Work. Solid Relationships.*

## About this repo

A static HTML/CSS site. Each page is a `.html` file in the repo root and
carries its own CSS in a `<style>` block — there is no shared stylesheet, so
shared elements like the nav and footer must be edited in every page.

Hosted on **GitHub Pages**, served from `main` at
<https://bdiconstruction.github.io/bdi-website/>. It is not on a custom
domain; `bdiconstruction.com` still points elsewhere.

| File | Page |
|---|---|
| `index.html` | Homepage |
| `projects.html` | Projects — generated, see below |
| `history.html` | About Us → History |
| `culture.html` | About Us → Culture |
| `community.html` | About Us → Community |
| `expertise.html` | Expertise |
| `work-with-us.html` | Work With Us — subcontractor prequalification |
| `contact.html` | Contact Us |

`oauth-worker/` is not part of the site — it is the small service that signs
administrators in. See its README.

Photographs live in the repo root (`project-*.jpg`, `leader-*.jpg`,
`community-*.jpg`, `proj-*.jpg`). Photos uploaded through the admin go to
`uploads/`.

## Editing projects

Site administrators sign in at **`/admin`** with their GitHub account. Editing
a project commits to this repo, and the site redeploys itself.

- Each project is one file in `content/projects/` — this is the source of truth
- `build.py` turns those files into `projects.html`. The admin cannot run it,
  so the workflow in `.github/workflows/build-projects.yml` rebuilds the page
  and commits the result whenever a project or photo changes
- The build also makes a card-sized copy of any newly uploaded photo. If Pillow
  is unavailable it falls back to the full-size image rather than failing

To add an administrator: invite them under Settings → Collaborators. Signing in
needs a step a static host cannot perform — see `oauth-worker/README.md`.

`projects.csv` is the original WordPress import — names, categories and photo
filenames for all 58 projects. It is kept for reference and for bulk edits; the
JSON files are what the site actually reads.

## Running it locally

```
python3 -m http.server 8000
```

Open http://localhost:8000/. Asset paths are relative, so opening the files
directly in a browser works too. Run `python3 build.py` after changing
anything in `content/projects/`.

## Design

- **Headlines:** Archivo (homepage) · Fraunces (inner pages) · **Body:** Inter
- **Navy:** `#0B1D2C` `#173352` `#28516B` · **Accent:** `#4FA8D8` ·
  **Off-white:** `#FAF9F5`
- Sections deliberately alternate light and dark
- Content fades and lifts into place on scroll; the effect is skipped entirely
  for `prefers-reduced-motion`, and nothing is hidden when JavaScript is off

## Status

Eight pages are built. Still open:

- **Project details** — every project has a name and a photo, but city, year,
  sector and delivery method are blank. The old WordPress site never stored
  them, so they have to be entered by hand at `/admin`
- **Logo** — `logo.svg` is a reconstruction traced from a picture of the
  artwork, not the original file. A rebrand is expected
- **Subcontractor form** — front-end only; needs a form backend
- **Contact page map** — placeholder
- **Custom domain** — not connected
