# kenya-3d 🌍

> **Claude + Blender MCP — Civic Data 3D Visualization for East Africa**

[![CI](https://github.com/gabrielmahia/kenya-3d/actions/workflows/ci.yml/badge.svg)](https://github.com/gabrielmahia/kenya-3d/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Portfolio](https://img.shields.io/badge/Portfolio-East%20Africa%20Decision%20Infrastructure-green)](https://github.com/gabrielmahia)

Part of the **East African Decision Infrastructure** portfolio.

> ⚠️ **DEMO MODE**: Sample data files (`data/`) contain synthetic values for illustration only.
> Connect live APIs via `fetchers/` for production use. See [DEMO vs REAL](#demo-vs-real).

## What This Does

`kenya-3d` connects [Claude Code](https://docs.anthropic.com/claude-code) to [Blender](https://www.blender.org/)
via the [Model Context Protocol](https://modelcontextprotocol.io/) so you can generate
civic data 3D visualizations for East Africa using plain English prompts.

| Visualization | Description |
|---|---|
| 🏙️ County Bar Chart | Per-county metrics as scaled 3D bars on Kenya's geographic footprint |
| 🌋 Drought Terrain | Drought severity displaced as a terrain mesh with drought-to-red colour ramp |
| 💧 Water Stress Map | County water stress as glowing emission cylinders — top-down view |

## Architecture

```
Claude Code ──► blender-mcp-server ──► Blender 4.x (bpy)
                                              │
                                 ┌────────────┤────────────┐
                                 │            │            │
                          county_bars.py  drought_terrain.py  water_stress_map.py
                                 │
                           fetchers/
                    wapimaji.py    counties.py
```

## Quick Start

### Prerequisites
- [Blender 4.x](https://www.blender.org/download/)
- Claude Code CLI (`npm install -g @anthropic-ai/claude-code`)
- Python 3.11+

### Setup

```bash
# 1. Enable blender-mcp add-on in Blender
#    Edit → Preferences → Get Extensions → search "MCP" → Install & Enable

# 2. Start the MCP server
pip install uv
uvx blender-mcp-server

# 3. Connect Claude Code
claude mcp add blender -- uvx blender-mcp-server
claude mcp get blender   # verify

# 4. Install Python deps
pip install -r requirements.txt
```

### Run a Visualization

With Blender open and MCP connected, tell Claude Code:

```
Load data/kenya_counties.json and run blender_scripts/county_bars.py in Blender.
Colour bars by water_stress, set a 60° top-down camera, and render a preview.
```

See [`prompts/`](prompts/) for ready-made prompt templates.

## DEMO vs REAL

| Component | Mode | Notes |
|---|---|---|
| `data/kenya_counties.json` | ⚠️ DEMO | Synthetic metrics |
| `data/sample_drought.json` | ⚠️ DEMO | Simulated NDVI grid |
| `fetchers/wapimaji.py` | ✅ REAL | Live wapimaji-mcp API |
| `fetchers/counties.py` | ✅ REAL | Kenya open data (KNBS) |
| Blender scripts | ✅ REAL | Runs via bpy inside Blender |

## Portfolio Integration

| Tool | Role |
|---|---|
| [wapimaji-mcp](https://github.com/gabrielmahia/wapimaji-mcp) | Drought/water data |
| [kenya-rag](https://github.com/gabrielmahia/kenya-rag) | Civic context for captions |
| [taarifa-ai](https://github.com/gabrielmahia/taarifa-ai) | Briefing text for render overlays |
| [civic-agent-kit](https://github.com/gabrielmahia/civic-agent-kit) | Orchestration SDK |

## IP & Collaboration

See [docs/architecture/IP_POLICY.md](docs/architecture/IP_POLICY.md).
Open an Issue before submitting any PR. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT License — developer infrastructure.
© 2026 Gabriel Mahia · contact@aikungfu.dev
