# seeding/seed_dam_group_members.py

import os
import json
import mysql.connector
from dotenv import load_dotenv

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "output_data", "dam_group_members.json")


def cfg():
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    return dict(
        host=os.getenv("LOCAL_DB_HOST", "127.0.0.1"),
        port=int(os.getenv("LOCAL_DB_PORT", "3306")),
        user=os.getenv("LOCAL_DB_USER"),
        password=os.getenv("LOCAL_DB_PASSWORD"),
        database=os.getenv("LOCAL_DB_NAME"),
    )


def load_dam_group_members():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [(d["group_name"], d["dam_id"]) for d in data]


def main():
    members = load_dam_group_members()
    if not members:
        print("seed_dam_group_members.py: No data found in JSON file.")
        return

    conn = mysql.connector.connect(**cfg())
    cur = conn.cursor()
    sql = """
    INSERT INTO dam_group_members (group_name, dam_id)
    VALUES (%s,%s)
    ON DUPLICATE KEY UPDATE group_name=VALUES(group_name), dam_id=VALUES(dam_id);
    """
    cur.executemany(sql, members)
    conn.commit()
    print(f"seed_dam_group_members.py: upserted {cur.rowcount} rows ({len(members)} members)")
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
