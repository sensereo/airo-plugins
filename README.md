# Airo for Codex

Sensereo's private plugin marketplace for internal Airo connection testing.
The Airo plugin supplies its name, MCP address, and guidance for reading sensors.
You do not download a ZIP or run an operating-system installer.

**Private hosted-service preview:** version `0.3.0` is configured to connect to
`https://airo-mcp-internal-preview.vercel.app/mcp/server`. No local backend,
project checkout, or developer setup is required. Each tool result identifies
whether its readings are live Console shared data or simulated data.

The plugin is distributed through the private Git source on `feat/airo-mcp`.
Existing installations must refresh the Sensereo source and authenticate with
the hosted service. This package retains the Airo reading guidance and supplied
silver-ring/blue-dot icons. Publishing the plugin does not deploy the backend.

## Before you connect

- Use a Codex client with plugin marketplace support. The commands below were
  checked against `codex-cli 0.162.0-alpha.2`.
- Your GitHub account needs read access to the private
  `sensereo/airo-plugins` repository. Git used by Codex must already be able to
  authenticate through your existing Git credential manager or SSH setup.
  Signing into Codex alone does not grant access to a private GitHub repository.
- Connect to the internet so Codex and your browser can reach the shared HTTPS
  Airo service.
- Obtain a share token separately from the data owner or test operator. The
  authorization page identifies the service and verifies the token's read-only
  scope. Live data requires a Console-issued share token; simulated data uses
  a token issued for that test service. These modes do not fall back to one another.

Repository access and Airo data access are separate. Never put a GitHub
credential in the source URL or enter a share token in Codex chat, configuration,
or a terminal command. Share tokens belong on the Airo authorization page.

## Add Airo and connect

1. In Codex's plugin settings, use **Add plugin marketplace** to add the
   Sensereo Git source:

   ```text
   https://github.com/sensereo/airo-plugins.git
   ```

2. Find **Airo** in **Sensereo** and install it. Its name and server address
   are already supplied by the plugin.
3. Follow the connection prompt. If authorization does not open automatically,
   select **Authenticate** for the plugin's `airo_shared` MCP connection.
4. On the Airo page opened in your browser, enter the matching share token and
   select **Review access**.
5. Review the shared devices and read-only access, then choose
   **Allow read-only access**. Return to Codex after authentication completes.
6. Start a new conversation and ask **“Hey Airo, how's the air?”** or
   **“What did Airo sense today?”**. The answer should identify synthetic data
   when simulated, and preserve measurement times and gaps when reading live data.

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

### Update an existing installation

Use **Upgrade** for the Sensereo Git source in Codex's plugin settings. The CLI
alternative refreshes the source and then installs its current Airo package:

```sh
codex plugin marketplace upgrade sensereo
codex plugin add airo@sensereo
```

Reopen the plugin page and confirm version `0.3.0`, the silver-ring/blue-dot
logo, and the HTTPS Airo server address. Select **Authenticate** for `airo_shared`
or run `codex mcp login airo_shared` to authorize the hosted service in your
browser. Authorization for the previous local service does not grant access to
this hosted service. Start a new conversation after connecting.

## Access and troubleshooting

- **Private source cannot be fetched:** confirm repository membership and Git
  authentication. Do not substitute your Airo share token as a Git credential.
- **Service cannot be reached:** open the
  [Airo connection page](https://airo-mcp-internal-preview.vercel.app/mcp), retry,
  and contact the test operator if the hosted service remains unavailable.
- **Authentication expired:** select **Authenticate**, or rerun
  `codex mcp login airo_shared`, then use a valid share token for that backend mode
  in the browser.
- **Console token rejected by a simulated page:** ask the operator to check the
  hosted service's data mode. Installing the plugin does not select the backend's
  data mode or bypass token validation.
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

To revoke one AI connection, use **Disconnect this AI app** on the Airo page
in the browser that authorized it. Ask the data owner or test operator to revoke
the source share if all connections using that share should lose access.
To remove only this plugin's connection and marketplace from Codex:

```sh
codex mcp logout airo_shared
codex plugin remove airo@sensereo
codex plugin marketplace remove sensereo
```

Logging out or uninstalling alone does not prove server-side revocation.

## Maintainers

**Hosted service verification for `0.3.0` passed on 2026-10-10** at
`https://airo-mcp-internal-preview.vercel.app`. OAuth discovery was reachable,
unauthenticated MCP requests returned `401`, and sensitive responses used
`no-store`. A real Console share token completed access review, authorization,
and the PKCE token exchange; replaying the authorization code was rejected.
The service exposed the four read-only tools, listed seven shared devices, and
returned a current reading for one device and history. A fresh Codex session
using `gpt-6-luna` with medium reasoning also completed a `get_current` call.

The stable HTTPS alias was then switched to a new Git Preview deployment of
backend commit `321cb11`. The existing access token continued to work after
that deployment change. Revoking the tested AI grant caused both existing and
new MCP clients to receive `401`, and its refresh token was rejected. The
underlying Console share was not revoked. No token or sensor records are stored
in this plugin repository.

These checks cover the hosted service and a fresh Codex tool call. A fresh
graphical plugin installation and native Codex browser authorization against
the hosted service still require user acceptance. They must not be inferred
from the earlier local-service installation test below. Package validation
alone does not establish runtime connectivity or successful authorization.

The earlier local-service preview was verified on 2026-10-10 with an isolated
Codex configuration: fetch from this
private HTTPS Git repository, install `airo@sensereo` 0.2.0, discover the
`airo_shared` connection, and complete native Codex OAuth using a temporary
simulated share. An MCP SDK call using that authorization listed the four
read-only tools and read two simulated devices. The test share was then revoked
and the isolated OAuth credentials removed. This does not validate other users'
Git credentials, desktop marketplace dialogs, public hosting, or live data.

Version `0.2.1` updated the guidance to follow live/fixture response metadata,
measurement freshness and Console request limits. Package validation alone does
not establish a successful live OAuth or natural-language test; those results
belong in the backend integration verification record. Version `0.2.2` included
these guidance improvements and continued to use the local service.

Version `0.2.2` added the owner-supplied silver-ring and blue-dot artwork as the
plugin listing logo and composer icon. `assets/airo-icon.svg` embeds a PNG
conversion of the supplied TIFF, centered at its original aspect ratio on a
square canvas. It has no external image dependencies. Both themes use the same
artwork. Refresh the Sensereo source in Codex to load the updated package.

This repository contains only marketplace metadata, the plugin configuration,
brand artwork, and the reading skill. It contains no backend, installer, runtime, account,
share token, OAuth credential, or sensor records. Keep backend implementation
and deployment credentials in the separate private service repository.

Validate the package without installing dependencies or connecting to Airo:

```sh
python3 scripts/validate_package.py
```

Changing this repository from private to public only changes who can obtain the
plugin files. It does not grant Airo data access. This remains a private Git
marketplace; a public-directory listing is separate and has not been completed
by this package. Hosted backend deployment and credentials remain in the
separate private service repository.

Plugin layout and Git marketplace documentation:
[OpenAI plugin development guide](https://developers.openai.com/plugins/build/plugins).
