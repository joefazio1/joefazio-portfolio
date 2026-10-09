"""Find a 30-second Apple preview clip for each record in the collection.

Run by hand when the collection changes:  python scripts/fetch_previews.py

Reads src/data/collection.json and writes src/data/previews.json, keyed by
each record's `art` slug. The site never calls these APIs at page load; it
only plays the saved clip URL, which Apple hosts, when a visitor picks a
record. Records already in previews.json are skipped, so delete an entry (or
change its `song`) to look it up again.

Which song: the record's `song` field if it has one, otherwise the album's
most popular track by Deezer's play-count rank. `song` can also be a list,
played back to back on the site; its entry in previews.json is then a list. Clean edits are preferred;
a clip is marked `explicit` only when Apple has no clean version of the song.
"""

import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COLLECTION = ROOT / "src" / "data" / "collection.json"
OUT = ROOT / "src" / "data" / "previews.json"


def get(url):
    # Apple rate-limits bursts (HTTP 429), so back off and retry.
    for _ in range(6):
        try:
            return json.load(urllib.request.urlopen(url, timeout=20))
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(30)
    raise SystemExit("Still rate limited; try again in a few minutes.")


def norm(s):
    s = re.sub(r"\(.*?\)|\[.*?\]", "", s.lower())
    return re.sub(r"[^a-z0-9]", "", s)


def first_artist(a):
    return re.split(r" & |, (?!the )", a)[0].strip()


def album_title(record):
    # `match` names the album as the stores list it, when that differs.
    return record.get("match") or re.sub(r"\s*\(.*?\)", "", record["title"])


def top_track(record):
    """Most popular track on the album, by Deezer rank."""
    q = urllib.parse.urlencode({"q": f"{first_artist(record['artist'])} {album_title(record)}"})
    albums = get(f"https://api.deezer.com/search/album?{q}")["data"]
    want = norm(album_title(record))
    album = next((a for a in albums if norm(a["title"]) == want), None) or next(
        (a for a in albums if norm(a["title"]).startswith(want[:8])), None
    )
    if not album:
        return None
    tracks = get(f"https://api.deezer.com/album/{album['id']}/tracks?limit=100")["data"]
    return max(tracks, key=lambda t: t.get("rank", 0))["title"]


ARTIST_IDS = {}


def artist_id(name):
    if name not in ARTIST_IDS:
        time.sleep(3)
        q = urllib.parse.urlencode({"term": name, "entity": "musicArtist", "limit": 10})
        hits = get(f"https://itunes.apple.com/search?{q}")["results"]
        exact = [a for a in hits if norm(a["artistName"]) == norm(name)]
        ARTIST_IDS[name] = exact[0]["artistId"] if exact else None
    return ARTIST_IDS[name]


def apple_albums(record):
    """The album's versions in Apple's store, clean edits first.

    Looks in the artist's catalog (full credit, then first-listed artist) and
    in a plain album search, since each sometimes misses a version."""
    want = norm(album_title(record))
    pool = {}
    for name in dict.fromkeys([record["artist"], first_artist(record["artist"])]):
        aid = artist_id(name)
        if aid:
            time.sleep(3)
            for a in get(f"https://itunes.apple.com/lookup?id={aid}&entity=album&limit=200")["results"][1:]:
                pool[a["collectionId"]] = a
    time.sleep(3)
    q = urllib.parse.urlencode({"term": f"{album_title(record)} {first_artist(record['artist'])}", "entity": "album", "limit": 50})
    for a in get(f"https://itunes.apple.com/search?{q}")["results"]:
        pool[a["collectionId"]] = a
    found = [a for a in pool.values() if norm(a["collectionName"]) == want] or [
        a for a in pool.values() if norm(a["collectionName"]).startswith(want)
    ]
    return sorted(found, key=lambda a: a.get("collectionExplicitness") != "cleaned")


def find_preview(record, song=None):
    song = song or record.get("song") or top_track(record)
    if not song:
        return None, "no album match"
    albums = apple_albums(record)
    for album in albums:
        time.sleep(3)
        songs = get(f"https://itunes.apple.com/lookup?id={album['collectionId']}&entity=song&limit=200")["results"]
        songs = [t for t in songs if t.get("wrapperType") == "track" and t.get("previewUrl")]
        # An exact title beats a longer one ("California Girls" over its remix).
        hit = next((t for t in songs if t["trackName"].lower() == song.lower()), None) or next(
            (t for t in songs if norm(t["trackName"]) == norm(song)), None
        ) or next(
            (t for t in songs if norm(t["trackName"]).startswith(norm(song)) or norm(song).startswith(norm(t["trackName"]))),
            None,
        )
        if hit:
            return {
                "song": hit["trackName"],
                "url": hit["previewUrl"],
                "apple": hit["trackViewUrl"],
                "explicit": hit.get("trackExplicitness") == "explicit",
            }, song
    return None, f"{song}; album {'found' if albums else 'not found'} on Apple"


def main():
    data = json.loads(COLLECTION.read_text(encoding="utf-8"))
    previews = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    for record in data["vinyl"] + data["cd"]:
        slug = record.get("art")
        if not slug or slug in previews:
            continue
        songs = record["song"] if isinstance(record.get("song"), list) else [None]
        found_all = []
        for song in songs:
            time.sleep(3)
            found, why = find_preview(record, song)
            if found:
                found_all.append(found)
                flag = "  EXPLICIT" if found["explicit"] else ""
                print(f"{slug:20} {found['song']}{flag}")
            else:
                print(f"{slug:20} NOT FOUND ({why})")
        if found_all:
            previews[slug] = found_all if len(songs) > 1 else found_all[0]
    OUT.write_text(json.dumps(previews, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
