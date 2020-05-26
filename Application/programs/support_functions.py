"""
support functions to manipulate data before plotting
"""

import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json


def create_line_chart(df, x_axis, y_axis, text_axis, group_axis):

    fig = go.Figure()

    # columns: date, close_price, symbol, simple_name

    data = []
    count = 0
    for group in df[group_axis].unique():

        df_sub = df[df[group_axis] == group]

        # cut clutter by only displaying four items at start
        if count < 4:
            visible = True
        else:
            visible = 'legendonly'

        data.append(go.Scatter(
            x = df_sub[x_axis],
            y = df_sub[y_axis],
            visible=visible,
            mode = 'lines',
            name = group,

        ))
        count += 1


    layout = go.Layout(
        title = 'Robinhood lineplot',
        showlegend = True,
        yaxis = {'title': y_axis},
        xaxis = {'title': x_axis},
        template='plotly_dark'
    )

    fig = dict(data=data, layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def format_table(df, columns, row_filter_col=None, row_filter=None):
    
    if row_filter_col:
        df = df.loc[df[row_filter_col] == row_filter, columns].copy()
    else:
        df = df.loc[:, columns].copy()

    return df

def create_table(df, columns):

    fig = go.Figure()

    data = [
        go.Table(
            header=dict(values= columns,
                    fill_color= 'paleturquoise',
                    align= 'left'),
            cells=dict(values= [ df[x] for x in columns ],
                    fill_color= 'lavender',
                    align= 'left'),
            )
        ]

    layout = go.Layout(
        title = 'data table',

        #width = 1200,

        #margin = { 'l': 20, 'r': 20, 't': 20, 'b': 20, 'pad': 10 },
        #autosize = False,

    )
    
    #fig.update_yaxes(automargin=True)

    
    fig = dict(data=data, layout=layout)

    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
