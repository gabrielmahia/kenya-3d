"""
fetchers/counties.py
kenya-3d — Kenya county reference data from open sources.

REAL data mode — Kenya National Bureau of Statistics / HDX.
"""
from __future__ import annotations
import json, urllib.request
from pathlib import Path

KNBS_URL    = "https://raw.githubusercontent.com/mikelmaron/kenyadata/master/data/counties.geojson"
OUTPUT_PATH = Path(__file__).parent.parent / "data" / "counties_live.json"


def download_county_data(output: Path = OUTPUT_PATH) -> list[dict]:
    print("Downloading Kenya county data...")
    try:
        with urllib.request.urlopen(KNBS_URL, timeout=20) as r:
            geo = json.loads(r.read())
    except Exception as e:
        raise RuntimeError(f"Download failed: {e}") from e

    counties = []
    for f in geo.get("features", []):
        props = f.get("properties", {})
        counties.append({
            "name": props.get("COUNTY_NAM", props.get("name", "Unknown")),
            "code": props.get("COUNTY_COD"),
            "geometry_type": f.get("geometry", {}).get("type"),
        })

    output.parent.mkdir(exist_ok=True)
    with open(output, "w") as fp:
        json.dump({"counties": counties, "source": KNBS_URL}, fp, indent=2)
    print(f"Saved {len(counties)} counties to {output}")
    return counties


if __name__ == "__main__":
    download_county_data()
