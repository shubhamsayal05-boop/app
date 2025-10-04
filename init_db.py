import sqlite3
from pathlib import Path

BASE = Path(__file__).parent
SCHEMA_FILE = BASE / "init_odriv.sql"
DB_FILE = BASE / "odriv.db"

with open(SCHEMA_FILE, "r") as f:
    schema = f.read()

with sqlite3.connect(DB_FILE) as conn:
    conn.executescript(schema)

print(f"Database created as {DB_FILE}")