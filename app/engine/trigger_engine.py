# app/engine/trigger_engine.py

from app.db import queries


# app/engine/trigger_engine.py
from app.db import queries

def handle_event_trigger(event_id, event_name):
    # Get all active rules matching event_name
    rules = queries.get_trigger_rules(event_name)
    for rule_id, process_to_spawn, params_json in rules:
        params = params_json or {}
        unit_type = params.get("unit_type", "Operations")  # fallback if missing
        amount = params.get("amount", 0.0)

        # Create the spawned process linked to this event
        spawned_process_id = queries.create_process(
            name=process_to_spawn,
            unit_type=unit_type,
            amount=amount,
            spawned_by_event_id=event_id,
            metadata=params
        )

        # Link the event to this spawned process
        queries.link_event_to_process(event_id, spawned_process_id)

        # Record revenue or cost in bookkeeping table
        # Note: costs should be negative amounts, so use the sign as is.
        if amount != 0:
            # For restock (cost), amount can be negative - you handle this in PREDEFINED_RULES by negating if needed
            queries.record_revenue(
                process_id=spawned_process_id,
                unit_type=unit_type,
                revenue=amount,  # amount can be negative for costs
                notes=f"Auto bookkeeping entry from trigger rule for event '{event_name}'"
            )
