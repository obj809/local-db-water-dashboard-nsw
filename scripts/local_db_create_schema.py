# scripts/local_db_create_schema.py

import os
import sys
import argparse
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "../schema.sql")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Drop all tables and recreate schema (DESTRUCTIVE)"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Skip confirmation prompt (for automation)"
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show what would be dropped without making changes"
    )
    return parser.parse_args()


def load_env() -> None:
    dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
    if not os.path.exists(dotenv_path):
        print(f"Error: .env not found at {dotenv_path}")
        sys.exit(1)
    load_dotenv(dotenv_path)


def db_cfg() -> dict:
    cfg = {
        "host": os.getenv("LOCAL_DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("LOCAL_DB_PORT", 3306)),
        "database": os.getenv("LOCAL_DB_NAME"),
        "user": os.getenv("LOCAL_DB_USER"),
        "password": os.getenv("LOCAL_DB_PASSWORD"),
    }
    missing = [k for k, v in cfg.items() if v in (None, "")]
    if missing:
        print(f"Error: Missing env vars: {', '.join(missing)}")
        sys.exit(1)
    return cfg


def connect(cfg: dict):
    try:
        conn = mysql.connector.connect(**cfg)
        if conn.is_connected():
            print(f"Connected to MySQL '{cfg['database']}'")
            return conn
        print("Error: could not connect to MySQL.")
        sys.exit(1)
    except Error as e:
        print(f"MySQL connection error: {e}")
        sys.exit(1)


def get_table_info(conn) -> list:
    """Return list of (table_name, row_count) tuples."""
    cur = conn.cursor()
    try:
        cur.execute("SHOW FULL TABLES WHERE Table_type='BASE TABLE';")
        tables = [r[0] for r in cur.fetchall()]
        result = []
        for t in tables:
            cur.execute(f"SELECT COUNT(*) FROM `{t}`;")
            count = cur.fetchone()[0]
            result.append((t, count))
        return result
    finally:
        cur.close()


def confirm_wipe(table_info: list, db_name: str) -> bool:
    """Show what will be deleted and ask for confirmation."""
    total_rows = sum(count for _, count in table_info)
    print(f"\n⚠️  WARNING: This will DROP all {len(table_info)} table(s) in '{db_name}':")
    for table, count in table_info:
        print(f"  - {table}: {count} rows")
    print(f"\nTotal: {total_rows} rows will be permanently deleted.\n")

    response = input("Type 'yes' to confirm: ").strip().lower()
    return response == "yes"


def wipe_all_tables(conn, dry_run: bool = False) -> None:
    cur = conn.cursor()
    try:
        cur.execute("SET FOREIGN_KEY_CHECKS=0;")
        cur.execute("SHOW FULL TABLES WHERE Table_type='BASE TABLE';")
        tables = [r[0] for r in cur.fetchall()]
        if not tables:
            print("No tables to drop.")
        else:
            if dry_run:
                print(f"[DRY RUN] Would drop {len(tables)} table(s):")
                for t in tables:
                    print(f"  - {t}")
            else:
                print(f"Dropping {len(tables)} table(s)…")
                for t in tables:
                    cur.execute(f"DROP TABLE IF EXISTS `{t}`;")
                    print(f"  - {t}")
        cur.execute("SET FOREIGN_KEY_CHECKS=1;")
        if not dry_run:
            conn.commit()
            print("Wipe complete.")
    finally:
        cur.close()


def run_schema(conn, schema_path: str, dry_run: bool = False) -> None:
    if not os.path.exists(schema_path):
        print(f"Error: schema file not found at {schema_path}")
        sys.exit(1)

    if dry_run:
        print(f"[DRY RUN] Would apply schema: {schema_path}")
        return

    with open(schema_path, "r", encoding="utf-8") as f:
        sql = f.read()

    cur = conn.cursor()
    try:
        cur.execute("SET FOREIGN_KEY_CHECKS=0;")
        print(f"Applying schema: {schema_path}")
        for _ in cur.execute(sql, multi=True):
            pass
        cur.execute("SET FOREIGN_KEY_CHECKS=1;")
        conn.commit()
        print("Schema applied successfully.")
    except Error as e:
        conn.rollback()
        print(f"Error applying schema: {e}")
        sys.exit(1)
    finally:
        cur.close()


def main() -> None:
    args = parse_args()
    load_env()
    cfg = db_cfg()
    conn = connect(cfg)
    try:
        table_info = get_table_info(conn)

        if table_info and not args.force and not args.dry_run:
            if not confirm_wipe(table_info, cfg["database"]):
                print("Aborted.")
                sys.exit(0)

        wipe_all_tables(conn, dry_run=args.dry_run)
        run_schema(conn, SCHEMA_FILE, dry_run=args.dry_run)

        if args.dry_run:
            print("\n[DRY RUN] No changes made.")
    finally:
        if conn.is_connected():
            conn.close()
            print("MySQL connection closed.")


if __name__ == "__main__":
    main()
