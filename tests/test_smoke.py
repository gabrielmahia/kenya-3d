"""
tests/test_smoke.py
Smoke test entry point — delegates to test_imports and test_data_loader.
Running this file alone gives a fast pass/fail signal.
"""
from tests.test_imports import (
    test_data_loader_imports,
    test_materials_imports,
    test_fetchers_import,
)
from tests.test_data_loader import (
    test_load_county_data,
    test_normalise,
    test_stress_colour_bounds,
    test_geo_to_blender_range,
)

__all__ = [
    "test_data_loader_imports",
    "test_materials_imports",
    "test_fetchers_import",
    "test_load_county_data",
    "test_normalise",
    "test_stress_colour_bounds",
    "test_geo_to_blender_range",
]
