"""
blender_scripts/water_stress_map.py
kenya-3d — County water stress map (emission glow, top-down view).

Usage via Claude Code MCP:
  "Run blender_scripts/water_stress_map.py in Blender"
"""
from __future__ import annotations
import sys
from pathlib import Path

try:
    import bpy
    BLENDER_AVAILABLE = True
except ImportError:
    BLENDER_AVAILABLE = False

SCRIPT_DIR = Path(__file__).parent
DATA_FILE  = SCRIPT_DIR.parent / "data" / "kenya_counties.json"


def run():
    if not BLENDER_AVAILABLE:
        print("[kenya-3d] water_stress_map: Blender not available")
        return

    sys.path.insert(0, str(SCRIPT_DIR.parent))
    from blender_scripts.utils.data_loader import (
        load_county_data, normalise, stress_colour, geo_to_blender)
    from blender_scripts.utils.materials import (
        make_emission_material, setup_civic_world)

    counties = load_county_data(DATA_FILE)
    ws_vals  = [c.get("water_stress", 0) for c in counties]
    mn, mx   = min(ws_vals), max(ws_vals)

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    setup_civic_world()

    # Dark base plane
    bpy.ops.mesh.primitive_plane_add(size=14.0, location=(0, 0, -0.05))
    base = bpy.context.active_object
    base.name = "kenya_base"
    bm = bpy.data.materials.new("base_mat")
    bm.use_nodes = True
    bsdf = bm.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.04, 0.04, 0.08, 1.0)
        bsdf.inputs["Roughness"].default_value = 1.0
    base.data.materials.append(bm)

    # County cylinders with emission glow
    for c in counties:
        ws   = c.get("water_stress", 0)
        norm = normalise(ws, mn, mx)
        x, y = geo_to_blender(c["lat"], c["lon"])
        col  = stress_colour(norm)
        h    = 0.04 + norm * 0.75

        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.16, depth=h, location=(x, y, h / 2))
        obj = bpy.context.active_object
        obj.name = f"ws_{c['name'].replace(' ', '_')}"
        strength = 0.4 + norm * 3.5
        mat = make_emission_material(f"ws_{c['id']}", col, strength=strength)
        if mat:
            obj.data.materials.append(mat)

    # Top-down camera
    bpy.ops.object.camera_add(location=(0.3, 0.2, 20), rotation=(0, 0, 0))
    cam = bpy.context.active_object
    cam.data.lens = 32
    bpy.context.scene.camera = cam

    bpy.ops.object.light_add(type="AREA", location=(0, 0, 16))
    area = bpy.context.active_object
    area.data.energy = 600.0
    area.data.size   = 22.0

    print(f"[kenya-3d] water_stress_map — {len(counties)} counties")
    print(f"[kenya-3d] range: {mn:.1f} (low) -> {mx:.1f} (critical)")
    print("[kenya-3d] -> Tell Claude: 'Render the water stress map from above'")


if __name__ == "__main__" or BLENDER_AVAILABLE:
    run()
