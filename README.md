# The Reading Room

A searchable bookshelf of **1,604 book files: 1,567 EPUBs and 37 PDFs**, organized into genre shelves with title and author search, filters, and individual downloads.

**[Open the book finder →](https://Aye-Shun.github.io/bookshelf/)**

Search for a title, author, series, filename, or genre. Combine shelf, genre, language, and format filters, then select **Download EPUB** or **Download PDF** beside a book. The finder works on a phone or desktop, and filters can be shared by copying the page URL.

## Browse the shelves

| Shelf | Book files |
| --- | ---: |
| [Cultivation & Martial Arts](catalog/cultivation-martial-arts.md) | 250 |
| [Game Worlds & Isekai](catalog/game-worlds-isekai.md) | 182 |
| [Science Fiction](catalog/science-fiction.md) | 32 |
| [Mystery & Horror](catalog/mystery-horror.md) | 23 |
| [Romance & Drama](catalog/romance-drama.md) | 54 |
| [Fantasy & Adventure](catalog/fantasy-adventure.md) | 218 |
| [Everyday & Comedy](catalog/everyday-comedy.md) | 1 |
| [Philosophy](catalog/philosophy.md) | 55 |
| [Programming & Technology](catalog/programming-technology.md) | 35 |
| [Language Learning](catalog/language-learning.md) | 4 |
| [Science & Nonfiction](catalog/science-nonfiction.md) | 2 |
| [Literature & Classics](catalog/literature.md) | 225 |
| [Other / Unclassified](catalog/unclassified.md) | 523 |

## Download a book

1. Open the [book finder](https://Aye-Shun.github.io/bookshelf/), or choose a shelf above.
2. Search or browse to the book you want. Volumes and editions are listed separately.
3. Choose **Download EPUB** or **Download PDF** and open the file in a compatible reader such as Apple Books, Calibre, or a PDF viewer.

You can download individual books without cloning this roughly 6.01 GB repository. **Code → Download ZIP** downloads the whole collection. The [CSV catalog](catalog.csv) is useful for spreadsheet searches; [SHA256SUMS](SHA256SUMS) records checksums for the published book files.

## How the catalog is organized

- EPUB titles, authors, languages, and genre tags come from book metadata. PDF titles and authors use embedded metadata when available, with filenames as a fallback. Some source metadata may be missing or inaccurate.
- Source collections and topic folders identify philosophy, programming, language learning, and Bengali literature; the classification basis appears in each book’s details.
- A book has one primary shelf and can have many searchable genre tags. Related volumes with the same normalized series and author can share genre metadata.
- When genre metadata is absent, explicit title keywords can suggest a shelf. These entries are labeled **Suggested from title keywords** in the finder; they are not verified genre classifications.
- Titles without enough information remain in **Other / Unclassified**. They are still searchable by title, author, and filename.
- Multiple volumes, editions, and compilations are preserved. The count is a file count, not a count of unique stories. Labels such as “complete” or “incomplete” are supplied by the source titles and are not editorial guarantees.
- The original 1,173-book collection is preserved. The latest import adds 431 verified files from the four repositories listed below. Two exact duplicates and one damaged source PDF were excluded from that import.
- App-generated account and reading-position metadata is excluded from published EPUB copies. Different editions and language versions are retained; duplicate checking compares file contents.

## Latest additions

| Source repository | Added files | Formats |
| --- | ---: | --- |
| [Fictioners](https://github.com/nagraj05/fictioners) | 122 | EPUB |
| [Wittgenstein Project](https://github.com/wittgenstein-project/wittgenstein-project.github.io) | 55 | EPUB |
| [Bongboi](https://github.com/eedeidk/bongboi) | 215 | EPUB |
| [Developer EBooks](https://github.com/tuantutanghuynh/Ebook) | 39 | 2 EPUB, 37 PDF |

Source links are included in each imported book’s details and in the catalog. The Wittgenstein import keeps EPUB editions rather than adding equivalent PDF and MOBI versions. These counts describe this published collection, not every book downloaded locally.

## Use the finder offline

Download the files in [`docs/`](docs/) and open `index.html` in a browser. Search and filtering work without a server. Book downloads still use GitHub and require an internet connection.

## Maintain the library

Requires Python 3.9 or later. Installing Poppler’s `pdfinfo` also enables PDF metadata extraction and readability checks.

To append a verified import while preserving existing catalog entries:

```sh
python3 tools/import_catalog.py /path/to/import-manifest.csv /path/to/books-folder
python3 tools/verify_catalog.py
```

The manifest uses `source`, `source_path`, `status`, `destination`, and `sha256` columns; only rows marked `added` are imported. Repeating the same import skips entries already in the catalog. The importer creates publication copies, strips app-generated EPUB metadata, and refreshes the finder, CSV, shelf lists, and checksums.

`tools/build_catalog.py` is for replacing the catalog with a single top-level EPUB folder. Use the importer above to extend this mixed-format collection.

The finder is a static HTML/CSS/JavaScript site in `docs/`. GitHub Pages serves a lightweight `gh-pages` branch generated from that directory; Book files are downloaded individually from the main repository.

## Rights and corrections

Book copyrights remain with their respective rights holders. Inclusion here does not grant additional reuse rights or place a book in the public domain. No blanket license is applied to the book collection.

For a metadata correction, broken download, or rights inquiry, [open an issue](https://github.com/Aye-Shun/bookshelf/issues/new) identifying the title and the requested change.
