ODRIV Dashboard – Python Version

1. Copy the ODRIV_Dashboard folder (all files & subfolders) to:
   C:\Program Files\AVL\AVL-DRIVE 5 V5.9.1\PLUGINS\Dashboards\ODRIV_Dashboard\

2. In the ODRIV_Dashboard/data folder, run:
   python init_db.py
   This will create the odriv.db SQLite database.

3. Make sure ODRIV_dashboard.json is in the Dashboards folder.

4. Start AVL-DRIVE and select ODRIV Dashboard from the dashboard selector.

5. For troubleshooting, look for print statements in your log or run app.py manually.