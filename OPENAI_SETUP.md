# OpenAI And Other AI Apps

Creative Studio MCP is a local MCP server.

## Claude Desktop

Claude Desktop can run this tool from your computer.

Use:

```text
SETUP_WINDOWS.bat
```

## OpenAI

OpenAI needs a remote MCP server URL.

That means this project must be deployed online before OpenAI can connect to it through the API.

For now, use Claude Desktop for the easiest setup.

## Other MCP Apps

Use this pattern:

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
