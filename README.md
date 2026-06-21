# Creative Studio MCP

<p>
  <a href="https://github.com/sponsors/Senseiglobal">
    <img src="https://img.shields.io/badge/Support%20Us-GitHub%20Sponsors-brightgreen?style=for-the-badge" alt="Support Us on GitHub Sponsors">
  </a>
</p>

Creative Studio MCP is a daily-use creative business workspace for quotes, payments, checklists, and project packages.

Developer: Thomas Ogun  
Organization: Senseiglobal  
Repository: https://github.com/Senseiglobal/creative-studio-mcp

## Use Without Claude

Download the ZIP file, extract it, then open the `creative-studio-mcp` folder.

Double-click:

```text
START_APP.bat
```

The app opens in your browser. Claude and OpenAI are not required.

## New Project Workflow

Use `New Project` to enter:

- Client name
- Service
- Design fee
- Upfront percent
- Project type

The app creates one project package with:

- Client quote
- Payment breakdown
- Project checklist
- Deliverables list
- Client email draft

## Local Saved Projects

Generated projects are saved locally in:

```text
projects.json
```

Recent projects appear on the dashboard.

## Optional Claude Or OpenAI Connection

Claude Desktop is optional.

Use:

```text
SETUP_WINDOWS.bat
```

OpenAI needs a remote MCP server URL, so use the local browser app first.

## Test The App

Double-click:

```text
TEST_APP.bat
```

If it says success, the app works.

## Keep Private

Do not share your `.env` file or API keys.
