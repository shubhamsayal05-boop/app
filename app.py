import os
import json
from dash import Dash, dcc, html, dash_table, Input, Output, State, ctx, no_update
import dash_bootstrap_components as dbc

MAX_ROWS = 30
MAX_COLS = 10

def load_json_sheets(json_dir):
    tabs = []
    files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
    for fname in sorted(files):
        fpath = os.path.join(json_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        cells = data.get("cells", {})
        rows = []
        cell_map = {}
        for cell, cell_data in cells.items():
            col, row = None, None
            for i, c in enumerate(cell):
                if c.isdigit():
                    col = cell[:i]
                    row = cell[i:]
                    break
            if col and row:
                if row not in cell_map:
                    cell_map[row] = {}
                cell_map[row][col] = cell_data.get("value")
        all_cols = sorted(list(set(col for row in cell_map.values() for col in row.keys())))
        if len(all_cols) > MAX_COLS:
            all_cols = all_cols[:MAX_COLS]
        row_keys = sorted(cell_map.keys(), key=lambda x: int(x))
        if len(row_keys) > MAX_ROWS:
            row_keys = row_keys[:MAX_ROWS]
        for row_num in row_keys:
            row_data = {"Row": row_num}
            for col in all_cols:
                row_data[col] = cell_map[row_num].get(col)
            rows.append(row_data)
        columns = [{"name": "Row", "id": "Row"}] + [{"name": col, "id": col} for col in all_cols]
        table = dash_table.DataTable(
            data=rows,
            columns=columns,
            page_size=10,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "maxWidth": "350px"},
            style_header={"fontWeight": "bold", "backgroundColor": "#e9ecef"},
        )
        tab_label = fname.replace(".json", "")
        tabs.append((tab_label, table))
    return tabs

def get_json_sheet_names(json_dir="data/json_sheets"):
    files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
    sheet_names = [f.replace(".json", "") for f in files]
    return sheet_names

ALWAYS_VISIBLE = ["RATING", "VERSIONS"]

PROJECT_FIELDS = [
    ("ID", "proj-id"), ("NAME / CODE", "proj-name"),
    ("MODE", "proj-mode"), ("FUEL", "proj-fuel"),
    ("GEARS", "proj-gears"), ("SOFTWARE MILESTONE", "proj-sw"),
    ("PRIORITY", "proj-priority"), ("VERSION", "proj-version"),
    ("ODRIV MILESTONE", "proj-odriv-milestone"), ("AREA", "proj-area"),
    ("TARGET VEHICLE", "proj-target"), ("NUMBER OF GEARS", "proj-num-gears"),
]

GRID_BUTTONS = [
    {"label": "NEW PROJECT", "color": "success", "id": "new-project-btn"},
    {"label": "ADD FILE TO DATABASE", "color": "warning", "id": "add-file-btn"},
    {"label": "CALCULATE RATING", "color": "primary", "id": "calc-rating-btn"},
    {"label": "OPEN DATABASE", "color": "info", "id": "open-db-btn"},
    {"label": "CREATE REPORT", "color": "secondary", "id": "create-report-btn"},
    {"label": "SETTINGS", "color": "secondary", "id": "settings-btn"},
    {"label": "VERSIONS", "color": "dark", "id": "versions-btn"},
    {"label": "ADD FILE (SUBJECTIVE)", "color": "warning", "id": "add-file-subj-btn"},
    {"label": "HELP", "color": "info", "id": "help-btn"},
    {"label": "ERASE ALL DATA", "color": "danger", "id": "erase-data-btn"},
]

def make_project_settings_panel():
    return dbc.Card(
        [
            dbc.CardHeader("PROJECT SETTINGS"),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label(label),
                        dbc.Input(type="text", id=input_id)
                    ], md=6) for label, input_id in PROJECT_FIELDS
                ])
            ])
        ], style={"marginBottom": "20px"}
    )

def make_action_grid():
    rows = []
    for i in range(0, len(GRID_BUTTONS), 4):
        row = dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        GRID_BUTTONS[j]["label"],
                        color=GRID_BUTTONS[j]["color"],
                        id=GRID_BUTTONS[j]["id"],
                        style={"width": "100%", "height": "75px", "fontWeight": "bold"}
                    )
                )
                for j in range(i, min(i+4, len(GRID_BUTTONS)))
            ],
            style={"marginBottom": "10px"}
        )
        rows.append(row)
    return html.Div(rows)

def get_tabs(visible_sheets, json_dir="data/json_sheets"):
    json_tabs = load_json_sheets(json_dir)
    tabs = []
    for sheet, table in json_tabs:
        if sheet in visible_sheets:
            tabs.append(dcc.Tab(label=sheet, value=sheet, children=[html.Div(table)]))
    return tabs

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def get_unlock_options():
    sheets = get_json_sheet_names()
    return [
        {"label": sheet, "value": sheet}
        for sheet in sheets if sheet not in ALWAYS_VISIBLE
    ]

