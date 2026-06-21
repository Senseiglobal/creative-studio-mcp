# Quick Start

This is the short setup guide.

## Windows

Open the extracted `creative-studio-mcp` folder.

Double-click:

1. `install.bat`
2. `CHECK_INSTALL.bat`
3. `CONNECT_CLAUDE.bat`

Then fully close Claude Desktop and open it again.

Important: use Claude Desktop, not Claude in a web browser.

## First Test In Claude

Start a new Claude chat.

Paste this:

```text
Use the Creative Studio MCP tool to list our services.

If you can see the tool, show the service list.

If you cannot see the tool, tell me that Creative Studio MCP is not connected yet.
```

You can also open `FIRST_CLAUDE_PROMPT.txt` and copy the same prompt.

## If Claude Says It Has No Business Information

That means Claude did not use the tool.

Do this:

1. Close Claude Desktop completely.
2. Open the `creative-studio-mcp` folder.
3. Double-click `CHECK_INSTALL.bat`.
4. If it says success, double-click `CONNECT_CLAUDE.bat`.
5. Open Claude Desktop again.
6. Start a new chat.
7. Paste the first test prompt again.

## Do Not Do This

Do not run `Activate.ps1`.

Do not type `.venv` commands manually.

Do not run files from inside the ZIP preview.

Always extract the ZIP first.

## OpenAI Or ChatGPT

Claude Desktop is the easiest first option.

OpenAI needs this tool to be deployed online as a remote MCP server.

Read `OPENAI_SETUP.md` when you are ready for that.
