# Quick Start

Use this page after you extract the ZIP file.

Do not run setup files from inside the ZIP preview or a temporary folder.

## The 3 Click Setup On Windows

Open the `creative-studio-mcp` folder.

Then double-click these files in this order:

1. `install.bat`
2. `CHECK_INSTALL.bat`
3. `CONNECT_CLAUDE.bat`

After step 3:

1. Fully close Claude Desktop.
2. Open Claude Desktop again.
3. Ask Claude: `What services do we offer?`

That is the full beginner setup.

## What Not To Do

Do not type `.\.venv\Scripts\python.exe server.py` in PowerShell.

Do not open `Activate.ps1`.

Do not edit Claude settings by hand unless you are technical.

## If You Use OpenAI Or ChatGPT

OpenAI works differently from Claude Desktop.

Claude Desktop can run this tool directly from your computer.

OpenAI API needs a remote MCP server URL, so this project must be deployed online first.

For the simple explanation, read `OPENAI_SETUP.md`.

## Try It In Claude

After connection, ask Claude:

```text
What services do we offer?
```

Try:

```text
Create a quote for John Smith for Brand Identity Design at $3,000.
```

Try:

```text
Calculate the payment breakdown for a $5,000 project.
```

Try:

```text
Generate a project checklist for product packaging design.
```

## If Something Goes Wrong

### I see a red PowerShell error

Do not type commands manually.

Close PowerShell and double-click:

```text
CHECK_INSTALL.bat
```

If the check passes, double-click:

```text
CONNECT_CLAUDE.bat
```

If the check fails, double-click:

```text
install.bat
```

### I see an Activate.ps1 error

Ignore it. You do not need `Activate.ps1`.

The installer and checker use a safer method.

### I cannot find the project folder

Open the folder called:

```text
creative-studio-mcp
```

Then double-click:

```text
START_WINDOWS.bat
```

## What This Tool Can Do

- Show your services and pricing
- Create client quotes
- Calculate upfront and balance payments
- Generate project checklists
- Help standardize creative business workflows

## Keep This Private

Do not share your `.env` file.

Do not share screenshots that show your API key.
