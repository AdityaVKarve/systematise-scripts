DROP DATABASE IF EXISTS coffee_shop;
CREATE DATABASE coffee_shop;
-- === ENUM TYPES ===
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'unit_type_enum') THEN
        CREATE TYPE unit_type_enum AS ENUM ('Sales', 'Marketing', 'Operations', 'Support', 'Logistics');
    END IF;
END$$;

-- === DOMAIN TABLES ===
CREATE TABLE IF NOT EXISTS event_definitions (
    event_name TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS process_definitions (
    process_name TEXT PRIMARY KEY,
    child_processes TEXT[],
    metadata_fields JSONB,
    execution_order TEXT,
    trigger_event TEXT REFERENCES event_definitions(event_name)
);

-- === EVENTS ===
CREATE TABLE IF NOT EXISTS events (
    event_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_process_id INTEGER,
    metadata JSONB DEFAULT '{}'
);

-- === PROCESSES ===
CREATE TABLE IF NOT EXISTS processes (
    process_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    unit_type unit_type_enum NOT NULL,
    amount NUMERIC(10, 2),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    parent_process_id INTEGER,
    spawned_by_event_id INTEGER,
    metadata JSONB DEFAULT '{}'
);

-- === LINKS AND LOGS ===
CREATE TABLE IF NOT EXISTS event_process_links (
    link_id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL,
    spawned_process_id INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS trigger_rules (
    rule_id SERIAL PRIMARY KEY,
    event_name TEXT NOT NULL,
    process_to_spawn TEXT NOT NULL,
    parameters JSONB,
    priority INTEGER DEFAULT 0,
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS process_event_log (
    log_id SERIAL PRIMARY KEY,
    description TEXT,
    related_process_id INTEGER,
    related_event_id INTEGER,
    log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS revenue_bookkeeping (
    entry_id SERIAL PRIMARY KEY,
    process_id INTEGER,
    unit_type unit_type_enum NOT NULL,
    revenue NUMERIC(10, 2) NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);

-- === FOREIGN KEYS ===
ALTER TABLE processes
    ADD CONSTRAINT fk_parent_process FOREIGN KEY (parent_process_id) REFERENCES processes(process_id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_spawned_by_event FOREIGN KEY (spawned_by_event_id) REFERENCES events(event_id) ON DELETE SET NULL;

ALTER TABLE events
    ADD CONSTRAINT fk_source_process FOREIGN KEY (source_process_id) REFERENCES processes(process_id) ON DELETE SET NULL;

ALTER TABLE event_process_links
    ADD CONSTRAINT fk_epl_event FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_epl_process FOREIGN KEY (spawned_process_id) REFERENCES processes(process_id) ON DELETE CASCADE;

ALTER TABLE process_event_log
    ADD CONSTRAINT fk_log_process FOREIGN KEY (related_process_id) REFERENCES processes(process_id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_log_event FOREIGN KEY (related_event_id) REFERENCES events(event_id) ON DELETE SET NULL;

ALTER TABLE revenue_bookkeeping
    ADD CONSTRAINT fk_revenue_process FOREIGN KEY (process_id) REFERENCES processes(process_id) ON DELETE CASCADE;

-- === INDEXES ===
CREATE INDEX IF NOT EXISTS idx_process_unit_type ON processes(unit_type);
CREATE INDEX IF NOT EXISTS idx_event_name ON events(name);
CREATE INDEX IF NOT EXISTS idx_bookkeeping_date ON revenue_bookkeeping(recorded_at);
