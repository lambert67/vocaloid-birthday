import json, urllib.request, sys, time
out = {}
base = "https://vocadb.net/api/songs?sort=RatingScore&songTypes=Original&maxResults=100&fields=PVs&lang={lang}&start={s}"
for s in range(0, 10000, 100):
    for lang in ("Romaji", "English"):
        for attempt in range(4):
            try:
                with urllib.request.urlopen(base.format(lang=lang, s=s), timeout=60) as r:
                    items = json.load(r)["items"]; break
            except Exception as e:
                print("retry", s, lang, e, file=sys.stderr); time.sleep(2 ** attempt)
        for it in items:
            rec = out.setdefault(it["id"], {})
            if lang == "Romaji":
                rec.update(id=it["id"], ro=it["name"], jp=it["defaultName"], a=it["artistString"],
                           d=(it.get("publishDate") or "")[:10], r=it["ratingScore"])
                pvs = [p for p in it.get("pvs", []) if not p.get("disabled") and p.get("pvType") == "Original"]
                yt = next((p["url"] for p in pvs if p["service"] == "Youtube"), None)
                nn = next((p["url"] for p in pvs if p["service"] == "NicoNicoDouga"), None)
                if yt: rec["yt"] = yt
                if nn: rec["nn"] = nn.replace("http://", "https://")
            else:
                rec["en"] = it["name"]
    print("done", s, file=sys.stderr); time.sleep(0.3)
songs = [v for v in out.values() if v.get("d")]
json.dump(songs, open("songs.json", "w"), ensure_ascii=False)
print(len(out), len(songs))
