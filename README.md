# The Reading Room

A searchable bookshelf of **8,192 book files: 8,151 EPUBs, 37 PDFs, and 4 AZW3s**, organized into genre shelves with title and author search, filters, and individual downloads.

**[Open the book finder →](https://Aye-Shun.github.io/bookshelf/)**

Search for a title, author, series, filename, or genre. Combine shelf, genre, language, and format filters, then select the format-specific download button beside a book. The finder works on a phone or desktop, and filters can be shared by copying the page URL.

## Browse the shelves

| Shelf | Book files |
| --- | ---: |
| [Cultivation & Martial Arts](catalog/cultivation-martial-arts.md) | 251 |
| [Game Worlds & Isekai](catalog/game-worlds-isekai.md) | 182 |
| [Science Fiction](catalog/science-fiction.md) | 1,227 |
| [Mystery & Horror](catalog/mystery-horror.md) | 226 |
| [Romance & Drama](catalog/romance-drama.md) | 256 |
| [Historical](catalog/historical.md) | 79 |
| [Fantasy & Adventure](catalog/fantasy-adventure.md) | 442 |
| [Everyday & Comedy](catalog/everyday-comedy.md) | 51 |
| [Philosophy](catalog/philosophy.md) | 156 |
| [Programming & Technology](catalog/programming-technology.md) | 35 |
| [Language Learning](catalog/language-learning.md) | 4 |
| [Science & Nonfiction](catalog/science-nonfiction.md) | 422 |
| [Literature & Classics](catalog/literature.md) | 3,280 |
| [Other / Unclassified](catalog/unclassified.md) | 1,581 |

## Download a book

1. Open the [book finder](https://Aye-Shun.github.io/bookshelf/), or choose a shelf above.
2. Search or browse to the book you want. Volumes and editions are listed separately.
3. Choose the format-specific download button. EPUB works with readers such as Apple Books and Calibre; PDF works with a PDF viewer; AZW3 requires a compatible Kindle-format reader or conversion tool.

You can download individual books without cloning this roughly 11.82 GB repository. **Code → Download ZIP** downloads the whole collection. The [CSV catalog](catalog.csv) is useful for spreadsheet searches; [SHA256SUMS](SHA256SUMS) records checksums for the published book files.

## How the catalog is organized

- EPUB titles, authors, languages, and genre tags come from book metadata. PDF titles and authors use embedded metadata when available, with filenames as a fallback. AZW3 labels use the source filenames and author folders. Some source metadata may be missing or inaccurate.
- Source collections and topic folders identify philosophy, programming, language learning, and Bengali literature; the classification basis appears in each book’s details.
- A book has one primary shelf and can have many searchable genre tags. Related volumes with the same normalized series and author can share genre metadata.
- When genre metadata is absent, explicit title keywords can suggest a shelf. These entries are labeled **Suggested from title keywords** in the finder; they are not verified genre classifications.
- Titles without enough information remain in **Other / Unclassified**. They are still searchable by title, author, and filename.
- Multiple volumes, editions, and compilations are preserved. The count is a file count, not a count of unique stories. Labels such as “complete” or “incomplete” are supplied by the source titles and are not editorial guarantees.
- The original 1,173-book collection is preserved. The imports add 7,019 verified files from the eight source collections listed below. The download process skipped 80 exact duplicates, 12 empty source files, and one damaged PDF.
- App-generated account and reading-position metadata is excluded from published EPUB copies. Different editions and language versions are retained; duplicate checking compares file contents.

## Included collections

| Source repository | Added files | Formats |
| --- | ---: | --- |
| Original collection | 1,173 | EPUB |
| [Feedbooks archive](https://github.com/ManuelFte/Feedbooks-public-domain-books) | 5,721 | EPUB |
| [Essential EBooks](https://github.com/GlenHenshaw/Essential-EBooks) | 822 | EPUB |
| [OpenLibrary book collection](https://github.com/Auchrio/.library) | 41 | EPUB |
| [E-Library book repository](https://github.com/TiiJeiJ8/E-Library-Books-Repo) | 4 | AZW3 |
| [Fictioners](https://github.com/nagraj05/fictioners) | 122 | EPUB |
| [Wittgenstein Project](https://github.com/wittgenstein-project/wittgenstein-project.github.io) | 55 | EPUB |
| [Bongboi](https://github.com/eedeidk/bongboi) | 215 | EPUB |
| [Developer EBooks](https://github.com/tuantutanghuynh/Ebook) | 39 | 2 EPUB, 37 PDF |
| **Total** | **8,192** | **8,151 EPUB, 37 PDF, 4 AZW3** |

Source links appear in each imported book’s details and in the catalog. OpenLibrary and Wittgenstein editions use EPUB instead of adding equivalent PDF and MOBI versions. Different languages and editions are retained.

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
