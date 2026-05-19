"""
fetchers/wapimaji.py
kenya-3d — Live drought/water data from wapimaji-mcp.

REAL data mode: requires wapimaji-mcp running.
See: https://github.com/gabrielmahia/wapimaji-mcp
"""
from __future__ import annotations
import json, urllib.request, urllib.error, urllib.parse
from pathlib import Path
from typing import Any

WAPIMAJI_BASE = "http://localhost:8080"


def get_county_water_stress(county: str | None = None) -> list[dict[str, Any]]:
    """Fetch county water stress from wapimaji-mcp."""
    url = f"{WAPIMAJI_BASE}/water-stress"
    if county:
        url += f"?county={urllib.parse.quote(county)}"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return json.loads(r.read()).get("counties", [])
    except urllib.error.URLError as e:
        raise ConnectionError(
            f"wapimaji-mcp not reachable at {WAPIMAJI_BASE}. "
            "Start with: uvx wapimaji-mcp"
        ) from e


def get_drought_grid() -> dict[str, Any]:
    """Fetch live drought grid from wapimaji-mcp."""
    url = f"{WAPIMAJI_BASE}/drought-grid"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.URLError as e:
        raise ConnectionError(f"wapimaji-mcp not reachable at {WAPIMAJI_BASE}.") from e


def fallback_demo(data_file: str) -> dict:
    """Load DEMO data when wapimaji-mcp is unavailable."""
    p = Path(data_file)
    if not p.exists():
        raise FileNotFoundError(f"Demo data not found: {p}")
    with open(p) as f:
        return json.load(f)


if __name__ == "__main__":
    print("Testing wapimaji-mcp...")
    try:
        data = get_county_water_stress()
        print(f"Connected — {len(data)} counties")
    except ConnectionError as e:
        print(f"Not reachable: {e}")
        print("Falling back to DEMO data")
