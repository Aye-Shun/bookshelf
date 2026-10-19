#!/usr/bin/env python3
"""Validate the catalog, publication files, and EPUB archive integrity."""
import collections, csv, hashlib, json, zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
from urllib.parse import unquote

root=Path(__file__).resolve().parents[1]
catalog=json.loads((root/'docs/catalog.json').read_text())
books=catalog['books']
assert len(books)==catalog['count']
assert len({b['id'] for b in books})==len(books)
assert {b['path'] for b in books}=={p.relative_to(root).as_posix() for p in (root/'books').rglob('*.epub')}
assert sum(b['bytes'] for b in books)==catalog['totalBytes']
counts=collections.Counter(b['category'] for b in books)
for category in catalog['categories']:assert category['count']==counts[category['id']]
with (root/'catalog.csv').open() as f:assert len(list(csv.DictReader(f)))==len(books)
assert len((root/'SHA256SUMS').read_text().splitlines())==len(books)
for i,b in enumerate(books,1):
 p=root/b['path']
 assert p.stat().st_size==b['bytes']
 assert b['bytes']<100*1024**2
 assert hashlib.sha256(p.read_bytes()).hexdigest()==b['sha256']
 assert b['downloadUrl'].endswith('/'+b['path'])
 with zipfile.ZipFile(p) as z:
  assert z.testzip() is None,p
  assert z.infolist()[0].filename=='mimetype'
  assert z.infolist()[0].compress_type==zipfile.ZIP_STORED
  assert z.read('mimetype')==b'application/epub+zip'
  assert not any(Path(n).name.lower() in {'itunesmetadata.plist','ibooksmetadata.plist','calibre_bookmarks.txt','.ds_store'} for n in z.namelist())
  c=ET.fromstring(z.read('META-INF/container.xml'))
  opf=next(e.attrib['full-path'] for e in c.iter() if e.tag.endswith('rootfile'))
  ET.fromstring(z.read(opf))
 if i%200==0:print(f'Verified {i}/{len(books)} EPUBs',flush=True)
print(f'PASS: {len(books)} EPUBs; checksums, ZIP integrity, metadata, catalog counts, and publication paths verified.')
