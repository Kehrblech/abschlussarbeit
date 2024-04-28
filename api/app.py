from flask import Flask, render_template
import sqlite3
import matplotlib.pyplot as plt
import io
import base64
import json
from datetime import datetime
import matplotlib.dates as mdates
from collections import Counter
import diagrams
app = Flask(__name__)
@app.route('/')
def home():
    data = diagrams.get_data_from_db()
    chart = diagrams.create_chart(data)
    data_scroll_percentage = diagrams.get_scroll_data_from_db()
    chart_scroll_percentage = diagrams.create_scroll_histogram(data_scroll_percentage)
    chart_time = diagrams.create_stay_time_pie_chart(); 
    os_count = diagrams.get_user_agent_count()
    pop_sections = diagrams.get_popular_sections()
    language_most_used = diagrams.get_most_used_language()
    resulution_most_used = diagrams.get_most_used_resolution()
    scroll_max_avg = diagrams.calculate_average_max_scroll()
    browser_most_pop = diagrams.get_most_popular_browsers()
    return render_template('index.html',browser_most_pop=browser_most_pop,scroll_max_avg=scroll_max_avg,language_most_used=language_most_used,resulution_most_used=resulution_most_used, chart=chart, chart_scroll_percentage=chart_scroll_percentage,chart_time=chart_time, os_count=os_count, pop_sections=pop_sections ,image_path='/annotated_screenshot.png')
@app.route('/analytics')
def analytics():
    data = diagrams.get_data_from_db()
    chart = diagrams.create_chart(data)
    data_scroll_percentage = diagrams.get_scroll_data_from_db()
    chart_scroll_percentage = diagrams.create_scroll_histogram(data_scroll_percentage)
    chart_time = diagrams.create_stay_time_pie_chart(); 
    return render_template('analytics.html', chart=chart, chart_scroll_percentage=chart_scroll_percentage,chart_time=chart_time, image_path='/annotated_screenshot.png')
@app.route('/heatmap')
def heatmap():
    data = diagrams.get_data_from_db()
    chart = diagrams.create_chart(data)
    data_scroll_percentage = diagrams.get_scroll_data_from_db()
    chart_scroll_percentage = diagrams.create_scroll_histogram(data_scroll_percentage)
    chart_time = diagrams.create_stay_time_pie_chart(); 
    return render_template('heatmap.html', chart=chart, chart_scroll_percentage=chart_scroll_percentage,chart_time=chart_time, image_path='/annotated_screenshot.png')
@app.route('/confettimap')
def confettimap():
    data = diagrams.get_data_from_db()
    chart = diagrams.create_chart(data)
    data_scroll_percentage = diagrams.get_scroll_data_from_db()
    chart_scroll_percentage = diagrams.create_scroll_histogram(data_scroll_percentage)
    chart_time = diagrams.create_stay_time_pie_chart(); 
    return render_template('confettimap.html', chart=chart, chart_scroll_percentage=chart_scroll_percentage,chart_time=chart_time, image_path='/annotated_screenshot.png')




if __name__ == '__main__':
    app.run(debug=True)
