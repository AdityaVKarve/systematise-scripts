import csv
from app.db import queries

def export_processes_events(filename="processes_events.csv"):
    # Fetch processes and events ordered by timestamp
    queries.cur.execute("""
        SELECT process_id, name, unit_type, amount, date, parent_process_id, spawned_by_event_id, metadata
        FROM processes
        ORDER BY date ASC;
    """)
    processes = queries.cur.fetchall()

    queries.cur.execute("""
        SELECT event_id, name, description, triggered_at, source_process_id, metadata
        FROM events
        ORDER BY triggered_at ASC;
    """)
    events = queries.cur.fetchall()

    # Write to CSV: We'll write processes and events sequentially in one file
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Header for processes
        writer.writerow([
            "type", "id", "name", "unit_type/description", "amount", "timestamp", "parent_process_id", "spawned_by_event_id/source_process_id", "metadata"
        ])

        for p in processes:
            writer.writerow([
                "process",
                p[0],          # process_id
                p[1],          # name
                p[2],          # unit_type
                p[3],          # amount
                p[4],          # date
                p[5],          # parent_process_id
                p[6],          # spawned_by_event_id
                p[7],          # metadata json
            ])

        for e in events:
            writer.writerow([
                "event",
                e[0],          # event_id
                e[1],          # name
                e[2],          # description
                "",            # amount empty for event
                e[3],          # triggered_at
                "",            # no parent_process_id
                e[4],          # source_process_id
                e[5],          # metadata json
            ])

    print(f"Exported processes and events to {filename}")

def export_bookkeeping(filename="bookkeeping.csv"):
    queries.cur.execute("""
        SELECT entry_id, process_id, unit_type, revenue, recorded_at, notes
        FROM revenue_bookkeeping
        ORDER BY recorded_at ASC;
    """)
    rows = queries.cur.fetchall()

    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "entry_id", "process_id", "unit_type", "revenue", "recorded_at", "notes"
        ])
        for r in rows:
            writer.writerow(r)

    print(f"Exported bookkeeping data to {filename}")

if __name__ == "__main__":
    export_processes_events()
    export_bookkeeping()
