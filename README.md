# Creative Studio MCP

<p>
  <a href="https://github.com/sponsors/Senseiglobal">
    <img src="https://img.shields.io/badge/Support%20Us-GitHub%20Sponsors-brightgreen?style=for-the-badge" alt="Support Us on GitHub Sponsors">
  </a>
</p>

Creative Studio MCP is a local-first creative business workspace for quotes, project packages, payment breakdowns, checklists, deliverables, client email drafts, saved projects, exports, and brand preferences.

It works as a browser app on your computer and can also run as an MCP server for Claude Desktop.

## Scan To Open

Share this with Reddit, communities, or anyone who wants to open the repo quickly.

<p>
  <a href="https://github.com/Senseiglobal/creative-studio-mcp">
    <img src="assets/repo-qr.svg" alt="QR code linking to the Creative Studio MCP GitHub repository" width="180">
  </a>
</p>

## What It Does

- Creates client-ready project packages from a client name, service, fee, upfront percentage, and project type.
- Generates quotes, payment breakdowns, checklists, deliverables, and client email drafts.
- Saves recent projects locally in `projects.json`.
- Saves business settings and services locally in `brand_profile.json`.
- Exports saved projects as TXT, Markdown, or PDF from the app preview.
- Supports additional MCP export formats from the tool layer: HTML, JSON, CSV, and DOC.
- Keeps deleted projects in a local bin that can be reviewed or emptied.
- Uses a responsive three-region workspace with sidebar navigation, a main work area, and a preview inspector.
- Includes app logo, loading, favicon, mobile icon, and manifest assets in `assets/`.

## Start The Local App

On Windows:

```text
START_APP.bat
```

Or run directly:

```text
python local_app.py
```

The app opens in your browser on a local address. No Claude or OpenAI setup is required for the browser app.

## Main Views

- `Dashboard`: recent projects, quick actions, beginner guidance, and app status.
- `Projects`: create a full project package.
- `Quote`: create a standalone quote.
- `Payment`: calculate upfront and balance payments.
- `Checklist`: generate and edit checklist items.
- `Services`: view saved services and remove custom entries.
- `Settings`: update business details, payment terms, services, theme, accent color, and local memory preferences.
- `Clients`: planned client database placeholder.
- `Learn`: short in-app lessons for new users.

## Exports

The preview inspector can copy the latest result and export saved projects as:

- TXT
- Markdown
- PDF

Generated export files are saved in `exports/`. This folder is ignored by Git because exported files may contain private client information.

## Recent Fix Notes

This repo recently fixed the QR and preview export workflow:

- Replaced the generated QR code with the provided Adobe Express QR SVG.
- Embedded the QR code in `README.md`.
- Added editable Quote preview text.
- Added editable Client Email preview text.
- Updated exports so TXT, Markdown, and PDF use the edited preview text.
- Verified Python and browser JavaScript checks before pushing.

## Local Files

Creative Studio MCP creates these local runtime files:

- `brand_profile.json`: business profile, payment terms, currency, and saved services.
- `projects.json`: saved active projects.
- `deleted_projects.json`: deleted project bin.
- `exports/`: generated project export files.

These files are intentionally ignored by Git and should not be shared publicly.

## Claude Desktop

Claude Desktop support is optional.

On Windows, run:

```text
SETUP_WINDOWS.bat
```

If Claude was not open during setup, open Claude Desktop once and then run:

```text
CONNECT_CLAUDE.bat
```

After setup, fully quit Claude Desktop and open it again.

## MCP Tools

The MCP server exposes tools for:

- Brand profile management
- Service listing
- Quote generation
- Payment calculation
- Project checklist generation
- Project package creation
- Project saving and recent project lookup
- Project deletion and bin listing
- Bin emptying
- Project export

Run the server with:

```text
python server.py
```

## Privacy And Safety

Creative Studio MCP is local-first. The browser app does not upload your projects, exports, or brand profile. Review [SECURITY.md](SECURITY.md) and [SAFE_DOWNLOAD.md](SAFE_DOWNLOAD.md) before sharing builds with non-technical users.

## About Developer

<p>
  <img src="assets/thomas-ogun.jpg" alt="Thomas Ogun" width="140">
</p>

Creative Studio MCP is developed by Thomas Ogun under Senseiglobal.

- Developer Linktree: https://linktr.ee/thomasogun
- LinkedIn: https://www.linkedin.com/in/ogunthomas/
- GitHub Sponsors: https://github.com/sponsors/Senseiglobal

Support helps improve Creative Studio MCP with better exports, client management, invoice tools, templates, storage options, and future mobile app features.
