#!/usr/bin/env python3
"""Build a portable catalog from a folder of EPUBs (Python standard library)."""
import argparse, collections, csv, hashlib, json, re, shutil, unicodedata, zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
DC = '{http://purl.org/dc/elements/1.1/}'
CATEGORIES = [
 ('cultivation-martial-arts', 'Cultivation & Martial Arts', {'xianxia','xuanhuan','wuxia','martial arts','cultivation'}),
 ('game-worlds-isekai', 'Game Worlds & Isekai', {'game elements','virtual reality','reincarnation','transported to another world','transported to another','isekai','litrpg'}),
 ('science-fiction', 'Science Fiction', {'sci-fi','science fiction','mecha'}),
 ('mystery-horror', 'Mystery & Horror', {'mystery','horror','crime'}),
 ('romance-drama', 'Romance & Drama', {'romance','josei','shoujo'}),
 ('historical', 'Historical', {'historical'}),
 ('fantasy-adventure', 'Fantasy & Adventure', {'fantasy','adventure','action','supernatural'}),
 ('everyday-comedy', 'Everyday & Comedy', {'slice of life','school life','comedy','sports','cooking','drama'}),
 ('philosophy', 'Philosophy', {'philosophy','ethics','logic'}),
 ('programming-technology', 'Programming & Technology', {'programming','computer science','computers','technology'}),
 ('language-learning', 'Language Learning', {'language learning','linguistics'}),
 ('science-nonfiction', 'Science & Nonfiction', {'science','nonfiction','non-fiction','history','biography'}),
 ('literature', 'Literature & Classics', {'fiction','literature','poetry','classics','plays'}),
 ('unclassified', 'Other / Unclassified', set()),
]

def clean(value):
 return re.sub(r'\s+', ' ', value).strip()

def slug(value):
 value=unicodedata.normalize('NFKD', value).encode('ascii','ignore').decode().lower()
 return re.sub(r'[^a-z0-9]+','-',value).strip('-')[:105] or 'book'

def read_book(path):
 with zipfile.ZipFile(path) as z:
  container=ET.fromstring(z.read('META-INF/container.xml'))
  opf=next(e.attrib['full-path'] for e in container.iter() if e.tag.endswith('rootfile'))
  package=ET.fromstring(z.read(opf))
  meta=next(e for e in package if e.tag.endswith('metadata'))
  def vals(tag): return [clean(''.join(e.itertext())) for e in meta if e.tag==DC+tag and clean(''.join(e.itertext()))]
  title=(vals('title') or [path.stem])[0]
  authors=vals('creator') or ['Unknown author']
  tags=[]
  for subject in vals('subject'):
   for tag in re.split(r'[,;]',subject):
    tag=clean(tag)
    if not tag or 'http' in tag.lower() or tag.lower() in {'unknown','(unspecified)','general'}: continue
    tag={'sci-fi':'Science Fiction','sci fi':'Science Fiction','ln':'Light Novel','light novel':'Light Novel'}.get(tag.lower(),tag)
    if tag not in tags:tags.append(tag)
  series=next((e.attrib.get('content','') for e in meta if e.attrib.get('name')=='calibre:series'),'')
  language=(vals('language') or ['und'])[0]
  language={'eng':'en','en-US':'en','en-us':'en','en-GB':'en'}.get(language,language)
 return {'title':title,'authors':authors,'tags':tags,'series':series,'language':language,'originalFile':path.name}

def family(book):
 # Only carry tags between volumes with the same normalized series AND author.
 name=book['series'] or re.split(r'\s*[-:]?\s*\b(?:vol(?:ume)?\.?|book|arc|chapter)\s*\d',book['title'],flags=re.I)[0]
 name=re.sub(r'\s+A Compilation$','',name,flags=re.I)
 return slug(name),tuple(a.lower() for a in book['authors'])

def category(tags):
 values={t.lower() for t in tags}
 for key,label,matches in CATEGORIES:
  if values & matches:return key,label
 return 'unclassified','Other / Unclassified'

