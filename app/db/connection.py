# app/db/connection.py

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Required ENV vars
required_vars = ["DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT"]
missing = [var for var in required_vars if os.getenv(var) is None]

if missing:
    raise EnvironmentError(f"Missing required database environment variables: {missing}")

# Build config dictionary
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

# Log basic (non-sensitive) config
print(f"Connecting to DB: dbname={DB_CONFIG['dbname']}, user={DB_CONFIG['user']}, host={DB_CONFIG['host']}")

def get_connection():
    return psycopg2.connect(**DB_CONFIG)
