
from logging import error
from numpy import true_divide
import pandas as pd
import datetime as dt
import pandas_ta as ta
import streamlit as st
import schedule
import yahoo_fin.stock_info as si
from functools import reduce
import time

# @st.cache(allow_output_mutation=True)
def stock_list():
    stock_list = list(pd.read_excel('stocks_list.xlsx', sheet_name='stocks_list')['Symbol'])[100:110] 
    
    return stock_list

symbols = stock_list()

def stock_live_data():
    for ticker in symbols:
        try:
            data = st.write(ticker, si.get_live_price(ticker))
        except:
            st.write(f'error with stock {ticker}')
            continue
    return data



schedule.every(10).seconds.do(stock_live_data)
while True:
    schedule.run_pending()
    time.sleep(1)