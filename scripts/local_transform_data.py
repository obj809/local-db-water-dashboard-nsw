# scripts/local_transform_data.py

import os
import sys
import subprocess
from typing import List

TRANSFORM_SCRIPTS: List[str] = [
    "transform/transform_dams.py",
    "transform/transform_dam_groups.py",
    "transform/transform_dam_group_members.py",
    "transform/transform_dam_resources_historical.py",
    "transform/transform_latest_data.py",
]


def root_dir() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def main() -> None:
    print("Transforming input_data/ -> output_data/")

    for rel_path in TRANSFORM_SCRIPTS:
        full_path = os.path.join(root_dir(), rel_path)
        if not os.path.isfile(full_path):
            print(f"Missing: {rel_path}")
            sys.exit(1)

        print(f"\n=== Running {rel_path} ===")
        result = subprocess.run([sys.executable, full_path], cwd=root_dir())
        if result.returncode != 0:
            print(f"{rel_path} failed with exit code {result.returncode}")
            sys.exit(result.returncode)

    print("\nTransformation completed successfully.")


if __name__ == "__main__":
    main()
