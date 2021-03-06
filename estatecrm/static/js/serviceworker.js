const VERSION = '1';
const staticCachePrefix = 'gen-static';
const staticCacheName = `${staticCachePrefix}-${VERSION}`;
const dynamicCacheName = 'gen-dynamic';
const appShell = [
  '/',
  '/base',
  '/static/css/styles.css',
  '/static/js/main.js',
  '/manifest.json',
  '/static/images/yeneses_pwa_192px.png',
  '/static/images/yeneses_pwa_160px.png',
  '/static/images/yeneses_pwa_512px.png',
  '/static/images/yeneses_landing.png',
  'https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css'
];

const maxNumberItemsDynamicCache = 100;
const urlsToCacheTimes = new Map();
// In milliseconds.
const networkWaitTime = 2000;

// INSTALLING THE SERVICE WORKER AND PRECACHING APPSHELL
self.addEventListener('install', function(event) {
  console.log('[SW] Installing SW version:', VERSION);
  event.waitUntil(
    caches.open(staticCacheName).then(function(cache) {
      console.log('[SW] Caching app shell');
      return cache.addAll(appShell);
    })
  );
});


// ACTIVATE THE SERVICE WORKER
self.addEventListener('activate', function(event) {
  console.log('[SW] Service Worker activated');
  event.waitUntil(
    caches.keys()
    .then(function(keyList) {
      return Promise.all(keyList.map(function(key) {
        if (key !== staticCacheName && key !== dynamicCacheName) { // If old cache exists
          console.log('[Service Worker] Deleting old cache', key);
          return caches.delete(key);  // Delete it and replace by new one
        }
      }));
    })
  );
  return self.clients.claim();
});


// MAIN SERVICE WORKER
self.addEventListener('fetch', (event) => {
  // Let the browser do its default thing
  // for non-GET requests.
  if (event.request.method !== 'GET') {
      return;
  }

  event.respondWith(
      networkThenCache(event),
  );
});

function networkThenCache(event) {
  // Always get the app shell from the cache.
  if (appShell.includes(event.request.url)) {
      console.log('[SW] Requested file from app shell, serving from the cache.');
      return getFromCache(event);
  }

  return Promise.race([
      tryToFetchAndSaveInCache(event, dynamicCacheName),
      new Promise((resolve, reject) => setTimeout(reject, networkWaitTime))
  ])
      .then(
          (response) => response,
          () => getFromCache(event).catch(() => provideOfflineFallback(event))
      );
}


function getFromCache(event) {
  return caches.match(event.request)
      .then((response) => {
          console.log(`[SW] Requesting ${event.request.url}.`);
          // If we have the response in the cache, we return it.
          // If not, we try to fetch it.
          if (response) {
              console.log(`[SW] Served response to ${event.request.url} from the cache.`);
              return response;
          }

          return Promise.reject();
      });
}


function tryToFetchAndSaveInCache(event, cacheName) {
  return fetchAndSaveInCache(event, cacheName)
      .catch(err => {
          console.warn('[SW] Network request failed, app is probably offline', err);
          return provideOfflineFallback(event)
              .catch(err => console.warn('[SW] failed to get response from network and cache.', err));
      });
}

function fetchAndSaveInCache(event, cacheName) {
  console.log(`[SW] Fetching ${event.request.url}`);
  return fetch(event.request)
      .then(res => {
          const requestSucceeded = res.status >= 200 && res.status <= 300;
          const cacheHeader = res.headers.get('cache-control') || [];
          const mustNotCache = cacheHeader.includes('no-cache');
          if (!requestSucceeded) {
              console.log('[SW] Request failed.');
              return res;
          } else if (mustNotCache) {
              console.log('[SW] The page must not be cached.');
              return res;
          }

          return caches.open(cacheName)
              .then(cache => {
                  // We can read a response only once. So if we don't clone it here,
                  // we won't be able to see anything in the browser.
                  cache.put(event.request.url, res.clone())
                      .then(() => {
                          urlsToCacheTimes.set(event.request.url, Date.now());
                          return trimCache(cache, maxNumberItemsDynamicCache, urlsToCacheTimes);
                      });

                  return res;
              });
      });
}


function trimCache(cache, maxItems, cacheTimeInfos) {
  if (cacheTimeInfos.size <= maxItems) {
      console.log('[SW] Nothing to trim from the cache.');
      return Promise.resolve();
  }

  // We sort all entries by descending dates.
  // We keep a slice of the maxItems more recent items.
  const urlsToKeep = Array.from(cacheTimeInfos.entries())
      .sort((a, b) => a[1] - b[1])
      .reverse()
      .slice(0, maxItems)
      .map(([url, _]) => url);

  console.log('[SW] Keeping in cache', urlsToKeep);
  return cache.keys()
      .then((keys) => {
          const deletions = keys.map(key => {
              if (urlsToKeep.includes(key.url)) {
                  return Promise.resolve();
              }

              console.log(`[SW] Removing ${key.url} from the cache.`);
              cacheTimeInfos.delete(key.url);
              return cache.delete(key);
          });
          return Promise.all(deletions);
      })
      .then(() => console.log('[SW] Done trimming cache.'))
      .catch(() => console.log('[SW] Error while trimming cache.'));
}

function provideOfflineFallback(event) {
  return caches.open(staticCacheName)
      .then((cache) => {
          // If the request expects an HTML response, we display the offline page.
          if (event.request.headers.get('accept').includes('text/html')) {
              console.log(event.request.headers)
              console.log('!!!')
              return cache.match('/');
          }

          return Promise.reject();
      });
}







// self.addEventListener('fetch', function(event) {
//   if (event.request.method !== 'GET') {
//     return;
//   }
//   // var requestUrl = new URL(event.request.url);
//   //   if (requestUrl.origin === location.origin) {
//   //     if ((requestUrl.pathname === '/')) {
//   //       event.respondWith(caches.match('/'));
        
//   //       return;
//   //     }
//   //   }

//   event.respondWith(
//     caches.match(event.request)
//         .then(response => {
//           if (response){
//             console.log(`[SW] Served response to ${event.request.url} from the cache.`);
//             return response;
//           }

//           return fetch(event.request)
//             .then(res=>{
//               const requestSucceeded = (res.status >= 200 && res.status <= 300);
//               if (!requestSucceeded) {
//                   return res;
//               }
              
//               return caches.open(dynamicCacheName)
//                 .then(cache =>{
//                   // We can read a response only once. So if we don't clone it here,
//                   // we won't be able to see anything in the browser.
//                   cache.put(event.request.url, res.clone());
//                   return res;
//                 });
//             })
//             .catch(err => {
//               console.warn('[SW] Network request failed, app is probably offline', err);
//               return caches.open(staticCacheName)
//                   .then((cache) => {
//                       // If the request expects an HTML response, we display the offline page.
//                       if (event.request.headers.get('accept').includes('text/html')) {
//                           return cache.match('/');
//                       }
          
//                       return Promise.reject();
//                   })
//                   .catch(err => console.warn('[SW] failed to get response from network and cache.', err));
//           });
//         })
//   );
//     // event.respondWith(
//     //   caches.match(event.request).then(function(response) {
//     //     return response || fetch(event.request);
//     //   })
//     // );
// });