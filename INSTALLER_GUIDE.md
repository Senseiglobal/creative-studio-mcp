Creative Studio MCP Installer Guide

This guide explains the beginner installer files included with Creative Studio MCP.

For a visual setup guide, open START_HERE.html.

Installer Files

- Windows start page launcher: START_WINDOWS.bat
- Windows: install.bat
- Windows setup check: CHECK_INSTALL.bat
- Mac and Linux: install.sh

What The Installer Does

The installer helps beginners set up the project without typing many commands.

It will:

- Set up the project
- Check that the setup works
- Show the next steps in plain language
- Create a .env file if one does not already exist
- Avoid confusing PowerShell activation commands

Important Folder Step

Run the installer from inside the creative-studio-mcp folder.

If you downloaded a ZIP file, extract it first. Do not run START_HERE.html, install.bat, or CHECK_INSTALL.bat from inside the ZIP preview or a temporary folder.

If your terminal shows this:

```powershell
PS C:\Users\User>
```

you are probably in the wrong folder.

It should look more like this:

```powershell
PS C:\Users\User\creative-studio-mcp>
```

To fix it, open the creative-studio-mcp folder in File Explorer, click the address bar, type `powershell`, and press Enter. This opens PowerShell in the correct folder.

You can also run:

```powershell
cd "C:\Users\User\creative-studio-mcp"
```

If your folder is in Downloads, use that path instead:

```powershell
cd "C:\Users\User\Downloads\creative-studio-mcp"
```

Windows Setup

1. Download the project from GitHub.
2. Right-click the ZIP file and choose Extract All.
3. Open the creative-studio-mcp folder.
4. Double-click START_WINDOWS.bat.
5. Follow the three short steps on the page.

Mac and Linux Setup

1. Download the project from GitHub.
2. Extract the ZIP file.
3. Open Terminal inside the creative-studio-mcp folder.
4. Run:

```bash
bash install.sh
```

5. Wait for the installation complete message.
6. Read QUICK_START.md for the next setup steps.

Testing The Server

On Windows:

```powershell
cd "C:\Users\User\creative-studio-mcp"
.\.venv\Scripts\python.exe server.py
```

On Mac and Linux:

```bash
cd ~/creative-studio-mcp
.venv/bin/python server.py
```

If the setup worked, the server should start and listen for MCP messages.

Common Problems

Python is not found:

Install Python from https://www.python.org/downloads/ and make sure Python is added to PATH.

The installer cannot install requirements:

Check your internet connection and run the installer again.

PowerShell says .venv is not recognized:

You are in the wrong folder. Open the creative-studio-mcp folder, click the address bar, type `powershell`, press Enter, and try again.

PowerShell says Activate.ps1 cannot be loaded:

This is a Windows security setting. You do not need to run Activate.ps1. Use:

```powershell
.\.venv\Scripts\python.exe server.py
```

The Windows installer uses this safer method automatically.

.env already exists:

This is normal. The installer will not overwrite your existing .env file.

server.py has a syntax problem:

Check that you are using the latest project files from GitHub.

Important Safety Note

Do not share your .env file publicly. It may contain private keys or local configuration.
