/**
 * Cloudflare Worker: Subdomain Rewrite Gateway for gov.edlconstructionpvtltd.in
 * 
 * - Rewrites root '/' to '/gov' transparently (status 200) without redirecting the browser.
 * - Routes clean sub-paths like '/tenders' or '/infrastructure' to '/gov/tenders' and '/gov/infrastructure'.
 * - Preserves static assets, icons, fonts, CSS, JS, and image requests without modification.
 * - Forwards requests to the main origin host while preserving query params and HTTP headers.
 */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const hostname = url.hostname.toLowerCase();

    // Target apex or primary origin host where the Astro static build is hosted
    // (Can be overridden via env.ORIGIN_HOSTNAME if configured in wrangler.toml)
    const originHost = env?.ORIGIN_HOSTNAME || 'edlconstructionpvtltd.in';

    // Check if the request is targeting the gov subdomain
    const isGovSubdomain = hostname.startsWith('gov.');

    if (isGovSubdomain) {
      const pathname = url.pathname;

      // Allow static files, Astro assets, and media to pass through untouched
      const isStaticAsset = (
        pathname.startsWith('/_astro/') ||
        pathname.startsWith('/frames/') ||
        pathname.startsWith('/frames-v1/') ||
        pathname.endsWith('.ico') ||
        pathname.endsWith('.jpeg') ||
        pathname.endsWith('.jpg') ||
        pathname.endsWith('.png') ||
        pathname.endsWith('.svg') ||
        pathname.endsWith('.webp') ||
        pathname.endsWith('.css') ||
        pathname.endsWith('.js') ||
        pathname.endsWith('.woff') ||
        pathname.endsWith('.woff2') ||
        pathname.endsWith('.ttf')
      );

      if (!isStaticAsset) {
        if (pathname === '/' || pathname === '') {
          // In Astro static builds, /gov/ is the directory index
          url.pathname = '/gov/';
        } else if (!pathname.startsWith('/gov')) {
          // Map /tenders -> /gov/tenders, /compliance -> /gov/compliance
          url.pathname = `/gov${pathname.endsWith('/') ? pathname : pathname + '/'}`;
        }
      }
    }

    // Set destination host to origin
    url.hostname = originHost;

    // Clone request with updated URL and host headers
    const newHeaders = new Headers(request.headers);
    newHeaders.set('Host', originHost);
    newHeaders.set('X-Forwarded-Host', hostname);

    const modifiedRequest = new Request(url.toString(), {
      method: request.method,
      headers: newHeaders,
      body: request.body,
      redirect: 'manual' // Do not automatically follow redirects so we can intercept and clean them
    });

    try {
      let response = await fetch(modifiedRequest);

      // If the origin responded with a redirect (e.g. 301/308 from /gov to /gov/)
      if ([301, 302, 307, 308].includes(response.status) && isGovSubdomain) {
        const location = response.headers.get('Location');
        if (location) {
          const locUrl = new URL(location, url.origin);
          
          // If the origin redirects from /gov to /gov/, fetch /gov/ directly behind the scenes
          if (locUrl.pathname === '/gov/' || locUrl.pathname === '/gov') {
            url.pathname = '/gov/';
            return await fetch(new Request(url.toString(), {
              method: request.method,
              headers: newHeaders,
              body: request.body,
              redirect: 'follow'
            }));
          }

          // Otherwise, rewrite any /gov/ prefixes out of the redirected location header
          let newLoc = locUrl.pathname.replace(/^\/gov(\/|$)/, '/');
          const respHeaders = new Headers(response.headers);
          respHeaders.set('Location', newLoc + locUrl.search + locUrl.hash);
          return new Response(response.body, {
            status: response.status,
            statusText: response.statusText,
            headers: respHeaders
          });
        }
      }

      return response;
    } catch (err) {
      return new Response(`Gateway error connecting to origin: ${err.message}`, { status: 502 });
    }
  }
};
