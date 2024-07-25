import draw_graphs
import sys

sys.path.append("./")
import config
import textwrap
import draw_graphs

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
            title = f"{dimension}. Bar chart showing the rate of {dimension} per 1000 people for {year}"
        else:
            title = textwrap.fill(f"{location}: {dimension} {year}", width=50)
            description = "Bar chart of broken down data, with markers comparing to All Submitters"
    else:
        title = textwrap.fill(f"{location}: {dimension}", width=50)
        description = "Time series of broken down data"

    return title, description


def get_map_title(dimension, year, org_level):
    title = textwrap.fill(
        f'{config.measure_dict[org_level][dimension]["map_title"]} for {year}', width=50
    )
    if org_level == "NHS England (Region)" or org_level == "National":
        description = "Chloropleth map of England, broken in seven regions"
    elif org_level == "Provider":
        description = "Scatter plot map of England, with each point representing a maternity care provider"

    return title, description
