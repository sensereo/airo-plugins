# Airo for Codex

Sensereo's private plugin marketplace for internal Airo connection testing.
The Airo plugin supplies its name, MCP address, and guidance for reading sensors.
You do not download a ZIP or run an operating-system installer.

**Current preview:** version `0.2.0` connects to the simulated Airo demo on
`http://127.0.0.1:8766/mcp/server`. It does not connect to production Sensereo
data. This repository does not contain or start the backend.

## Before you connect

- Use a Codex client with plugin marketplace support. The commands below were
  checked against `codex-cli 0.162.0-alpha.2`.
- Your GitHub account needs read access to the private
  `sensereo/airo-plugins` repository. Git used by Codex must already be able to
  authenticate through your existing Git credential manager or SSH setup.
  Signing into Codex alone does not grant access to a private GitHub repository.
- Keep the Airo demo running on the **same computer** at
  `http://127.0.0.1:8766/mcp`. Another person's `127.0.0.1` is their computer,
  not the demo operator's computer. Testers on other computers each need a local
  demo until a shared HTTPS service is deployed.
- Obtain a short-lived demo share token separately from the demo operator.
  It must be issued by the simulated demo you are connecting to. It is not a
  GitHub token, an Airo password, or a production Sensereo API token.

Repository access and Airo data access are separate. Never put a GitHub
credential in the source URL or enter a share token in Codex chat, configuration,
or a terminal command. Share tokens belong on the Airo authorization page.

## Add Airo and connect

1. On the Airo page, choose **Codex**.
2. In Codex's plugin settings, use **Add plugin marketplace** to add the
   Sensereo Git source:

   ```text
   https://github.com/sensereo/airo-plugins.git
   ```

   Codex's CLI supports this Git source. The desktop dialog and webpage-to-Codex
   installation link have not been exercised in this acceptance run; the
   verified route uses the CLI steps below.
3. Find **Airo** in **Sensereo** and install it. Its name and server address
   are already supplied by the plugin.
4. Follow the connection prompt. If authorization does not open automatically,
   select **Authenticate** for the plugin's `airo_shared` MCP connection.
5. On the Airo page opened in your browser, enter your demo share token and
   select **Review access**.
6. Review the shared devices and read-only access, then choose
   **Allow read-only access**. Return to Codex after authentication completes.
7. Start a new conversation and ask **“Hey Airo, how's the air?”** or
   **“What did Airo sense today?”**. The answer should identify simulated data.

### CLI alternative

Run these commands individually. The final command starts browser authorization;
the plugin installation command alone does not guarantee that a browser opens.

```sh
codex plugin marketplace add https://github.com/sensereo/airo-plugins.git
codex plugin add airo@sensereo
codex mcp login airo_shared
```

The source's initial default and development branch is `feat/airo-mcp`. To pin
that branch explicitly, append `--ref feat/airo-mcp` to the marketplace command.
If using SSH with
an already configured GitHub SSH key, the corresponding source is
`git@github.com:sensereo/airo-plugins.git`. Use one source consistently. If
**sensereo** is already registered elsewhere, inspect
`codex plugin marketplace list` before deliberately changing that registration.

If `codex` is not on your PATH, the Mac build used for this preview provides it
at the following path. If present, use this quoted path instead of `codex` in
each command above:

```text
"/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex"
```

If commands are unavailable, use a client version with plugin support. This
plugin has no OS-specific installer; availability and UI depend on the Codex
client. If an existing window does not show the newly installed plugin, reopen
the window before starting a fresh conversation.

## Access and troubleshooting

- **Private source cannot be fetched:** confirm repository membership and Git
  authentication. Do not substitute your Airo share token as a Git credential.
- **Service cannot be reached:** open `http://127.0.0.1:8766/mcp` on this computer
  and ask the demo operator to start the local backend if necessary.
- **Authentication expired:** select **Authenticate**, or rerun
  `codex mcp login airo_shared`, then use a valid demo share token in the browser.
- **Connection succeeded but no readings:** check which devices the reviewed
  share allows. Do not assume the plugin grants access to every Airo device.

The four MCP tools are `list_devices`, `get_current`, `get_history`, and
`explain_metric`. They read shared devices, current readings, history, and
metric explanations. They cannot change Pod settings. The backend enforces
authorization; a plugin label or a skill is not an access-control boundary.

The MCP key `airo_shared` is distinct from existing `airo`, `airo-2`, and
`airo_demo_local` connections. If more than one Airo integration is installed,
specify the shared Airo plugin when checking which data source was used.

## Disconnect or remove

To revoke authorized access, use **Disconnect this AI app** on the Airo page
in the browser that authorized it, or ask the demo operator to revoke its share.
To remove only this plugin's local connection and marketplace:

```sh
codex mcp logout airo_shared
codex plugin remove airo@sensereo
codex plugin marketplace remove sensereo
```

Logging out or uninstalling alone does not prove server-side revocation.

## Maintainers

Verified on 2026-10-10 with an isolated Codex configuration: fetch from this
private HTTPS Git repository, install `airo@sensereo` 0.2.0, discover the
`airo_shared` connection, and complete native Codex OAuth using a temporary
simulated share. An MCP SDK call using that authorization listed the four
read-only tools and read two simulated devices. The test share was then revoked
and the isolated OAuth credentials removed. This does not validate other users'
Git credentials, desktop marketplace dialogs, public hosting, or live data.

This repository contains only marketplace metadata, the plugin configuration,
and the reading skill. It contains no backend, installer, runtime, account,
share token, OAuth credential, or sensor records. Keep backend implementation
and deployment credentials in the separate private service repository.

Validate the package without installing dependencies or connecting to Airo:

```sh
python3 scripts/validate_package.py
```

Changing this repository from private to public only changes who can obtain the
plugin files. It does not grant Airo data access. Before opening testing to
people who do not run the backend locally, deploy and validate a shared HTTPS
MCP/OAuth service, update `.mcp.json` and preview descriptions, bump the plugin
version, and retest a fresh install and authorization. That deployment and the
public-directory listing have not been completed by this package.

Plugin layout and Git marketplace documentation:
[OpenAI plugin development guide](https://developers.openai.com/plugins/build/plugins).
