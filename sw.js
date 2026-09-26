const CACHE='ssw-caregiver-v4-premium';
const CORE=[
 './','./index.html','./styles.css','./app.js','./manifest.json','./sw.js',
 './data/pages.json','./data/study.json','./data/curriculum.json','./data/mcq.json',
 './data/official-answer-key.json','./data/image-map.json','./data/japanese-questions.json','./data/visual-groups.json','./data/japanese-care.json'
];
self.addEventListener('install',event=>event.waitUntil((async()=>{
 const c=await caches.open(CACHE);
 await c.addAll(CORE);
 const map=await fetch('./data/image-map.json').then(r=>r.json());
 const jp=await fetch('./data/japanese-questions.json').then(r=>r.json());
 const assets=[...new Set([
   ...map.references.map(x=>'./assets/images/'+x.image),
   ...jp.questions.map(x=>'./assets/jp-pages/'+x.image)
 ])];
 await Promise.allSettled(assets.map(u=>c.add(u)));
 await self.skipWaiting();
})()));
self.addEventListener('activate',event=>event.waitUntil((async()=>{
 const keys=await caches.keys();await Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)));await self.clients.claim();
})()));
self.addEventListener('fetch',event=>event.respondWith(
 caches.match(event.request).then(cached=>cached||fetch(event.request).then(response=>{
   const copy=response.clone();caches.open(CACHE).then(c=>c.put(event.request,copy));return response;
 }).catch(()=>cached))
));
