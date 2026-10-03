# Ragsak website: use, edit, and publish

Reviewed October 4, 2026 (Asia/Shanghai).

## Open the cloud website

[Ragsak Manila Cafe](https://ragsak-manila-cafe.kelvindeasis2323.chatgpt.site)

The existing site belongs to your account and is private. Sign in using its owner account to review it. Deployment and public sharing are separate settings; the review release preserves private access.

To make it available to customers, confirm current business details and photo reuse with the cafe, then tell Codex: “Make the existing Ragsak website public for customers.” Codex should change access on this same site, remove the private noindex directive, replace the private robots policy, add a sitemap, validate, and redeploy. Sending the private URL to a customer does not grant them access. Do not create a second site for this change.

## Preview locally

Open PowerShell and run:

```powershell
Set-Location 'C:\KELVIN\Ragsak'
npm start
```

Open `http://127.0.0.1:4187/`. Keep the terminal running during review. Refresh the browser after editing. Press Ctrl+C when finished. If this port is already in use, stop your earlier preview, or use a different local port:

```powershell
$env:PORT = '4188'
npm start
```

The preview runs on your computer only; stopping it does not stop the cloud website. No `npm install` or `npm run build` is needed for this project.

## Edit the site

| Change | File |
|---|---|
| Text, menu details, address, hours, phone, and links | `dist/index.html` |
| Colors, spacing, font sizes, mobile layouts, and photo crops | `dist/style.css` |
| Scroll reveals, reduced motion, and copyright year | `dist/site.js` |
| Photos and locally hosted fonts | `dist/assets/` |
| Missing-page message | `dist/404.html` |
| Business evidence and photo source URLs | `OWNER-REVIEW.md` |

Update every occurrence of an address or phone number, including the footer, Maps links, and the JSON-LD business data near the bottom of `index.html`. Keep canonical and business URLs aligned with the actual site address. Maintain descriptive alt text, width/height, and responsive image candidates when replacing photos. The current gallery and menu photos link to their recorded source posts.

After changing the JSON-LD block, refresh its security hash:

```powershell
npm run sync:csp
```

Then check the site:

```powershell
npm run check
```

Check on your phone as well as desktop. Test View Menu, the menu photograph, Find us, Get Directions, the phone link, keyboard navigation, and Back to top. Check with enlarged text. A passing automated check does not verify that business information is current.

## Publish future updates

Local edits are not automatically published. In this chat, ask: “Review my changes in C:\KELVIN\Ragsak and redeploy the existing Ragsak site, preserving its current access.”

Codex will open the existing site identified by `.openai/hosting.json`, run the relevant checks, push the exact source state, package `dist/`, and publish a saved version. Deployment is complete only when the hosting service reports success. Keep `.openai/hosting.json` linked to the existing site. Never add secrets to `dist/`, source control, screenshots, or documentation. This static site does not need API keys.

## Before public launch

1. Confirm the address and phone with the cafe.
2. Confirm opening days, closing time, and holiday hours. The recorded 10am–1am listing was not freshly verifiable during this review.
3. Obtain the current complete menu. Approve item names, prices, and availability. The existing photo contains historical prices and the page now warns visitors about that.
4. Confirm permission to reuse the logo and selected photos. Official profile attribution alone is not proof of reuse rights.
5. Choose public access and publish the corresponding indexing changes.

## Custom domain and recovery

You can keep the supplied cloud address. For a domain you already own, send Codex the exact domain; it can request the site's domain mapping and provide the DNS records returned by the host. Do not guess DNS targets. Keep the current URL until the host verifies the domain and HTTPS certificate; then update the canonical, business URL, robots/sitemap URLs, and redeploy.

If a release breaks navigation, images, or access, ask Codex to redeploy the last working saved version on this same site. The review started from saved version 2, source commit `d830f90fd16f9b28bc2210c9cfd6c55ce517e6fa`. Reverting local files alone does not roll back the hosted version. Use hosting version history, confirm successful deployment, and preserve the intended audience.

The site has no ordering, reservation, payment, contact form, database, analytics, or automated business-content refresh. Its menu and visit information need manual updates when the cafe changes them.
