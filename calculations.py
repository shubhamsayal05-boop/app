from logic.db import get_conn, get_latest_project_rating

def get_thresholds():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT key, value FROM config")
        thresholds = {row[0]: float(row[1]) for row in cur.fetchall()}
    return thresholds

def calculate_project_rating(project_id):
    thresholds = get_thresholds()
    drivability_score = 90 + (project_id % 10)
    status = "GREEN" if drivability_score >= thresholds.get("threshold_green", 90) else \
             "ORANGE" if drivability_score >= thresholds.get("threshold_orange", 75) else "RED"
    warnings = "None" if status == "GREEN" else "Check parameters"
    from logic.db import save_project_rating
    save_project_rating(project_id, drivability_score, status, warnings)
    return {
        "drivability_score": drivability_score,
        "status": status,
        "warnings": warnings
    }

def calculate_all_ratings(project_id):
    return calculate_project_rating(project_id)