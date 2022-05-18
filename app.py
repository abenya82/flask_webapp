
import os

from unicodedata import category
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import itertools
import sqlite3
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

import helpers


basedir = os.getcwd()

app = Flask(__name__, static_url_path='/static')


filename = 'retail774.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,filename)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db = SQLAlchemy(app)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])


@app.route('/')
def index():
    
    return render_template('home.html')


@app.route('/one_column_landing/', methods=['POST','GET'])
def one_column_landing():
    if request.method == "POST":
        column = request.form['pie_chart_columns']
        year = request.form['year']
        return redirect(url_for('pie_chart',column_name=column, year=year))
    else:
        return render_template('one_column_landing_page.html')







@app.route('/shipping_landing/', methods=['POST','GET'])
def shipping_landing():
    if request.method == "POST":
        if request.form['column_summed']:
            column_summed = request.form['column_summed']
            locations = request.form['locations']
            return redirect(url_for('shipping_bar_chart',column_summed=column_summed, column_location_type=locations))
        if request.form['column1']:
            column1 = request.form['column1']
            column2 = request.form['column2']
            return redirect(url_for('shipping_freq_chart',column1=column1, column2=column2))

    else:
        return render_template('shipping_landing.html')




    


@app.route('/product_landing/', methods=['POST','GET'])
def product_landing():

    top_product_chart = helpers.get_top_items_count_graph(engine=engine,number_of_items=10)
    if request.method == "POST":
        product = request.form['product']
        return redirect(url_for('product_chart1',product=product))
    product_list_whole = helpers.get_list_product_names(list_length=0,engine=engine)
    product_list_top10 = helpers.get_list_product_names(list_length=10,engine=engine)
    
    return render_template('product_landing.html',product_list_whole=product_list_whole,product_list_top10=product_list_top10,top_chart_filename=(url_for('static',filename='top_count_chart1.png')))


@app.route('/product/<product>/', methods=['POST','GET'])
def product_chart1(product):

    top_country_counts_chart_filename = helpers.get_top_country_counts_chart(product=product,engine=engine)

    product_list_whole = helpers.get_list_product_names(list_length=0,engine=engine)


    return render_template('product_chart1.html',product=product,product_list_whole=product_list_whole,top_country_counts_chart_filename=(url_for('static',filename='country_prod_chart1.png')))





@app.route('/pie_chart/<string:column_name>/<year>/')
def pie_chart(column_name,year):

    pie_chart_filename = helpers.get_pie_chart_of_frequencies(column_name,year,engine=engine)
    #full_filename = os.path.join(app.root_path, pie_chart_filename)
    options=[1,2,3,5,8]
    
    return render_template('pie_chart.html',options=options,pie_chart_filename=(url_for('static', filename=pie_chart_filename)))



@app.route('/shipping/<string:column_summed>/<column_location_type>/')
def shipping_bar_chart(column_summed,column_location_type):
    bar_chart_filename = helpers.get_2D_sum_stacked_bar_graph(column_summed,column_location_type,engine=engine)


    return render_template('shipping_chart.html',bar_chart_filename=(url_for('static',filename='chart1.png')))


@app.route('/shipping/freq/',methods=['POST','GET'])
def shipping_freq_chart():
    if request.method == "POST":
        column1 = request.form['column1']
        column2 = request.form['column2']
        bar_chart_filename = helpers.get_2D_freq_stacked_bar(column1=column1,column2=column2,engine=engine)
        return render_template('shipping_chart.html',bar_chart_filename=(url_for('static',filename='freqBarChart1.png')))

        return redirect(url_for('shipping_chart_freq.html',bar_chart_filename=(url_for('static',filename='freqBarChart1.png'))))
    else:
    
        return render_template('shipping_landing.html')



@app.route('/time_landing/', methods=['POST','GET'])
def time_landing():
    return render_template('time_landing.html')

@app.route('/time_chart/', methods= ['POST','GET'])
def time_chart():
    if request.method == "POST":
        column1 = request.form['time_selection']
        column2 = request.form['column']
        bar_chart_filename = helpers.get_time_freq_bar_chart_all(time_selection=column1,column=column2,engine=engine)
        return render_template('time_chart.html',bar_chart_filename=(url_for('static',filename='time_chart2.png')))

    return render_template('time_chart.html',)


if __name__ == '__main__':
    app.run(debug=True)
