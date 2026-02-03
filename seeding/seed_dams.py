# seeding/seed_dams.py

import os
import json
import mysql.connector
from dotenv import load_dotenv

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "dams.json")


def cfg():
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    return dict(
        host=os.getenv("LOCAL_DB_HOST", "127.0.0.1"),
        port=int(os.getenv("LOCAL_DB_PORT", "3306")),
        user=os.getenv("LOCAL_DB_USER"),
        password=os.getenv("LOCAL_DB_PASSWORD"),
        database=os.getenv("LOCAL_DB_NAME"),
    )


def load_dams():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [
        (
            d["dam_id"],
            d["dam_name"],
            d.get("full_volume"),
            d.get("lat"),
            d.get("long"),
        )
        for d in data
    ]


def main():
    dams = load_dams()
    conn = mysql.connector.connect(**cfg())
    cur = conn.cursor()
    sql = """
    INSERT INTO dams (dam_id, dam_name, full_volume, latitude, longitude)
    VALUES (%s,%s,%s,%s,%s)
    ON DUPLICATE KEY UPDATE
      dam_name=VALUES(dam_name),
      full_volume=VALUES(full_volume),
      latitude=VALUES(latitude),
      longitude=VALUES(longitude);
    """
    cur.executemany(sql, dams)
    conn.commit()
    print(f"seed_dams.py: upserted {cur.rowcount} rows ({len(dams)} dams)")
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
