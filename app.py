
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from datetime import date
from dash.dependencies import Input, Output

import plotly.express as px

from process import profit_comparision,full_marketcap_price, top_industry_marketcap        
data_price = full_marketcap_price(data='price')  
data_market = full_marketcap_price(data='market')
list_industry =list(data_market['Industry'].unique())    
options = []
for industry in list_industry:
    options.append(dict(zip(['label','value'],[industry,industry])))

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
                    className='plot-1-plot',
                    config= {'displaylogo': False}
                )

            ], className= 'plot-1'
        ),
        html.Div(
            [
                html.Div(
                    'SINGAPORE STOCK MARKET DASHBOARD', className='title-inside'
                )
            ], className= 'title'
        ),
        html.Div(
            [
                dcc.DatePickerRange(
                    id='plot-2-picker',
                    min_date_allowed=date(2019, 9, 24),
                    max_date_allowed=date(2021, 9, 24),
                    start_date_placeholder_text = '2021-01-01',
                    start_date= '2021-01-01',
                    end_date_placeholder_text = '2021-09-24',
                    end_date= '2021-09-24',
                    className= 'plot-2-date'
                ),
                dcc.Graph(
                    id= 'plot-2-fig',
                    className='plot-2-plot',
                    config= {'displaylogo': False}
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
                dcc.Dropdown(
                    id='plot-4-dropdown',
                    options=options,
                    value='Industrials',
                    className='drop-down-plot-4',
                    placeholder="Select Industrials"
                ),
                dcc.Graph(
                    id= 'plot-4-fig', 
                    className= 'plot-4-plot',
                    config= {'displaylogo': False}
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
    fig1_df = profit_comparision(data=data_price,before=start_date, after=end_date)
    symbols = list(fig1_df['Symbol'])
    tick = []
    for symbol in symbols:
        part = symbol.split(':')
        tick.append(part[1])
    fig1_df['Symbol'] = tick
    fig = px.bar(fig1_df, x='Symbol', y='Profit')
    fig.update_layout(title_text='TOP 10 HIGHEST RETURN RATES',
                        title_yref='paper',
                        title_y=0.9,
                        title_xref='paper',
                        title_x=0.3,
                        margin_b = 0,
                        margin_l= 0,
                        margin_r = 5,
                        margin_t = 5, paper_bgcolor='#f2f0eb',
                        plot_bgcolor='#f2f0eb')
    fig.update_xaxes(title_text= 'Company')
    fig.update_yaxes(title_text= 'Profit(%)', showgrid=False,zerolinecolor='#000000',zeroline=True,linecolor='#000000',zerolinewidth=0.3)
    fig.update_traces(marker_color='#718BA5', marker_line_color='#000000')
    return fig

@app.callback(
    Output('plot-2-fig', 'figure'),
    Input('plot-2-picker', 'start_date'),
    Input('plot-2-picker', 'end_date'))

def draw_fig2(start_date, end_date):
    fig2_df = profit_comparision(data=data_price,before=start_date, after=end_date, desc= False)
    symbols = list(fig2_df['Symbol'])
    tick = []
    for symbol in symbols:
        part = symbol.split(':')
        tick.append(part[1])
    fig2_df['Symbol'] = tick
    fig = px.bar(fig2_df, x='Symbol', y='Profit')
    fig.update_layout(title_text='TOP 10 LOWEST RETURN RATES',
                        title_yref='container',
                        title_y=0.97,
                        title_xref='paper',
                        title_x=0.5,
                        margin_b = 0,
                        margin_l= 0,
                        margin_r = 5,
                        margin_t = 30, paper_bgcolor='#f2f0eb',
                        plot_bgcolor='#f2f0eb',
                        modebar_add=['drawopenpath','eraseshape'],
                        modebar_remove=['lasso'],
                        modebar_orientation='v')
    fig.update_xaxes(title_text= 'Company')
    fig.update_yaxes(title_text= 'Profit(%)', showgrid=False,zerolinecolor='#000000',zeroline=True,linecolor='#000000',zerolinewidth=0.3)
    fig.update_traces(marker_color='#fdd0a2', marker_line_color='#000000')
    return fig

@app.callback(
    Output('plot-4-fig', 'figure'),
    Input('plot-4-dropdown', 'value')
)
def  draw_fig4(value):
    fig4_df = top_industry_marketcap(data=data_market, industry=value)

    fig = px.bar(fig4_df, x='Symbol', y='MarketCap')
    fig.update_layout(title_text='TOP 5 BIGGEST COMPANY BY INDUSTRY',
                        title_yref='container',
                        title_y=0.97,
                        title_xref='paper',
                        title_x=0.5,
                        margin_b = 0,
                        margin_l= 0,
                        margin_r = 5,
                        margin_t = 30, paper_bgcolor='#f2f0eb',
                        plot_bgcolor='#f2f0eb',
                        modebar_add=['drawopenpath','eraseshape'],
                        modebar_remove=['lasso'],
                        modebar_orientation='v')
    fig.update_xaxes(title_text= 'Company')
    fig.update_yaxes(title_text= 'Profit(%)', showgrid=False,zerolinecolor='#000000',zeroline=True,linecolor='#000000',zerolinewidth=0.3)
    fig.update_traces(marker_color='#718BA5', marker_line_color='#000000')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)