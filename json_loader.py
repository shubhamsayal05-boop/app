import os
import json
from dash import dcc, html, dash_table

def load_json_sheets(json_dir):
    tabs = []
    files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
    for fname in sorted(files):
        fpath = os.path.join(json_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        cells = data.get("cells", {})
        # Parse cells into rows/columns for DataTable
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
        all_cols = set()
        for row in cell_map.values():
            all_cols.update(row.keys())
        all_cols = sorted(all_cols)
        for row_num in sorted(cell_map.keys(), key=lambda x: int(x)):
            row_data = {"Row": row_num}
            for col in all_cols:
                row_data[col] = cell_map[row_num].get(col)
            rows.append(row_data)
        columns = [{"name": "Row", "id": "Row"}] + [{"name": col, "id": col} for col in all_cols]
        table = dash_table.DataTable(
            data=rows,
            columns=columns,
            page_size=20,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "maxWidth": "350px"},
            style_header={"fontWeight": "bold", "backgroundColor": "#e9ecef"},
        )
        tab_label = fname.replace(".json", "")
        tabs.append(
            dcc.Tab(
                label=tab_label,
                value=tab_label,
                children=[
                    html.H5(f"JSON Sheet: {tab_label}"),
                    table
                ]
            )
        )
    if tabs:
        return dcc.Tabs(
            id="json-sheet-tabs",
            value=tabs[0].value,
            children=tabs,
        )
    else:
        return html.Div("No JSON sheets found.")