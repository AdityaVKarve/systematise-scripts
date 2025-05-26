# === load_definitions.py ===
import csv
from app.db import queries
import json

def load_event_definitions(csv_path):
    with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            event_name = row['Event'].strip()
            queries.cur.execute("""
                INSERT INTO event_definitions (event_name)
                VALUES (%s)
                ON CONFLICT (event_name) DO NOTHING;
            """, (event_name,))

def load_process_definitions(csv_path):
    with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            process_name = row['Process'].strip()
            children = [x.strip() for x in row['Child Processes'].split(',')] if row['Child Processes'] else []
            metadata_fields = json.dumps([x.strip() for x in row['Metadata'].split(',')]) if row['Metadata'] else json.dumps([])
            execution_order = row.get('Child execution order', '').strip() or 'sequential'

            trigger_event = row.get('Trigger', '').strip()
            if trigger_event == "NA" or trigger_event == "":
                trigger_event = None  # treat as NULL to avoid FK violation

            queries.cur.execute("""
                INSERT INTO process_definitions 
                    (process_name, child_processes, metadata_fields, execution_order, trigger_event)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (process_name) DO UPDATE 
                    SET child_processes = EXCLUDED.child_processes,
                        metadata_fields = EXCLUDED.metadata_fields,
                        execution_order = EXCLUDED.execution_order,
                        trigger_event = EXCLUDED.trigger_event;
            """, (process_name, children, metadata_fields, execution_order, trigger_event))



if __name__ == '__main__':
    import os
    print(os.getcwd())
    load_event_definitions('./app/processes_and_events/events.csv')
    load_process_definitions('./app/processes_and_events/processes.csv')
    print("Event and process definitions loaded.")
