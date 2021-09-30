
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from datetime import date
from dash.dependencies import Input, Output

import plotly.express as px

from process import profit_comparision

df = profit_comparision(before='2020-08-05')
fig = px.bar(df, x='Symbol', y='Profit')

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.Div(
            [
                dcc.DatePickerRange(
                    id='plot-1-picker',
                    min_date_allowed=date(2019, 9, 24),
                    max_date_allowed=date(2021, 9, 24),
                    start_date_placeholder_text = '2021-01-01',
                    start_date= '2021-01-01',
                    end_date_placeholder_text = '2021-09-24',
                    end_date= '2021-09-24',
                    className= 'plot-1-date'
                ),
                dcc.Graph(
                    id= 'plot-1-fig',
                    className='plot-1-plot'
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

@app.callback(
    Output('plot-1-fig', 'figure'),
    Input('plot-1-picker', 'start_date'),
    Input('plot-1-picker', 'end_date'))

def draw_fig1(start_date, end_date):
    fig1_df = profit_comparision(before=start_date, after=end_date)
    fig = px.bar(fig1_df, x='Symbol', y='Profit')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)