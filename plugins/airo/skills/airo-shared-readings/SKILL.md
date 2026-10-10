---
name: airo-shared-readings
description: Read connected Airo indoor-air sensors through the Airo shared-access MCP. Use for questions such as "Hey Airo, how's the air?", "What Airo sensed today", or Airo Pod readings and history. Not for outdoor weather or developing the integration.
---

# Airo shared readings

Use the installed `airo_shared` MCP tools for Airo sensor questions. The backend
can supply live Console shared data or synthetic fixtures; determine which from
each tool result's `data_mode` and `source`. No Airo project folder needs to be open.

Check the available Airo tools before saying that sensor access is unavailable.
If tools are deferred, use the client's tool discovery mechanism and the actual
tool schemas. In Codex code mode, search `ALL_TOOLS` for Airo names or descriptions
and call the discovered tools through `tools`. Empty MCP resource listings do
not establish that tools are missing. Do not search workspace files or browser
tabs for readings, inspect credentials, or bypass MCP with direct API requests.

- For the latest air readings, call `get_current` without filters unless a
  particular Pod was requested. It includes IDs and available metrics. Shared
  room names do not have room IDs; resolve a named room to its returned Pod IDs.
- For today or trends, use returned Pod IDs and metrics with `get_history`.
  Prefer `realtime` for recent trends. Its window and `day` are rolling 24-hour
  windows, not calendar days. Use the response's exact window when supplied.
  For a broad daily question, make a first pass of at most four relevant Pod/metric
  history calls, prioritizing the user's stated interests and fresh readings.
  State which rooms and metrics the answer covers; do not imply an exhaustive
  account report. An old latest reading does not prove its history is empty.
  Do not fetch every device and metric by default. For an explicitly exhaustive
  request, use bounded batches and pagination within Console's shared limits of
  20 history requests and 60 total requests per minute; each MCP tool can make
  multiple upstream requests for inventory and authorization. If a rate limit
  occurs, stop further Airo calls for this turn, explain any incomplete coverage,
  and let the user retry later. Do not relabel full-window summaries as
  calendar-today statistics.
- Use `list_devices` for inventory and `explain_metric` for metric meanings.
- If the service is unreachable or needs authentication, report that specific
  failure and direct the user to start the service or authenticate in Codex. Share
  tokens belong only on the Airo authorization page, never in chat.

Lead with supported observations and preserve units and meaningful gaps. Label
`data_mode=fixture` as simulated; do not call `data_mode=live` simulated. Missing
values are not zero. Use each reading's `measured_at` and age for freshness; an
online Pod can retain old readings. `last_reported_at` is a device report time,
and retrieval time is when the response was produced, not when air was measured.
Preserve TVOC concentration units; do not relabel them as VOC Index. History may
be truncated or downsampled; source-reported bucket min/max/sample counts are
not independently verified, and bucket means are not raw-sample averages.
Do not invent measurements, health bands or an overall safety rating.
Use the user's known timezone internally; ordinary answers need no timezone
label unless requested or needed to resolve ambiguity. The plugin only reads;
it does not authorize changing devices, sharing access, or scheduling tasks.
