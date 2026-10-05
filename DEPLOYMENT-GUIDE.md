# Edit and update the Cloudflare website

Updated October 4, 2026. The local Git remote is `https://github.com/KelvinDeAsis/Ragsak-Cafe.git`; the working branch is `main`. The user has reported a Cloudflare deployment. Its actual public URL and dashboard settings have not been inspected during this update. The former private Sites release is historical and does not automatically update when GitHub changes.

## Preview and check

1. Open the **whole** `C:\KELVIN\Ragsak` folder in VS Code.
2. Edit the files listed in `README.md`. Save them. If changing menu rows, update their evidence in `Docs/evidence/menu-transcription.json`, then run `npm run sync:menu`.
3. In the VS Code terminal, run:

```powershell
Set-Location 'C:\KELVIN\Ragsak'
npm run check
npm start
```

4. Open the printed local URL. Check desktop and phone widths, landing/menu/privacy pages, phone/maps/social links, and the exact footer disclaimer. `127.0.0.1` previews your computer; it is not the public Cloudflare address.
5. Resolve the remaining owner/hero/photo items in [Docs/WEBSITE-UPDATE.md](Docs/WEBSITE-UPDATE.md). Do not replace the requested hero with an unrelated image or claim a booking system exists.

## Save the changes to GitHub

In a second terminal, review what will be uploaded:

```powershell
Set-Location 'C:\KELVIN\Ragsak'
git status
git diff --stat
git diff
```

After reviewing the edits, stage the website, source records, tools, and documentation:

```powershell
git add dist scripts tests package.json README.md DEPLOYMENT-GUIDE.md OWNER-REVIEW.md REVIEW-REPORT.md Docs images
git diff --cached --stat
git commit -m "Improve Ragsak landing page, menu and privacy notice"
git push origin main
git log -1 --oneline
```

The text in quotes after `-m` is simply a short description of the saved changes. Do not type documentation into that field. A commit saves a local version; a push uploads that version to GitHub. Record the latest commit ID so you can compare it with Cloudflare.

If `git status` says there is nothing to commit, saved files may already be committed; check the latest commit and GitHub before retrying. If a push is rejected, fetch and inspect the remote changes; do not use a force push. Resolve the history difference before publishing.

## Cloudflare Pages settings and automatic updates

For this static project the expected configuration is:

| Setting | Value |
|---|---|
| Source repository | `KelvinDeAsis/Ragsak-Cafe` |
| Production branch | `main` |
| Root directory | Repository root |
| Framework preset | None |
| Build command | Blank; the checked-in site requires no build |
| Build output directory | `dist` |

If Cloudflare Pages is connected to this repository and automatic production deployments are enabled, pushing a new commit to `main` triggers deployment. Usually you do not need to click Redeploy. Open Workers & Pages → your Pages project → Deployments, and verify that the **new** deployment uses the commit ID printed by `git log -1 --oneline`.

After that deployment succeeds, open the production `pages.dev` address or configured custom domain. Verify the menu and privacy pages and use Ctrl+Shift+R if your browser shows cached files. Retrying an old successful deployment can redeploy old code, so always compare the source commit.

If the project was created by direct upload instead of Git integration, a GitHub push will not update it. Upload the contents of the checked `dist` folder as a new deployment, or configure a Git-integrated Pages project deliberately. The full repository belongs on GitHub; only `dist` is public website content. Never serve `Docs`, `images`, `.git`, or local artifacts as the website root.

## Public concept and privacy

The site identifies itself as an independent proposal on every page. It uses `noindex, nofollow` and a restrictive robots file; a public URL can still be visited, but search indexing is intentionally discouraged. Reconsider indexing and absolute canonical/social metadata only when the actual public domain and publication status are confirmed. Keep the concept disclaimer unless the owner explicitly authorizes an official site and the content is reviewed.

The source files add no analytics. Check Cloudflare settings separately before making privacy claims about host-level services. Update `privacy.html` if analytics, forms, embeds, or a booking service is actually added.

## Rollback

Choose a previously working production deployment in Cloudflare, or revert the offending Git commit, check the result and push the revert. Compare the resulting deployment commit and public page. Keep your source history; avoid force pushes or deleting work to perform a rollback.
