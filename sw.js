/* 诗径 PWA Service Worker — 离线缓存(山里信号差是刚需) */
const CACHE = 'shijing-v1';

/* App 壳 + 数据 + 地图库 + 图标,首次访问即预缓存 */
const CORE = [
  './',
  './index.html',
  './manifest.json',
  './data/poems.json',
  './data/trail-gushan.json',
  './data/trail-lingyin.json',
  './data/trail-qiantang.json',
  './data/trail-xihu-scatter.json',
  './icons/icon-180.png',
  './icons/icon-192.png',
  './icons/icon-512.png',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c =>
      /* 逐个 add,单个失败(如 CDN 偶发)不拖垮整体安装 */
      Promise.allSettled(CORE.map(u => c.add(u)))
    ).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  /* 地图瓦片(CartoDB):缓存优先 + 后台更新,实地省流量、断网仍显示已缓存区域 */
  const isTile = /basemaps|cartocdn|tile/.test(url.hostname) || /\.png($|\?)/.test(url.pathname) && url.hostname.includes('cartocdn');

  /* 本站资源 & 数据:缓存优先,命中即返回,后台静默更新 */
  e.respondWith(
    caches.match(req).then(cached => {
      const network = fetch(req).then(res => {
        if (res && (res.ok || res.type === 'opaque')) {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(req, copy)).catch(()=>{});
        }
        return res;
      }).catch(() => cached); /* 断网时回落缓存 */
      return cached || network;
    })
  );
});
