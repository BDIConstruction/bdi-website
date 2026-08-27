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
| `leadership.html` | Leadership — **held back for review: unlinked, out of the sitemap, `noindex`** |
| `culture.html` | About Us → Culture |
| `community.html` | About Us → Community |
| `expertise.html` | Expertise — the leadership row, currently without its links out |
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

- **Leadership page is not published** — the client is reviewing it with their
  bosses first. Three things hold it back and come off together when it is
  approved: the About Us menu entry (nine pages), the links out of the Expertise
  row, and the `noindex` plus the sitemap entry. The `noindex` is the one that
  matters — an unlinked page on a static host is still a public URL, and
  removing links alone would not keep it out of search results. The CSS for the
  links is left in place, so restoring them is markup only
- **Who is on it** — Carlos Rosell (Operations), Andrea Loguzzo (Controller),
  Dayana Colmenares (Marketing & Business Development), Lourdes Escandon
  (Pre-Construction), then the four construction directors, one to a division:
  Yamile Dominguez in South Florida, Scott Lowrance in Central & West Florida,
  Christopher Alvarez in Special Projects, Lazaro Villar in Government. That
  order is the client's. David Galdeano came off — the USPS work is service
  rather than construction — and his headshot went with him, into the history
- **Headshots** — all eight are 240px square on the same framing: crown eight
  per cent down, chin at fifty-six. Carlos Rosell's was cut from the 700x1050
  portrait `history.html` uses, and Dayana Colmenares's from a 1024x1536
  original. Faces are centred within about one per cent of the frame; the two
  most recent were checked against a drawn centre line, because an automated
  measurement of the widest non-background span reads hair and backdrop and
  gets it wrong
- **Special Projects** — the org chart calls Christopher Alvarez's division
  College | University and his resume calls it the Higher Learning Division;
  neither fits, because it is the small-cap division, projects under $5M:
  interior renovations, build-outs and fit-outs, of which campus work is only a
  part. The client is renaming it on the chart to match the site
- **Leadership photographs** — all six are 240px square, framed the same way:
  crown eight per cent down the frame, chin at fifty-six. That size is why the
  row uses circles at 130px rather than the large photo cards the client asked
  for after seeing Moss's site — anything bigger visibly softens. Higher
  resolution originals would let the row become photo cards; only the layout
  would change. Two were cropped from originals recovered out of the history,
  which is where the uploaded source files end up once they are removed from the
  repository root
- **Education and certifications** — kept off every profile by request. Training
  that bears on the work is stated in the prose instead ("an architect by
  training", "a civil engineer by training"). Christopher Alvarez's Certified
  General Contractor licence is the one exception: it is a licence to build in
  Florida rather than a training credential, and it is worded to match Carlos
  Rosell's on `history.html`
- **Lazaro Villar's biography** — written from his personal resume, because his
  BDI one does not exist yet. It deliberately names no former employer and no
  past project: the client asked for the company names out, and once they are
  gone the projects and dollar figures cannot stay either — unattributed, work
  he did elsewhere reads as BDI's, which is exactly what a prequalification
  would catch. Replace it when the company resume is written
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
