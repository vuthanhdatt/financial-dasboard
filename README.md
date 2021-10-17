# Financial report dashboard
![Example](https://github.com/vuthanhdatt/financial-dasboard/blob/main/images/singapore.png)
## Introduction
- This project visualizes the profitability of stocks in the market as well as the market capitalization over time to the present time. The data collected for analysis  mainly belongs to companies, share prices and capitalization on the Singapore stock market.
- App: https://singapore-dashboard.herokuapp.com/
## Data Description
- Data is collected from 24th, September 2019 to 24th, September, 2021.
- Database - a data set distributed in rows and columns. All information in the database is contained in the records and fields.
### Singapore ICB (Singapore ICB.xlsx)
### Singapore -  Price – Market Cap (Singapore - Price - Market Cap.xlsx)
## Workflow
### 1. Data Preprocessing
#### Singapore ICB (Singapore ICB.xlsx) Cleaning
- This dataframe only needs to be filled the missing values and dropped some useless columns.
#### Singapore -  Price – Market Cap (Singapore - Price - Market Cap.xlsx) Cleaning
- Because the initial data is inconsistent, so the dataframe should be skipped some residual rows and columns to be in a rectangular shape.
- The dataframe also has some "Error" columns that don't make sense, so it should be dropped.
- There are some companies having the price that is unchanged time by time or some companies are delisted or suspended before the time this data is recorded, which is not useful for analyzing, so it was also dropped. There are some companies that are delisted or suspended after the time data is recorded, these observations should be modified in order to be no misunderstanding.
- The dataframe needs to be refilled due to some missing entrance data.
#### Data Merging - Final Dataframe
- Merging company information with its price or marketcap value
- After merging data, noticed that there are some Exchange-traded fund and company was not listed in Singapore, so these observations should be removed.
- The final dataframe also has some duplicated companies due to the error while collecting data that need to be dropped.
### 2. Data Visualization
