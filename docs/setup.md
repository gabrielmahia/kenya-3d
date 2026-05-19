# Setup Guide: Claude Code + Blender MCP

## Requirements

| Component | Version |
|---|---|
| Blender | 4.0+ |
| Python | 3.11+ |
| Claude Code CLI | latest |

## Installation

### 1. Blender

Download from https://www.blender.org/download/

### 2. blender-mcp Add-on

In Blender: Edit -> Preferences -> Get Extensions -> search MCP -> Install -> Enable

### 3. MCP Server

```bash
pip install uv
uvx blender-mcp-server
```

Runs on localhost:9000 by default.

### 4. Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

### 5. Connect

```bash
claude mcp add blender -- uvx blender-mcp-server
claude mcp get blender
```

### 6. Python Dependencies

```bash
pip install -r requirements.txt
```

## First Visualization

Tell Claude Code:

    Load data/kenya_counties.json and run blender_scripts/county_bars.py in Blender.
    Render a preview from the default camera.

## Live Data

```bash
python fetchers/wapimaji.py   # requires wapimaji-mcp running
python fetchers/counties.py   # downloads KNBS county reference
```

## Troubleshooting

| Issue | Fix |
|---|---|
| MCP refused | Blender MCP panel must show Running |
| Empty render | scene.camera must not be None |
| Import error | pip install -r requirements.txt |
