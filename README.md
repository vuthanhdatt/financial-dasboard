# Financial report dashboard
## Introduction
- This project visualizes the profitability of stocks in the market as well as the market capitalization over time to the present time. The data collected for analysis  mainly belongs to companies, share prices and capitalization on the Singapore stock market.
- App: https://singapore-dashboard.herokuapp.com/
### Preview
![Dasboard](https://github.com/vuthanhdatt/financial-dasboard/blob/main/images/singapore.png)
## Data Description
- Data is collected from 24th, September 2019 to 24th, September, 2021.
- Database - a data set distributed in rows and columns. All information in the database is contained in the records and fields.
### [Singapore ICB (Singapore ICB.xlsx)](https://github.com/vuthanhdatt/financial-dasboard/blob/main/data/Singapore%20ICB.xlsx)
- Almost all the data in this sheet is text.
- Data in field “Name” describes companies’ abbreviated names in Singapore Exchange Stock. It shows if the company is listed in the form of stock or ETF. Besides, if a company's stock is not bidded in SGX, it displays in SES or (SES).
- Field “Symbol” is text (numbers and letters) representing publicly-traded securities on an exchange Singapore stock by Thomson reuter.
- Field “RIC” is used to describe the unique codes used by Reuters to identify a piece of Reuters data.
- Field “Type” is the same as Field Symbol.
- Field “NAME” describes the company's status. They have 3 status: Dead - SUSP- DELIST
- Field “Name Company” describes the company’s full name or their corporation.
- Field “ICB INDUSTRY NAME” describes the industry to which these companies belong.

### [Singapore -  Price – Market Cap (Singapore - Price - Market Cap.xlsx)](https://github.com/vuthanhdatt/financial-dasboard/blob/main/data/Singapore%20-%20Price%20-%20Market%20Cap.xlsx)
#### Price sheet
- Data in these fields is inconsistent and is arranged not according to any trends.
- Each variable “Name” shows the company’s status. Each column **represents the company’s price stock at that time**.
- Field Name, Symbol, RIC, Type link to field Name, Symbol, RIC, Type in [Singapore ICB](https://github.com/vuthanhdatt/financial-dasboard/blob/main/data/Singapore%20ICB.xlsx).
#### Market Value Sheet 
- Data in these fields is inconsistent and is arranged not according to any trends.
- Field Name, Symbol, RIC, Type link to with field Name, Symbol, RIC, Type in [Singapore ICB](https://github.com/vuthanhdatt/financial-dasboard/blob/main/data/Singapore%20ICB.xlsx).
- Each column Name company **represents company’s capitalization at that time**. 


## Workflow
### 1. Structures
```
├───assets
│       favion.ico
│       style.css
├───data
│
├───ideas
│
├───images
│
├── app.py        
├── config.py
├── process.py                 
├── Procfile           
└── requirements.txt
```

### 2. Data Preprocessing
In order to improve app performance, we converted ```.xlsx``` file to ```.csv``` file. However, for convenience, we still assume using ```.xlsx``` file for all explanation below. All processing returns are in ``process.py`` file

#### Singapore ICB (Singapore ICB.xlsx) Cleaning
- This dataframe only needs to be filled the missing values and dropped some useless columns.
#### Singapore -  Price – Market Cap (Singapore - Price - Market Cap.xlsx) Cleaning
- Because the initial data is inconsistent, so the dataframe should be skipped some residual rows and columns to be in a rectangular shape.
- The dataframe also has some "Error" columns that don't make sense, so it should be dropped.
- There are some companies having the price that is unchanged time by time or some companies are delisted or suspended before the time this data is recorded, which is not useful for analyzing, so it was also dropped. There are some companies that are delisted or suspended after the time data is recorded, these observations should be modified in order to be no misunderstanding.
- The dataframe needs to be refilled due to some missing entrance data.
#### Data Merging - Final Dataframe
- Merging company information with its price or marketcap value.
- After merging data, noticed that there are some Exchange-traded fund and company was not listed in Singapore, so these observations should be removed.
- The final dataframe also has some duplicated companies due to the error while collecting data that need to be dropped.
### 3. Data Visualization
For visualization, we using [Plotly](https://plotly.com/python/) to draw figure and [Dash](https://dash.plotly.com/) to represent. We also using [Heroku](https://heroku.com/) for hosting web app.
#### Figures
There are 3 type of charts in this dashboard: [Bar charts](https://plotly.com/python/bar-charts/), [Line charts](https://plotly.com/python/line-charts/) and [Treemap charts](https://plotly.com/python/treemaps/). All figures are in ``app.py`` file.

- To present top 10 companies have highest/lowest return rates and top 5 companies have biggest marketcap, we using **Bar chart**. Users can interactive with these figures, change dates, change industries, draw, zoom in, etc.
- To have an overview of market, we using **Treemap chart**. With this chart, users can click on any industry or company for more information. Users can also know overall marketcap or marketcap by industry.
- With companies on highest price in 52 weeks, we using **Line chart**. With this chart, users can easily check pirce of these companies at any time over 52 weeks past. Users can also choose date, note that, with date have companies with unscale prices, for example, 7 SGD and 0.5 SGD, users can click on company legends to remove this company from chart. This help our chart is more beautiful.
#### App layout

We redefined all default Dash layout in ``style.css``. This require some little knowledge about [CSS](https://en.wikipedia.org/wiki/CSS). Since this not relevant to our subject, we will not mention here.

## Conclusion
This is an interesting project, since we all start from zero and we study lots of things through this project. Many thanks to contributing and helping from [@123olala](https://github.com/123olala), [@GiapHoangLong](https://github.com/GiapHoangLong), [@LNPLoc](https://github.com/LNPLoc), [@hathanhtna](https://github.com/hathanhtna).
