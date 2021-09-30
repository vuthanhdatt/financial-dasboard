
import dash
from dash.dcc.Tab import Tab
from dash.dcc.Tabs import Tabs
from dash.html.Div import Div
from dash.html.Label import Label
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px

df = px.data.iris()  # iris is a pandas DataFrame
fig = px.scatter(df, x="sepal_width", y="sepal_length")

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.Div(
            [
                html.Div(
                    'Choose date', className='plot-1-date'
                ),
                
                html.Div(
                    'Plot 1', className='plot-1-plot'
                )
            ], className= 'plot-1'
        ),
        html.Div(
            [
                html.Div(
                    'Singapore Stock Market Dasboard', className='title-inside'
                )
            ], className= 'title'
        ),
        html.Div(
            [
                html.Div(
                    'Choose date', className='plot-2-date'
                ),
                html.Div(
                    'Plot 2', className= 'plot-2-plot'
                )
            ], className= 'plot-2'
        ),
        html.Div(
            [
                'Plot 3'
            ], className= 'plot-3'
        ),
        html.Div(
            [
                'Credit'
            ], className= 'credit'
        ),
        html.Div(
            [
                html.Div(
                    'Drop down', className='drop-down-plot-4'
                ),
                html.Div(
                    'Plot 4', className= 'plot-4-plot'
                )
            ], className= 'plot-4'
        ),
        html.Div(
            [
                'Plot 5'
            ], className='plot-5'
        )

    ], className= 'container'
)

  



if __name__ == '__main__':
    app.run_server(debug=True)