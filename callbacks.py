from dash import Input, Output, State, ctx
import dash
from logic.db import add_project, get_project_details
from logic.calculations import calculate_all_ratings

def register_callbacks(app):
    @app.callback(
        Output("modal-new-project", "is_open"),
        [Input("open-project-modal", "n_clicks")],
        [State("modal-new-project", "is_open")],
    )
    def toggle_new_project_modal(open_clicks, is_open):
        if open_clicks:
            return not is_open
        return is_open

    @app.callback(
        Output("current-project-id", "data"),
        Output("modal-new-project", "is_open"),
        Input("modal-apply-btn", "n_clicks"),
        State("modal-proj-name", "value"),
        State("modal-vehicle-select", "value"),
        State("modal-milestone-select", "value"),
        State("modal-user", "value"),
    )
    def handle_new_project(apply_click, name, vehicle, milestone, user):
        if apply_click:
            proj_id = add_project(name, vehicle, milestone, user)
            return proj_id, False
        return dash.no_update, dash.no_update

    @app.callback(
        Output("project-info", "children"),
        Input("current-project-id", "data")
    )
    def update_project_info(project_id):
        if not project_id:
            return "No project selected."
        project = get_project_details(project_id)
        return f"Project: {project['name']} | Vehicle: {project['vehicle']} | Milestone: {project['milestone']} | User: {project['user']}"

    @app.callback(
        Output("dashboard-tiles", "children"),
        Input("current-project-id", "data")
    )
    def update_dashboard_tiles(project_id):
        if not project_id:
            return ""
        ratings = calculate_all_ratings(project_id)
        from dash import html
        color = "green" if ratings['status'] == "GREEN" else "orange" if ratings['status'] == "ORANGE" else "red"
        return [
            html.Div(f"Drivability: {ratings['drivability_score']}", className="tile-score"),
            html.Div(f"Status: {ratings['status']}", className=f"tile-status {color}"),
            html.Div(f"Warnings: {ratings['warnings']}", className="tile-warning")
        ]

    @app.callback(
        Output("main-graph", "figure"),
        Input("current-project-id", "data")
    )
    def update_main_graph(project_id):
        if not project_id:
            from plotly.graph_objs import Figure
            return Figure()
        import plotly.graph_objs as go
        ratings = calculate_all_ratings(project_id)
        fig = go.Figure(data=[go.Bar(x=["Drivability"], y=[ratings["drivability_score"]])])
        fig.update_layout(title="Drivability Score")
        return fig