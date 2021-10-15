import plotly.express as px
from process import full_marketcap_price, top_industry_marketcap
data_market = full_marketcap_price(data='market')

plot5_df = top_industry_marketcap(data_market,industry='all',date='2021-09-24',get_all=True)[['Industry','Symbol','MarketCap','Company']]
fig = px.treemap(plot5_df, path=[px.Constant("Singapore Stock Marketcap"), 'Industry', 'Symbol'],values='MarketCap',hover_data=['Company'])
fig.update_layout(margin = dict(t=0, l=0, r=0, b=0),
                    treemapcolorway = ['#718ba5', '#7994ae','#829eb8','#88a4bf','#90acc8','#96b2ce','#99b6d2','#9dbad6','#a2c0dc','#a8c6e2','#accae7'])
fig.update_traces(root_color = '#f2f0eb',
hovertemplate= 'labels: %{label}<br> MarketCap: %{value} billion SGD <br>Parent: %{parent}<br>Company: %{customdata[0]}<extra></extra>'
                            )
fig.show()


# if __name__ == 'main':
#     print(plot5(data_market))