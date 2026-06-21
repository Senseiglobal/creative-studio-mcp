import json
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


SERVER_NAME = "creative-studio-mcp"


def read_json(path: Path) -> dict:
    if not path.exists() or not path.read_text(encoding="utf-8").strip():
        return {}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = path.with_name(f"{path.stem}.broken-{stamp}{path.suffix}")
        shutil.copy2(path, backup)
        print(f"Old unreadable config backed up: {backup}")
        return {}


def write_config(path: Path, python_path: Path, server_path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    data = read_json(path)
    servers = data.setdefault("mcpServers", {})
    servers[SERVER_NAME] = {
        "command": str(python_path),
        "args": [str(server_path)],
    }

    if path.exists():
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = path.with_name(f"{path.stem}.backup-{stamp}{path.suffix}")
        shutil.copy2(path, backup)

    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def find_claude_configs() -> list[Path]:
    targets: list[Path] = []

    appdata = os.environ.get("APPDATA")
    if appdata:
        targets.append(Path(appdata) / "Claude" / "claude_desktop_config.json")

    localappdata = os.environ.get("LOCALAPPDATA")
    if localappdata:
        packages = Path(localappdata) / "Packages"
        if packages.exists():
            for item in packages.glob("Claude_*"):
                targets.append(
                    item
                    / "LocalCache"
                    / "Roaming"
                    / "Claude"
                    / "claude_desktop_config.json"
                )

    unique: list[Path] = []
    seen: set[str] = set()
    for target in targets:
        key = str(target).lower()
        if key not in seen:
            seen.add(key)
            unique.append(target)
    return unique


def claude_running() -> bool:
    try:
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq Claude.exe"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except Exception:
        return False
    return "Claude.exe" in result.stdout


def main() -> int:
    project_dir = Path(__file__).resolve().parent
    python_path = project_dir / ".venv" / "Scripts" / "python.exe"
    server_path = project_dir / "server.py"

    print()
    print("Creative Studio MCP")
    print("Claude connection setup")
    print()
    print(f"Project folder: {project_dir}")

    if not python_path.exists():
        print()
        print("Setup is not complete yet.")
        print("Double-click SETUP_WINDOWS.bat first.")
        return 1

    if not server_path.exists():
        print()
        print("server.py is missing.")
        print("Make sure all project files are in the creative-studio-mcp folder.")
        return 1

    print()
    print("Checking the tool...")
    try:
        import server  # noqa: F401
    except Exception as exc:
        print("The tool could not load.")
        print(str(exc))
        print()
        print("Run SETUP_WINDOWS.bat again.")
        return 1

    configs = find_claude_configs()
    if not configs:
        print("No Claude folder was found yet.")
        print("Install and open Claude Desktop once, then run this again.")
        return 1

    print()
    print("Writing Claude config...")
    for config in configs:
        write_config(config, python_path, server_path)
        print(f"Updated: {config}")

    print()
    print("Connection file is ready.")
    print()

    if claude_running():
        print("Claude Desktop is currently open.")
        print("Fully quit Claude Desktop now, then open it again.")
    else:
        print("Open Claude Desktop now.")

    print()
    print("First test prompt:")
    print("Use the Creative Studio MCP tool to list our services.")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
