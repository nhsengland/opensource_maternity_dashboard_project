from dash import Dash, dcc, html, Input, Output, callback, ctx
import process_data, draw_graphs
import plotly.express as px
import sys
import geopandas as gpd
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import json
sys.path.append('./')
import config


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
org_level =  "NHS England (Region)"
dimension = "AgeAtBookingMotherGroup"
year = "2022-23"
chart_type = "Bar Chart"


def get_map(org_level, dimension, year, selectedpoints=None):
    if org_level == "NHS England (Region)":
        fig = draw_graphs.draw_region_map(org_level, dimension, year, selectedpoints)
    if org_level == "Provider":
        fig = draw_graphs.draw_provider_map(org_level, dimension, year, selectedpoints)
    return fig

def get_chart(org_level, dimension, year, chart_type, location):
    if chart_type == "Bar Chart":
        # change this to a variavle within config
        if dimension in config.special_dimensions:
            fig = draw_graphs.draw_special_bar_chart(dimension, year)

        else:
            fig = draw_graphs.draw_bar_chart(org_level, dimension, year, location)
    else:
        fig = draw_graphs.draw_time_series(org_level, dimension, location) 
    
    return fig


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
    "margin-left": "8rem", 
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout", className="lead"
        ),
        dcc.RadioItems(
        options=['NHS England (Region)', 'Provider'],
        value='NHS England (Region)',
        id = "org_level_button"
        ),
        html.P("Pick a year to see the data", className="lead"),
        dcc.RadioItems(
        options=['2022-23', '2021-22'],
        value='2022-23',
        id = "year_button"
        ),
        html.P("Pick a measure to view", className="lead"),
        dcc.Dropdown(list(config.measure_dict.keys()), dimension, id='dimension-dropdown'), #this might need updated for region/provider. 
        html.P("View the Bar chart or time series", className="lead"),
        dcc.RadioItems(
        options=['Bar Chart', 'Time Series'],
        value='Bar Chart',
        id = "chart_button"
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(
    [dbc.Row(
        [
            dbc.Col(
                dcc.Graph(
                    id='map',
                    figure=get_map(org_level, dimension, year),
                    style={"height": "800px"}
                ), width=5, style={"padding": "0"}
            ),
            dbc.Col(
                dcc.Graph(
                    id='bar-chart',
                    figure=get_chart(org_level, dimension, year, chart_type, location="All Submitters"),
                    style={"height": "800px"}
                ), width=7, style={"padding": "0"} 
            )
        ]
    ),
            html.Div([
            html.Pre(id='selectedData')
        ]),   

    html.Div([
            html.Pre(id='selectedpoints')
        ]),   
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


# @callback(
#     Output('click-data', 'children'),
#     Input('map', 'selectedData'))
# def display_click_data(clickData):
#     return json.dumps(clickData, indent=2)



@callback(
    Output('bar-chart', 'figure'),
    Input('dimension-dropdown', 'value'),
    Input('map', 'selectedData'),
    Input('org_level_button', 'value'),
    Input('year_button', 'value'),
    Input('chart_button', 'value'))
def display_chart(dimension, selectedData, org_level, year, chart_type):
    location = "All Submitters"

    if selectedData is None:
        org_level = "National"
    else:
        if org_level == "NHS England (Region)":
            if "location" in selectedData["points"][0]:
                location = selectedData["points"][0]["location"]
            else:
                org_level = "National"

        elif org_level == "Provider":
            if "text" in selectedData["points"][0]:
                location = selectedData["points"][0]["text"].split('<br>')[0]
            else: 
                org_level = "National"


    # I have fixed this so it will now revert to a bar chart of all submitters when flicking between org levels
    # before, i was getting callback errors because it couldn't find a location
    # is reverting to all submitters the best thing?
    fig = get_chart(org_level, dimension, year, chart_type, location)
    return fig


@callback(
    Output('map', 'figure'),
    Output('selectedData', 'children'),
    Output('selectedpoints', 'children'),
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

    return fig, json.dumps(selectedData), json.dumps(selectedpoints)

if __name__ == '__main__':
    app.run(debug=True)
