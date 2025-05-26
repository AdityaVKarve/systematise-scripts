

from app.db.connection import get_connection
import json
from datetime import datetime

conn = get_connection()
cur = conn.cursor()

TABLES = [
    "processes",
    "events",
    "event_process_links",
    "trigger_rules",
    "process_event_log",
    "revenue_bookkeeping",
]

def pretty_print(row):
    # Converts datetime and JSON fields nicely
    def format_value(v):
        if isinstance(v, (datetime,)):
            return v.strftime("%Y-%m-%d %H:%M:%S")
        try:
            return json.dumps(v, indent=2) if isinstance(v, (dict, list)) else v
        except Exception:
            return v
    return [format_value(col) for col in row]

def view_table(table_name):
    print(f"\n--- TABLE: {table_name} ---")
    cur.execute(f"SELECT * FROM {table_name} LIMIT 20;")
    rows = cur.fetchall()
    if not rows:
        print("(No rows)")
        return
    colnames = [desc[0] for desc in cur.description]
    print(" | ".join(colnames))
    print("-" * 80)
    for r in rows:
        formatted = pretty_print(r)
        print(" | ".join(str(f) for f in formatted))

if __name__ == "__main__":
    for tbl in TABLES:
        view_table(tbl)
