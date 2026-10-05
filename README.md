# Ragsak Manila Café concept website

An independent landing page and digital business card by Kelvin De Asis, with separate menu and privacy pages. Public files are in `dist/`. No database, booking service, runtime secrets, npm dependencies, or required build step. Node.js 22+ runs local checks and preview.

```powershell
Set-Location 'C:\KELVIN\Ragsak'
npm start
```

Open the printed local URL. In a second terminal, run `npm run check`. Stop preview with Ctrl+C.

| Edit | File |
|---|---|
| Landing page, navigation, contact details | `dist/index.html` |
| Menu introduction/photos | `dist/menu.html` |
| Menu rows and their source record | `Docs/evidence/menu-transcription.json`, then `npm run sync:menu` |
| Privacy notice | `dist/privacy.html` |
| Layout and reduced-motion styles | `dist/style.css` |
| Optional responsive link targets and reveal animations | `dist/site.js` |
| Served images and local fonts | `dist/assets/` |

The photo transcription displays historical printed figures, with a visible caution. It does not promise current prices or availability. The photographed menu is served from `dist/assets/breakfast-menu.webp` and `drinks-menu.webp`, with their watermark intact. The source menu JPGs are not in this checkout; provide them at the paths expected by `scripts/prepare-menu-images.py` if you need to regenerate those WebP files. The user-selected wall-sign photo, `images/menu/ragsak bg.jpg`, is optimized into `hero-sign-640.webp`, `hero-sign-960.webp` and `hero-sign-1536.webp`. The original is preserved; `scripts/prepare-hero-image.py` can rebuild these variants with Pillow. The homepage uses a dark cinematic hero, full-sign portrait-phone framing, orange menu CTA, short entrance animations, and native smooth scrolling. Earlier coffee-photo assets remain available for historical reference.

Read [the current Docs checklist](Docs/WEBSITE-UPDATE.md), [owner/source record](OWNER-REVIEW.md), [review results](REVIEW-REPORT.md), and [Cloudflare/Git update guide](DEPLOYMENT-GUIDE.md). The earlier PDF handbook is retained as an archived build record.

The latest menu preview and shared-table experience photos come from `images/menu/phase 3/`. Responsive WebP assets can be rebuilt with `scripts/prepare-phase3-images.py` and Pillow. See [the phase 3 photo mapping and review checklist](Docs/PHASE-3-PHOTOS.md); exact pictured dish/drink identities are unverified, so captions use broad categories only.

Internal navigation stays in the same tab. External websites/maps/social links open a new tab on desktop and the same tab on narrow or coarse-touch devices. Telephone links use the device handler. Without JavaScript, native links remain usable in the current tab. Content and the text menu remain readable without motion or scripts.

Search indexing is disabled for this independent concept. Its code includes no analytics, cookies, storage, forms, third-party widgets or embedded maps. Cloudflare hosting settings are separate; see the privacy notice before adding any services.
