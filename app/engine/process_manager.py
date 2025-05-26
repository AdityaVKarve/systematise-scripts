# app/engine/process_manager.py

from app.db import queries
from datetime import datetime

def create_process_and_link(name, unit_type, amount=0.0, parent_id=None, spawned_by_event_id=None, metadata=None):
    process_id = queries.create_process(
        name=name,
        unit_type=unit_type,
        amount=amount,
        parent_id=parent_id,
        spawned_by_event_id=spawned_by_event_id,
        metadata=metadata
    )
    queries.log_event(f"Created process '{name}' (unit: {unit_type})", process_id=process_id)
    return process_id

def create_event_and_handle(name, description="", source_process_id=None, metadata=None, logger=None):
    event_id = queries.create_event(
        name=name,
        description=description,
        source_process_id=source_process_id,
        metadata=metadata
    )
    queries.log_event(f"New event: {name}", event_id=event_id)
    if logger:
        logger.info(f"Event logged: {name} with ID {event_id}")
    
    # Trigger process spawning for this event
    handle_event_trigger(event_id, name, logger=logger)

    return event_id


def handle_event_trigger(event_id, event_name, logger=None):
    rules = queries.get_trigger_rules(event_name)
    spawned_processes = []

    for rule in rules:
        rule_id, process_to_spawn, parameters_json = rule
        parameters = parameters_json or {}

        process_id = queries.create_process(
            name=process_to_spawn,
            unit_type=parameters.get("unit_type", "Unknown"),
            amount=parameters.get("amount"),
            parent_id=None,
            spawned_by_event_id=event_id,
            metadata=parameters,
            date=datetime.now()
        )
        queries.link_event_to_process(event_id, process_id)

        message = (
            f"Triggered process '{process_to_spawn}' (ID: {process_id}) "
            f"from event '{event_name}' (ID: {event_id})"
        )
        queries.log_event(message, process_id=process_id, event_id=event_id)
        if logger:
            logger.info(message)

        spawned_processes.append(process_id)

    return spawned_processes
