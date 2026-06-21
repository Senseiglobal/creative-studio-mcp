# Creative Studio MCP

<p>
  <a href="https://github.com/sponsors/Senseiglobal">
    <img src="https://img.shields.io/badge/Support%20Us-GitHub%20Sponsors-brightgreen?style=for-the-badge" alt="Support Us on GitHub Sponsors">
  </a>
</p>

Creative Studio MCP is a local-first creative business workspace for quotes, payments, checklists, project packages, and business preferences.

## Install

1. Download the ZIP file from GitHub.
2. Right-click the ZIP file.
3. Choose `Extract All`.
4. Open the extracted `creative-studio-mcp` folder.

## Start Local App

Double-click:

```text
START_APP.bat
```

The app opens in your browser and works without Claude or OpenAI.

## Create First Project

1. Click `Business Settings`.
2. Save your business name, payment terms, and services.
3. Click `New Project`.
4. Fill in the client and project details.
5. Click `Generate`.
6. Copy the quote, email draft, or full package.

## Optional Claude Or OpenAI Connection

Claude Desktop is optional.

Use:

```text
SETUP_WINDOWS.bat
```

OpenAI needs a remote MCP server URL, so deploy the project online before connecting OpenAI.

## Troubleshooting

If the app does not open, double-click:

```text
TEST_APP.bat
```

If Claude cannot see the tool, use the local app first. The local app is the main reliable version.

## Local Files

- `brand_profile.json` stores business preferences.
- `projects.json` stores saved projects.

Do not share these files if they contain private business information.
