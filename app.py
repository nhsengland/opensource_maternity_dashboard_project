from dash import Dash, dcc, html, Input, Output, callback, ctx
import draw_graphs
import sys
import dash_bootstrap_components as dbc
import json

sys.path.append("./")
import config
import textwrap
from layout import sidebar, content
import style
import map_utils


# if debug is true display all the debug info


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Set defaults
org_level = "NHS England (Region)"
dimension = "AgeAtBookingMotherGroup"
year = "2022-23"
chart_type = "Bar Chart"




app.layout = html.Div(
    [
        dcc.Location(id="url"),
        dbc.Row(
            [
                dbc.Col(sidebar, width=1),
                dbc.Col(content, width=11, style={"padding": "0"}),
            ]
        ),
    ]
)

@callback(
    Output("bar-chart", "figure"),
    Output("chart_title", "children"),
    Output("chart_description", "children"),
    Input("dimension-dropdown", "value"),
    Input("map", "selectedData"),
    Input("org_level_button", "value"),
    Input("year_button", "value"),
    Input("chart_button", "value"),
)
def display_chart(dimension, selectedData, org_level, year, chart_type):
    location = "All Submitters"
    if selectedData is None and not (
        org_level == "Provider"
        and dimension in config.special_dimensions
        and chart_type == "Time Series"
    ):
        org_level = "National"
    else:
        if org_level == "NHS England (Region)":
            if "location" in selectedData["points"][0]:
                location = selectedData["points"][0]["location"]
            else:
                org_level = "National"

        elif org_level == "Provider" and not (selectedData == None):
            if "customdata" in selectedData["points"][0]:
                location = selectedData["points"][0]["customdata"][0]
            else:
                org_level = "National"
    if (
        selectedData is None
        and org_level == "Provider"
        and dimension in config.special_dimensions
        and chart_type == "Time Series"
    ):
        org_level = "Provider"
    elif (
        selectedData is not None
        and org_level == "Provider"
        and dimension in config.special_dimensions
        and chart_type == "Time Series"
    ):
        org_level = "Provider"
        location = selectedData["points"][0]["customdata"][0]

    if ctx.triggered_id == "org_level_button":
        location = "All Submitters"
        org_level = "National"

    fig = map_utils.get_chart(org_level, dimension, year, chart_type, location)
    title, description = map_utils.get_chart_title(dimension, year, location, chart_type)
    return fig, title, description


@callback(
    Output("map", "figure"),
    Output("map_title", "children"),
    Output("map_description", "children"),
    Output('selectedDataDisplay', 'children'),
    Output('selectedpointsdisplay', 'children'),
    Input("dimension-dropdown", "value"),
    Input("map", "selectedData"),
    Input("org_level_button", "value"),
    Input("year_button", "value"),
)
def display_map(dimension, selectedData, org_level, year):

    if selectedData is None or ctx.triggered_id == "org_level_button":
        selectedpoints = None
    else:
        selectedpoints = [point["pointIndex"] for point in selectedData["points"]]

    fig = map_utils.get_map(org_level, dimension, year, selectedpoints=selectedpoints)
    map_title, map_description = map_utils.get_map_title(dimension, year, org_level)

    return (
        fig,
        map_title,
        map_description,
        json.dumps(selectedData), json.dumps(selectedpoints))



if __name__ == "__main__":
    app.run(debug=True)
