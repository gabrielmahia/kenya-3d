"""
blender_scripts/drought_terrain.py
kenya-3d — Drought terrain mesh displaced by severity index.

Usage via Claude Code MCP:
  "Run blender_scripts/drought_terrain.py in Blender"
"""
from __future__ import annotations
import math, sys
from pathlib import Path

try:
    import bpy, bmesh
    BLENDER_AVAILABLE = True
except ImportError:
    BLENDER_AVAILABLE = False

SCRIPT_DIR       = Path(__file__).parent
DATA_FILE        = SCRIPT_DIR.parent / "data" / "sample_drought.json"
TERRAIN_SCALE    = 12.0
DISPLACEMENT     = 2.8


def run():
    if not BLENDER_AVAILABLE:
        print("[kenya-3d] drought_terrain: Blender not available")
        return

    sys.path.insert(0, str(SCRIPT_DIR.parent))
    from blender_scripts.utils.data_loader import load_drought_grid, stress_colour
    from blender_scripts.utils.materials import setup_civic_world

    grid, meta = load_drought_grid(DATA_FILE)
    rows, cols = len(grid), len(grid[0])
    print(f"[kenya-3d] drought grid {rows}x{cols}")

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    setup_civic_world()

    bpy.ops.mesh.primitive_grid_add(
        x_subdivisions=cols - 1, y_subdivisions=rows - 1,
        size=TERRAIN_SCALE, location=(0, 0, 0))
    terrain = bpy.context.active_object
    terrain.name = "drought_terrain"

    mesh = terrain.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.verts.ensure_lookup_table()

    half  = TERRAIN_SCALE / 2
    cw    = TERRAIN_SCALE / max(cols - 1, 1)
    ch    = TERRAIN_SCALE / max(rows - 1, 1)

    for v in bm.verts:
        col_i = round((v.co.x + half) / cw)
        row_i = round((v.co.y + half) / ch)
        col_i = max(0, min(cols - 1, col_i))
        row_i = max(0, min(rows - 1, row_i))
        v.co.z = grid[row_i][col_i] * DISPLACEMENT

    bm.to_mesh(mesh)
    bm.free()
    mesh.update()

    # Vertex colour pass
    if not mesh.vertex_colors:
        mesh.vertex_colors.new(name="drought_col")
    vcol = mesh.vertex_colors.active
    for poly in mesh.polygons:
        for idx in poly.loop_indices:
            vi    = mesh.loops[idx].vertex_index
            col_i = max(0, min(cols - 1, vi % cols))
            row_i = max(0, min(rows - 1, vi // cols))
            d     = grid[row_i][col_i]
            vcol.data[idx].color = (*stress_colour(d), 1.0)

    mat = bpy.data.materials.new("terrain_mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf  = nodes.get("Principled BSDF")
    vc    = nodes.new("ShaderNodeVertexColor")
    vc.layer_name = "drought_col"
    if bsdf:
        mat.node_tree.links.new(vc.outputs["Color"], bsdf.inputs["Base Color"])
        bsdf.inputs["Roughness"].default_value = 0.85
    terrain.data.materials.append(mat)

    bpy.ops.object.camera_add(
        location=(0, -TERRAIN_SCALE, TERRAIN_SCALE * 0.9),
        rotation=(math.radians(52), 0, 0))
    bpy.context.scene.camera = bpy.context.active_object

    bpy.ops.object.light_add(type="SUN", location=(6, -6, 18))
    bpy.context.active_object.data.energy = 4.0

    print("[kenya-3d] drought_terrain ready — green=low, red=critical")
    print("[kenya-3d] -> Tell Claude: 'Render the drought terrain'")


if __name__ == "__main__" or BLENDER_AVAILABLE:
    run()
