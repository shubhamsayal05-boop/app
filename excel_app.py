"""
Excel-like Spreadsheet Application
Phase 1: Basic spreadsheet with cell editing, values, and simple formulas
"""

import dash
from dash import Dash, html, dcc, dash_table, Input, Output, State, ALL, ctx
import dash_bootstrap_components as dbc
import json
import re
from typing import Dict, Any, List, Tuple

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Constants
NUM_ROWS = 100
NUM_COLS = 26  # A-Z
COLUMN_LETTERS = [chr(65 + i) for i in range(NUM_COLS)]


class FormulaEvaluator:
    """Evaluates simple Excel-like formulas"""
    
    @staticmethod
    def evaluate(formula: str, cell_data: Dict[str, Any]) -> Any:
        """
        Evaluate a formula string
        Supported: =SUM(A1:A5), =AVERAGE(B1:B10), =A1+B1, =A1*2, etc.
        """
        if not formula or not formula.startswith('='):
            return formula
        
        formula = formula[1:]  # Remove '=' prefix
        
        try:
            # Handle SUM function
            sum_pattern = r'SUM\(([A-Z]+\d+):([A-Z]+\d+)\)'
            sum_match = re.search(sum_pattern, formula, re.IGNORECASE)
            if sum_match:
                start_cell = sum_match.group(1).upper()
                end_cell = sum_match.group(2).upper()
                values = FormulaEvaluator._get_range_values(start_cell, end_cell, cell_data)
                return sum(values)
            
            # Handle AVERAGE function
            avg_pattern = r'AVERAGE\(([A-Z]+\d+):([A-Z]+\d+)\)'
            avg_match = re.search(avg_pattern, formula, re.IGNORECASE)
            if avg_match:
                start_cell = avg_match.group(1).upper()
                end_cell = avg_match.group(2).upper()
                values = FormulaEvaluator._get_range_values(start_cell, end_cell, cell_data)
                return sum(values) / len(values) if values else 0
            
            # Handle cell references in arithmetic expressions
            cell_pattern = r'([A-Z]+\d+)'
            cells_in_formula = re.findall(cell_pattern, formula)
            
            for cell_ref in cells_in_formula:
                cell_value = cell_data.get(cell_ref, {}).get('value', 0)
                # If the cell contains a formula, evaluate it first
                if isinstance(cell_value, str) and cell_value.startswith('='):
                    cell_value = FormulaEvaluator.evaluate(cell_value, cell_data)
                # Convert to number if possible
                try:
                    cell_value = float(cell_value) if cell_value else 0
                except (ValueError, TypeError):
                    cell_value = 0
                formula = formula.replace(cell_ref, str(cell_value))
            
            # Evaluate the arithmetic expression
            result = eval(formula)
            return round(result, 2) if isinstance(result, float) else result
            
        except Exception as e:
            return f"#ERROR: {str(e)}"
    
    @staticmethod
    def _get_range_values(start_cell: str, end_cell: str, cell_data: Dict[str, Any]) -> List[float]:
        """Get numeric values from a cell range"""
        start_col = ''.join(filter(str.isalpha, start_cell))
        start_row = int(''.join(filter(str.isdigit, start_cell)))
        end_col = ''.join(filter(str.isalpha, end_cell))
        end_row = int(''.join(filter(str.isdigit, end_cell)))
        
        start_col_idx = ord(start_col) - ord('A')
        end_col_idx = ord(end_col) - ord('A')
        
        values = []
        for row in range(start_row, end_row + 1):
            for col_idx in range(start_col_idx, end_col_idx + 1):
                col = chr(ord('A') + col_idx)
                cell_ref = f"{col}{row}"
                cell_value = cell_data.get(cell_ref, {}).get('value', '')
                
                # If it's a formula, evaluate it
                if isinstance(cell_value, str) and cell_value.startswith('='):
                    cell_value = FormulaEvaluator.evaluate(cell_value, cell_data)
                
                # Convert to number
                try:
                    if cell_value:
                        values.append(float(cell_value))
                except (ValueError, TypeError):
                    pass
        
        return values


def create_empty_spreadsheet():
    """Create empty spreadsheet data structure"""
    data = []
    for row in range(1, NUM_ROWS + 1):
        row_data = {'row': row}
        for col in COLUMN_LETTERS:
            row_data[col] = ''
        data.append(row_data)
    return data


