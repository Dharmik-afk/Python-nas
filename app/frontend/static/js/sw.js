/* Service Worker for Media Vault - Performance Infrastructure */
const CACHE_NAME = 'media-vault-v1';
const MEDIA_EXTENSIONS = /\.(mp4|webm|ogg|mp3|wav|jpg|jpeg|png|gif|webp|svg|ico)$/i;

self.addEventListener('install', (event) => {
    event.waitUntil(self.skipWaiting());
});

self.addEventListener('activate', (event) => {
    event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);

    // Only intercept same-origin media requests or thumbnails
    if (url.origin === self.location.origin && (MEDIA_EXTENSIONS.test(url.pathname) || url.search.includes('thumb'))) {
        if (event.request.headers.get('range')) {
            event.respondWith(handleRangeRequest(event.request));
        } else {
            event.respondWith(handleRegularRequest(event.request));
        }
    }
});

async function handleRegularRequest(request) {
    const cache = await caches.open(CACHE_NAME);
    const cachedResponse = await cache.match(request);
    
    if (cachedResponse) {
        return cachedResponse;
    }

    try {
        const networkResponse = await fetch(request);
        // Cache successful responses for media
        if (networkResponse.ok && networkResponse.status !== 206) {
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    } catch (error) {
        console.error('[SW] Fetch failed:', error);
        return Response.error();
    }
}

/**
 * Handles Range Requests.
 * If the full file is in cache, it serves the requested slice.
 * Otherwise, it fetches from the network.
 */
async function handleRangeRequest(request) {
    const cache = await caches.open(CACHE_NAME);
    const cachedResponse = await cache.match(request.url, { ignoreSearch: true });

    if (cachedResponse && cachedResponse.status === 200) {
        const rangeHeader = request.headers.get('range');
        const totalSize = parseInt(cachedResponse.headers.get('content-length'));
        
        const parts = rangeHeader.replace(/bytes=/, "").split("-");
        const start = parseInt(parts[0], 10);
        const end = parts[1] ? parseInt(parts[1], 10) : totalSize - 1;

        const blob = await cachedResponse.blob();
        const slice = blob.slice(start, end + 1);

        return new Response(slice, {
            status: 206,
            statusText: 'Partial Content',
            headers: new Headers({
                'Content-Type': cachedResponse.headers.get('Content-Type'),
                'Content-Range': `bytes ${start}-${end}/${totalSize}`,
                'Content-Length': slice.size.toString(),
                'Accept-Ranges': 'bytes',
                'Cache-Control': 'public, max-age=31536000'
            })
        });
    }

    // Fallback to network if not in cache or if it's already a partial response
    return fetch(request);
}
