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
#from bokeh.plotting import figure
#import sqlalchemy
#import sqlite3
import yfinance as yf
import schedule
from schedule import every, repeat, run_pending
import time


# GET STOCK LIST
##################################################################################################################################
st.sidebar.header('VIEW STOCKS')
st.header('REVOLUT STOCKS LIST')

# Market title web page:
@st.cache(allow_output_mutation=True)
def stock_list():
    stock_list = pd.read_excel(r'01_STOCK_LIST\stocks_list.xlsx',
                                   sheet_name='stocks_list')        
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
          
          

##################################################################################################################################
# # Selection stocks by company sector
##################################################################################################################################
def selection_stocks_by_sector():
    try:
        st.text('Stocks selected by sector')
        stocks_selected_by_stocks_sector = stocks[(stocks['Sector'].isin(stocks_filtered_by_sector))]
        stocks_selected_by_stocks_sector
    except:
        st.warning('Please select a sector')
    return stocks_selected_by_stocks_sector

##################################################################################################################################
checkbox_company_sector = st.sidebar.checkbox('Stocks by company sector:', key='checkbox_company_sector')
if checkbox_company_sector:
    stocks_filtered_by_sector = st.sidebar.multiselect('Sector:', stocks_sector)
    if stocks_filtered_by_sector:
        stocks_selected_by_stocks_sector = selection_stocks_by_sector()
          
          
          
##################################################################################################################################
# # Selection stocks by company industry
##################################################################################################################################
def selection_stocks_by_industry():
    try:
        st.text('Stocks selected by industry')
        stocks_selected_by_stocks_industry = stocks[(stocks['Industry'].isin(stocks_filtered_by_industry))]
        stocks_selected_by_stocks_industry
    except:
        st.warning('Please select an industry')
    return stocks_selected_by_stocks_industry

##################################################################################################################################
checkbox_company_industry = st.sidebar.checkbox('Stocks by company industry:', key='checkbox_company_industry')
if checkbox_company_industry:
    stocks_filtered_by_industry = st.sidebar.multiselect('Industry:', stocks_industry)
    if stocks_filtered_by_industry:
        stocks_selected_by_stocks_industry = selection_stocks_by_industry()


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
                interval = "1m",

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
        
        delta = data['Close'].diff()
        up = delta.clip(lower=0)
        down = -1*delta.clip(upper=0)
        ema_up = up.ewm(com=13, adjust=False).mean()
        ema_down = down.ewm(com=13, adjust=False).mean()
        rs = ema_up/ema_down
        data['RSI'] = 100 - (100/(1 + rs))  
        data
               
    except (KeyError, ValueError, UnboundLocalError): 
        st.warning('No stock has been selected')  
    
        
    return data


def get_live_data():
    company_names = stocks_selected_by_stocks_names['Company name'].values
    company_symbols = stocks_selected_by_stocks_names['Symbol'].values
    for name, symbol in zip(company_names, company_symbols):
        st.write(name, " | ", symbol)
        stocks_final = get_data(symbol)
    
    return stocks_final

import time
t3 = 0
period3 = 60.0 # do function3() every minute
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
        
     
# while True:
#          

# # Using the "with" syntax
# with st.form(key='final_stocks'):
#     submit_button = st.form_submit_button(label='Select your final stock list')
#     if submit_button:
#         stocks_selected_by_stocks_names = selection_stocks_by_names()
#         company_names = stocks_selected_by_stocks_names['Company name'].values
#         company_symbols = stocks_selected_by_stocks_names['Symbol'].values
#         for name, symbol in zip(company_names, company_symbols):
#            st.write(name, " | ", symbol)
#            stocks_final = get_data(symbol)
        

# schedule.every(10).seconds.do(get_data, symbol)
# while True:
#     schedule.run_pending()
#     time.sleep(1)        


# def stocks_with_rsi():
#     st.header('Final Stocks Selection')
#     company_names = stocks_selected_by_stocks_names['Company name'].values
#     company_symbols = stocks_selected_by_stocks_names['Symbol'].values
#     for name, symbol in zip(company_names, company_symbols):
#         st.write(name, " | ", symbol)
#         stocks_final = get_data(symbol)
#         delta = stocks_final['Close'].diff()
#         up = delta.clip(lower=0)
#         down = -1*delta.clip(upper=0)
#         ema_up = up.ewm(com=13, adjust=False).mean()
#         ema_down = down.ewm(com=13, adjust=False).mean()
#         rs = ema_up/ema_down
#         stocks_final['RSI'] = 100 - (100/(1 + rs))  
#         stocks_final

#     return stocks_final















##################################################################################################################################
# STOCK CONCATENATION
##################################################################################################################################
# if checkbox_company_name & checkbox_company_sector & checkbox_company_industry:
#     st.subheader('Select final stocks')
#     if stocks_filtered_by_name & stocks_filtered_by_industry & stocks_filtered_by_sector:
#         stocks_final = pd.concat([stocks_selected_by_stocks_names, stocks_selected_by_stocks_sector, stocks_selected_by_stocks_industry])




        
    # elif stocks_filtered_by_sector & stocks_filtered_by_industry:
    #     stocks_final = pd.concat([stocks_selected_by_stocks_sector, stocks_selected_by_stocks_names])

    # elif stocks_filtered_by_name & stocks_filtered_by_industry:
    #     stocks_final = pd.concat([stocks_selected_by_stocks_names, stocks_selected_by_stocks_industry]) 

    # elif stocks_filtered_by_name & stocks_selected_by_stocks_sector:
    #     stocks_final = pd.concat([stocks_selected_by_stocks_names, stocks_selected_by_stocks_sector])

    # elif stocks_filtered_by_sector:
    #     stocks_final = pd.concat([stocks_selected_by_stocks_sector])

    # elif stocks_filtered_by_industry: 
    #     stocks_final = pd.concat([stocks_selected_by_stocks_industry])  

    # else:
    #     stocks_final = pd.concat([stocks_selected_by_stocks_names])
    
    # stocks_final = stocks_final.drop_duplicates(subset = ["Symbol"])
    # stocks_final
    # return stocks_final



# # Using the "with" syntax
# with st.form(key='final_stocks'):
#     submit_button = st.form_submit_button(label='Select your final stock list')
#     if submit_button:
#         stocks_data = stock_concat()