def create_spreadsheet_table(data, cell_data):
    """Create the spreadsheet table component"""
    columns = [{'name': 'Row', 'id': 'row', 'editable': False, 'type': 'text'}]
    columns.extend([
        {'name': col, 'id': col, 'editable': True, 'type': 'text'}
        for col in COLUMN_LETTERS
    ])
    
    # Calculate display values (formulas show results)
    display_data = []
    for row_dict in data:
        display_row = {'row': row_dict['row']}
        for col in COLUMN_LETTERS:
            cell_ref = f"{col}{row_dict['row']}"
            cell_value = cell_data.get(cell_ref, {}).get('value', '')
            
            # If it's a formula, show the calculated result
            if isinstance(cell_value, str) and cell_value.startswith('='):
                calculated = FormulaEvaluator.evaluate(cell_value, cell_data)
                display_row[col] = calculated
            else:
                display_row[col] = cell_value
        display_data.append(display_row)
    
    return dash_table.DataTable(
        id='spreadsheet-table',
        columns=columns,
        data=display_data,
        editable=True,
        row_selectable='multi',
        cell_selectable=True,
        style_table={
            'overflowX': 'auto',
            'overflowY': 'auto',
            'height': '600px'
        },
        style_cell={
            'textAlign': 'left',
            'minWidth': '80px',
            'maxWidth': '180px',
            'whiteSpace': 'normal',
            'fontSize': '14px',
            'fontFamily': 'Arial, sans-serif',
            'border': '1px solid #ddd'
        },
        style_header={
            'backgroundColor': '#f0f0f0',
            'fontWeight': 'bold',
            'border': '1px solid #999',
            'fontSize': '14px'
        },
        style_data_conditional=[
            {
                'if': {'column_id': 'row'},
                'backgroundColor': '#f0f0f0',
                'fontWeight': 'bold'
            }
        ],
        page_action='none',
        fixed_rows={'headers': True},
    )


# App layout
app.layout = dbc.Container([
    html.H1("Excel-like Spreadsheet Application", className="mt-3 mb-3"),
    
    dbc.Card([
        dbc.CardHeader([
            html.H5("Spreadsheet - Sheet1", className="mb-0")
        ]),
        dbc.CardBody([
            # Toolbar
            dbc.Row([
                dbc.Col([
                    dbc.ButtonGroup([
                        dbc.Button("Clear Sheet", id="btn-clear", color="danger", size="sm"),
                        dbc.Button("Export JSON", id="btn-export", color="primary", size="sm"),
                        dbc.Button("Sample Data", id="btn-sample", color="info", size="sm"),
                    ])
                ], width=6),
                dbc.Col([
                    html.Div(id="formula-bar", children=[
                        dbc.Label("Formula Bar:", className="me-2"),
                        dbc.Input(
                            id="formula-input",
                            type="text",
                            placeholder="Select a cell to edit...",
                            size="sm",
                            style={'width': '300px', 'display': 'inline-block'}
                        )
                    ])
                ], width=6, className="text-end")
            ], className="mb-3"),
            
            # Store for cell data
            dcc.Store(id='cell-data-store', data={}),
            dcc.Store(id='selected-cell-store', data=None),
            
            # Spreadsheet table
            html.Div(id='spreadsheet-container', children=[
                create_spreadsheet_table(create_empty_spreadsheet(), {})
            ]),
            
            # Status bar
            html.Div(id="status-bar", className="mt-2", children=[
                dbc.Alert("Ready. Enter values or formulas (start with =)", color="info", className="mb-0")
            ])
        ])
    ]),
    
    # Feature documentation
    dbc.Card([
        dbc.CardHeader("Supported Features"),
        dbc.CardBody([
            html.H6("Cell Editing:"),
            html.Ul([
                html.Li("Click any cell to edit its value"),
                html.Li("Values are stored in real-time"),
            ]),
            html.H6("Formulas:"),
            html.Ul([
                html.Li("Start with = (e.g., =A1+B1)"),
                html.Li("Arithmetic: +, -, *, / (e.g., =A1*2)"),
                html.Li("SUM function: =SUM(A1:A10)"),
                html.Li("AVERAGE function: =AVERAGE(B1:B5)"),
                html.Li("Cell references: =A1+B2*C3"),
            ]),
            html.H6("Examples:"),
            html.Ul([
                html.Li("=10+20 → 30"),
                html.Li("=A1+B1 → Sum of cells A1 and B1"),
                html.Li("=SUM(A1:A5) → Sum of range A1 to A5"),
                html.Li("=AVERAGE(C1:C10) → Average of range"),
            ])
        ])
    ], className="mt-3")
    
], fluid=True)


