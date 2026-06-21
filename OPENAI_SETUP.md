# OpenAI and Other AI Apps

Creative Studio MCP is a local MCP server.

That means it is easiest to connect with desktop apps that can run a local MCP server, such as Claude Desktop.

## Best Beginner Choice

Use Claude Desktop first.

On Windows:

1. Double-click `install.bat`
2. Double-click `CHECK_INSTALL.bat`
3. Double-click `CONNECT_CLAUDE.bat`
4. Fully close Claude Desktop
5. Open Claude Desktop again
6. Ask: `What services do we offer?`

## About OpenAI

OpenAI supports MCP through remote MCP servers in the Responses API.

This is different from Claude Desktop.

Claude Desktop can run this project from your computer.

OpenAI API needs a server URL, which means this project must first be deployed online as a remote MCP server.

## Simple OpenAI Path

For now, use one of these options:

1. Use Claude Desktop for the live MCP connection.
2. Copy results from Claude into ChatGPT when needed.
3. Ask a developer to deploy this project as a remote MCP server before connecting it to OpenAI.

## Other Apps

For any AI app that supports local MCP servers, use these values:

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

Replace `C:\\FULL\\PATH\\TO\\creative-studio-mcp` with the real folder path on your computer.

On Windows, you can use `CONNECT_CLAUDE.bat` to create the Claude Desktop version automatically.
