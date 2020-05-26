"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from python_webapp_flask import app

from flask import Flask, flash, render_template, request, redirect, url_for
from flask_uploads import UploadSet
import plotly
import plotly.graph_objs as go
import plotly.express as px

import pandas as pd
import numpy as np
import json

from programs import gran_postgres
#from programs import support_functions
import programs.support_functions as support

from programs.machine_A import MachineA


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        message='Your home page.'
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/correction')
def correction():
    """Renders the about page."""
    return render_template(
        'correction.html',
        title='Correction',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/visualise')
def visualise():
    """Renders the visualize page."""

    # get df of stocks

    artifact = gran_postgres.StockConn()
    S2 = artifact.get_stocks_df()
    columns = S2.columns

    # create line graph
    x_axis, y_axis, group_axis = 'date', 'close_price', 'symbol'
    linechart = support.create_line_chart(S2, x_axis, y_axis, y_axis, group_axis)
    '''    '''
    return render_template(
        'visualise.html',
        linechart=linechart,
        table=json.dumps(go.Figure(), cls=plotly.utils.PlotlyJSONEncoder),
        title='Visualise',
        year=datetime.now().year,
        message='Visualize digested data using plotly'
    )

docs = UploadSet('docs')

@app.route('/upload_data', methods=['GET', 'POST'])
def upload_data():
    print("accessed upload_data!")
    print("Posted file: {}".format(request.files['file']))
    if request.method == 'POST':

        flash("Machine Data saved.")

        # get file
        doc = request.files['file']


        parent_dir = 'Application/programs/sample_data/'
        print(doc.filename)
        #path = 'sample_data/Magellan Sheet 4.csv'
        if 'Magellan' in doc.filename:

            # create a class and process
            MACA = MachineA()
            df = MACA.process(parent_dir + doc.filename)
        else:
            df = pd.read_csv(doc)
            
        #print(df.head())
        columns = df.columns
        '''
        row_filter_col = 'Country Code'
        row_filter = 'JPN'
        df = support.format_table(df, columns, row_filter_col, row_filter)
        '''
        df = support.format_table(df, columns)
        print(df.shape)

        graphJSON = support.create_table(df, columns, doc.filename)

    else:
        print("machine_data not uploaded")
        graphJSON = None

    return graphJSON