def suggested_category(title):
 rules=[
  ('cultivation-martial-arts',r'\b(martial|cultivat\w*|wuxia|xianxia|immortal\w*|heaven\w*|dan god)\b'),
  ('game-worlds-isekai',r'\b(isekai|another world|different world|reincarnat\w*|rpg|vrmmo|virtual reality|game world|level\w*|summon\w*)\b'),
  ('science-fiction',r'\b(mecha|galactic|spaceship|space opera|android|robot)\b'),
  ('mystery-horror',r'\b(detective|mystery|murder|coroner|horror)\b'),
  ('romance-drama',r'\b(wife|husband|bride|marriage|romance|girlfriend|boyfriend|love story)\b'),
  ('fantasy-adventure',r'\b(magic\w*|mahou|demon\w*|dragon\w*|dungeon\w*|sorcer\w*|wizard\w*|hero\w*|sword\w*|goblin\w*|necromanc\w*|elf|elves|vampire\w*|witch\w*|gods?|fantasy)\b'),
 ]
 for key,pattern in rules:
  if re.search(pattern,title,re.I):return key,next(l for k,l,_ in CATEGORIES if k==key)
 return 'unclassified','Other / Unclassified'

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('source',type=Path)
 parser.add_argument('--repo',default='Aye-Shun/bookshelf')
 args=parser.parse_args()
 files=sorted(args.source.glob('*.epub'))
 entries=[read_book(p) for p in files]
 families=collections.defaultdict(set)
 for book in entries:families[family(book)].update(book['tags'])
 for book,path in zip(entries,files):
  tags=book['tags']; basis='EPUB subject metadata'
  if not tags and families[family(book)]:
   tags=sorted(families[family(book)]);basis='Related-volume metadata (same series and author)'
  book['tags']=tags
  key,label=category(tags)
  if key=='unclassified':
   key,label=suggested_category(book['title'])
   basis='Suggested from title keywords' if key!='unclassified' else 'No matching genre metadata'
  book.update(category=key,categoryLabel=label,categoryBasis=basis)
  book['id']=hashlib.sha256(path.name.encode()).hexdigest()[:12]
  relative=f"books/{key}/{slug(path.stem)}--{book['id']}.epub"
  target=ROOT/relative;target.parent.mkdir(parents=True,exist_ok=True)
  # Strip app-generated account/reading metadata from public copies only.
  private_names={'itunesmetadata.plist','ibooksmetadata.plist','calibre_bookmarks.txt','.ds_store'}
  with zipfile.ZipFile(path) as original:
   omit=[n for n in original.namelist() if Path(n).name.lower() in private_names]
   if omit:
    with zipfile.ZipFile(target,'w') as public:
     for info in original.infolist():
      if info.filename not in omit:public.writestr(info,original.read(info.filename))
   elif not target.exists():shutil.copyfile(path,target)
  book['sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
  book['bytes']=target.stat().st_size
  book['path']=relative
  book['downloadUrl']=f'https://raw.githubusercontent.com/{args.repo}/main/{relative}'
  book['githubUrl']=f'https://github.com/{args.repo}/blob/main/{relative}'
 known={b['path'] for b in entries}
 for old in (ROOT/'books').rglob('*.epub'):
  if old.relative_to(ROOT).as_posix() not in known:old.unlink()
 write_catalog(entries,args.repo)

def write_catalog(entries,repo):
 counts=collections.Counter(b['category'] for b in entries)
 data={'updated':date.today().isoformat(),'repo':repo,'count':len(entries),'totalBytes':sum(b['bytes'] for b in entries),'categories':[{'id':k,'label':l,'count':counts[k]} for k,l,_ in CATEGORIES], 'books':entries}
 (ROOT/'docs').mkdir(exist_ok=True)
 (ROOT/'docs/catalog.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 # JS data permits opening the finder directly from disk without a server.
 (ROOT/'docs/catalog-data.js').write_text('window.BOOK_CATALOG = '+json.dumps(data,ensure_ascii=False).replace('</','<\\/')+';\n')
 with (ROOT/'catalog.csv').open('w',newline='') as f:
  writer=csv.writer(f,lineterminator="\n");writer.writerow(['Title','Author','Category','Tags','Language','Format','Source','Original filename','Bytes','Download URL','SHA-256'])
  for b in entries:writer.writerow([b['title'],'; '.join(b['authors']),b['categoryLabel'],'; '.join(b['tags']),b['language'],b.get('format','EPUB'),b.get('source','Original collection'),b['originalFile'],b['bytes'],b['downloadUrl'],b['sha256']])
 (ROOT/'SHA256SUMS').write_text(''.join(f"{b['sha256']}  {b['path']}\n" for b in entries))
 (ROOT/'catalog').mkdir(exist_ok=True)
 def md(s):return s.replace('|','\\|').replace('[','\\[').replace(']','\\]')
 for key,label,_ in CATEGORIES:
  group=sorted((b for b in entries if b['category']==key),key=lambda b:b['title'].casefold())
  lines=[f'# {label}', '',f'{len(group):,} book files. [Open the searchable finder](https://{repo.split("/")[0]}.github.io/{repo.split("/")[1]}/?category={key}) · [Back to README](../README.md)', '', '| Title | Author | Download |', '| --- | --- | --- |']
  for b in group:lines.append(f"| {md(b['title'])} | {md('; '.join(b['authors']))} | [{b.get('format','EPUB')} · {b['bytes']/1e6:.1f} MB]({b['downloadUrl']}) |")
  (ROOT/f'catalog/{key}.md').write_text('\n'.join(lines)+'\n')
 print(json.dumps({'books':data['count'],'bytes':data['totalBytes'],'categories':data['categories']}))

if __name__=='__main__':main()
