from os import write
import sys
from pathlib import Path

from pkg_resources import resource_listdir
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
import yfinance as yf
import time
import pandas_ta as ta
import schedule



# GET STOCK LIST
##################################################################################################################################
st.sidebar.header('REVOLUT STOCKS SCANNER')
st.header('REVOLUT STOCKS LIST')

# Market title web page:
# @st.cache(allow_output_mutation=True)
def stock_list_excel():
    stock_list_excel = pd.read_excel('stocks_list.xlsx', sheet_name='stocks_list')
    return stock_list_excel

stocks_sellection = stock_list_excel()
##################################################################################################################################
st.sidebar.subheader('Stock interval')
# Period selection
valid_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y' , '5y', '10y', 'ytd' , 'max']
period_selection = st.sidebar.selectbox('Period:', valid_periods, key='period_selection', index=4)

# Interval selection
valid_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d' , '1wk', '1mo', '3mo']
interval_selection = st.sidebar.selectbox('Interval:', valid_intervals, key='interval_selection', index=8)

# Schedule time:
schedule_time = st.sidebar.number_input(label="Schedule time:",
                                        min_value=1,
                                        max_value=3600,
                                        step=1,
                                        value=1,
                                        )
##################################################################################################################################

##################################################################################################################################
st.sidebar.subheader('Stock selection')


# # Stock selection
stoc_selection_list = st.sidebar.radio('Selection mode:', options=("Revolut stocks", "Personal portfolio"), index=0)

def stock_select_mode():
    
    if stoc_selection_list=="Revolut stocks":    
        stocks_final = stocks_sellection.copy()
        stocks_final
        return stocks_final

    elif stoc_selection_list=="Personal portfolio" :
        st.text('Stocks selected by name')
        stocks_company_name = stocks_sellection['Company name'].unique()
        stocks_filtered_by_name = st.multiselect('Company name:', stocks_company_name)
        if stocks_filtered_by_name:
            stocks_final = stocks_sellection[(stocks_sellection['Company name'].isin(stocks_filtered_by_name))]
            stocks_final
            return stocks_final
        else:
            
            st.warning('Please select a stock')
            
stocks_final = stock_select_mode()



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
        
        data['RSI'] = data.ta.rsi(inplace=True) # Calculate RSI
        data['SMA'] = data.ta.sma(inplace=True)
        data[['MACD_12_26_9', 'MACDh_12_26_9', 'MACDs_12_26_9']] = data.ta.macd(inplace=True)
        data['Symbol'] = tickers
        #data['timestamp'] = data.index[-1]   #Get timestamp
                
    except (KeyError, ValueError, UnboundLocalError): 
        st.warning('No stock has been selected')  
        
    return data

def color_negative_red(val):
    color = 'red' if val < 30 else 'green'
    return 'color: %s' % color



##################################################################################################################################
def rsi_live():
    company_names = stocks_final['Company name'].values
    company_symbols = stocks_final['Symbol'].values
    for name, symbol in zip(company_names, company_symbols):
    
    
        try: 
            stocks_data = yahoo_data(symbol).iloc[-1:].style.applymap(color_negative_red, subset=['RSI']) #Get data
            stocks_data
            # results = st.write(stocks_data)
            
            # if stocks_data['RSI'][-1] < 50 and stocks_data['RSI'][-1] > 30:
            #     stocks_data['recommndation'] = "bearish downtrend"
            # elif stocks_data['RSI'][-1] < 30:
            #     stocks_data['recommndation'] = "buy - cheap stock"
            # elif stocks_data['RSI'][-1] > 50 and stocks_data['RSI'][-1] < 70:
            #     stocks_data['recommndation'] = "bullish uptrend"        
            # elif stocks_data['RSI'][-1] > 70:
            #     stocks_data['recommndation'] = "sell - expensive stock"
            # else:
            #     stocks_data['recommndation'] = "neutral"
            
            
            # # Write recommandation
            # results = st.write(
            #     "|", stocks_data['timestamp'][-1], "|", name, "-", symbol,
            #     "|", "Price = ", stocks_data['close'][-1],
            #     "|", "RSI = ", stocks_data['RSI'][-1], 
            #     "|", "MACD_12_26_9 = " , stocks_data['MACD_12_26_9'][-1],
            #     "|", "MACDh_12_26_9 = " , stocks_data['MACDh_12_26_9'][-1],
            #     "|", "MACDs_12_26_9 = " , stocks_data['MACDs_12_26_9'][-1],
            #     "|", "Stock recommandation => ", stocks_data['recommndation'][-1])
 
            
                
        except:
            st.write(f'error with stock {name, symbol}')
            continue
        
        #st.write('The End')
        #st.stop()
        
    return stocks_data

##################################################################################################################################
with st.form(key='final_stocks'):
   
    stock_data_button = st.form_submit_button(label='Get stocks data')
    if stock_data_button:
        schedule.every(schedule_time).minutes.do(rsi_live)
        while True:
            schedule.run_pending()
            time.sleep(1)
        else:
            st.stop()
            

        







