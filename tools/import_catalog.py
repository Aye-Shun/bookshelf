#!/usr/bin/env python3
"""Append verified EPUB/PDF imports without replacing the current collection."""
import argparse, csv, hashlib, json, re, shutil, subprocess, zipfile
from pathlib import Path
from build_catalog import ROOT, CATEGORIES, read_book, category, suggested_category, slug, write_catalog

PRIVATE_NAMES = {'itunesmetadata.plist', 'ibooksmetadata.plist', 'calibre_bookmarks.txt', '.ds_store'}

def pdf_metadata(path):
    info = {}
    if shutil.which('pdfinfo'):
        result = subprocess.run(['pdfinfo', str(path)], capture_output=True, text=True, check=True)
        info = dict(line.split(':', 1) for line in result.stdout.splitlines() if ':' in line)
    title = info.get('Title', '').strip() or path.stem
    author = info.get('Author', '').strip() or 'Unknown author'
    return dict(title=title, authors=[author], tags=[], series='', language='und', originalFile=path.name)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('source', type=Path)
    args = parser.parse_args()
    data = json.loads((ROOT/'docs/catalog.json').read_text())
    entries = data['books']
    known = {b['sha256'] for b in entries}
    known_imports = {(b.get('source'), b.get('sourcePath')) for b in entries if b.get('sourcePath')}
    added = 0
    with args.manifest.open() as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        if row['status'] != 'added' or (row['source'], row['source_path']) in known_imports:
            continue
        path = (args.source/row['destination']).resolve()
        assert path.is_relative_to(args.source.resolve()), 'Source path leaves its folder'
        assert path.suffix.lower() in {'.epub', '.pdf'}
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256'], path
        book = read_book(path) if path.suffix.lower() == '.epub' else pdf_metadata(path)
        if book['title'].isdigit() or book['title'].lower().endswith(('.indd','.qxd','.doc','.docx')):
            book['title'] = path.stem
        book['language'] = book['language'].lower()
        key, label = category(book['tags'])
        basis = 'EPUB subject metadata'
        source = row['source']
        if source.startswith('wittgenstein-project/'):
            key, basis = 'philosophy', 'Source collection: Wittgenstein Project'
        elif source == 'tuantutanghuynh/Ebook':
            key = 'language-learning' if row['source_path'].startswith('Languages/') else 'programming-technology'
            basis = 'Source repository topic folder'
            if row['source_path'].startswith('Languages/French/'):
                book['language'] = 'fr'
        elif key == 'unclassified' and source == 'eedeidk/bongboi':
            key, basis = 'literature', 'Source collection: Bengali literature'
        elif key == 'unclassified':
            key, label = suggested_category(book['title'])
            basis = 'Suggested from title keywords' if key != 'unclassified' else 'No matching genre metadata'
        label = next(label for ident, label, _ in CATEGORIES if ident == key)
        ident = hashlib.sha256((source+'\0'+row['source_path']).encode()).hexdigest()[:12]
        relative = f"books/{key}/{slug(path.stem)}--{ident}{path.suffix.lower()}"
        target = ROOT/relative
        assert not target.exists(), f'Unexpected destination collision: {relative}'
        target.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix.lower() == '.epub':
            with zipfile.ZipFile(path) as original, zipfile.ZipFile(target, 'w') as public:
                public.writestr('mimetype', b'application/epub+zip', compress_type=zipfile.ZIP_STORED)
                for info in original.infolist():
                    if info.filename != 'mimetype' and Path(info.filename).name.lower() not in PRIVATE_NAMES:
                        public.writestr(info, original.read(info.filename))
        else:
            shutil.copyfile(path, target)
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        if digest in known:
            target.unlink()
            continue
        book.update(id=ident, category=key, categoryLabel=label, categoryBasis=basis,
                    format=path.suffix[1:].upper(), source=source, sourcePath=row['source_path'],
                    sourceUrl='https://github.com/'+source, path=relative, sha256=digest,
                    bytes=target.stat().st_size,
                    downloadUrl=f"https://raw.githubusercontent.com/{data['repo']}/main/{relative}",
                    githubUrl=f"https://github.com/{data['repo']}/blob/main/{relative}")
        entries.append(book)
        known.add(digest)
        added += 1
    write_catalog(entries, data['repo'])
    print(f'Added {added} books; existing entries preserved.')

if __name__ == '__main__':
    main()
