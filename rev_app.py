from os import write
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
from alpha_vantage.techindicators import TechIndicators




# GET STOCK LIST
##################################################################################################################################
st.sidebar.header('REVOLUT STOCKS SCANNER')
st.header('REVOLUT STOCKS LIST')

# Market title web page:
@st.cache(allow_output_mutation=True)
def stock_list():
    stock_list = pd.read_excel('stocks_list.xlsx', sheet_name='stocks_list')        
    return stock_list


##################################################################################################################################
st.sidebar.subheader('Stock data')
# Period selection
valid_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y' , '5y', '10y', 'ytd' , 'max']
period_selection = st.sidebar.selectbox('Period:', valid_periods, key='period_selection', index=4)

#Interval selection
valid_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d' , '1wk', '1mo', '3mo']
interval_selection = st.sidebar.selectbox('Interval:', valid_intervals, key='interval_selection', index=8)
##################################################################################################################################

##################################################################################################################################
st.sidebar.subheader('Stock selection')
# Stock selection
stock_selection_option = ['Company name',
                          'Company sector',
                          'Company industry',
                          'Revolut stocks',
                          'Personal portfolio']

stoc_selection_list = st.sidebar.selectbox('Selection mode:', stock_selection_option, key='1')
##################################################################################################################################

##################################################################################################################################
def stocks_selections():
    # View stocks list
    stocks = stock_list()
    # Filters
    stocks_company_name = stocks['Company name'].unique()
    stocks_company_symbol = stocks['Symbol'].unique()
    stocks_company_sector = stocks['Sector'].unique()
    stocks_company_industry = stocks['Industry'].unique()
        
    if stoc_selection_list == 'Company name':    
        st.text('Stocks selected by name')
        stocks_filtered_by_name = st.sidebar.multiselect('Company name:', stocks_company_name)
        if stocks_filtered_by_name:
            stocks = stocks[(stocks['Company name'].isin(stocks_filtered_by_name))]
            stocks
            return stocks
        
    elif stoc_selection_list == 'Company sector':    
        st.text('Stocks selected by sector')
        stocks_filtered_by_sector = st.sidebar.multiselect('Company sector:', stocks_company_sector)
        if stocks_filtered_by_sector:
            stocks = stocks[(stocks['Sector'].isin(stocks_filtered_by_sector))]
            stocks 
            return stocks 
    
    elif stoc_selection_list == 'Company industry':    
        st.text('Stocks selected by industry')
        stocks_filtered_by_industry = st.sidebar.multiselect('Company industry:', stocks_company_industry)
        if stocks_filtered_by_industry:
            stocks = stocks[(stocks['Industry'].isin(stocks_filtered_by_industry))]
            stocks
            return stocks  
    
    elif stoc_selection_list == 'Revolut stocks':    
        st.text('All Revolut Stocks')
        if stoc_selection_list:
            stocks
            return stocks
    
    elif stoc_selection_list == 'Personal portfolio':    
        st.text('Personal portfolio Stocks')        
            
            
    else:
        st.warning('Please load data')
        
    return stocks

stocks_selection = stocks_selections()
#################################################################################################################################

#Tehnical indicators
##################################################################################################################################
st.sidebar.subheader('Tehnical indicators')
indicators = ['RSI', 'MACD']
tehnical_indicators = st.sidebar.multiselect('Interval:', indicators, key='tehnical_indicators')

# Download yahoo data
##################################################################################################################################
def yahoo_data(tickers,  *args, **kwargs):
    try:
        data = yf.download(tickers,  # or pdr.get_data_yahoo(...
                
                period = period_selection,

                # fetch data by interval (including intraday if period < 60 days)
                # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                # (optional, default is '1d')
                interval = interval_selection,

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
        
        #data['RSI'] = data.ta.rsi()
                     
    except (KeyError, ValueError, UnboundLocalError): 
        st.warning('No stock has been selected')  
        
    return data


##################################################################################################################################
def rsi_live():
    company_names = stocks_selection['Company name'].values
    company_symbols = stocks_selection['Symbol'].values
    for name, symbol in zip(company_names, company_symbols):
        try:
            
            stocks = yahoo_data(symbol) #Get data
            stocks['RSI'] = stocks.ta.rsi() # Calculate RSI
            timestamp = yahoo_data(symbol).index[-1] #Get timestamp
            
            # Make recommandation
            if stocks['RSI'][-1] < 30:
                stocks['recommndation'] = "buy"
            elif stocks['RSI'][-1]  > 70:
                stocks['recommndation'] = "sell"
            else:
                stocks['recommndation'] = "neutral"
            
            # Write recommandation
            st.write("|", timestamp, "|", name, "-", symbol,  "|", "Price = ", stocks['close'][-1],
                     "|", "RSI = ", stocks['RSI'][-1], "||", stocks['recommndation'][-1])
                
        except:
            st.write(f'error with stock {name, symbol}')
            continue
        
        
    return stocks



t3 = 0
period3 = 60 #seconds do function3() every minute
sleep_seconds = 1   # or whatever makes sense

with st.form(key='final_stocks'):
    submit_button = st.form_submit_button(label='Get stocks data')
    if submit_button:
        while True:
            t = time.time()
            if t - t3 >= period3:
                stock_live_data = rsi_live()
                t3 = time.time()
            time.sleep(sleep_seconds)







