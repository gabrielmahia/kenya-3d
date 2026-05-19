"""
blender_scripts/county_bars.py
kenya-3d — County 3D bar chart.

Usage via Claude Code MCP:
  "Run blender_scripts/county_bars.py in Blender using data/kenya_counties.json"
"""
from __future__ import annotations
import math, sys
from pathlib import Path

try:
    import bpy
    BLENDER_AVAILABLE = True
except ImportError:
    BLENDER_AVAILABLE = False

SCRIPT_DIR = Path(__file__).parent
DATA_FILE  = SCRIPT_DIR.parent / "data" / "kenya_counties.json"
METRIC     = "water_stress"   # swap: drought_index | population_m
BAR_WIDTH  = 0.32
BAR_SCALE  = 0.28
CAM_HEIGHT = 18.0


def run():
    if not BLENDER_AVAILABLE:
        print("[kenya-3d] county_bars: Blender not available")
        return

    sys.path.insert(0, str(SCRIPT_DIR.parent))
    from blender_scripts.utils.data_loader import (
        load_county_data, normalise, stress_colour, geo_to_blender)
    from blender_scripts.utils.materials import (
        make_principled_material, setup_civic_world)

    counties = load_county_data(DATA_FILE)
    vals     = [c.get(METRIC, 0) for c in counties]
    mn, mx   = min(vals), max(vals)
    print(f"[kenya-3d] {len(counties)} counties | {METRIC}: {mn:.1f}–{mx:.1f}")

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    setup_civic_world()

    for c in counties:
        v     = c.get(METRIC, 0)
        norm  = normalise(v, mn, mx)
        x, y  = geo_to_blender(c["lat"], c["lon"])
        h     = max(0.05, v * BAR_SCALE)
        col   = stress_colour(norm)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, h / 2))
        obj = bpy.context.active_object
        obj.name = f"bar_{c['name'].replace(' ', '_')}"
        obj.scale = (BAR_WIDTH, BAR_WIDTH, h)
        mat = make_principled_material(f"mat_{c['id']}", col, roughness=0.55)
        if mat:
            obj.data.materials.append(mat)

    bpy.ops.object.camera_add(
        location=(0, -CAM_HEIGHT * 0.75, CAM_HEIGHT),
        rotation=(math.radians(58), 0, 0))
    bpy.context.scene.camera = bpy.context.active_object

    bpy.ops.object.light_add(type="SUN", location=(5, 5, 20))
    bpy.context.active_object.data.energy = 3.5

    print(f"[kenya-3d] county_bars ready — metric: {METRIC}")
    print("[kenya-3d] -> Tell Claude: 'Render a preview of the Blender scene'")


if __name__ == "__main__" or BLENDER_AVAILABLE:
    run()
