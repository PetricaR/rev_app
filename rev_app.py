import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
try:
    sys.path.remove(str(parent))
except ValueError: # Already removed
    pass

# Python packages
import sys
import pandas as pd
import numpy as np
import streamlit as st
from streamlit import dataframe, stop
from datetime import datetime, date
import math
import yfinance as yf
import time
import pandas_ta as ta




# GET STOCK LIST
##################################################################################################################################
st.sidebar.header('VIEW STOCKS')
st.header('REVOLUT STOCKS LIST')

# Market title web page:
@st.cache(allow_output_mutation=True)
def stock_list():
    stock_list = pd.read_excel('stocks_list.xlsx', sheet_name='stocks_list')        
    return stock_list

# View stocks list
stocks = stock_list()
stocks_company_name = stocks['Company name'].unique()
stocks_symbols = stocks['Symbol'].unique()
stocks_sector = stocks['Sector'].unique()
stocks_industry = stocks['Industry'].unique()

##################################################################################################################################
# # Selection stocks by company name
##################################################################################################################################
# checkbox_company_name = st.sidebar.checkbox('Stocks by company name:', key='checkbox_company_name')


# def selection_stocks_by_names():
#     try:
#         st.text('Stocks selected by name')
#         if checkbox_company_name:
#             stocks_filter_by_name = st.sidebar.multiselect('Name:', stocks_company_name)
#             if stocks_filter_by_name:
#                 stocks_selected_by_stocks_names = stocks[(stocks['Company name'].isin(stocks_filter_by_name))]
#             else:
#                 st.warning('Please select a name')
#         else:
#             st.warning('Please select a name')
#     except UnboundLocalError:
#         st.warning('Please select a name')
        
#     return stocks_selected_by_stocks_names

# final_stocks_selection = selection_stocks_by_names()
##################################################################################################################################
def selection_stocks_by_names():
    try:
        st.text('Stocks selected by name')
        stocks_selected_by_stocks_names = stocks[(stocks['Company name'].isin(stocks_filtered_by_name))]
        stocks_selected_by_stocks_names
    except:
        st.warning('Please select a name')
    return stocks_selected_by_stocks_names

##################################################################################################################################
checkbox_company_name = st.sidebar.checkbox('Stocks by company name:', key='checkbox_company_name')
if checkbox_company_name:
    stocks_filtered_by_name = st.sidebar.multiselect('Name:', stocks_company_name)
    if stocks_filtered_by_name:
        stocks_selected_by_stocks_names = selection_stocks_by_names()
          


# # Download stock data
##################################################################################################################################
def get_data(tickers,  *args, **kwargs):
    try:
        data = yf.download(tickers,  # or pdr.get_data_yahoo(...
                # tickers list or string as well
                # tickers = "PATH",

                # use "period" instead of start/end
                # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                # (optional, default is '1mo')
                period = "1d",

                # fetch data by interval (including intraday if period < 60 days)
                # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                # (optional, default is '1d')
                interval = "15m",

                # group by ticker (to access via data['SPY'])
                # (optional, default is 'column')
                group_by = 'ticker',

                # adjust all OHLC automatically
                # (optional, default is False)
                auto_adjust = True,

                # download pre/post regular market hours data
                # (optional, default is False)
                prepost = True,

                # use threads for mass downloading? (True/False/Integer)
                # (optional, default is True)
                threads = True,

                # proxy URL scheme use use when downloading?
                # (optional, default is None)
                proxy = None
            )
        
                     
    except (KeyError, ValueError, UnboundLocalError): 
        st.warning('No stock has been selected')  
    
        
    return data




def get_live_data():
    company_names = stocks_selected_by_stocks_names['Company name'].values
    company_symbols = stocks_selected_by_stocks_names['Symbol'].values
    for name, symbol in zip(company_names, company_symbols):
        try:
            stocks_final = get_data(symbol)
            timestamp = get_data(symbol).index[-1]
            stocks_final['RSI'] = stocks_final.ta.rsi()
            # stocks_final
            
            if stocks_final['RSI'][-1] < 30:
                stocks_final['recommndation'] = "buy"
            elif stocks_final['RSI'][-1]  > 70:
                stocks_final['recommndation'] = "sell"
            else:
                stocks_final['recommndation'] = "neutral"
            
            st.write("|", timestamp, "|", name, "-", symbol,  "|", "Price = ", stocks_final['close'][-1],
                     "|", "RSI = ", stocks_final['RSI'][-1], "||", stocks_final['recommndation'][-1])
        
        except:
            st.write(f'error with stock {name, symbol}')
            continue
        
    return stocks_final



t3 = 0
period3 = 60 #seconds do function3() every minute
sleep_seconds = 1   # or whatever makes sense

with st.form(key='final_stocks'):
    submit_button = st.form_submit_button(label='Select your final stock list')
    if submit_button:
        while True:
            t = time.time()
            if t - t3 >= period3:
                stock_live_data = get_live_data()
                t3 = time.time()
            time.sleep(sleep_seconds)
        
 





