"""Check this small preview package without loading credentials or using a network."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_FILES = {
    ".gitignore",
    "README.md",
    ".agents/plugins/marketplace.json",
    "plugins/airo/.codex-plugin/plugin.json",
    "plugins/airo/.mcp.json",
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
    require(manifest["version"] == "0.2.1", "update validation when releasing a new version")
    require("hooks" not in manifest, "hooks are outside this package's scope")
    require(manifest["interface"]["capabilities"] == ["Read"], "unexpected capability")
    for key, expected in (("mcpServers", "./.mcp.json"), ("skills", "./skills/")):
        require(manifest[key] == expected, f"unexpected {key} path")
        require((plugin_root / expected).exists(), f"missing {key} target")

    mcp = read_json("plugins/airo/.mcp.json")
    require(
        mcp == {"mcpServers": {"airo_shared": {"url": "http://127.0.0.1:8766/mcp/server"}}},
        "preview must contain only the known HTTP endpoint, no commands, headers, or credentials",
    )
    skill = (plugin_root / "skills/airo-shared-readings/SKILL.md").read_text()
    require(skill.startswith("---\nname: airo-shared-readings\n"), "unexpected skill identity")
    require("airo_shared" in skill and "airo_demo_local" not in skill, "stale MCP routing")
    print("Validated 7 distribution files: Airo 0.2.1 / Sensereo / local HTTP service.")
    print("Package metadata does not prove server authorization or runtime connectivity.")


if __name__ == "__main__":
    main()
