# transform/transform_dams.py

import os
import json

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")
INPUT_FILE = os.path.join(PROJECT_ROOT, "input_data", "dams.json")
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "output_data", "dams.json")


def transform_dam(dam: dict) -> dict:
    """Transform a dam record to match schema.sql format."""
    return {
        "dam_id": dam["dam_id"],
        "dam_name": dam["dam_name"],
        "full_volume": dam.get("full_volume"),
        "latitude": dam.get("lat"),
        "longitude": dam.get("long"),
    }


def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file not found: {INPUT_FILE}")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        input_data = json.load(f)

    output_data = [transform_dam(dam) for dam in input_data]

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

    print(f"Transformed {len(output_data)} dams")
    print(f"Output written to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
