# seeding/seed_dam_group_members.py

import os
import mysql.connector
from dotenv import load_dotenv

MEMBERS = [
    # Sydney dams
    ("sydney_dams", "212232"),  # Cataract Dam
    ("sydney_dams", "212220"),  # Cordeaux Dam
    ("sydney_dams", "212211"),  # Avon Dam
    ("sydney_dams", "212205"),  # Nepean Dam
    ("sydney_dams", "213210"),  # Woronora Dam
    ("sydney_dams", "213240"),  # Prospect Reservoir
    ("sydney_dams", "212212"),  # Wingecarribee Reservoir
    ("sydney_dams", "215235"),  # Fitzroy Falls Reservoir
    # Popular dams
    ("popular_dams", "212243"),  # Warragamba Dam
    ("popular_dams", "212232"),  # Cataract Dam
    ("popular_dams", "212220"),  # Cordeaux Dam
    ("popular_dams", "212211"),  # Avon Dam
    ("popular_dams", "212205"),  # Nepean Dam
    ("popular_dams", "213210"),  # Woronora Dam
    ("popular_dams", "215212"),  # Tallowa Dam
    ("popular_dams", "213240"),  # Prospect Reservoir
    # Large dams (>500,000 ML capacity)
    ("large_dams", "401027"),   # Hume Dam
    ("large_dams", "212243"),   # Warragamba Dam
    ("large_dams", "410102"),   # Blowering Dam
    ("large_dams", "412010"),   # Lake Wyangala
    ("large_dams", "418035"),   # Copeton Dam
    ("large_dams", "410131"),   # Burrinjuck Dam
    ("large_dams", "421078"),   # Burrendong Dam
    ("large_dams", "210097"),   # Glenbawn Dam
    # Small dams (<50,000 ML capacity)
    ("small_dams", "219033"),   # Cochrane Dam
    ("small_dams", "215235"),   # Fitzroy Falls Reservoir
    ("small_dams", "215212"),   # Tallowa Dam
    ("small_dams", "42510037"), # Lake Copi Hollow
    ("small_dams", "219027"),   # Brogo Dam
    ("small_dams", "203042"),   # Toonumbar Dam
    ("small_dams", "210102"),   # Lostock Dam
    ("small_dams", "412107"),   # Lake Cargelligo
    # Greatest released
    ("greatest_released", "401027"),  # Hume Dam
    ("greatest_released", "410102"),  # Blowering Dam
    ("greatest_released", "410131"),  # Burrinjuck Dam
    ("greatest_released", "421078"),  # Burrendong Dam
    ("greatest_released", "418035"),  # Copeton Dam
    ("greatest_released", "210117"),  # Glennies Creek Dam
    ("greatest_released", "210097"),  # Glenbawn Dam
    ("greatest_released", "419041"),  # Keepit Dam
]


def cfg():
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    return dict(
        host=os.getenv("LOCAL_DB_HOST", "127.0.0.1"),
        port=int(os.getenv("LOCAL_DB_PORT", "3306")),
        user=os.getenv("LOCAL_DB_USER"),
        password=os.getenv("LOCAL_DB_PASSWORD"),
        database=os.getenv("LOCAL_DB_NAME"),
    )


def main():
    conn = mysql.connector.connect(**cfg())
    cur = conn.cursor()
    sql = """
    INSERT INTO dam_group_members (group_name, dam_id)
    VALUES (%s,%s)
    ON DUPLICATE KEY UPDATE group_name=VALUES(group_name), dam_id=VALUES(dam_id);
    """
    cur.executemany(sql, MEMBERS)
    conn.commit()
    print(f"seed_dam_group_members.py: upserted {cur.rowcount} rows ({len(MEMBERS)} members)")
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
