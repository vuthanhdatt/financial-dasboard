
import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import date
from dash.dependencies import Input, Output
import plotly.graph_objects as go


import plotly.express as px

from process import greater_price, profit_comparision,full_marketcap_price, top_industry_marketcap        
data_price = full_marketcap_price(data='price')  
data_market = full_marketcap_price(data='market')
list_industry =list(data_market['Industry'].unique())    
options = []
for industry in list_industry:
    options.append(dict(zip(['label','value'],[industry,industry])))
def change_tick(data):
    symbols = list(data['Symbol'])
    tick = []
    for symbol in symbols:
        try:
            part = symbol.split(':')
            tick.append(part[1])
        except:
            tick.append(symbol)
    data['Symbol'] = tick
    return data
plot5_df = top_industry_marketcap(data_market,industry='all',date='2021-09-24',get_all=True)[['Industry','Symbol','MarketCap','Company']]
plot5_df = change_tick(plot5_df)
fig = px.treemap(plot5_df, path=[px.Constant("Singapore Stock Marketcap"), 'Industry', 'Symbol'],
                    values='MarketCap',hover_data=['Company'])
fig.update_layout(margin = dict(t=0, l=0, r=0, b=0),
                    treemapcolorway = ['#718ba5', '#7994ae','#829eb8','#88a4bf','#90acc8'
                                        ,'#96b2ce','#99b6d2','#9dbad6','#a2c0dc','#a8c6e2','#accae7'])
fig.update_traces(root_color = '#f2f0eb',
hovertemplate= 'labels: %{label}<br>MarketCap: %{value} billion SGD <br>Parent: %{parent}<br>Company: %{customdata[0]}<extra></extra>')

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
                dcc.DatePickerSingle(
                    id='plot-3-picker',
                    min_date_allowed=date(2020, 9, 24),
                    max_date_allowed=date(2021, 9, 24),
                    initial_visible_month=date(2021, 9, 24),
                    date=date(2021, 9, 24,),
                    className= 'plot-3-date'
                ),
                dcc.Graph(
                    id= 'plot-3-fig',
                    className='plot-3-plot',
                    config= {'displaylogo': False}
                )
            ], className= 'plot-3'
        ),
        html.Div(
            [
                'credit'

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
        dcc.Graph(
            figure= fig, className='plot-5'
        )

    ], className= 'container'
)



@app.callback(
    Output('plot-1-fig', 'figure'),
    Input('plot-1-picker', 'start_date'),
    Input('plot-1-picker', 'end_date'))

def draw_fig1(start_date, end_date):

    fig1_df = profit_comparision(data=data_price,before=start_date, after=end_date)
    fig1_df = change_tick(fig1_df)

    fig = px.bar(fig1_df, x='Symbol', y='Profit', hover_data=['Company', start_date, end_date])
    fig.update_layout(title_text='TOP 10 HIGHEST RETURN RATES',
                        title_yref='container',
                        title_y=0.97,
                        title_xref='paper',
                        title_x=0.5,
                        margin_b = 0,
                        margin_l= 0,
                        margin_r = 5,
                        margin_t = 30,
                        paper_bgcolor='#f2f0eb',
                        plot_bgcolor='#f2f0eb',
                        modebar_add=['drawopenpath','eraseshape'],
                        modebar_remove=['lasso'],
                        modebar_orientation='v')
    fig.update_xaxes(title_text= 'Company')
    fig.update_yaxes(title_text= 'Profit(%)',
                        showgrid=False,
                        zerolinecolor='#000000',
                        zeroline=True,
                        linecolor='#000000',
                        zerolinewidth=0.3)
    fig.update_traces(marker_color='#718BA5', 
                        marker_line_color='#000000',
                        hovertemplate= 'Symbol: %{x}<br><b>Profit: %{y}% </b><br>Company: %{customdata[0]}<br>Open price: %{customdata[1]} SGD<br>Close price: %{customdata[2]} SGD')

    return fig

@app.callback(
    Output('plot-2-fig', 'figure'),
    Input('plot-2-picker', 'start_date'),
    Input('plot-2-picker', 'end_date'))

def draw_fig2(start_date, end_date):

    fig2_df = profit_comparision(data=data_price,before=start_date, after=end_date, desc= False)
    fig2_df = change_tick(fig2_df)

    fig = px.bar(fig2_df, x='Symbol', y='Profit', hover_data=['Company', start_date, end_date])
    fig.update_layout(title_text='TOP 10 LOWEST RETURN RATES',
                        title_yref='container',
                        title_y=0.97,
                        title_xref='paper',
                        title_x=0.5,
                        margin_b = 0,
                        margin_l= 0,
                        margin_r = 5,
                        margin_t = 30, 
                        paper_bgcolor='#f2f0eb',
                        plot_bgcolor='#f2f0eb',
                        modebar_add=['drawopenpath','eraseshape'],
                        modebar_remove=['lasso'],
                        modebar_orientation='v')
    fig.update_xaxes(title_text= 'Company')
    fig.update_yaxes(title_text= 'Profit(%)',
                        showgrid=False,
                        zerolinecolor='#000000',
                        zeroline=True,
                        linecolor='#000000',
                        zerolinewidth=0.3)
    fig.update_traces(marker_color='#fdd0a2', 
                        marker_line_color='#000000',
                        hovertemplate= 'Symbol: %{x}<br><b>Profit: %{y}% </b><br>Company: %{customdata[0]}<br>Open price: %{customdata[1]} SGD<br>Close price: %{customdata[2]} SGD')
    return fig

@app.callback(
    Output('plot-3-fig', 'figure'),
    Input('plot-3-picker', 'date')
)
def draw_fig3(date_value):
    fig3_df = greater_price(data=data_price, date=date_value)
    fig3_df = change_tick(fig3_df)

    traces = [go.Scatter(
    x = fig3_df.columns,
    y = fig3_df.loc[rowname],
    mode = 'lines',
    name = fig3_df.loc[rowname][0],
    customdata= [rowname]*len(fig3_df.columns),
    hovertemplate= 'Date: %{x} <br> <b>Price: %{y} SGD</b><br> Company: %{customdata}'
)for rowname in fig3_df.index]
    fig = go.Figure(data=traces)
    fig.update_layout(title_text='COMPANY ON HIGHEST PRICE IN 52 WEEKS',
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
                        modebar_orientation='v',
                        legend= dict(bordercolor='#000000', borderwidth= 0.5))
    fig.update_xaxes(showgrid=False)               
    fig.update_yaxes(title_text= 'Price(SGD)',
                        showgrid=False,
                        zerolinecolor='#000000',
                        zeroline=True,
                        linecolor='#000000',
                        linewidth = 0.3,
                        zerolinewidth=0.3)
    return fig
    


@app.callback(
    Output('plot-4-fig', 'figure'),
    Input('plot-4-dropdown', 'value')
)
def  draw_fig4(value):
    fig4_df = top_industry_marketcap(data=data_market, industry=value)

    fig = px.bar(fig4_df, x='Symbol', y='MarketCap', hover_data=['Company'])
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
    fig.update_yaxes(title_text= 'Marketcap(Billion)', showgrid=False,zerolinecolor='#000000',zeroline=True,linecolor='#000000',zerolinewidth=0.3)
    fig.update_traces(marker_color='#718BA5', marker_line_color='#000000',
                        hovertemplate= 'Symbol: %{x}<br><b>MarketCap: %{y} Billion SGD</b><br>Company: %{customdata[0]}')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)