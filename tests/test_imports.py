"""Smoke: all modules import cleanly without bpy."""
import importlib, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def test_data_loader_imports():
    m = importlib.import_module("blender_scripts.utils.data_loader")
    assert hasattr(m, "load_county_data")
    assert hasattr(m, "normalise")
    assert hasattr(m, "stress_colour")
    assert hasattr(m, "geo_to_blender")


def test_materials_imports():
    m = importlib.import_module("blender_scripts.utils.materials")
    assert hasattr(m, "make_principled_material")
    assert hasattr(m, "make_emission_material")


def test_fetchers_import():
    w = importlib.import_module("fetchers.wapimaji")
    c = importlib.import_module("fetchers.counties")
    assert hasattr(w, "get_county_water_stress")
    assert hasattr(c, "download_county_data")
