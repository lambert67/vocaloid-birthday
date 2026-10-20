"""Download the most popular original songs from VocaDB and write songs.json.

Usage: python3 scripts/fetch_songs.py [count]   (default 10000)

songs.json looks like {"updated": "YYYY-MM-DD", "songs": [row, ...]}, most popular first.
Each row is [vocadbId, romajiTitle, englishTitle, japaneseTitle, artists, "YYYY-MM-DD", youtubeId, niconicoId].
englishTitle and japaneseTitle are "" when they repeat the romaji title.
"""
import datetime
import json
import pathlib
import sys
import time
import urllib.request

API = "https://vocadb.net/api/songs?sort=RatingScore&songTypes=Original&maxResults=100&fields=PVs&lang={lang}&start={start}"
OUT = pathlib.Path(__file__).resolve().parent.parent / "songs.json"
EARLIEST = "2004"  # VOCALOID's first release; anything older is a joke entry


def get(url):
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "vocaloid-birthday (github.com/lambert67/vocaloid-birthday)"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)["items"]
        except Exception as e:
            print(f"retrying {url}: {e}", file=sys.stderr)
            time.sleep(2 ** attempt)
    raise RuntimeError(f"giving up on {url}")


def original_pv(pvs, service):
    for p in pvs:
        if p.get("service") == service and p.get("pvType") == "Original" and not p.get("disabled"):
            return p["pvId"]
    return ""


def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    songs = {}
    for start in range(0, count, 100):
        for lang in ("Romaji", "English"):
            for it in get(API.format(lang=lang, start=start)):
                rec = songs.setdefault(it["id"], {"id": it["id"]})
                if lang == "Romaji":
                    pvs = it.get("pvs", [])
                    rec.update(ro=it["name"], jp=it["defaultName"], a=it["artistString"], r=it["ratingScore"],
                               d=(it.get("publishDate") or "")[:10],
                               yt=original_pv(pvs, "Youtube"), nn=original_pv(pvs, "NicoNicoDouga"))
                else:
                    rec["en"] = it["name"]
        print(f"fetched {min(start + 100, count)}/{count}", file=sys.stderr)
        time.sleep(0.3)

    rows = []
    for s in sorted(songs.values(), key=lambda s: (-s.get("r", 0), s["id"])):
        if not s.get("d") or s["d"] < EARLIEST or "ro" not in s:
            continue
        en = s.get("en", "")
        en = "" if en == s["ro"] else en
        jp = "" if s["jp"] in (s["ro"], en) else s["jp"]
        rows.append([s["id"], s["ro"], en, jp, s["a"], s["d"], s["yt"], s["nn"]])

    data = {"updated": datetime.date.today().isoformat(), "songs": rows}
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"wrote {len(rows)} songs to {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
