# Birthday Vocaloid Finder

Enter your birthday and see which Vocaloid songs came out on that day.

Live at https://lambert67.github.io/vocaloid-birthday/

- About 8,600 original songs: the 10,000 highest-rated originals on [VocaDB](https://vocadb.net) that have a release date. A song's date is its first public upload, usually on Niconico or YouTube.
- Play songs right on the page, filter by singer, or search for a song to see the day it came out.
- Every result has its own link, such as `#03-09` or `#03-09-2005` with a birth year.

## Files

| File | What it is |
| --- | --- |
| `index.html` | The whole site: markup, styles and script |
| `songs.json` | The song list, loaded by the page |
| `scripts/fetch_songs.py` | Downloads the song list from VocaDB |
| `.github/workflows/update-songs.yml` | Refreshes `songs.json` on the 1st of every month |
| `og.png`, `favicon.svg` | Link preview image and tab icon |

## Run it locally

The page loads `songs.json`, so open it through a local web server rather than double-clicking the file:

```sh
python3 -m http.server
# then open http://localhost:8000
```

## Refresh the song list

The monthly GitHub Action does this automatically. To run it yourself:

```sh
python3 scripts/fetch_songs.py         # top 10,000 songs
python3 scripts/fetch_songs.py 20000   # or any other count
```

You can also start the update from the repo's Actions tab: choose "Update song list", then "Run workflow".

Each row in `songs.json` is `[vocadbId, romajiTitle, englishTitle, japaneseTitle, artists, date, youtubeId, niconicoId]`, ordered most popular first.

Song data © VocaDB contributors.
