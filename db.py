import sqlite3
from pathlib import Path
import os

DB_PATH = Path(os.path.dirname(os.path.abspath(__file__))).parent / "data" / "odriv.db"
print(f"DB_PATH resolved to: {DB_PATH}")

if not DB_PATH.exists():
    raise FileNotFoundError(f"SQLite DB missing at {DB_PATH}")

def get_conn():
    return sqlite3.connect(DB_PATH)

def get_projects():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, vehicle, milestone, user FROM projects ORDER BY id DESC")
        return [
            {"id": row[0], "name": row[1], "vehicle": row[2], "milestone": row[3], "user": row[4]}
            for row in cur.fetchall()
        ]

def add_project(name, vehicle, milestone, user):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO projects (name, vehicle, milestone, user) VALUES (?, ?, ?, ?)",
            (name, vehicle, milestone, user)
        )
        conn.commit()
        return cur.lastrowid

def get_project_details(project_id):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, name, vehicle, milestone, user, created_at FROM projects WHERE id=?",
            (project_id,)
        )
        row = cur.fetchone()
        if row:
            return {
                "id": row[0], "name": row[1], "vehicle": row[2],
                "milestone": row[3], "user": row[4], "created_at": row[5]
            }
        else:
            return {}

def get_dropdown_options(table):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT value FROM {table}")
        return [{"label": row[0], "value": row[0]} for row in cur.fetchall()]

def save_project_rating(project_id, drivability_score, status, warnings):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO project_ratings (project_id, drivability_score, status, warnings) VALUES (?, ?, ?, ?)",
            (project_id, drivability_score, status, warnings)
        )
        conn.commit()

def get_latest_project_rating(project_id):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT drivability_score, status, warnings FROM project_ratings WHERE project_id=? ORDER BY id DESC LIMIT 1",
            (project_id,)
        )
        row = cur.fetchone()
        if row:
            return {"drivability_score": row[0], "status": row[1], "warnings": row[2]}
        return {}