# seeding/seed_dam_groups.py

import os
import json
import mysql.connector
from dotenv import load_dotenv

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "output_data", "dam_groups.json")


def cfg():
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    return dict(
        host=os.getenv("LOCAL_DB_HOST", "127.0.0.1"),
        port=int(os.getenv("LOCAL_DB_PORT", "3306")),
        user=os.getenv("LOCAL_DB_USER"),
        password=os.getenv("LOCAL_DB_PASSWORD"),
        database=os.getenv("LOCAL_DB_NAME"),
    )


def load_dam_groups():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [(d["group_name"],) for d in data]


def main():
    groups = load_dam_groups()
    conn = mysql.connector.connect(**cfg())
    cur = conn.cursor()
    sql = """
    INSERT INTO dam_groups (group_name)
    VALUES (%s)
    ON DUPLICATE KEY UPDATE group_name=VALUES(group_name);
    """
    cur.executemany(sql, groups)
    conn.commit()
    print(f"seed_dam_groups.py: upserted {cur.rowcount} rows ({len(groups)} groups)")
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
