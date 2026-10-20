# Birthday Vocaloid Finder

Enter your birthday and see which Vocaloid songs came out on that day.

The site is a single `index.html` with no build step. It includes 8,603 original songs: the 10,000 highest-rated originals on [VocaDB](https://vocadb.net), minus those without a release date. The data was downloaded on October 20, 2026. A song's date is its first public upload, usually on Niconico or YouTube.

## Run it locally

Open `index.html` in a browser.

## Refresh the song list

```sh
python3 scripts/fetch_songs.py   # writes songs.json from the VocaDB API
```

The song list lives in the `const RAW = [...]` line of `index.html`. Each row is `[vocadbId, romajiTitle, englishTitle, japaneseTitle, artists, date, youtubeUrl, niconicoUrl]`, ordered most popular first.

Song data © VocaDB contributors.
