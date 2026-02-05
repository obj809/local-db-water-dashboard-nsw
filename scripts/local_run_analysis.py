# scripts/local_run_analysis.py

import os
import mysql.connector
from dotenv import load_dotenv


def cfg():
    load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))
    return dict(
        host=os.getenv("LOCAL_DB_HOST", "127.0.0.1"),
        port=int(os.getenv("LOCAL_DB_PORT", "3306")),
        user=os.getenv("LOCAL_DB_USER"),
        password=os.getenv("LOCAL_DB_PASSWORD"),
        database=os.getenv("LOCAL_DB_NAME"),
    )


def main():
    conn = mysql.connector.connect(**cfg())
    cursor = conn.cursor()

    print("Running dam analysis calculation...")

    for result in cursor.execute("CALL calculate_dam_analysis()", multi=True):
        if result.with_rows:
            for row in result.fetchall():
                print(row[0])

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
