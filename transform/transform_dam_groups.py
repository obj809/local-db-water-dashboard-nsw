# transform/transform_dam_groups.py

import os
import json

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "output_data", "dam_groups.json")

# Dam group definitions (no input file - these are manually curated categories)
GROUPS = [
    {"group_name": "sydney_dams"},
    {"group_name": "popular_dams"},
    {"group_name": "large_dams"},
    {"group_name": "small_dams"},
    {"group_name": "greatest_released"},
]


def main():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(GROUPS, f, indent=2)

    print(f"Generated {len(GROUPS)} dam groups")
    print(f"Output written to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
