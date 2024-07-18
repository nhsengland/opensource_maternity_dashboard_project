from dash import Dash, dcc, html, Input, Output, callback, ctx
from create_maps import draw_graphs
import sys
import dash_bootstrap_components as dbc
import json
sys.path.append('./')
import config
import textwrap


#if debug is true display all the debug info


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Set defaults
org_level =  "NHS England (Region)"
dimension = "AgeAtBookingMotherGroup"
year = "2022-23"
chart_type = "Bar Chart"

def get_map(org_level, dimension, year, selectedpoints=None):
    fig = draw_graphs.draw_map(org_level, dimension, year, selectedpoints)
    return fig

def get_chart(org_level, dimension, year, chart_type, location):
    if chart_type == "Bar Chart":
        if dimension in config.special_dimensions:
            fig = draw_graphs.draw_special_bar_chart(dimension, year)
        else:
            fig = draw_graphs.draw_bar_chart(org_level, dimension, year, location)
    else:
        fig = draw_graphs.draw_time_series(org_level, dimension, location) 
    
    return fig

def get_chart_title(dimension, year, location, chart_type):
    description = None
    if chart_type == "Bar Chart":
        if dimension in config.special_dimensions:
            title=f"{dimension}. Bar chart showing the rate of {dimension} per 1000 people for {year}"
        else:
            title=textwrap.fill(f"{location}: {dimension} {year}", width=50)
            description = "Bar chart of broken down data, with markers comparing to All Submitters"
    else:
        title=textwrap.fill(f"{location}: {dimension}", width=50)
        description = "Time series of broken down data"

    return title, description

def get_map_title(dimension, year, org_level):
    title = textwrap.fill(f'{config.measure_dict[org_level][dimension]["map_title"]} for {year}',width=50)
    if org_level == "NHS England (Region)" or org_level == "National":
        description = "Chloropleth map of England, broken in seven regions"
    elif org_level == "Provider":
        description = "Scatter plot map of England, with each point representing a maternity care provider"

    return title, description


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",  # Adjusted the width to reduce the gap
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "2rem", 
    "margin-right": "2rem",
    "padding": "2rem 10rem",
}

sidebar = html.Div(
    [
        html.H4("Visualising: NHS England Maternity Dataset ", className="display-6"),
        html.Hr(),
        html.P(
            "Choose a level", className="lead"
        ),
        dcc.RadioItems(
        options=['NHS England (Region)', 'Provider'],
        value='NHS England (Region)',
        id = "org_level_button"
        ),
        html.P(""),
        html.Hr(),
        html.P("Pick a year to see the data", className="lead"),
        dcc.RadioItems(
        options=['2022-23', '2021-22', '2020-21'],
        value='2022-23',
        id = "year_button"
        ),
        html.P(""),
        html.Hr(),
        html.P("View the breakdown using a bar chart or time series", className="lead"),
        dcc.RadioItems(
        options=['Bar Chart', 'Time Series'],
        value='Bar Chart',
        id = "chart_button"
        ),
        html.P(""),
        html.Hr(),
        html.P("Pick a measure to view", className="lead"),
        dcc.Dropdown(list(config.measure_dict["NHS England (Region)"].keys()), dimension, id='dimension-dropdown'),
        html.Hr(),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(
    [dbc.Row(
        [
            dbc.Col(
                [html.H2("Percentage of Mothers OVER the age of 35 for 2022-23", id='map_title'),
                html.H4("Chloropleth map of England, broken in seven regions", id='map_description'), # move these to have different rowsand cols
                dcc.Graph(
                    id='map',
                    figure=get_map(org_level, dimension, year),
                    style={"height": "800px"}
                )], width=6
            ),
            dbc.Col(
                [html.H2("All Submitters: AgeAtBookingMotherGroup 2022-23", id='chart_title'),
                html.H4("Bar chart of broken down data, with markers comparing to All Submitters", id='chart_description'),
                dcc.Graph(
                    id='bar-chart',
                    figure=get_chart(org_level, dimension, year, chart_type, location="All Submitters"),
                    style={"height": "800px"}
                )], width=6
            )
        ]
    ),
    #         html.Div([
    #         html.Pre(id='selectedDataDisplay')
    #     ]),   

    # html.Div([
    #         html.Pre(id='selectedpointsdisplay')
    #     ]),   
    ],
    style=CONTENT_STYLE
)

app.layout = html.Div([
    dcc.Location(id="url"),
    dbc.Row([
        dbc.Col(sidebar, width=1),
        dbc.Col(content, width=11, style={"padding": "0"})
    ]),
])


@callback(
    Output('bar-chart', 'figure'),
    Output('chart_title', 'children'),
    Output('chart_description', 'children'),
    Input('dimension-dropdown', 'value'),
    Input('map', 'selectedData'),
    Input('org_level_button', 'value'),
    Input('year_button', 'value'),
    Input('chart_button', 'value'))
def display_chart(dimension, selectedData, org_level, year, chart_type):
    location = "All Submitters"
    if selectedData is None and not(org_level == "Provider" and dimension in config.special_dimensions and chart_type == "Time Series"):
        org_level = "National"
    else:
        if org_level == "NHS England (Region)":
            if "location" in selectedData["points"][0]:
                location = selectedData["points"][0]["location"]
            else:
                org_level = "National"

        elif org_level == "Provider" and not(selectedData == None):
            if "customdata" in selectedData["points"][0]:
                location = selectedData["points"][0]["customdata"][0]
            else: 
                org_level = "National"
    if selectedData is None and org_level == "Provider" and dimension in config.special_dimensions and chart_type == "Time Series":
        org_level = "Provider"
    elif selectedData is not None and org_level == "Provider" and dimension in config.special_dimensions and chart_type == "Time Series":
        org_level = "Provider"
        location =  selectedData["points"][0]["customdata"][0]

    if ctx.triggered_id == "org_level_button":
        location = "All Submitters"
        org_level = "National"
        
    fig = get_chart(org_level, dimension, year, chart_type, location)
    title, description = get_chart_title(dimension, year, location, chart_type)
    return fig, title, description


@callback(
    Output('map', 'figure'),
    Output('map_title', 'children'),
    Output('map_description', 'children'),
    #Output('selectedDataDisplay', 'children'),
    #Output('selectedpointsdisplay', 'children'),
    Input('dimension-dropdown', 'value'),
    Input('map', 'selectedData'),
    Input('org_level_button', 'value'),
    Input('year_button', 'value'))
def display_map(dimension, selectedData, org_level, year):

    if selectedData is None or ctx.triggered_id == "org_level_button":
        selectedpoints = None
    else:
        selectedpoints = [point["pointIndex"] for point in selectedData["points"]]

    fig = get_map(org_level, dimension, year, selectedpoints=selectedpoints)
    map_title, map_description = get_map_title(dimension, year, org_level)

    return fig, map_title, map_description#, json.dumps(selectedData), json.dumps(selectedpoints)

if __name__ == '__main__':
    app.run(debug=True)
