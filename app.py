from flask import Flask, render_template, request
import plotly
import pypyodbc
import plotly.graph_objects as go
import numpy as np
import plotly.offline as ply
import json
import pandas as pd
import collections

app = Flask(__name__)
conn = pypyodbc.connect('Driver=ODBC Driver 13 for SQL Server;'
                        'Server=localhost\SQLEXPRESS;'
                        'Database=TestDB;'
                        'username=boyd;'
                        'password=P@ssw0rd;'
                        'Trusted_Connection=yes;')


@app.route('/')
def hello_world():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Person')
    rows = cursor.fetchall()
    return render_template("index.html", datas=rows)


@app.route('/simpleGraph1')
def generate_graph1():
    return render_template("json_graph.html")


def get_data():
    # Create sample data
    n = 201
    x = np.linspace(0, 2.0 * np.pi, n)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = y1 + y2

    trace1 = go.Scatter(
        x=x,
        y=y1,
        name="sine curve",
        line=dict(
            color=("red"),
            width=4,
            dash='dash'
        )
    )

    trace2 = go.Scatter(
        x=x,
        y=y2,
        name="cosine curve",
        line=dict(
            color=("green"),
            width=4,
            dash='dot'  # dot, dashdot
        )
    )

    trace3 = go.Scatter(
        x=x,
        y=y3,
        name="sine + cosine curve",
        line=dict(
            color=("blue"),
            width=4,
            dash="dashdot"
        )
    )

    layout = dict(
        title="Some sample sinusoidal curves",
        xaxis=dict(title="Angle in Radian"),
        yaxis=dict(title="Magnitude")
    )

    # Pack the data
    data = [trace1, trace2, trace3]

    # Create a figure
    fig = dict(data=data, layout=layout)
    # Plot
    # url_plot = ply.plot(fig)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


@app.route('/simpleGraph2')
def graph2():
    data = get_data()
    return render_template("line_graph.html", plot=data)

def create_plot(feature):
    if feature == 'Bar':
        N = 40
        x = np.linspace(0, 1, N)
        y = np.random.randn(N)
        df = pd.DataFrame({'x': x, 'y': y})
        data = [
            go.Bar(
                x=df['x'],
                y=df['y']
            )
        ]
    else:
        N = 1000
        random_x = np.random.randn(N)
        random_y = np.random.randn(N)

        # Create a trace
        data = [go.Scatter(
            x = random_x,
            y = random_y,
            mode = 'markers'
        )]


    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


@app.route('/bar', methods=['GET', 'POST'])
def change_features():

    feature = request.args['selected']
    graphJSON= create_plot(feature)

    return graphJSON


@app.route('/simpleGraph3')
def go_generate_graph3():
    bar = create_plot('Bar')
    return render_template("simple_plot.html", plot=bar)


if __name__ == '__main__':
    app.run(debug=True)
