import json
import shutil
from datetime import datetime
from pathlib import Path


def write_config(config_file: Path, python_path: Path, server_path: Path) -> None:
    config_file.parent.mkdir(parents=True, exist_ok=True)

    data = {}
    if config_file.exists() and config_file.read_text(encoding="utf-8").strip():
        try:
            data = json.loads(config_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            backup = config_file.with_name(f"claude_desktop_config.broken-{stamp}.json")
            shutil.copy2(config_file, backup)
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

    config_file.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main() -> int:
    project_dir = Path(__file__).resolve().parent
    python_path = project_dir / ".venv" / "Scripts" / "python.exe"
    server_path = project_dir / "server.py"

    print()
    print("Creative Studio MCP")
    print("Claude repair tool")
    print()
    print(f"Project folder: {project_dir}")
    print()

    if not python_path.exists():
        print("The installer has not finished yet.")
        print("Double-click install.bat first.")
        return 1

    if not server_path.exists():
        print("server.py is missing.")
        print("Make sure this file is inside the creative-studio-mcp folder.")
        return 1

    print("Checking the tool...")
    try:
        import server  # noqa: F401
    except Exception as exc:
        print("The tool could not load.")
        print(str(exc))
        print()
        print("Double-click install.bat again, then run this repair file.")
        return 1

    config_file = Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
    write_config(config_file, python_path, server_path)

    print()
    print("Claude config was updated.")
    print(f"Config file: {config_file}")
    print()
    print("Very important:")
    print("1. Fully close Claude Desktop.")
    print("2. If Claude is still in the taskbar tray, quit it there too.")
    print("3. Open Claude Desktop again.")
    print("4. Start a new chat.")
    print("5. Paste the test prompt from FIRST_CLAUDE_PROMPT.txt.")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