# Callback to update cell data when table is edited
@app.callback(
    Output('cell-data-store', 'data'),
    Output('spreadsheet-container', 'children'),
    Output('status-bar', 'children'),
    Input('spreadsheet-table', 'data'),
    Input('spreadsheet-table', 'active_cell'),
    Input('btn-clear', 'n_clicks'),
    Input('btn-sample', 'n_clicks'),
    State('cell-data-store', 'data'),
    prevent_initial_call=True
)
def update_spreadsheet(table_data, active_cell, clear_clicks, sample_clicks, cell_data):
    """Update spreadsheet when cells are edited or buttons clicked"""
    trigger = ctx.triggered_id
    
    # Clear sheet
    if trigger == 'btn-clear':
        empty_data = create_empty_spreadsheet()
        return {}, [create_spreadsheet_table(empty_data, {})], \
               dbc.Alert("Sheet cleared!", color="success", className="mb-0")
    
    # Load sample data
    if trigger == 'btn-sample':
        sample_cell_data = {
            'A1': {'value': '10'},
            'A2': {'value': '20'},
            'A3': {'value': '30'},
            'A4': {'value': '40'},
            'A5': {'value': '50'},
            'B1': {'value': '=A1*2'},
            'B2': {'value': '=A2*2'},
            'B3': {'value': '=A3*2'},
            'B4': {'value': '=A4*2'},
            'B5': {'value': '=A5*2'},
            'C1': {'value': '=A1+B1'},
            'C5': {'value': '=SUM(A1:A5)'},
            'C6': {'value': '=AVERAGE(A1:A5)'},
        }
        empty_data = create_empty_spreadsheet()
        return sample_cell_data, [create_spreadsheet_table(empty_data, sample_cell_data)], \
               dbc.Alert("Sample data loaded! See columns A, B, C", color="success", className="mb-0")
    
    # Update cell data from table edits
    if trigger == 'spreadsheet-table' and table_data:
        # Extract changes
        for row_dict in table_data:
            row_num = row_dict.get('row')
            for col in COLUMN_LETTERS:
                cell_ref = f"{col}{row_num}"
                cell_value = row_dict.get(col, '')
                
                if cell_value:
                    cell_data[cell_ref] = {'value': cell_value}
                elif cell_ref in cell_data:
                    del cell_data[cell_ref]
        
        # Recreate table with updated data
        empty_data = create_empty_spreadsheet()
        return cell_data, [create_spreadsheet_table(empty_data, cell_data)], \
               dbc.Alert("Spreadsheet updated!", color="success", className="mb-0")
    
    return cell_data, dash.no_update, dash.no_update


# Callback to export data
@app.callback(
    Output('status-bar', 'children', allow_duplicate=True),
    Input('btn-export', 'n_clicks'),
    State('cell-data-store', 'data'),
    prevent_initial_call=True
)
def export_data(n_clicks, cell_data):
    """Export cell data to JSON"""
    if n_clicks:
        export_json = json.dumps(cell_data, indent=2)
        print("\n=== EXPORTED DATA ===")
        print(export_json)
        print("===================\n")
        return dbc.Alert(
            f"Data exported to console! {len(cell_data)} cells with data.",
            color="success",
            className="mb-0"
        )
    return dash.no_update


if __name__ == '__main__':
    print("Starting Excel-like Spreadsheet Application...")
    print("Open your browser to: http://127.0.0.1:8050")
    print("\nFeatures:")
    print("- Edit cells by clicking on them")
    print("- Enter formulas starting with = (e.g., =A1+B1)")
    print("- Supported functions: SUM, AVERAGE")
    print("- Try the 'Sample Data' button for examples")
    app.run(debug=True, port=8050)
