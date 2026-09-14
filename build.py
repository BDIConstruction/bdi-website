#!/usr/bin/env python3
"""Rebuilds projects.html from content/projects/*.json.

Runs on every deploy. The JSON files are the source of truth — the admin
at /admin edits them, and this turns them back into the static page.

Card images are generated for any photo that lacks one. If Pillow is not
available the build still succeeds and the full-size photo is used for the
card instead, so a missing dependency can never take the site down.
"""

from __future__ import annotations   # keeps the type hints valid on older Pythons

import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
CONTENT = ROOT / "content" / "projects"
CARD_WIDTH = 760

try:
    from PIL import Image
except ImportError:                                    # keep deploying regardless
    Image = None
    print("note: Pillow unavailable — using full-size photos for cards")


def local(path: str) -> pathlib.Path | None:
    """Map a site-absolute photo path to a file in the repo."""
    if not path:
        return None
    p = ROOT / path.lstrip("/")
    return p if p.exists() else None


def card_for(photo: str) -> str:
    """Return the path to use for a card, making a smaller copy when we can."""
    src = local(photo)
    if src is None:
        return photo
    card = src.with_name(src.stem + "-card.jpg")
    if not card.exists() and Image is not None:
        try:
            im = Image.open(src).convert("RGB")
            w, h = im.size
            if w > CARD_WIDTH:
                im = im.resize((CARD_WIDTH, round(h * CARD_WIDTH / w)), Image.LANCZOS)
            im.save(card, "JPEG", quality=80, optimize=True, progressive=True)
            print(f"  card image created: {card.name}")
        except Exception as exc:                       # noqa: BLE001 - never fail the build
            print(f"  could not resize {src.name} ({exc}); using full size")
            return photo
    # keep the folder the photo lives in; uploads sit in /uploads, the
    # originally migrated set sits at the repo root
    return "/" + card.relative_to(ROOT).as_posix() if card.exists() else photo


def load():
    items = []
    for f in sorted(CONTENT.glob("*.json")):
        try:
            d = json.loads(f.read_text())
        except json.JSONDecodeError as exc:
            print(f"  skipping {f.name}: {exc}")
            continue
        if not d.get("title"):
            continue
        d["_slug"] = f.stem
        d["_card"] = card_for(d.get("photo", ""))
        items.append(d)
    # position first, then newest-first as the old site ordered them
    items.sort(key=lambda d: (int(d.get("order") or 0), _neg_date(d.get("wp_date", ""))))
    return items


def _neg_date(s: str) -> str:
    """Sort dates descending inside an ascending sort."""
    return "".join(chr(255 - ord(c)) for c in s) if s else "\xff"


def rel(path: str) -> str:
    """The CMS stores site-absolute paths; every page sits at the repo root, so
    emit them relative. Keeps the site working when files are opened directly."""
    return (path or "").lstrip("/")


def place_for(d):
    # Every project is in Florida, so the state adds nothing - show the city
    # alone, and only append a state if it is somewhere other than FL.
    city = str(d.get("city") or "").strip()
    state = str(d.get("state") or "").strip()
    place = city if not state or state.upper() in ("FL", "FLORIDA") else f"{city}, {state}"
    return place if city else ""


def card_html(d, i):
    name = html.escape(d["title"])
    place = place_for(d)
    meta = f'\n        <div class="loc">{html.escape(place)}</div>' if place else ""
    href = f"project-{d['_slug']}.html"
    return (
        f'      <a class="rv pcard" data-d="{(i % 3) * 90}" href="{html.escape(href)}">\n'
        f'        <span class="photo"><img src="{html.escape(rel(d["_card"]))}" loading="lazy" '
        f'decoding="async" alt="{name}"></span>{meta}\n'
        f'        <h4>{name}</h4>\n      </a>'
    )


def gallery_images(d):
    photos = []
    cover = d.get("photo") or ""
    if cover:
        photos.append(cover)
    for p in d.get("gallery") or []:
        if p and p not in photos:
            photos.append(p)
    return photos


def gallery_html(d):
    imgs = gallery_images(d)
    name = html.escape(d["title"])
    cells = []
    for idx, photo in enumerate(imgs):
        thumb = card_for(photo)
        alt = f"{name} — photo {idx + 1}" if len(imgs) > 1 else name
        cells.append(
            f'        <button type="button" class="rv gcard" data-d="{(idx % 3) * 90}" '
            f'data-full="{html.escape(rel(photo))}" aria-label="View larger: {alt}">\n'
            f'          <img src="{html.escape(rel(thumb))}" loading="lazy" decoding="async" '
            f'alt="{alt}"></button>'
        )
    return "\n".join(cells)


def location_block(d):
    place = place_for(d)
    if not place:
        return ""
    return f'      <div class="rv loc" data-d="130">{html.escape(place)}</div>'


def description_block(d):
    desc = str(d.get("description") or "").strip()
    if not desc:
        return ""
    paras = [p.strip() for p in desc.split("\n\n") if p.strip()]
    body = "\n".join(f'      <p class="rv" data-d="{(i % 2) * 90}">{html.escape(p)}</p>'
                      for i, p in enumerate(paras))
    return f'  <section class="intro">\n    <div class="wrap">\n{body}\n    </div>\n  </section>'


DETAIL_TEMPLATE = (ROOT / "content" / "project-template.html").read_text()


def detail_html(d):
    name = html.escape(d["title"])
    first_para = str(d.get("description") or "").strip().split("\n\n")[0][:160]
    meta_desc = first_para or f"{d['title']} — a project by BDI Construction."
    page = DETAIL_TEMPLATE
    page = page.replace("__TITLE__", name)
    page = page.replace("__META_DESC__", html.escape(meta_desc))
    page = page.replace("__SLUG_PAGE__", f"project-{d['_slug']}.html")
    page = page.replace("__LOCATION_BLOCK__", location_block(d))
    page = page.replace("__DESCRIPTION_BLOCK__", description_block(d))
    page = page.replace("__GALLERY__", gallery_html(d))
    return page


def write_detail_pages(items):
    for d in items:
        (ROOT / f"project-{d['_slug']}.html").write_text(detail_html(d))


def main():
    items = load()
    if not items:
        sys.exit("no projects found in content/projects — refusing to write an empty page")

    page = (ROOT / "projects.html").read_text()
    grid = "\n".join(card_html(d, i) for i, d in enumerate(items))

    page, n = re.subn(r'(<div class="pgrid">\n).*?(\n      </div>)',
                      lambda m: m.group(1) + grid + m.group(2), page, flags=re.S)
    if n != 1:
        sys.exit("could not find the project grid in projects.html")

    page = re.sub(r'(<div class="rv count">)\d+ projects(</div>)',
                  rf'\g<1>{len(items)} projects\g<2>', page)

    (ROOT / "projects.html").write_text(page)
    write_detail_pages(items)
    missing = sum(1 for d in items if not local(d.get("photo", "")))
    print(f"projects.html rebuilt — {len(items)} projects, {len(items)} project pages written"
          + (f", {missing} without a photo on disk" if missing else ""))


if __name__ == "__main__":
    main()
