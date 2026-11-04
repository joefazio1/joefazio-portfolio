"""Download a TMDB poster for each movie and show on the ranked lists.

Run by hand when a list changes:  python scripts/fetch_posters.py

Reads the titles and years from the first list in src/pages/movies.astro and
src/pages/shows.astro (the ranked one, not the honorable mentions) and saves
one poster per title to src/assets/posters/<slug>.jpg, where Astro resizes it at build
time. The site never calls TMDB at page load. Posters already saved are
skipped, so delete a file to fetch it again.

Needs a free TMDB API key in a .env file at the repo root:
    TMDB_API_KEY=...
.env is gitignored, so the key never reaches the public repo.
"""

import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Page, TMDB search type, the year filter it takes, and its title field.
SOURCES = [
    ("movies.astro", "movie", "primary_release_year", "title"),
    ("shows.astro", "tv", "first_air_date_year", "name"),
]
OUT = ROOT / "src" / "assets" / "posters"
# w500 is plenty for a thumbnail and keeps the originals small.
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"


def api_key():
    for line in (ROOT / ".env").read_text(encoding="utf8").splitlines():
        if line.startswith("TMDB_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("No TMDB_API_KEY in .env")


def slug(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def norm(title):
    # TMDB writes WALL·E with a middle dot; compare letters and digits only.
    return re.sub(r"[^a-z0-9]", "", title.lower())


def main():
    key = api_key()
    OUT.mkdir(parents=True, exist_ok=True)

    for page, kind, year_param, field in SOURCES:
        # Only the first array on the page: the ranked list.
        ranked = (ROOT / "src" / "pages" / page).read_text(encoding="utf8").split("];")[0]
        # A show's year is its run ('2008-2013'), so take the first four digits.
        for title, year in re.findall(r"title: ['\"](.+?)['\"], year: '?(\d{4})", ranked):
            dest = OUT / f"{slug(title)}.jpg"
            if dest.exists():
                continue
            q = urllib.parse.urlencode({"api_key": key, "query": title, year_param: year})
            results = json.load(urllib.request.urlopen(f"https://api.themoviedb.org/3/search/{kind}?{q}", timeout=20))["results"]
            results = [r for r in results if r.get("poster_path")]
            # Prefer an exact title match, then the most popular result, so a
            # same-year short ("WALL-E's Treasures") cannot beat the film itself.
            exact = [r for r in results if norm(r[field]) == norm(title)]
            hit = max(exact or results, key=lambda r: r.get("popularity", 0), default=None)
            if not hit:
                print(f"--  {title} ({year}): no match")
                continue
            urllib.request.urlretrieve(IMAGE_BASE + hit["poster_path"], dest)
            print(f"OK  {title} ({year}) -> {hit[field]}")


if __name__ == "__main__":
    main()
