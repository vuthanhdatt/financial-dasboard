import pandas as pd
import numpy as np
import config
import warnings
from datetime import datetime as dt
from datetime import timedelta as delta
warnings.filterwarnings("ignore")

def clean_marketcap_price(data='market'):
    """
    Parameter:
        data: 'market' or 'price'
    """
    
    #Extract the Symbol in order to set the columns name
    symbol_name = [
        str(name) for name in list(pd.read_excel(config.MARKETCAP_PRICE,sheet_name='Market cap')['Symbol'])
    ]
    if data == 'market':
        #Load data and drop useless columns and rows
        df = pd.read_excel(config.MARKETCAP_PRICE,sheet_name='Market cap',skiprows=3).iloc[:,4:]
    elif data == 'price':
        #Load data and drop useless columns and rows
        df = pd.read_excel(config.MARKETCAP_PRICE,sheet_name='Price',skiprows=3).iloc[:,4:]
    else:
        return 'Dataset not found.'
    #Delete residual rows
    df = df.loc[df['Name'].notnull()]
    #Convert data of time to datetime 
    df['Name'] = pd.to_datetime(df['Name'])
    #Rename the columns of date
    df.rename(columns={'Name':'Date'},inplace=True)
    #Set Date column as index
    df.set_index('Date',inplace=True)
    #Shortcut the name of columns
    df.columns = symbol_name
    # Drop "Error" columns
    df = df.select_dtypes(exclude='object')
    #Delete useless columns
    to_drop = [col for col in df.columns if len(df[col].unique()) == 1]
    df.drop(to_drop,axis=1,inplace=True)
    #Get the name of columns that have missing values
    missing_col = {}
    col_countnull = df.isnull().sum().reset_index()
    for i in range(len(col_countnull)):
        if col_countnull.loc[i,0] != 0:
            missing_col[col_countnull.loc[i,'index']] = col_countnull.loc[i,0]
    #Fill the missing values 
    for col in missing_col:
        #Because the missing value is only located in the left tail, it implies that the company was not listed on those days.
        df[col].fillna(value=0,inplace=True)

    return df

def full_marketcap_price(data='market'):
    """
    Return dataframe of companies with price/marketcap information.
    Parameter:
        data: 'market' or 'price'
    """

    if (data == 'market') or (data == 'price'):
        company = pd.read_excel(config.COMPANY)
        #Choose columns to merge and rename them
        to_merge = company[['Symbol','Name','NAME','COMPANY NAME','RIC','ICB INDUSTRY NAME']]
        to_merge.columns = ['Symbol','Name','Status Name','Company','RIC','Industry']
        #Fill in the missing values
        to_merge.fillna(value='Unknown',inplace=True)
        to_merge['RIC'].replace('-','Unknown',inplace=True)
        #Load data cleaned
        main = clean_marketcap_price(data).reset_index()
        main['Date'] = main['Date'].astype('string')
        main = main.transpose()
        main.reset_index(inplace=True)
        main.columns = main.iloc[0]
        main = main.iloc[1:].reset_index(drop=True)
        main.rename(columns={'Date':'Symbol'},inplace=True)
        #Merge the dataset
        df = to_merge.merge(main,how='right',on='Symbol')
        #Correct datatype of df
        for col in df.columns[6:]:
            df[col] = df[col].astype('float64')
        #Delete Exchange-traded fund and company was not listed in Singagore
        df = df[~df['Name'].str.contains("\\(SES")]
        df = df[~df['Name'].str.contains("ETF")]
        df.reset_index(drop=True,inplace=True)
        #Correct data of Delist or Suspended company 
        delist_time = [name.split('.')[-1] for name in df.loc[df['Status Name'].str.contains('DELIST')]['Status Name']]
        delist_time = [date_available(dt.strftime(dt.strptime(i,'%d/%m/%y'),'%Y-%m-%d')) for i in delist_time]
        delist_code = [code for code in df.loc[df['Status Name'].str.contains('DELIST')]['Symbol']]
        delist = {delist_code[i]:delist_time[i] for i in range(len(delist_time))}
        for symbol,date in delist.items():
            df.loc[df['Symbol'] == symbol,date:] = 0
        susp_time = [name.split('.')[-1] for name in df.loc[df['Status Name'].str.contains('SUSP')]['Status Name']]
        susp_time = [date_available(dt.strftime(dt.strptime(i,'%d/%m/%y'),'%Y-%m-%d')) for i in susp_time]
        susp_code = [code for code in df.loc[df['Status Name'].str.contains('SUSP')]['Symbol']]
        susp = {susp_code[i]:susp_time[i] for i in range(len(susp_time))}
        for symbol,date in susp.items():
            df.loc[df['Symbol'] == symbol,date:] = 0
    else:
        return 'Dataset not found.'

    return df

