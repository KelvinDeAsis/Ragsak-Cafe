# Phase 3 photograph update

October 4, 2026. Changes are local; this update does not publish a Cloudflare deployment.

## Photo selection

All four originals were visually inspected. Filenames alone are not evidence of a particular menu item. Images are assigned to broad categories, not named dishes. The rice-table photo is used for the breakfast preview, while the lamp-and-table photo is used for the café experience; this differs from the headings suggested by their filenames.

| Supplied filename in `images/menu/phase 3/` | Website placement | Safe description | Still unverified |
|---|---|---|---|
| `a cup for your kind of day.jpeg` | On the Menu: Coffee & drinks → espresso category | A cup of coffee on a café table | Exact coffee menu name; identities of surrounding dishes |
| `pull up a chair.jpeg` | On the Menu: All-day breakfast → breakfast category | Rice plates and colorful drinks on a café table | Exact dish/drink names, ingredients, and correspondence to individual printed menu entries |
| `save room for something sweet.jpg` | On the Menu: Croissant Collection → croissants category | A croissant dessert on a ceramic plate beside a warm lamp | Exact dessert name, toppings and ingredients; no Nutella/almond claim inferred |
| `a little more  than a coffee.jpg` (two spaces after `more`) | A Closer Look | A warm lamp beside plates on a patterned café table | Exact dish names/ingredients; intended branch and source provenance |

“A Closer Look” now says **Make time to gather.** Its copy describes the lamp, patterned tabletop, and shared-table experience. It no longer describes curtains or wooden chairs absent from this photograph, and does not repeat a dish list. Phone, café directions and Instagram reel actions remain usable.

## Optimization and implementation

- [x] Preserved every original; made EXIF-aware, proportional full-frame WebP derivatives with Pillow (quality 85, LANCZOS resize, method 6), without upscaling, retouching, or changing depicted food.
- [x] Added 480/960 px variants for all four photos and a 1152 px variant for the larger atmosphere photo. Browser `srcset`/`sizes` select an appropriate local resource; below-fold images load lazily with asynchronous decoding.
- [x] Added accurate intrinsic dimensions and descriptive alt text, avoiding unverified named dishes or ingredients.
- [x] Preserved the three-card desktop and stacked mobile layout, rounded frames, category links and existing gentle transitions. CSS cover framing keeps proportions without stretching; coffee/dessert focal positions keep their subjects prominent. Wider phones use taller, equal frames to limit cropping.
- [x] Left menu names/prices unchanged; the separate menu page continues to use its reviewed transcription and original photographed menus.
- [x] Fixed missing spaces in preview headings when mobile hides desktop line breaks.

The four 960 px variants total **647,058 bytes**, compared with **1,291,782 bytes** for the originals (about 50% smaller). Actual transfer varies with browser-selected size and screen density. Full file dimensions, sizes and SHA-256 hashes are recorded in [the asset manifest](evidence/phase3-assets.json). `scripts/prepare-phase3-images.py` reproduces these assets; Pillow is needed only for image maintenance, not hosting.

## Review checklist

- [x] Browser verification passed at eight viewport sizes (320×568, 390×844, 430×932, 740×360, 768×1024, 1024×768, 1440×900 and 1920×1080), including device densities 1–3. All 32 new-photo loads passed; card alignment and equal frame heights stayed consistent; no horizontal overflow or console errors were observed. Desktop/mobile screenshots were visually inspected for subject framing and text accuracy.
- [x] All three category cards navigate in the same tab on desktop and mobile (six navigation checks). The hero still keeps the next section below the initial viewport.
- [x] Four additional checks passed: reduced motion, no JavaScript, and 200% text at mobile/desktop widths. Photos remain visible and proportions intact, with no horizontal overflow. `npm run check` passed all four pages, 45 menu entries and 11 regression tests; Git whitespace checking passed.
- [ ] Owner/source: confirm exact names of every pictured dish/drink before adding named-item captions or ingredient/allergen claims. The new photos have no accompanying readable menu labels, so exact identity remains unverified.
- [ ] Owner/source: confirm image provenance, reuse permission and intended café branch. No source URL or capture date was supplied with these four files.
- [ ] Owner: confirm current menu availability and prices independently of the representative photos.
- [ ] Publish the reviewed local changes to the connected GitHub production branch, then check Cloudflare's deployed commit and public site using [the deployment guide](../DEPLOYMENT-GUIDE.md).

Browser results and desktop/mobile section screenshots are saved as `Docs/evidence/phase3-responsive.json` and `phase3-*.png`. The current review report summarizes verification. Older screenshots remain historical evidence of the preceding design.
