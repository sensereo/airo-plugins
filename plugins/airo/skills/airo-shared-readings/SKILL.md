---
name: airo-shared-readings
description: Read connected Airo indoor-air sensors through the Airo shared-access MCP. Use for questions such as "Hey Airo, how's the air?", "What Airo sensed today", or Airo Pod readings and history. Not for outdoor weather or developing the integration.
---

# Airo shared readings

Use the installed `airo_shared` MCP tools for Airo sensor questions. This
plugin supplies simulated readings, not a live Sensereo account. No Airo project
folder needs to be open.

Check the available Airo tools before saying that sensor access is unavailable.
If tools are deferred, use the client's tool discovery mechanism and the actual
tool schemas. In Codex code mode, search `ALL_TOOLS` for Airo names or descriptions
and call the discovered tools through `tools`. Empty MCP resource listings do
not establish that tools are missing. Do not search workspace files or browser
tabs for readings, inspect credentials, or bypass MCP with direct API requests.

- For the latest air readings, call `get_current` without filters unless a
  particular Pod or room was requested. It includes IDs and available metrics.
- For today or trends, use returned Pod IDs and metrics with `get_history`.
  Prefer `realtime` for recent trends. Its window and `day` are rolling 24-hour
  windows, not calendar days. Follow the server's guidance when filtering local
  today and interpreting sampled history; do not relabel full-window summaries.
- Use `list_devices` for inventory and `explain_metric` for metric meanings.
- If the service is unreachable or needs authentication, report that specific
  failure and direct the user to start the demo or authenticate in Codex. Share
  tokens belong only on the Airo authorization page, never in chat.

Lead with the supported observations, identify simulated data, and preserve
units and meaningful gaps. Do not invent measurements, health bands or an
overall safety rating. Report age is not an individual measurement timestamp.
Use the user's known timezone internally; ordinary answers need no timezone
label unless requested or needed to resolve ambiguity. The plugin only reads;
it does not authorize changing devices, sharing access, or scheduling tasks.
