Creative Studio MCP Installer Guide

This guide explains the beginner installer files included with Creative Studio MCP.

Installer Files

- Windows: install.bat
- Mac and Linux: install.sh

What The Installer Does

The installer helps beginners set up the project without typing many commands.

It will:

- Check that Python is installed
- Create a local workspace called .venv
- Install the required Python package from requirements.txt
- Create a .env file if one does not already exist
- Check that server.py can compile
- Show the next steps after setup

Windows Setup

1. Download the project from GitHub.
2. Extract the ZIP file.
3. Open the creative-studio-mcp folder.
4. Double-click install.bat.
5. Wait for the installation complete message.
6. Read QUICK_START.md for the next setup steps.

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
.venv\Scripts\python.exe server.py
```

On Mac and Linux:

```bash
.venv/bin/python server.py
```

If the setup worked, the server should start and listen for MCP messages.

Common Problems

Python is not found:

Install Python from https://www.python.org/downloads/ and make sure Python is added to PATH.

The installer cannot install requirements:

Check your internet connection and run the installer again.

.env already exists:

This is normal. The installer will not overwrite your existing .env file.

server.py has a syntax problem:

Check that you are using the latest project files from GitHub.

Important Safety Note

Do not share your .env file publicly. It may contain private keys or local configuration.
