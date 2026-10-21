/* Dependency-free catalog UI. All book metadata is rendered as text. */
(() => {
  'use strict';
  const data = window.BOOK_CATALOG;
  const $ = id => document.getElementById(id);
  const pageSize = 24;
  const normalize = s => s.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase();
  const searchable = data.books.map(book => ({ ...book, search: normalize([book.title, ...book.authors, book.series, ...book.tags, book.originalFile].join(' ')) }));
  const names = { en: 'English', de: 'German', fr: 'French', bn: 'Bengali', ca: 'Catalan', da: 'Danish', es: 'Spanish', it: 'Italian', nl: 'Dutch', pt: 'Portuguese', ru: 'Russian', tr: 'Turkish', zh: 'Chinese', und: 'Not specified' };
  const allGenres = [...new Set(data.books.flatMap(b => b.tags))].sort((a,b)=>a.localeCompare(b));
  const allFormats = [...new Set(data.books.map(b => b.format || 'EPUB'))];
  const allLanguages = [...new Set(data.books.map(b => b.language))];
  let state = { q: '', category: '', genre: '', language: '', format: '', sort: 'title', page: 1 };

  function el(tag, cls, text) { const e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; }
  function options(id, values, label) { values.forEach(value => { const o = el('option', '', label(value)); o.value = value; $(id).append(o); }); }
  options('genre', allGenres, x => x);
  options('language', allLanguages, x => names[x] || x);
  options('format', allFormats, x => x);
  const shelves = [{ id: '', label: 'All books', count: data.count }, ...data.categories.filter(c => c.count)];
  shelves.forEach(c => {
    const button = el('button'); button.type = 'button'; button.dataset.category = c.id; button.setAttribute('aria-pressed', 'false');
    button.append(el('span', '', c.label), el('span', 'count', c.count.toLocaleString()));
    button.addEventListener('click', () => { state.category = c.id; change(); });
    $('shelves').append(button);
  });
  function loadURL() {
    const p = new URLSearchParams(location.search);
    state.q = p.get('q') || '';
    state.category = shelves.some(s => s.id === p.get('category')) ? p.get('category') : '';
    state.genre = allGenres.includes(p.get('genre')) ? p.get('genre') : '';
    state.language = allLanguages.includes(p.get('language')) ? p.get('language') : '';
    state.format = allFormats.includes(p.get('format')) ? p.get('format') : '';
    state.sort = ['title','title-desc','author','size'].includes(p.get('sort')) ? p.get('sort') : 'title';
    state.page = Math.max(1, parseInt(p.get('page'), 10) || 1);
    $('query').value = state.q; ['genre','language','format','sort'].forEach(id => $(id).value = state[id]);
  }
  function updateURL() {
    const p = new URLSearchParams();
    for (const k of ['q','category','genre','language','format']) if (state[k]) p.set(k,state[k]);
    if (state.sort !== 'title') p.set('sort',state.sort);
    if (state.page !== 1) p.set('page',state.page);
    const query = p.toString();
    try { history.replaceState(null, '', location.pathname + (query ? '?' + query : '')); } catch (_) { /* file:// remains usable */ }
  }
  function card(book) {
    const article = el('article','book-card');
    const top = el('div','card-top');
    const monogram = el('span','book-monogram', [...book.title.replace(/^\W+/, '')][0] || 'B'); monogram.setAttribute('aria-hidden','true');
    top.append(monogram,el('span','category-label',book.categoryLabel));
    const title = el('h3','',book.title);
    const author = el('p','author',book.authors.join(' · '));
    const tags = el('div','tags');
    book.tags.slice(0,3).forEach(tag=>tags.append(el('span','tag',tag)));
    if (book.tags.length>3) tags.append(el('span','tag','+'+(book.tags.length-3)));
    const bottom = el('div','card-bottom');
    const format = book.format || 'EPUB';
    const link = el('a','download','Download '+format+' ↓'); link.href = book.downloadUrl; link.download = book.originalFile; link.setAttribute('aria-label','Download '+book.title+' as '+format);
    bottom.append(link,el('span','size',(book.bytes/1e6).toFixed(1)+' MB · '+(names[book.language] || book.language)));
    const details=el('details');details.append(el('summary','','Book details'));
    details.append(el('p','','Shelf: '+book.categoryBasis),el('p','','Original file: '+book.originalFile));
    if (book.tags.length) details.append(el('p','','All tags: '+book.tags.join(', ')));
    if (book.sourceUrl) { const source = el('a','','Source: '+book.source); source.href=book.sourceUrl; const paragraph=el('p');paragraph.append(source);details.append(paragraph); }
    const github=el('a','','View file on GitHub ↗');github.href=book.githubUrl;
    const gp=el('p');gp.append(github);details.append(gp);
    article.append(top,title,author,tags,bottom,details);return article;
  }
  function render() {
    const words=normalize(state.q.trim()).split(/\s+/).filter(Boolean);
    const found=searchable.filter(b => (!state.category || b.category===state.category) && (!state.genre || b.tags.includes(state.genre)) && (!state.language || b.language===state.language) && (!state.format || (b.format || 'EPUB')===state.format) && words.every(w=>b.search.includes(w)));
    found.sort((a,b)=>{
      if(state.sort==='size') return a.bytes-b.bytes || a.title.localeCompare(b.title,undefined,{numeric:true});
      if(state.sort==='author') return a.authors.join().localeCompare(b.authors.join()) || a.title.localeCompare(b.title,undefined,{numeric:true});
      return a.title.localeCompare(b.title,undefined,{numeric:true})*(state.sort==='title-desc'?-1:1);
    });
    const pages=Math.max(1,Math.ceil(found.length/pageSize));state.page=Math.min(state.page,pages);
    const start=(state.page-1)*pageSize;
    $('books').replaceChildren(...found.slice(start,start+pageSize).map(card));
    $('result-count').replaceChildren(el('strong','',found.length.toLocaleString()+' books'),document.createTextNode(found.length ? ` · Showing ${start+1}–${Math.min(start+pageSize,found.length)}` : ' · Try another search'));
    $('page-label').textContent=`Page ${state.page} of ${pages}`;
    $('previous').disabled=state.page<=1;$('next').disabled=state.page>=pages;
    $('empty').hidden=found.length>0;
    document.querySelector('.pagination').hidden=found.length===0;
    document.querySelectorAll('[data-category]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.category===state.category)));
    updateURL();
  }
  function change(){state.page=1;render();}
  function reset(){state={q:'',category:'',genre:'',language:'',format:'',sort:'title',page:1};$('query').value='';['genre','language','format','sort'].forEach(id=>$(id).value=state[id]);render();}
  $('search-form').addEventListener('submit',e=>{e.preventDefault();change();});
  $('query').addEventListener('input',e=>{state.q=e.target.value;change();});
  ['genre','language','format','sort'].forEach(id=>$(id).addEventListener('change',e=>{state[id]=e.target.value;change();}));
  ['reset','empty-reset'].forEach(id=>$(id).addEventListener('click',reset));
  for(const [id,delta] of [['previous',-1],['next',1]]) $(id).addEventListener('click',()=>{state.page+=delta;render();$('results').scrollIntoView({behavior:'smooth',block:'start'});$('results').focus({preventScroll:true});});
  window.addEventListener('popstate',()=>{loadURL();render();});
  $('total').textContent=data.count.toLocaleString();loadURL();render();
})();
