# scripts/local_db_create_procedures.py

import os
import sys
import mysql.connector
from dotenv import load_dotenv

SQL_FILE = os.path.join(os.path.dirname(__file__), "../queries/analysis_procedures.sql")


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
    if not os.path.exists(SQL_FILE):
        print(f"Error: SQL file not found at {SQL_FILE}")
        sys.exit(1)

    with open(SQL_FILE, "r", encoding="utf-8") as f:
        sql_content = f.read()

    conn = mysql.connector.connect(**cfg())
    cursor = conn.cursor()

    print(f"Connected to {cfg()['database']}")

    # Split by DELIMITER and handle each section
    # We need to execute statements with proper delimiter handling
    statements = []
    current_delimiter = ";"
    current_statement = ""

    lines = sql_content.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Check for DELIMITER change
        if line.upper().startswith("DELIMITER"):
            parts = line.split()
            if len(parts) >= 2:
                # Execute any pending statement
                if current_statement.strip():
                    statements.append(current_statement.strip())
                    current_statement = ""
                current_delimiter = parts[1]
            i += 1
            continue

        # Skip empty lines and comments at statement start
        if not current_statement and (not line or line.startswith("--")):
            i += 1
            continue

        current_statement += lines[i] + "\n"

        # Check if statement is complete
        if current_delimiter == ";" and line.endswith(";"):
            statements.append(current_statement.strip())
            current_statement = ""
        elif current_delimiter != ";" and line.endswith(current_delimiter):
            # Remove the custom delimiter from the end
            stmt = current_statement.strip()
            if stmt.endswith(current_delimiter):
                stmt = stmt[:-len(current_delimiter)].strip()
            statements.append(stmt)
            current_statement = ""

        i += 1

    # Add any remaining statement
    if current_statement.strip():
        statements.append(current_statement.strip())

    # Execute each statement
    for stmt in statements:
        if not stmt or stmt.startswith("--"):
            continue
        try:
            # Handle multi-statement results
            for result in cursor.execute(stmt, multi=True):
                if result.with_rows:
                    rows = result.fetchall()
                    for row in rows:
                        print(row)
            conn.commit()
            # Print a summary of what was executed
            first_line = stmt.split("\n")[0][:60]
            print(f"OK: {first_line}...")
        except mysql.connector.Error as e:
            print(f"Error executing: {stmt[:50]}...")
            print(f"  {e}")

    cursor.close()
    conn.close()
    print("\nProcedures and event created successfully.")
    print("\nTo manually trigger the analysis:")
    print("  CALL calculate_dam_analysis();")


if __name__ == "__main__":
    main()
