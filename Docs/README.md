# Ragsak documentation

Start with [the current website update and checklist](WEBSITE-UPDATE.md) for the landing page, separate menu/privacy pages, source limitations, and future reservation requirements. See [the current review report](../REVIEW-REPORT.md) and [Cloudflare update guide](../DEPLOYMENT-GUIDE.md).

The [illustrated PDF handbook](Ragsak-Technical-Documentation.pdf) and its [Markdown source](Ragsak-Technical-Documentation.md) are a historical snapshot of the earlier single-page build. They have not been regenerated for this update. Their diagram, deployment and menu descriptions should not be treated as the current implementation.

That historical handbook records the private Sites deployment, version 3, source commit `a28583be1ffb58736657525245dadc208bc5bc0c`. The user later deployed through Cloudflare; the current public URL/dashboard settings have not been inspected. Documentation changes do not publish the website.

## Contents

| File/folder | Purpose |
|---|---|
| [Current website update](WEBSITE-UPDATE.md) | Completed changes, current system design, outstanding facts/assets, and future ideas |
| [Phase 3 photographs](PHASE-3-PHOTOS.md) | Photo-to-category mapping, optimization, current section screenshots, and uncertain item identities |
| [Menu transcription](evidence/menu-transcription.json) | Reviewed menu names, printed figures, source references, and uncertainties; input to `npm run sync:menu` |
| `evidence/redesign-*.json` and `redesign-*.png` | Current browser validation and screenshots |
| [PDF handbook](Ragsak-Technical-Documentation.pdf) | Complete build history, system design, content model, workflow, review, release, and maintenance handbook |
| [Markdown source](Ragsak-Technical-Documentation.md) | Editable source for the handbook |
| `diagrams/` | Four architecture, content-model, runtime-flow, and development-workflow diagrams, each as PNG and SVG |
| `evidence/` | Existing release screenshots, viewport/navigation observations, deployment record, and an asset inventory |
| `reference/` | Copies of the earlier owner, review, and deployment records for a self-contained handoff |
| `tools/build_docs.py` | Rebuilds diagram images, inventory, and PDF from the Markdown source |
| `tools/requirements.txt` | Python libraries used by the documentation generator only |

## Diagrams

| Diagram | Image | Vector |
|---|---|---|
| System architecture | [PNG](diagrams/system-architecture.png) | [SVG](diagrams/system-architecture.svg) |
| Content model | [PNG](diagrams/content-model.png) | [SVG](diagrams/content-model.svg) |
| Visitor/runtime flow | [PNG](diagrams/runtime-flow.png) | [SVG](diagrams/runtime-flow.svg) |
| Development and deployment | [PNG](diagrams/development-workflow.png) | [SVG](diagrams/development-workflow.svg) |

## Rebuild

The website does not depend on the documentation generator. For a documentation rebuild, use Python with the libraries in `tools/requirements.txt` and Poppler's `pdftoppm` on PATH:

```powershell
Set-Location 'C:\KELVIN\Ragsak'
python -m pip install -r Docs/tools/requirements.txt
python Docs/tools/build_docs.py
```

The script uses Windows Segoe UI and Consolas when available, with standard PDF font fallbacks. It checks the project files for inventory data, copies the existing evidence, renders diagram PNGs, and exports the PDF. Local output remains in `Docs`. Rendered QA pages are temporary and are not part of the handoff.

Edit the Markdown and diagram definitions in the builder when project behavior changes. Recheck dates, source commit, current access, and recorded release information; rebuilding a PDF alone does not reverify the live deployment.
