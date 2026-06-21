import json
import shutil
from datetime import datetime
from pathlib import Path


def main() -> int:
    project_dir = Path(__file__).resolve().parent
    python_path = project_dir / ".venv" / "Scripts" / "python.exe"
    server_path = project_dir / "server.py"

    print()
    print("Creative Studio MCP")
    print("Claude Desktop connection helper")
    print()
    print(f"Project folder: {project_dir}")
    print()

    if not python_path.exists():
        print("Setup is not complete yet.")
        print("Please double-click install.bat first, then run CONNECT_CLAUDE.bat again.")
        return 1

    if not server_path.exists():
        print("server.py is missing.")
        print("Please make sure this file is inside the creative-studio-mcp folder.")
        return 1

    config_dir = Path.home() / "AppData" / "Roaming" / "Claude"
    config_file = config_dir / "claude_desktop_config.json"
    config_dir.mkdir(parents=True, exist_ok=True)

    data = {}
    if config_file.exists() and config_file.read_text(encoding="utf-8").strip():
        try:
            data = json.loads(config_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            backup = config_file.with_name(f"claude_desktop_config.broken-{stamp}.json")
            shutil.copy2(config_file, backup)
            print("Your old Claude config could not be read.")
            print(f"A backup was saved here: {backup}")
            data = {}

    if not isinstance(data, dict):
        data = {}

    servers = data.setdefault("mcpServers", {})
    servers["creative-studio-mcp"] = {
        "command": str(python_path),
        "args": [str(server_path)],
    }

    if config_file.exists():
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = config_file.with_name(f"claude_desktop_config.backup-{stamp}.json")
        shutil.copy2(config_file, backup)
        print(f"Backup saved: {backup}")

    config_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    print()
    print("Claude Desktop is now connected to Creative Studio MCP.")
    print()
    print("Next steps:")
    print("1. Fully close Claude Desktop.")
    print("2. Open Claude Desktop again.")
    print("3. Ask: What services do we offer?")
    print()
    print(f"Config file updated: {config_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
