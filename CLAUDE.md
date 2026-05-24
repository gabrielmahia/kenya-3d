# CLAUDE.md — kenya-3d

> This file tells Claude Code how to work effectively in this repository.
> It is read automatically when you run `claude` from this directory.

## What this repo does

`kenya-3d` generates 3D civic data visualizations of Kenya's 47 counties using:
- **Claude Code** (this session) as the AI orchestrator
- **Blender MCP** as the 3D rendering engine (via `blender-mcp` SSE on port 9876)
- **wapimaji-mcp** as the live data source for drought and water stress
- **kenya-civic-data** (HuggingFace dataset) for county metadata

## Blender MCP — Connection and Verification

Before any visualization work, verify the connection:

```
Connect to Blender MCP and tell me how many objects are in the current scene.
```

If connection fails:
1. Ensure Blender 5.x is open
2. In Blender: Edit → Preferences → Add-ons → enable "Interface: Blender MCP"
3. In 3D viewport: press N → BlenderMCP tab → click "Connect to Claude"
4. Verify: `netstat -ano | findstr 9876` should show LISTENING

## Visualization Prompts — Ready to Run

### County Bar Chart (Water Stress)
```
Run blender_scripts/county_bars.py in Blender using data/kenya_counties.json.
Colour bars by water_stress field:
  green (< 0.3) = low stress
  yellow (0.3–0.6) = moderate  
  orange (0.6–0.8) = high
  red (> 0.8) = critical
Add a title "Kenya Water Stress by County" and render a preview PNG.
Save the render to outputs/water_stress_bars.png.
```

### Drought Terrain Mesh
```
Run blender_scripts/drought_terrain.py in Blender.
Load data/kenya_counties.json.
Create a terrain mesh where height = drought_severity * 10.
Apply a heatmap material: blue=0 (no drought), red=1 (severe).
Position camera at 45° elevation looking at the center of Kenya.
Render and save to outputs/drought_terrain.png.
```

### Water Stress County Map
```
Run blender_scripts/water_stress_map.py in Blender.
Load data/kenya_counties.json.
Place a sphere at each county centroid (lat/lon → XY coordinates).
Scale sphere size proportional to population.
Colour by water_stress using the standard heatmap.
Add county name labels for the top 10 most stressed counties.
Render top-down orthographic view to outputs/water_stress_map.png.
```

### Custom Analysis
```
I want to visualize [specific metric] for Kenya's 47 counties.
Use the data in data/kenya_counties.json.
Create a [bar chart/terrain/map/scatter] visualization.
Colour by [field_name] using [colour scheme].
```

## Data Schema

`data/kenya_counties.json`:
```json
{
  "county_name": "string",
  "latitude": float,
  "longitude": float,  
  "population": int,
  "water_stress": float,  // 0.0 (low) to 1.0 (critical)
  "drought_severity": float,  // 0.0 to 1.0
  "county_code": int  // 1-47
}
```

## File Structure

```
kenya-3d/
├── blender_scripts/
│   ├── county_bars.py       # Bar chart by county
│   ├── drought_terrain.py   # Terrain mesh
│   ├── water_stress_map.py  # County dot map
│   └── utils/
│       ├── data_loader.py   # Load kenya_counties.json
│       └── materials.py     # Heatmap material generator
├── data/
│   └── kenya_counties.json  # Kenya 47-county dataset
├── fetchers/
│   ├── counties.py          # Fetch from wapimaji-mcp
│   └── wapimaji.py          # Live drought data
├── outputs/                 # Rendered PNG/video outputs
└── tests/                   # pytest smoke tests
```

## Testing

```bash
# Run smoke tests (no Blender needed)
pytest tests/ -v

# Lint
ruff check .
```

## Portfolio Context

This repo demonstrates:
1. **Claude Code + MCP** — AI-directed 3D visualization pipeline
2. **East African civic data** — Kenya drought and water stress visualization  
3. **First African MCP server** — part of the East African Decision Infrastructure portfolio

See: [gabrielmahia.github.io](https://gabrielmahia.github.io)
