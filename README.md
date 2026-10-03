# Ragsak Manila Cafe

A responsive static website hosted through Sites. Public files are in `dist/`. No build step, database, runtime secrets, or npm dependencies are required. Node.js 22 or later runs the local preview and checks.

From PowerShell:

```powershell
Set-Location 'C:\KELVIN\Ragsak'
npm start
```

Open the Local URL printed in the terminal. Press Ctrl+C to stop. In another terminal, run `npm run check` to validate links, assets, metadata, and animation behavior. See `DEPLOYMENT-GUIDE.md` for editing, publishing, and rollback instructions, and `REVIEW-REPORT.md` for the latest audit.

Business content and photo provenance are recorded in `OWNER-REVIEW.md`. Update that record along with website content. Preserve all original image attribution. Use `dist/index.html` for text/links, `dist/style.css` for layout, `dist/site.js` for reduced-motion-aware reveals, and `dist/assets/` for optimized images/fonts.

No booking or ordering integration is configured. No prices appear in website text. The photographed official menu contains historical published prices; confirm current prices directly with the cafe.
