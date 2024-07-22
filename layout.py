from dash import Dash, dcc, html, Input, Output, callback, ctx
import draw_graphs
import sys
import dash_bootstrap_components as dbc
import json

sys.path.append("./")
import config
import textwrap
import defaults
import style
import map_utils

debug = False
visibility = "hidden" if not (debug) else "visible"

sidebar = html.Div(
    [
        html.H4("Visualising: NHS England Maternity Dataset ", className="display-6"),
        html.Hr(),
        html.P("Choose a level", className="lead"),
        dcc.RadioItems(
            options=["NHS England (Region)", "Provider"],
            value="NHS England (Region)",
            id="org_level_button",
        ),
        html.P(""),
        html.Hr(),
        html.P("Pick a year to see the data", className="lead"),
        dcc.RadioItems(
            options=["2022-23", "2021-22", "2020-21"], value="2022-23", id="year_button"
        ),
        html.P(""),
        html.Hr(),
        html.P("View the breakdown using a bar chart or time series", className="lead"),
        dcc.RadioItems(
            options=["Bar Chart", "Time Series"], value="Bar Chart", id="chart_button"
        ),
        html.P(""),
        html.Hr(),
        html.P("Pick a measure to view", className="lead"),
        dcc.Dropdown(
            list(config.measure_dict["NHS England (Region)"].keys()),
            defaults.dimension,
            id="dimension-dropdown",
        ),
        html.Hr(),
    ],
    style=style.SIDEBAR_STYLE,
)


content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2(
                            "Percentage of Mothers OVER the age of 35 for 2022-23",
                            id="map_title",
                        ),
                        html.H4(
                            "Chloropleth map of England, broken in seven regions",
                            id="map_description",
                        ),  # move these to have different rowsand cols
                        dcc.Graph(
                            id="map",
                            figure=map_utils.get_map(
                                defaults.org_level, defaults.dimension, defaults.year
                            ),
                            style={"height": "800px"},
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.H2(
                            "All Submitters: AgeAtBookingMotherGroup 2022-23",
                            id="chart_title",
                        ),
                        html.H4(
                            "Bar chart of broken down data, with markers comparing to All Submitters",
                            id="chart_description",
                        ),
                        dcc.Graph(
                            id="bar-chart",
                            figure=map_utils.get_chart(
                                defaults.org_level,
                                defaults.dimension,
                                defaults.year,
                                defaults.chart_type,
                                location="All Submitters",
                            ),
                            style={"height": "800px"},
                        ),
                    ],
                    width=6,
                ),
            ]
        ),
        html.Div(
            [html.Pre(id="selectedDataDisplay")], style={"visibility": visibility}
        ),
        html.Div(
            [html.Pre(id="selectedpointsdisplay")], style={"visibility": visibility}
        ),
    ],
    style=style.CONTENT_STYLE,
)
