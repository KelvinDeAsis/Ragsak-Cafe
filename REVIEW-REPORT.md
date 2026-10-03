# Website review — October 4, 2026

Reviewed the complete Ragsak static website: source, navigation, content/source records, security exposure, accessibility, responsive layouts, image loading, metadata, local preview, and deployment configuration. The established orange, cream, red, and brown design is preserved.

## Issues fixed

| Finding | Change |
|---|---|
| The hero preloaded a fixed 960px image even when a mobile browser selected the 480px candidate | Preload now matches the hero's responsive candidates and size hints. Mobile selection verified as `coffee-480.webp`. |
| Gallery images lacked responsive candidates on wider/dense screens | Added matching local WebP srcsets and layout-specific size hints. |
| A focused card could remain invisible while awaiting its reveal animation | Keyboard focus reveals the card in both CSS and JavaScript. Observation failures restore all content. |
| Motion preference was only checked at page load | Switching to reduced motion restores pending cards and disconnects observation. Print rules expose every card. |
| Skip target was not explicitly focusable | The main landmark now accepts focus; Enter on Skip to content was verified to focus `main`. |
| Repeated and conflicting mobile navigation rules made changes fragile | Consolidated mobile navigation, retained the visible logo and four links, and increased link hit areas. |
| Small text and intrinsic grid sizing caused horizontal overflow when text was doubled | Converted font sizes to relative units, allowed grid items to shrink/wrap, and wrapped social/footer rows. |
| The historical menu photo could imply current prices | Added a visible caution associated with the menu-photo link. |
| The website said hours were currently listed without a fresh verification | Changed wording to “Previously listed” and kept the call-to-confirm guidance. |
| Footer logo repeated the accessible link name | Logo is decorative within the already named home link. |
| Static hosting had no explicit missing-page behavior | Added a branded 404 page and configured `404-page` handling. |
| Business structured data omitted the actual website/menu URL | Added URLs and verified alignment with the canonical URL. No unconfirmed opening days, branches, coordinates, or prices were added. |
| Content had no explicit browser resource policy | Added a restrictive meta CSP and a structured-data hash, plus a referrer policy. This is a document policy, not a substitute for host-level security headers. |
| Future releases had no repeatable checks or local workflow | Added dependency-free local preview, static validation, eight regression tests, and an editing/deployment guide. |

## Verification

- `npm run check`: HTML anchors/assets/metadata pass; eight animation and accessibility fallback tests pass.
- 11 image elements and all referenced local image/font/script/style assets exist. Font licenses are retained.
- Browser layouts checked at 320, 390, 700, approximately 701/702, 768, 1024, 1440, and 1920 pixels. No content overflow in normal layouts. Intentional clipped decorative ribbon text is excluded.
- Text doubled through the local QA stylesheet, including body text, checked at 320, 390, 768, 1024, and 1440 pixels. No content clips; the 768px result has a one-pixel rounding extension in page width.
- All seven internal navigation actions resolve to the expected anchors. The menu photograph opens and browser Back returns to the menu section.
- Without the site JavaScript, cards remain visible and menu navigation works. Eight regression tests cover viewport entry, keyboard focus, preference changes, missing APIs, and observer failures.
- Image loading and gallery responsive selection were reviewed in the browser. No browser errors or CSP violations appeared on reviewed routes.
- Primary color pairs retain approximately 5.16:1 brown/orange, 14.06:1 brown/cream, and 9.27:1 cream/red contrast.
- Local 404/error responses and the packaged archive are checked during release preparation. Deployment is considered complete only on a successful native hosting result.

## Remaining content checks

Facebook blocked fresh fetching and Instagram throttled it on October 4. Existing business evidence from October 1 remains recorded in `OWNER-REVIEW.md`; this review does not claim fresh verification. Confirm address, phone, opening days/hours, menu/prices/availability, and photo/logo reuse with the cafe before a customer launch.

The existing audience remains private. Private noindex/robots directives are intentional and must change together when public sharing is requested. A social-preview image is optional and was not generated during this review. Booking, ordering, payments, and forms are outside the site's existing capabilities.

This is a source and browser review, not a penetration test, screen-reader certification, or measured field Core Web Vitals report. No Lighthouse score or production traffic/performance measurement is claimed.

Screenshots and raw viewport/navigation observations are in the ignored local `artifacts/` directory. They are not included in the website's public assets.
