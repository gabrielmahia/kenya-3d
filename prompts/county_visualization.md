# Prompt: County 3D Bar Chart

---

Use Blender MCP to create a Kenya county 3D bar chart:

1. Load `data/kenya_counties.json`
2. Run `blender_scripts/county_bars.py` in Blender
3. Bars coloured by water_stress (green=low, red=critical)
4. Camera: 58° top-down angle, dramatic overview of Kenya
5. Sun light at 3.5 energy from upper-left
6. Render a preview and describe the stress distribution

Expected: 47 bars on Kenya's geographic footprint.
Kericho/Bomet = shortest green bars. Mandera/Turkana = tallest red bars.

**Variations**
- "Use drought_index instead" — switches metric
- "Label top 5 most stressed counties" — adds text objects
- "Animate bars rising" — 30-frame animation