new_proj_modal = dbc.Modal(
    [
        dbc.ModalHeader("New Project"),
        dbc.ModalBody([
            dbc.Label("Enter new project info..."),
            dbc.Input(type="text", placeholder="Project Name", id="new-project-name"),
            dbc.Button("Save", id="save-project-btn", color="success"),
        ]),
        dbc.ModalFooter([
            dbc.Button("Close", id="close-new-proj-btn", color="secondary"),
        ])
    ],
    id="new-proj-modal",
    is_open=False,
)

app.layout = dbc.Container([
    html.H2("ODRIV Dashboard"),
    dcc.Store(id="unlocked-sheets-store", data=[]),
    dbc.Row([
        dbc.Col(make_project_settings_panel(), width=4),
        dbc.Col(make_action_grid(), width=8),
    ], style={"marginBottom": "25px"}),
    html.Div(id="tabs-container"),
    dbc.Button("Configuration Sheet", id="cfg-sheet-btn", color="primary", style={"marginTop": "30px"}),
    dbc.Modal(
        [
            dbc.ModalHeader("Unlock Sheets"),
            dbc.ModalBody([
                dbc.Label("Select Sheets to Unlock:"),
                dcc.Dropdown(
                    id="sheet-select",
                    options=get_unlock_options(),
                    multi=True
                ),
                dbc.Label("Enter password:"),
                dbc.Input(type="password", id="unlock-pwd"),
                html.Div(id="unlock-msg", style={"color": "red", "marginTop": "10px"})
            ]),
            dbc.ModalFooter([
                dbc.Button("Unlock", id="unlock-btn", color="success"),
                dbc.Button("Close", id="close-btn", color="secondary"),
            ])
        ],
        id="cfg-modal",
        is_open=False,
    ),
    new_proj_modal,
], fluid=True)

@app.callback(
    Output("cfg-modal", "is_open"),
    Output("new-proj-modal", "is_open"),
    [Input("cfg-sheet-btn", "n_clicks"),
     Input("close-btn", "n_clicks"),
     Input("new-project-btn", "n_clicks"),
     Input("close-new-proj-btn", "n_clicks")],
    [State("cfg-modal", "is_open"), State("new-proj-modal", "is_open")]
)
def toggle_modals(cfg_open, cfg_close, new_proj_open, new_proj_close, cfg_is_open, new_proj_is_open):
    triggered = ctx.triggered_id
    if triggered == "cfg-sheet-btn":
        return True, new_proj_is_open
    if triggered == "close-btn":
        return False, new_proj_is_open
    if triggered == "new-project-btn":
        return cfg_is_open, True
    if triggered == "close-new-proj-btn":
        return cfg_is_open, False
    return cfg_is_open, new_proj_is_open

@app.callback(
    Output("unlocked-sheets-store", "data"),
    Output("unlock-msg", "children"),
    Input("unlock-btn", "n_clicks"),
    State("sheet-select", "value"),
    State("unlock-pwd", "value"),
)
def save_unlocked_sheets(unlock_click, selected_sheets, pwd):
    msg = ""
    sheets = []
    if unlock_click and selected_sheets and pwd is not None:
        if pwd == "unlock":
            sheets = selected_sheets
        else:
            msg = "Incorrect password!"
    return sheets, msg

@app.callback(
    Output("tabs-container", "children"),
    Input("unlocked-sheets-store", "data"),
)
def show_tabs(unlocked_sheets):
    visible_sheets = ALWAYS_VISIBLE.copy()
    if unlocked_sheets:
        visible_sheets += unlocked_sheets
    tabs = get_tabs(visible_sheets)
    return dcc.Tabs(
        id="sheet-tabs",
        value=visible_sheets[0] if visible_sheets else None,
        children=tabs,
        parent_style={"marginTop": "40px"},
    )

# Added: Clear project fields when NEW PROJECT is clicked
@app.callback(
    [Output("proj-id", "value"),
     Output("proj-name", "value"),
     Output("proj-mode", "value"),
     Output("proj-fuel", "value"),
     Output("proj-gears", "value"),
     Output("proj-sw", "value"),
     Output("proj-priority", "value"),
     Output("proj-version", "value"),
     Output("proj-odriv-milestone", "value"),
     Output("proj-area", "value"),
     Output("proj-target", "value"),
     Output("proj-num-gears", "value")],
    [Input("new-project-btn", "n_clicks")]
)
def clear_project_fields(n_clicks):
    if n_clicks:
        return [""] * len(PROJECT_FIELDS)
    return [no_update] * len(PROJECT_FIELDS)

if __name__ == "__main__":
    app.run(debug=True)