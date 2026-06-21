# OpenAI and Other AI Apps

Creative Studio MCP is a local MCP server.

## Use Claude First

Claude Desktop is the easiest option because it can run this tool from your computer.

Use this setup:

1. `install.bat`
2. `CHECK_INSTALL.bat`
3. `CONNECT_CLAUDE.bat`
4. Restart Claude Desktop

## OpenAI

OpenAI works differently.

OpenAI needs a remote MCP server URL.

That means this project must be hosted online before OpenAI can connect to it through the API.

For now, use Claude Desktop for the live connection.

Later, deploy the project online and connect OpenAI to the remote server URL.

## Other MCP Apps

Use this pattern if your app supports local MCP servers:

```json
{
  "mcpServers": {
    "creative-studio-mcp": {
      "command": "C:\\FULL\\PATH\\TO\\creative-studio-mcp\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\FULL\\PATH\\TO\\creative-studio-mcp\\server.py"
      ]
    }
  }
}
```

Replace the path with your real project folder.
