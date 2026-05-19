"""Unit tests: data loading + coordinate utilities."""
import json, sys, tempfile, pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from blender_scripts.utils.data_loader import (
    load_county_data, load_drought_grid,
    normalise, stress_colour, geo_to_blender, PALETTE,
)

SAMPLE_C = {"counties": [
    {"id": 1, "name": "Nairobi", "lat": -1.28, "lon": 36.82, "water_stress": 6.8},
    {"id": 2, "name": "Turkana", "lat": 3.12,  "lon": 35.60, "water_stress": 9.8},
]}
SAMPLE_G = {"metadata": {}, "grid": [[0.1, 0.5], [0.8, 0.3]]}


def tmp(data):
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(data, f)
    f.close()
    return Path(f.name)


def test_load_county_data():
    cs = load_county_data(tmp(SAMPLE_C))
    assert len(cs) == 2
    assert cs[0]["name"] == "Nairobi"


def test_load_county_missing():
    with pytest.raises(FileNotFoundError):
        load_county_data("/no/such/file.json")


def test_load_drought_grid():
    grid, _ = load_drought_grid(tmp(SAMPLE_G))
    assert len(grid) == 2 and len(grid[0]) == 2


def test_normalise():
    assert normalise(5.0, 0.0, 10.0) == pytest.approx(0.5)
    assert normalise(0.0, 0.0, 10.0) == 0.0
    assert normalise(10.0, 0.0, 10.0) == 1.0
    assert normalise(-5.0, 0.0, 10.0) == 0.0
    assert normalise(5.0, 5.0, 5.0) == 0.0


def test_stress_colour_bounds():
    for v in [0.0, 0.25, 0.5, 0.75, 1.0]:
        col = stress_colour(v)
        assert len(col) == 3
        assert all(0.0 <= c <= 1.0 for c in col)


def test_stress_colour_safe():
    assert stress_colour(0.0) == PALETTE["safe"]


def test_geo_to_blender_range():
    x1, _ = geo_to_blender(0.0, 34.0)
    x2, _ = geo_to_blender(0.0, 42.0)
    assert x2 > x1
