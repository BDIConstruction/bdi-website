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


def card_html(d, i):
    name = html.escape(d["title"])
    # state alone is meaningless - show the line only once a city is set
    city = str(d.get("city") or "").strip()
    state = str(d.get("state") or "").strip()
    place = ", ".join(x for x in [city, state] if x) if city else ""
    meta = f'\n        <div class="loc">{html.escape(place)}</div>' if place else ""
    return (
        f'      <button type="button" class="rv pcard" data-d="{(i % 3) * 90}" '
        f'data-full="{html.escape(rel(d.get("photo", "")))}" aria-label="View larger: {name}">\n'
        f'        <span class="photo"><img src="{html.escape(rel(d["_card"]))}" loading="lazy" '
        f'decoding="async" alt="{name}"></span>{meta}\n'
        f'        <h4>{name}</h4>\n      </button>'
    )


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
    missing = sum(1 for d in items if not local(d.get("photo", "")))
    print(f"projects.html rebuilt — {len(items)} projects"
          + (f", {missing} without a photo on disk" if missing else ""))


if __name__ == "__main__":
    main()
