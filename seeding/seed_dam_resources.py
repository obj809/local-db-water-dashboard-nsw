# seeding/seed_dam_resources.py

import os
import json
import mysql.connector
from dotenv import load_dotenv

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "output_data", "dam_resources.json")


def cfg():
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    return dict(
        host=os.getenv("LOCAL_DB_HOST", "127.0.0.1"),
        port=int(os.getenv("LOCAL_DB_PORT", "3306")),
        user=os.getenv("LOCAL_DB_USER"),
        password=os.getenv("LOCAL_DB_PASSWORD"),
        database=os.getenv("LOCAL_DB_NAME"),
    )


def load_dam_resources():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [
        (
            d["dam_id"],
            d.get("date"),
            d.get("storage_volume"),
            d.get("percentage_full"),
            d.get("storage_inflow"),
            d.get("storage_release"),
        )
        for d in data
    ]


def main():
    rows = load_dam_resources()
    if not rows:
        print("seed_dam_resources.py: No data found in JSON file.")
        return

    conn = mysql.connector.connect(**cfg())
    cur = conn.cursor()

    sql = """
    INSERT INTO dam_resources
      (dam_id, date, storage_volume, percentage_full, storage_inflow, storage_release)
    VALUES (%s,%s,%s,%s,%s,%s)
    ON DUPLICATE KEY UPDATE
      storage_volume=VALUES(storage_volume),
      percentage_full=VALUES(percentage_full),
      storage_inflow=VALUES(storage_inflow),
      storage_release=VALUES(storage_release);
    """
    cur.executemany(sql, rows)
    conn.commit()

    print(f"seed_dam_resources.py: upserted {cur.rowcount} rows ({len(rows)} records)")
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
