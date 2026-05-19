"""
blender_scripts/utils/data_loader.py
kenya-3d — data loading + coordinate utilities.

Safe to import outside Blender (bpy gracefully absent).
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

try:
    import bpy  # noqa: F401
    BLENDER_AVAILABLE = True
except ImportError:
    BLENDER_AVAILABLE = False

PALETTE = {
    "safe":     (0.18, 0.62, 0.35),
    "moderate": (0.94, 0.77, 0.20),
    "high":     (0.90, 0.47, 0.12),
    "critical": (0.80, 0.15, 0.15),
}


def load_county_data(json_path: str | Path) -> list[dict[str, Any]]:
    path = Path(json_path)
    if not path.exists():
        raise FileNotFoundError(f"County data not found: {path}")
    with open(path) as f:
        raw = json.load(f)
    counties = raw.get("counties", [])
    required = {"id", "name", "lat", "lon"}
    for c in counties:
        missing = required - c.keys()
        if missing:
            raise ValueError(f"County {c.get('name', '?')} missing: {missing}")
    return counties


def load_drought_grid(json_path: str | Path) -> tuple[list[list[float]], dict]:
    path = Path(json_path)
    if not path.exists():
        raise FileNotFoundError(f"Drought data not found: {path}")
    with open(path) as f:
        raw = json.load(f)
    return raw["grid"], raw.get("metadata", {})


def normalise(value: float, min_val: float, max_val: float) -> float:
    if max_val == min_val:
        return 0.0
    return max(0.0, min(1.0, (value - min_val) / (max_val - min_val)))


def stress_colour(norm: float) -> tuple[float, float, float]:
    """Map 0-1 stress to RGB via civic palette."""
    def lerp(a, b, t):
        return tuple(a[i] + t * (b[i] - a[i]) for i in range(3))

    if norm < 0.33:
        return lerp(PALETTE["safe"], PALETTE["moderate"], norm / 0.33)
    elif norm < 0.67:
        return lerp(PALETTE["moderate"], PALETTE["high"], (norm - 0.33) / 0.34)
    else:
        return lerp(PALETTE["high"], PALETTE["critical"], (norm - 0.67) / 0.33)


def geo_to_blender(
    lat: float, lon: float,
    lat_range: tuple = (-5.0, 5.0),
    lon_range: tuple = (34.0, 42.0),
    scale: float = 10.0,
) -> tuple[float, float]:
    x = (lon - lon_range[0]) / (lon_range[1] - lon_range[0]) * scale - scale / 2
    y = (lat - lat_range[0]) / (lat_range[1] - lat_range[0]) * scale - scale / 2
    return x, y
