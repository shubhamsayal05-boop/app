CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    vehicle TEXT,
    milestone TEXT,
    user TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS project_ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    drivability_score REAL,
    status TEXT,
    warnings TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value TEXT
);
CREATE TABLE IF NOT EXISTS milestones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value TEXT
);
CREATE TABLE IF NOT EXISTS config (
    key TEXT PRIMARY KEY,
    value TEXT
);

-- Initial values for config
INSERT OR IGNORE INTO config (key, value) VALUES
  ('threshold_green', '90'),
  ('threshold_orange', '75');

-- Initial vehicles
INSERT OR IGNORE INTO vehicles (value) VALUES ('VehicleA'), ('VehicleB');
-- Initial milestones
INSERT OR IGNORE INTO milestones (value) VALUES ('Milestone1'), ('Milestone2');