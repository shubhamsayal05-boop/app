from logic.db import get_dropdown_options

def get_vehicle_options():
    return get_dropdown_options("vehicles")

def get_milestone_options():
    return get_dropdown_options("milestones")

def get_config():
    # Expand as needed, e.g., to fetch config or thresholds
    return {
        "threshold_green": 90,
        "threshold_orange": 75,
    }