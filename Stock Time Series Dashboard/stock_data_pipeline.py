import os
import pandas as pd
import yfinance as yf

ticker = ["AAPL","TSLA","^NSEI"]


def update_stock_csv(ticker,filepath = "Stock_data.csv"):

    if not os.path.exists(filepath):
        ticker = ["AAPL","TSLA","^NSEI"]
        data = yf.download(ticker,period = '1y',interval = '1d')
        data.columns = [f"{col[1]}.{col[0]}" for col in data.columns]
        data.to_csv("Stock_data.csv", index_label='Date')
        return data
    
    existing_index = pd.read_csv(filepath,usecols=[0],parse_dates=[0],index_cols=[0])

    if existing_index.empty:
        ticker = ["AAPL","TSLA","^NSEI"]
    
        data = yf.download(ticker,)
        data.columns = [f"{col[1]}.{col[0]}" for col in data.columns]
        data.to_csv("Stock_data.csv", index_label='Date')
        return data
    
    last_date = existing_index.index.max()
    new_data = yf.download(ticker,start = last_date)
    new_data = new_data[new_data.index>last_date]

    if new_data.empty:
        return pd.read_csv(filepath, parse_dates=[0],index_col=[0])
     
    
    new_data.to_csv(filepath,mode ="a",header=False)
    
    return pd.read_csv(filepath,parse_dates=[0],index_col=[0])

update_stock_csv