# BDI Construction — Website

## What this is

The website for BDI Construction (Miami-based general contractor, founded
1994, second-generation family-owned, statewide across Florida).

This is a **static HTML/CSS site hosted on GitHub Pages**. It replaces the
old WordPress site at bdiconstruction.com. There is no CMS, no build step,
and no server-side code — the `.html` files in the repo root are the site.

**These pages are the approved design.** Do not redesign, restyle, or
"improve" the visual direction without being asked. Changes to layout,
type, or color should be treated as requiring explicit approval.

## Files

| File | Page |
|---|---|
| `index.html` | Homepage |
| `history.html` | About Us → History (landing page for the About Us dropdown) |
| `culture.html` | About Us → Culture |
| `community.html` | About Us → Community |
| `expertise.html` | Expertise — Project Management, Team, Safety |
| `work-with-us.html` | Work With Us — subcontractor prequalification form |
| `contact.html` | Contact Us |
| `images/` | Project photography used on the homepage |

Each page is self-contained: its CSS lives in a `<style>` block in the
document head, and fonts load from Google Fonts via `@import`. There is no
shared stylesheet — a change to the nav or footer has to be made in all
seven files.

## Local preview

```
python3 -m http.server 8000
```

Then open http://localhost:8000/. Opening the files directly with `file://`
also works, since all links and asset paths are relative.

## Navigation structure (final, approved)

```
About Us  (dropdown → History / Culture / Community)
Projects
Expertise
Work With Us
Contact Us
```

Notes:
- Clicking "About Us" itself lands on **History**.
- The old site's **Sustainability** page and standalone **Community** tab
  were intentionally removed. Do not reinstate them.
- **Projects** has no page yet — its nav link points at `#`. See
  "Outstanding work" below.

## Design system

- **Headlines:** Archivo (600–800 weight) — Google Fonts
- **Body / nav / labels:** Inter (300–500 weight) — Google Fonts
- **Navy:** `#0B1D2C` (deep), `#173352`, `#28516B` (mid)
- **Accent:** `#4FA8D8` (light blue)
- **Off-white:** `#FAF9F5`
- Pages deliberately alternate light and dark sections. Do not make the
  site uniformly dark or uniformly white.
- Nav is white with a hairline bottom border on every page, including home.

**Known inconsistency:** `index.html` uses Archivo for headlines, matching
the spec above. The other six pages use **Fraunces** (serif italic). Each
page is internally consistent, but home does not match the other six. This
needs a decision from whoever signed off on the design — do not silently
normalize it in either direction.

## Images

Source photos were 4–5MB each. They have been resized and re-encoded as
progressive JPEG (quality 82) for web delivery — the whole `images/`
directory is now ~2MB. There is no build step that regenerates these, so
**any new photo added to the repo must be optimized before committing.**
Roughly: 2000px wide for full-bleed use, 1600px for grid cards.

`proj-c2.jpg` is committed but not referenced by any page — it is being
held for the Projects page.

## Outstanding work

### 1. Projects page
Not built. The old WordPress site had 58 projects in a Portfolio custom
post type rendered through Essential Grid. Moving off WordPress means those
projects and their photos need to be exported and rebuilt as a static grid.
Project examples: Dulce Vida, Grand East, Havana Enclave, Tucker Tower,
The Fountains at Hidden Lake.

### 2. Subcontractor form
`work-with-us.html` is front-end markup only. A static site cannot send
email, so the form currently does nothing on submit. It needs a form
backend (Formspree, Netlify Forms, a Cloudflare Worker, or similar).

**Confirm the correct recipient inbox before wiring it up** — the old site
footer used `info@bdico.com`, but `info@bdiconstruction.com` was also
specified. These are different addresses; ask, don't guess.

### 3. Custom domain
The site needs `bdiconstruction.com` pointed at GitHub Pages via DNS at
GoDaddy, with a `CNAME` file in the repo root. Not yet done.

### 4. Remaining placeholders
- **Logo:** every page uses a text wordmark plus a small placeholder
  triangle. The real logo file has not been provided yet.
- **Two project names** on the homepage grid are marked
  `[Confirm project name]` — needs client input.
- **Contact page map** is a CSS placeholder, not a real embedded map.
- **Community page gallery** is empty placeholder tiles; the client will
  supply event photos later. These empty tiles currently cause the page to
  scroll horizontally, which should resolve when real images land.

### 5. Home hero contrast
`.hero` defines a navy scrim gradient, but `.hero .skyline img` is
positioned absolutely over it, so the scrim never darkens the photo. The
label and body text wash out against the bright sky. Fixing this is a
visual change to an approved design — confirm before touching it.

## Content accuracy rules

These figures appear in print materials too and must stay consistent:

- Founded **1994**, Miami
- **Second-generation, family-owned**
- **50+** employees, statewide across Florida
- **80%+** repeat client business — use this figure, not 85%, not "all clients"
- Tagline: **Solid People. Solid Work. Solid Relationships.**
- Leadership: Teobaldo Rosell Jr. (Founder), Teobaldo Rosell III
  (President), Carlos Rosell (VP / Director of Operations)

Do not invent statistics, project details, certifications, or safety
metrics. If a number is needed and not in these files, ask.

## Cautions

- The **Safety** section on the Expertise page is deliberately brief. The
  client explicitly asked to keep it minimal — do not expand it with OSHA
  policy text or stat counters.
- This repo is **public**, because GitHub Pages requires it on the free
  plan. Do not commit credentials, form-backend API keys, client contact
  lists, or notes about the client's hosting accounts.
