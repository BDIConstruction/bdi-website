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
<https://bdiconstruction.com> — see `CNAME`. DNS is managed at Cloudflare;
the records for the site are deliberately unproxied, because GitHub cannot
issue a certificate for a name that resolves to somebody else's servers.
The domain remains registered with GoDaddy, which hosts nothing.

Email is not on this domain and never was. It runs on `bdico.com` through
Mimecast, untouched by anything here.

| File | Page |
|---|---|
| `index.html` | Homepage — the hero crossfades three projects (`hero-*.jpg`) |
| `404.html` | Shown for any address that does not exist, including old links |
| `projects.html` | Projects — generated, see below |
| `history.html` | About Us → History |
| `leadership.html` | About Us → Leadership — the four directors, with what each role covers |
| `culture.html` | About Us → Culture |
| `community.html` | About Us → Community |
| `expertise.html` | Expertise — the leadership row links through to `leadership.html` |
| `work-with-us.html` | Work With Us — subcontractor prequalification and careers |
| `contact.html` | Contact Us |

`oauth-worker/` is not part of the site — it is the small service that signs
administrators in. See its README.

Photographs live in the repo root (`project-*.jpg`, `leader-*.jpg`,
`team-*.jpg`, `community-*.jpg`, `proj-*.jpg`). Photos uploaded through the admin go to
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
- **Width:** pages run near full-bleed — `.wrap` caps at 1800px with 56px
  gutters, so grids and photographs take the whole window on a normal laptop.
  Prose does not: paragraphs carry their own `max-width` so line lengths stay
  readable however wide the screen gets
- **Navy:** `#0B1D2C` `#173352` `#28516B` · **Accent:** `#4FA8D8` ·
  **Off-white:** `#FAF9F5`
- Sections deliberately alternate light and dark
- Content fades and lifts into place on scroll; the effect is skipped entirely
  for `prefers-reduced-motion`, and nothing is hidden when JavaScript is off

## Status

Eight pages are built. Still open:

- **Leadership photographs** — the six headshots are 240px square, which is
  why the leadership row uses circles at 130px rather than the large photo
  cards the client asked for after seeing Moss's site. Anything bigger visibly
  softens on a high-density screen. Higher-resolution originals would let the
  row become proper photo cards; the layout is the only thing that would change
- **Leadership biographies** — `leadership.html` describes what each *role*
  covers, because that much follows from the job title. Nothing personal is
  claimed about anyone: no tenure, no history, no named projects. Real
  biographies have to come from the people themselves, and drop straight into
  the profile blocks when they do. The three Directors of Construction share
  one description because they share one title
- **Team section** — six of the ten people originally listed. The other four
  were held back by request, or in Lazaro Villar's case for want of a
  photograph. Their headshots were removed with their entries rather than left
  on the site unshown; all of it is in the history if anyone is added back
- **Project details** — every project has a name and a photo, but city, year,
  sector and delivery method are blank. The old WordPress site never stored
  them, so they have to be entered by hand at `/admin`
- ~~**Logo**~~ — `logo.png` is the real artwork, scaled from
  `bdi_logo_final_2011_high_res.png`, which is kept as the master. It replaces
  a reconstruction traced from a photograph. A rebrand is still expected, so
  when new artwork arrives it is one file and eight `src` attributes
- ~~**Subcontractor form**~~ — now posts to Web3Forms, which relays to
  `info@bdico.com`. The access key sits in `work-with-us.html` and is public by
  design: it names an inbox and grants no access to anything. Whoever watches
  that inbox should let the mail filter know to expect it
- **Careers form** — the right-hand half of `work-with-us.html` takes a resume,
  and Web3Forms does not relay attachments on the free plan, so that one form
  posts to FormSubmit instead and lands in `hiring@bdico.com`. **One thing is
  needed before it works:** the first submission after it goes live sends an
  activation email to that address, and somebody has to click the link in it,
  once. Until they do the relay accepts applications and delivers nothing.
  Attachments are capped at 10MB and the form refuses anything larger before
  sending rather than after, offering `hiring@bdico.com` instead. Unlike the
  Web3Forms key, the address is necessarily in the page source; if that draws
  spam, deleting the `_captcha` line makes the relay challenge senders

- ~~**Mail records**~~ — no mail runs on this domain and it now says so:
  `v=spf1 -all` and a DMARC policy of `reject`, so nobody can forge an address
  here. Anything later configured to send as `@bdiconstruction.com` will be
  refused until those records are changed — deliberately
- ~~**Old WordPress links**~~ — the addresses Google still indexes now redirect
  instead of falling through to `404.html`. `about-us/`, `projects/` and
  `projects-portfolio-test/` are stubs, as is `projects/<slug>/` for all 58
  projects — the WordPress slugs match the filenames in `content/projects/`,
  which is how they could be generated rather than transcribed. GitHub Pages
  cannot issue a 301, so each stub is a `<meta http-equiv="refresh">` with a
  `rel="canonical"` pointing at the real page; Google follows both and
  consolidates. Any old address not in this list still 404s — the full list
  lives in Search Console under Indexing → Pages, and more stubs can be added
  from it. New projects do not need one: only addresses WordPress published
  are indexed
