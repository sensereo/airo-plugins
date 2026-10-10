"""Check this small preview package without loading credentials or using a network."""

import json
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_FILES = {
    ".gitignore",
    "README.md",
    ".agents/plugins/marketplace.json",
    "plugins/airo/.codex-plugin/plugin.json",
    "plugins/airo/.mcp.json",
    "plugins/airo/assets/airo-icon.svg",
    "plugins/airo/skills/airo-shared-readings/SKILL.md",
    "scripts/validate_package.py",
}


def require(condition, message):
    if not condition:
        raise SystemExit(f"Invalid package: {message}")


def read_json(relative):
    return json.loads((ROOT / relative).read_text())


def main():
    # A strict allowlist stops accidental credential files, executable helpers,
    # hooks, or copied backend code from entering this distribution package.
    actual = {
        str(path.relative_to(ROOT))
        for path in ROOT.rglob("*")
        if ".git" not in path.relative_to(ROOT).parts
        and "__pycache__" not in path.relative_to(ROOT).parts
        and path.is_file()
    }
    require(actual == ALLOWED_FILES, f"unexpected or missing files: {actual ^ ALLOWED_FILES}")
    require(not any((ROOT / path).is_symlink() for path in actual), "symlink in package")

    marketplace = read_json(".agents/plugins/marketplace.json")
    require(marketplace["name"] == "sensereo", "unexpected marketplace name")
    entries = marketplace["plugins"]
    require(len(entries) == 1 and entries[0]["name"] == "airo", "unexpected plugin catalog")
    require(
        entries[0]["source"] == {"source": "local", "path": "./plugins/airo"},
        "plugin source must stay inside this repository",
    )

    plugin_root = ROOT / "plugins/airo"
    manifest = read_json("plugins/airo/.codex-plugin/plugin.json")
    require(manifest["name"] == "airo", "unexpected plugin identity")
    require(manifest["version"] == "0.3.0", "update validation when releasing a new version")
    require("hooks" not in manifest, "hooks are outside this package's scope")
    require(manifest["interface"]["capabilities"] == ["Read"], "unexpected capability")
    for key in ("logo", "composerIcon"):
        require(
            manifest["interface"][key] == "./assets/airo-icon.svg",
            f"unexpected {key} asset",
        )
    icon_path = plugin_root / "assets/airo-icon.svg"
    require(icon_path.stat().st_size <= 5 * 1024 * 1024, "icon exceeds 5 MiB")
    icon = ET.parse(icon_path).getroot()
    require(icon.tag == "{http://www.w3.org/2000/svg}svg", "icon must be SVG")
    require(
        icon.get("width") == icon.get("height") == "892"
        and icon.get("viewBox") == "0 0 892 892",
        "icon must have the expected square canvas",
    )
    require(
        len(icon) == 1
        and icon[0].tag == "{http://www.w3.org/2000/svg}image"
        and icon[0].get("href", "").startswith("data:image/png;base64,")
        and not list(icon[0]),
        "icon must contain only one embedded PNG image",
    )
    for key, expected in (("mcpServers", "./.mcp.json"), ("skills", "./skills/")):
        require(manifest[key] == expected, f"unexpected {key} path")
        require((plugin_root / expected).exists(), f"missing {key} target")

    mcp = read_json("plugins/airo/.mcp.json")
    require(
        mcp == {"mcpServers": {"airo_shared": {"url": "https://airo-mcp-internal-preview.vercel.app/mcp/server"}}},
        "preview must contain only the known HTTPS endpoint, no commands, headers, or credentials",
    )
    skill = (plugin_root / "skills/airo-shared-readings/SKILL.md").read_text()
    require(skill.startswith("---\nname: airo-shared-readings\n"), "unexpected skill identity")
    require("airo_shared" in skill and "airo_demo_local" not in skill, "stale MCP routing")
    print("Validated 8 distribution files: Airo 0.3.0 / Sensereo / hosted HTTPS service.")
    print("Package metadata does not prove server authorization or runtime connectivity.")


if __name__ == "__main__":
    main()
