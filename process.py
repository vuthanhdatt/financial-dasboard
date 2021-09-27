import pandas as pd
import numpy as np
import config
import warnings
warnings.filterwarnings("ignore")

def clean_marketcap_price(data='market'):
    """
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
        if missing_col[col] < 30:
            df[col].fillna(method='bfill',inplace=True)
        else:
            df[col].fillna(value=0,inplace=True)

    return df

def full_marketcap_price(data='market'):
    """
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
    else:
        return 'Dataset not found.'

    return df

if __name__ == "__main__":
    # print(full_marketcap_price(data='price'))
    pass