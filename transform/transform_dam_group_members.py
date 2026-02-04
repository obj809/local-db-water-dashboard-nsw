# transform/transform_dam_group_members.py

import os
import json

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "output_data", "dam_group_members.json")

# Dam group membership definitions (manually curated)
MEMBERS = [
    # Sydney dams
    {"group_name": "sydney_dams", "dam_id": "212232"},  # Cataract Dam
    {"group_name": "sydney_dams", "dam_id": "212220"},  # Cordeaux Dam
    {"group_name": "sydney_dams", "dam_id": "212211"},  # Avon Dam
    {"group_name": "sydney_dams", "dam_id": "212205"},  # Nepean Dam
    {"group_name": "sydney_dams", "dam_id": "213210"},  # Woronora Dam
    {"group_name": "sydney_dams", "dam_id": "213240"},  # Prospect Reservoir
    {"group_name": "sydney_dams", "dam_id": "212212"},  # Wingecarribee Reservoir
    {"group_name": "sydney_dams", "dam_id": "215235"},  # Fitzroy Falls Reservoir
    # Popular dams
    {"group_name": "popular_dams", "dam_id": "212243"},  # Warragamba Dam
    {"group_name": "popular_dams", "dam_id": "212232"},  # Cataract Dam
    {"group_name": "popular_dams", "dam_id": "212220"},  # Cordeaux Dam
    {"group_name": "popular_dams", "dam_id": "212211"},  # Avon Dam
    {"group_name": "popular_dams", "dam_id": "212205"},  # Nepean Dam
    {"group_name": "popular_dams", "dam_id": "213210"},  # Woronora Dam
    {"group_name": "popular_dams", "dam_id": "215212"},  # Tallowa Dam
    {"group_name": "popular_dams", "dam_id": "213240"},  # Prospect Reservoir
    # Large dams (>500,000 ML capacity)
    {"group_name": "large_dams", "dam_id": "401027"},   # Hume Dam
    {"group_name": "large_dams", "dam_id": "212243"},   # Warragamba Dam
    {"group_name": "large_dams", "dam_id": "410102"},   # Blowering Dam
    {"group_name": "large_dams", "dam_id": "412010"},   # Lake Wyangala
    {"group_name": "large_dams", "dam_id": "418035"},   # Copeton Dam
    {"group_name": "large_dams", "dam_id": "410131"},   # Burrinjuck Dam
    {"group_name": "large_dams", "dam_id": "421078"},   # Burrendong Dam
    {"group_name": "large_dams", "dam_id": "210097"},   # Glenbawn Dam
    # Small dams (<50,000 ML capacity)
    {"group_name": "small_dams", "dam_id": "219033"},   # Cochrane Dam
    {"group_name": "small_dams", "dam_id": "215235"},   # Fitzroy Falls Reservoir
    {"group_name": "small_dams", "dam_id": "215212"},   # Tallowa Dam
    {"group_name": "small_dams", "dam_id": "42510037"}, # Lake Copi Hollow
    {"group_name": "small_dams", "dam_id": "219027"},   # Brogo Dam
    {"group_name": "small_dams", "dam_id": "203042"},   # Toonumbar Dam
    {"group_name": "small_dams", "dam_id": "210102"},   # Lostock Dam
    {"group_name": "small_dams", "dam_id": "412107"},   # Lake Cargelligo
    # Greatest released
    {"group_name": "greatest_released", "dam_id": "401027"},  # Hume Dam
    {"group_name": "greatest_released", "dam_id": "410102"},  # Blowering Dam
    {"group_name": "greatest_released", "dam_id": "410131"},  # Burrinjuck Dam
    {"group_name": "greatest_released", "dam_id": "421078"},  # Burrendong Dam
    {"group_name": "greatest_released", "dam_id": "418035"},  # Copeton Dam
    {"group_name": "greatest_released", "dam_id": "210117"},  # Glennies Creek Dam
    {"group_name": "greatest_released", "dam_id": "210097"},  # Glenbawn Dam
    {"group_name": "greatest_released", "dam_id": "419041"},  # Keepit Dam
]


def main():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(MEMBERS, f, indent=2)

    print(f"Generated {len(MEMBERS)} dam group memberships")
    print(f"Output written to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
