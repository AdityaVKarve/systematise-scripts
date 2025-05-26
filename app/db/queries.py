# app/db/queries.py

from app.db.connection import get_connection
from app.db import connection
from datetime import datetime
import json
conn = get_connection()
conn.autocommit = True
cur = conn.cursor()

# === PROCESS OPERATIONS ===

def create_process(name, unit_type, amount=None, parent_id=None, spawned_by_event_id=None, metadata=None, date=None):
    metadata = metadata or {}
    date = date or datetime.now()

    cur.execute("""
        INSERT INTO processes (name, unit_type, amount, date, parent_process_id, spawned_by_event_id, metadata)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING process_id;
    """, (name, unit_type, amount, date, parent_id, spawned_by_event_id, json.dumps(metadata)))
    
    return cur.fetchone()[0]

def get_process(process_id):
    cur.execute("SELECT * FROM processes WHERE process_id = %s;", (process_id,))
    return cur.fetchone()

# === EVENT OPERATIONS ===

def create_event(name, description=None, source_process_id=None, metadata=None, triggered_at=None):
    metadata = metadata or {}
    triggered_at = triggered_at or datetime.now()

    cur.execute("""
        INSERT INTO events (name, description, source_process_id, triggered_at, metadata)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING event_id;
    """, (name, description, source_process_id, triggered_at, json.dumps(metadata)))
    
    return cur.fetchone()[0]

def get_event(event_id):
    cur.execute("SELECT * FROM events WHERE event_id = %s;", (event_id,))
    return cur.fetchone()

# === EVENT → PROCESS LINKING ===

def link_event_to_process(event_id, process_id):
    cur.execute("""
        INSERT INTO event_process_links (event_id, spawned_process_id)
        VALUES (%s, %s);
    """, (event_id, process_id))

# === LOGGING ===

def log_event(description, process_id=None, event_id=None, log_time=None):
    log_time = log_time or datetime.now()

    cur.execute("""
        INSERT INTO process_event_log (description, related_process_id, related_event_id, log_time)
        VALUES (%s, %s, %s, %s);
    """, (description, process_id, event_id, log_time))

# === TRIGGER RULES ===

def get_trigger_rules(event_name):
    cur.execute("""
        SELECT rule_id, process_to_spawn, parameters
        FROM trigger_rules
        WHERE event_name = %s AND active = TRUE
        ORDER BY priority DESC;
    """, (event_name,))
    return cur.fetchall()

# === REVENUE TRACKING ===

def record_revenue(process_id, unit_type, revenue, notes=None, recorded_at=None):
    recorded_at = recorded_at or datetime.now()

    cur.execute("""
        INSERT INTO revenue_bookkeeping (process_id, unit_type, revenue, recorded_at, notes)
        VALUES (%s, %s, %s, %s, %s);
    """, (process_id, unit_type, revenue, recorded_at, notes))
