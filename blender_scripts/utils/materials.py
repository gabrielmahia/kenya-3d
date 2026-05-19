"""
blender_scripts/utils/materials.py
kenya-3d — Blender material helpers.

Functions return None gracefully when bpy is absent (test mode).
"""
from __future__ import annotations

try:
    import bpy
    BLENDER_AVAILABLE = True
except ImportError:
    BLENDER_AVAILABLE = False


def make_principled_material(name: str, colour: tuple,
                             roughness: float = 0.7, metallic: float = 0.0):
    if not BLENDER_AVAILABLE:
        return None
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*colour, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
    return mat


def make_emission_material(name: str, colour: tuple, strength: float = 1.0):
    if not BLENDER_AVAILABLE:
        return None
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    em = nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*colour, 1.0)
    em.inputs["Strength"].default_value = strength
    out = nodes.new("ShaderNodeOutputMaterial")
    mat.node_tree.links.new(em.outputs["Emission"], out.inputs["Surface"])
    return mat


def setup_civic_world(sky: tuple = (0.04, 0.04, 0.08)):
    if not BLENDER_AVAILABLE:
        return
    world = bpy.context.scene.world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (*sky, 1.0)
        bg.inputs["Strength"].default_value = 0.4