def date_available(to_convert):
    if dt.strptime(to_convert,'%Y-%m-%d').weekday() == 6:   #Sunday
        sub = dt.strptime(to_convert,'%Y-%m-%d') - delta(days=2)        #Convert to the closet Friday
        to_convert = dt.strftime(sub,'%Y-%m-%d')
    elif dt.strptime(to_convert,'%Y-%m-%d').weekday() == 5:     #Saturday
        sub = dt.strptime(to_convert,'%Y-%m-%d') - delta(days=1)    #Convert to the closet Friday
        to_convert = dt.strftime(sub,'%Y-%m-%d')
    else:
        return to_convert
    
    return to_convert

def profit_comparision(data,before='2021-01-01',after='2021-09-24',top=10,desc=True):
    """
    Return dataframe of top companies with the highest or lowest profit in a specified time range.
    Parameters:
        data: dataframe from full_marketcap_price function
        before: 'YYYY-MM-DD' format
        after: 'YYYY-MM-DD' format
        top: The number of top companies is returned
        desc: Return dataframe in descending order if True, return dataframe in ascending order if False
    """
    before = date_available(before)
    after = date_available(after)
    df_price = data
    df = df_price[
        (df_price[before]!=0) & (df_price[after]!=0)
    ][['Symbol','Name','Company','Industry',before,after]]
    df['Profit'] = (df[after] - df[before])/df[before] *100
    if desc == True:
        df = df.sort_values('Profit',ascending=False).head(top).reset_index(drop=True)
    else:
        df = df.sort_values('Profit',ascending=True).head(top).reset_index(drop=True)
    
    return df

def top_industry_marketcap(data, industry='Financials', date='2021-09-24',top=5,desc=True,get_all=False):
    """
    Return top companies with highest or lowest market cap in specified time group by industry.
    Parameters:
        data: dataframe from full_marketcap_price function
        industry: Return dataframe filtered by industry. If industry = "all", return the whole industry 
        date: 'YYYY-MM-DD' format
        top: The number of top companies is returned
        desc: Return dataframe in descending order if True, return dataframe in ascending order if False
        get_all: Return the whole companies with market cap in specified time group by industry
    """
    date = date_available(date)
    df_market = data
    df_market = df_market[df_market[date] != 0]
    if get_all == False:
        if desc == True:
            order = False
        else:
            order = True  
        industry_info = [
            df_market[
                df_market['Industry']==industry][['Symbol','Name','Company','Industry',date]]\
                    .sort_values(by=date,ascending=order).head(top)\
                        for industry in df_market['Industry'].unique()
            ]
        df = pd.concat(industry_info).reset_index(drop=True)
    else:
        df = df_market[['Symbol','Name','Company','Industry',date]].sort_values(by='Industry').reset_index(drop=True)

    df.rename(columns={date:'MarketCap'},inplace=True)
    
    if industry == 'all':
        return df
    
    return df[df['Industry'] == industry]

def greater_price(data,week=52,date='2021-09-24'):
    """
    Return dataframe of companies have price above the specified week mark
    Parameters: 
        data: dataframe from full_marketcap_price function
        week: Number of weeks is selected as the mark
        date: 'YYYY-MM-DD' format, date is selected for comparision
    """
    from datetime import datetime as dt
    from datetime import timedelta as delta
    
    date = date_available(date)
    
    df_price = data
    df_price = df_price[df_price[date] != 0]

    compare_tail = dt.strftime((dt.strptime(date,'%Y-%m-%d') - delta(days=1)),'%Y-%m-%d')
    compare_head = dt.strftime((dt.strptime(compare_tail,'%Y-%m-%d') - delta(weeks=week)),'%Y-%m-%d')
    
    tail_available = date_available(compare_tail)
    head_available = date_available(compare_head)

    df = df_price.loc[:,head_available:tail_available]
    df['Max Price'] = df.max(axis=1)
    df = df_price[['Symbol','Name','Company','Industry']].join(df)
    df = df.join(df_price[date])
    df = df[(df[date] > df['Max Price'])].reset_index(drop=True)
    df['Difference'] = df[date]-df['Max Price']

    return df


if __name__ == "__main__":
    data_market = full_marketcap_price(data='market')
    data_price = full_marketcap_price(data='price')
    # print(profit_comparision(data=data_price,before='2021-08-06',after='2021-09-24',top=10, desc= True))
    # print(profit_comparision(data=data_price,before='2020-02-11',after='2021-09-24',top=10,desc=False))
    print(greater_price(data=data_price,week=52,date='2021-09-24'))
    # print(top_industry_marketcap(data=data_market,date='2021-09-24',top=5,desc=True,industry='all'))
    # print(top_industry_marketcap(data=data_market,date='2021-09-24',get_all=True))
    # print(data_price)
    
    
