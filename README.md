# The Reading Room

A searchable bookshelf of **1,173 EPUB files**, organized into genre shelves with title and author search, filters, and individual downloads.

**[Open the book finder →](https://Aye-Shun.github.io/bookshelf/)**

Search for a title, author, series, filename, or genre. Combine shelf, genre, and language filters, then select **Download EPUB** beside a book. The finder works on a phone or desktop, and filters can be shared by copying the page URL.

## Browse the shelves

| Shelf | EPUB files |
| --- | ---: |
| [Cultivation & Martial Arts](catalog/cultivation-martial-arts.md) | 250 |
| [Game Worlds & Isekai](catalog/game-worlds-isekai.md) | 182 |
| [Science Fiction](catalog/science-fiction.md) | 28 |
| [Mystery & Horror](catalog/mystery-horror.md) | 21 |
| [Romance & Drama](catalog/romance-drama.md) | 52 |
| [Fantasy & Adventure](catalog/fantasy-adventure.md) | 210 |
| [Everyday & Comedy](catalog/everyday-comedy.md) | 1 |
| [Other / Unclassified](catalog/unclassified.md) | 429 |

## Download a book

1. Open the [book finder](https://Aye-Shun.github.io/bookshelf/), or choose a shelf above.
2. Search or browse to the book you want. Volumes and editions are listed separately.
3. Choose **Download EPUB** and open the file in an EPUB reader such as Apple Books or Calibre.

You can download individual books without cloning this roughly 5.08 GB repository. **Code → Download ZIP** downloads the whole collection. The [CSV catalog](catalog.csv) is useful for spreadsheet searches; [SHA256SUMS](SHA256SUMS) records checksums for the published EPUB files.

## How the catalog is organized

- Title, author, language, and genre tags come from the EPUB metadata. Some source metadata may be missing or inaccurate.
- A book has one primary shelf and can have many searchable genre tags. Related volumes with the same normalized series and author can share genre metadata.
- When genre metadata is absent, explicit title keywords can suggest a shelf. These entries are labeled **Suggested from title keywords** in the finder; they are not verified genre classifications.
- Titles without enough information remain in **Other / Unclassified**. They are still searchable by title, author, and filename.
- Multiple volumes, editions, and compilations are preserved. The count is a file count, not a count of unique stories. Labels such as “complete” or “incomplete” are supplied by the source titles and are not editorial guarantees.
- This collection covers the 1,173 accessible iCloud Books exports. Additional local-only titles could not be checked. Book content and original Desktop exports were preserved; app-generated account and reading-position metadata was excluded from these public copies.

## Use the finder offline

Download the files in [`docs/`](docs/) and open `index.html` in a browser. Search and filtering work without a server. Book downloads still use GitHub and require an internet connection.

## Maintain the library

Requires Python 3.9 or later, using only its standard library:

```sh
python3 tools/build_catalog.py /path/to/epub-folder --repo Aye-Shun/bookshelf
python3 tools/verify_catalog.py
```

The builder extracts metadata, creates organized publication copies in `books/`, removes app-generated private metadata, and regenerates the JSON, browser data, CSV, shelf lists, and checksums. The original EPUB folder is preserved.

The finder is a static HTML/CSS/JavaScript site in `docs/`. GitHub Pages serves a lightweight `gh-pages` branch generated from that directory; EPUB files are downloaded individually from the main repository.

## Rights and corrections

Book copyrights remain with their respective rights holders. Inclusion here does not grant additional reuse rights or place a book in the public domain. No blanket license is applied to the EPUB collection.

For a metadata correction, broken download, or rights inquiry, [open an issue](https://github.com/Aye-Shun/bookshelf/issues/new) identifying the title and the requested change.
