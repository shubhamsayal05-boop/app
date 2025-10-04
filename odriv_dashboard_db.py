import pandas as pd
import sqlite3
from pathlib import Path
from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc

EXCEL_PATH = "ODRIV_v28_0_6.xlsm"
DB_PATH = "odriv.db"

def bootstrap_db_from_excel(excel_path, db_path):
    """
    Loads all sheets from Excel file and saves each sheet as a table in SQLite DB.
    SKIPS sheets that are empty or have no column headers (to avoid SQL syntax errors).
    """
    xls = pd.ExcelFile(excel_path, engine="openpyxl")
    conn = sqlite3.connect(db_path)
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        # Skip empty sheets or sheets with no columns
        if df.empty or df.shape[1] == 0:
            print(f"Skipping empty or invalid sheet: {sheet_name}")
            continue
        # Replace table if already exists
        df.to_sql(sheet_name, conn, if_exists="replace", index=False)
    conn.close()
    print(f"Bootstrapped database from {excel_path}")

def load_sheets_from_db(db_path):
    """
    Loads all tables from SQLite DB as {sheet_name: dataframe}
    """
    conn = sqlite3.connect(db_path)
    # Get all table names
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
    sheets = {}
    for sheet_name in tables["name"]:
        df = pd.read_sql(f"SELECT * FROM '{sheet_name}'", conn)
        sheets[sheet_name] = df
    conn.close()
    return sheets

def make_project_settings():
    return dbc.Card(
        [
            dbc.CardHeader("PROJECT SETTINGS", className="settings-header"),
            dbc.CardBody(
                dbc.Form([
                    dbc.Row([
                        dbc.Col([dbc.Label("ID"), dbc.Input(type="text", id="proj-id")], md=6),
                        dbc.Col([dbc.Label("NAME / CODE"), dbc.Input(type="text", id="proj-name")], md=6),
                    ]),
                    dbc.Row([
                        dbc.Col([dbc.Label("MODE"), dbc.Input(type="text", id="proj-mode")], md=6),
                        dbc.Col([dbc.Label("FUEL"), dbc.Input(type="text", id="proj-fuel")], md=6),
                    ]),
                    dbc.Row([
                        dbc.Col([dbc.Label("GEARS"), dbc.Input(type="number", id="proj-gears")], md=6),
                        dbc.Col([dbc.Label("SOFTWARE MILESTONE"), dbc.Input(type="text", id="proj-sw")], md=6),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("PRIORITY"),
                            dbc.Select(
                                id="proj-priority",
                                options=[
                                    {"label": "Low", "value": "Low"},
                                    {"label": "Medium", "value": "Medium"},
                                    {"label": "High", "value": "High"},
                                ],
                                placeholder="Select priority",
                            ),
                        ], md=6),
                        dbc.Col([dbc.Label("VERSION"), dbc.Input(type="text", id="proj-version")], md=6),
                    ]),
                    dbc.Row([
                        dbc.Col([dbc.Label("ODRIV MILESTONE"), dbc.Input(type="text", id="proj-odriv-milestone")], md=6),
                        dbc.Col([dbc.Label("AREA"), dbc.Input(type="text", id="proj-area")], md=6),
                    ]),
                    dbc.Row([
                        dbc.Col([dbc.Label("TARGET VEHICLE"), dbc.Input(type="text", id="proj-target")], md=6),
                        dbc.Col([dbc.Label("NUMBER OF GEARS"), dbc.Input(type="number", id="proj-num-gears")], md=6),
                    ]),
                    dbc.Button("APPLY", id="apply-project", color="primary", className="mt-2"),
                ])
            ),
        ],
        className="settings-panel",
        id="project-settings-card",
        style={"display": "block"},
    )

def make_sheet_tabs(sheets):
    tabs = []
    for sheet, df in sheets.items():
        if df.empty:
            table = html.Div("No data in this sheet.")
        else:
            table = dash_table.DataTable(
                data=df.to_dict("records"),
                columns=[{"name": col, "id": col} for col in df.columns],
                page_size=20,
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "left", "maxWidth": "350px"},
                style_header={"fontWeight": "bold", "backgroundColor": "#e9ecef"},
            )
        tabs.append(
            dcc.Tab(
                label=sheet,
                value=sheet,
                children=[
                    html.H5(f"Sheet: {sheet}"),
                    table
                ]
            )
        )
    return dcc.Tabs(
        id="odriv-sheet-tabs",
        value=list(sheets.keys())[0] if sheets else None,
        children=tabs,
    )

def serve_layout():
    sheets = load_sheets_from_db(DB_PATH)
    return dbc.Container(
        [
            html.H2("ODRIV Dashboard"),
            dbc.Row([
                dbc.Col(make_project_settings(), width=3),
                dbc.Col(make_sheet_tabs(sheets), width=9),
            ], align="start"),
        ],
        fluid=True,
        className="main-dashboard"
    )

# --- Bootstrap: Load Excel data to DB only if Excel exists ---
if Path(EXCEL_PATH).exists():
    bootstrap_db_from_excel(EXCEL_PATH, DB_PATH)
    print(f"You can now delete {EXCEL_PATH}: All data is stored in {DB_PATH}.")

# --- Create Dash app ---
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"],
)

app.layout = serve_layout

if __name__ == "__main__":
    app.run_server(debug=True)