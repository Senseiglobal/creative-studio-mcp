# Quick Start After Installation

This guide is for people who already ran `install.bat`.

If you have not installed yet, open `START_HERE.html` and follow the visual guide.

## What You Should See

After installation, the installer should show:

```text
Installation complete
Setup check passed
```

If you saw that, the tool is installed.

You do not need to type `.\.venv\Scripts\python.exe server.py` in PowerShell.

You do not need to open `Activate.ps1`.

## Step 1: Confirm The Tool Is Installed

On Windows, double-click:

```text
CHECK_INSTALL.bat
```

If everything is fine, you will see:

```text
Success. Creative Studio MCP is installed correctly.
```

## Step 2: Connect The Tool To Claude Desktop

Creative Studio MCP works best when connected to Claude Desktop.

1. Open Claude Desktop.
2. Open Claude Desktop settings.
3. Find the developer or tools configuration area.
4. Add Creative Studio MCP as a local MCP server.
5. Use the project file:

```text
server.py
```

If Claude asks for the folder, use the folder where this project is saved.

Example:

```text
C:\Users\User\creative-studio-mcp
```

## Step 3: Use It

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
START_HERE.html
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
