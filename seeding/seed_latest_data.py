# seeding/seed_latest_data.py

import os
import json
import mysql.connector
from dotenv import load_dotenv

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "dams_resources_latest.json")


def cfg():
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    return dict(
        host=os.getenv("LOCAL_DB_HOST", "127.0.0.1"),
        port=int(os.getenv("LOCAL_DB_PORT", "3306")),
        user=os.getenv("LOCAL_DB_USER"),
        password=os.getenv("LOCAL_DB_PASSWORD"),
        database=os.getenv("LOCAL_DB_NAME"),
    )


def load_latest_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    for item in data:
        dam_id = item["dam_id"]
        dam_name = item["dam_name"]
        resources = item.get("resources", [])
        if resources:
            r = resources[0]
            rows.append((
                dam_id,
                dam_name,
                r.get("date"),
                r.get("storage_volume"),
                r.get("percentage_full"),
                r.get("storage_inflow"),
                r.get("storage_release"),
            ))
    return rows


def main():
    rows = load_latest_data()
    if not rows:
        print("seed_latest_data.py: No data found in JSON file.")
        return

    conn = mysql.connector.connect(**cfg())
    cur = conn.cursor()

    sql = """
    INSERT INTO latest_data
      (dam_id, dam_name, date, storage_volume, percentage_full, storage_inflow, storage_release)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    ON DUPLICATE KEY UPDATE
      dam_name=VALUES(dam_name),
      date=VALUES(date),
      storage_volume=VALUES(storage_volume),
      percentage_full=VALUES(percentage_full),
      storage_inflow=VALUES(storage_inflow),
      storage_release=VALUES(storage_release);
    """
    cur.executemany(sql, rows)
    conn.commit()

    print(f"seed_latest_data.py: upserted {cur.rowcount} row(s) for {len(rows)} dam(s)")
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
