# McCasland Research Archive

This repository is a public-facing research archive on retired U.S. Air Force Maj. Gen. William Neil McCasland, the public reporting on his disappearance in February 2026, the theory connecting him to the X account `@TMBSpaceships`, the Ashton Forbes connection, and the hand-drawn schematic introduced into that discussion.

The project is designed to do two things at once:

- preserve the working research materials and captured source files;
- publish a readable website that separates documented fact from inference.

## Repo map

The repository is organized around four roles:

- [`docs/`](docs/): the public GitHub Pages site
- [`research/`](research/README.md): the main working analysis and compiled report source
- [`research/datasets/`](research/datasets/README.md): generated analysis package, structured outputs, and follow-up guides
- [`sources/`](sources/), [`research-targets/`](research-targets/), and [`artifacts/`](artifacts/README.md): captured source material, target downloads, scraper outputs, and evidence artifacts

## Public site

The GitHub Pages site lives in [`docs/`](docs/).

Key files:

- [`docs/index.html`](docs/index.html): public landing page
- [`docs/styles.css`](docs/styles.css): site styling
- [`docs/app.js`](docs/app.js): timeline, gallery, claim matrix, and source interactions
- [`docs/assets/docs/findings-report.pdf`](docs/assets/docs/findings-report.pdf): compiled report download

## Research materials

The underlying archive remains in the source directories:

- [`research/findings.md`](research/findings.md): main working brief
- [`research/trail-analysis.md`](research/trail-analysis.md): synthesis of the technical / nuclear / attribution trails
- [`research/timeline.md`](research/timeline.md): dated chronology
- [`research/findings-report.tex`](research/findings-report.tex): LaTeX source for the compiled report
- [`research/datasets/README.md`](research/datasets/README.md): generated analysis package index
- [`notes/claim-matrix.md`](notes/claim-matrix.md): claim-by-claim assessments
- [`sources/manifest.md`](sources/manifest.md): source inventory and capture notes
- [`sources/primary/`](sources/primary/): downloaded primary and near-primary records
- [`sources/context/`](sources/context/): downloaded context pages and public commentary captures
- [`research-targets/`](research-targets/): downloaded reading list, saved pages, media, and supporting technical references
- [`artifacts/evidence/`](artifacts/evidence): loose evidence artifacts used during analysis
- [`artifacts/x-scrape/`](artifacts/x-scrape): timestamped scraper outputs for public X profile capture runs

## Working model

This repository is best understood as:

1. a public casefile and publishing surface in `docs/`
2. a human-written research narrative in `research/` and `notes/`
3. a source archive in `sources/` and `research-targets/`
4. a generated analysis workspace in `research/datasets/` and `artifacts/`

Rule of thumb for future additions:

- put sourced narrative work in `research/` or `notes/`
- put captured evidence in `sources/` or `artifacts/evidence/`
- put generated analysis outputs in `research/datasets/`
- keep `docs/` limited to public-site assets

## Working standards

- Verified facts are attributed to captured sources whenever possible.
- Public speculation is labeled as speculation.
- The attribution of `@TMBSpaceships` to McCasland is treated as unconfirmed unless direct evidence appears.
- Gaps, blocked captures, and unresolved questions are documented rather than silently smoothed over.

## Local preview

To preview the public site locally from the repository root:

```powershell
Set-Location docs
python -m http.server 4173
```

Then open:

```text
http://127.0.0.1:4173/
```

## X scraping

The repo now includes a browser-based scraper for public X profile pages that does not use the X API:

- [`scripts/scrape_x_profile.py`](scripts/scrape_x_profile.py)

It uses Playwright to render the public profile timeline, scroll for status URLs, revisit each status page, and write out:

- `posts.json`: full scraped post records
- `links.json` and `links.csv`: extracted links
- `media.json` and `media.csv`: discovered image and thumbnail URLs
- `profile.json`: basic profile metadata
- `summary.json`: run totals

Install Chromium once if needed:

```powershell
python -m pip install playwright beautifulsoup4 lxml
python -m playwright install chromium
```

For authenticated scraping, add a local cookie file at `secrets/x-cookies.json`:

```json
{
  "auth_token": "YOUR_VALUE",
  "ct0": "YOUR_VALUE"
}
```

The scraper will load that file automatically when it exists.

Example runs:

```powershell
python scripts/scrape_x_profile.py TMBSPACESHIPS --tab posts --tab media
python scripts/scrape_x_profile.py TMBSPACESHIPS --tab posts --tab media --download-media
```

Note: on current guest sessions, X may block direct access to some profile tabs such as `media` or `replies`. The scraper now detects that case, skips the blocked tab, and continues with any tabs that are still publicly reachable.

Outputs are written under:

```text
artifacts/x-scrape/<handle>/<timestamp>/
```

## GitHub Pages

This repo includes a GitHub Actions workflow that deploys the contents of `docs/` to GitHub Pages.

Once the repository exists on GitHub:

1. Push the repo.
2. In GitHub, enable Pages with **GitHub Actions** as the source.
3. The workflow in [`.github/workflows/pages.yml`](.github/workflows/pages.yml) will publish the site automatically on pushes to `main`.
