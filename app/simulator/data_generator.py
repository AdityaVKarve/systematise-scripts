import random
from datetime import datetime, timedelta
from app.engine.process_manager import create_event_and_handle
from app.engine.trigger_engine import handle_event_trigger
from app.db import queries
from app.simulator.customer_simulator import Customer
import json

# === CONFIGURATION ===

SIMULATION_START = datetime.now() - timedelta(days=14)
SIMULATION_END = datetime.now()

# Example trigger rules for simulation setup
PREDEFINED_RULES = [
    {
        "event_name": "Order Drink",
        "process_to_spawn": "Order Drink",
        "parameters": {"unit_type": "Sales", "amount": 4.50},
    },
    {
        "event_name": "Customer Sign Up",
        "process_to_spawn": "Register Customer",
        "parameters": {"unit_type": "Marketing"},
    }
]

# === SETUP UTILITIES ===

def insert_dummy_rules():
    for rule in PREDEFINED_RULES:
        queries.cur.execute("""
            INSERT INTO trigger_rules (event_name, process_to_spawn, parameters)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, (rule["event_name"], rule["process_to_spawn"], json.dumps(rule["parameters"])))

def clear_database():
    tables = [
        "process_event_log",
        "event_process_links",
        "revenue_bookkeeping",
        "trigger_rules",
        "processes",
        "events",
    ]
    print("Clearing database tables...")
    for table in tables:
        queries.cur.execute(f"TRUNCATE TABLE {table} CASCADE;")
    print("Database cleared.")

# === SIMULATOR CORE ===

def simulate_day(date):
    customer_count = random.randint(20, 30)
    for _ in range(customer_count):
        name = random.choice(["Alice", "Bob", "Carlos", "Diana", "Eva", "Frank"])
        customer = Customer(f"{name}-{random.randint(1000, 9999)}")
        customer.visited_at = datetime.combine(date.date(), datetime.min.time()) + timedelta(
            minutes=random.randint(8 * 60, 18 * 60)
        )
        customer.simulate()

def run_simulation():
    clear_database()
    print("Inserting predefined rules...")
    insert_dummy_rules()

    current_day = SIMULATION_START
    while current_day <= SIMULATION_END:
        print(f"Simulating {current_day.date()}...")
        simulate_day(current_day)
        current_day += timedelta(days=1)

    print("Simulation complete.")

# === ENTRY POINT ===

if __name__ == "__main__":
    run_simulation()
