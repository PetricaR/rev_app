# stock_selection_option = ['Company name',
#                           'Company sector',
#                           'Company industry',
#                           'Revolut stocks',
#                           'Personal portfolio']

# stoc_selection_list = st.sidebar.selectbox('Selection mode:', stock_selection_option, key='1')
##################################################################################################################################

##################################################################################################################################
# def stocks_selections():
#     # View stocks list
#     stocks = stock_list()
#     # Filters
#     stocks_company_name = stocks['Company name'].unique()
#     stocks_company_symbol = stocks['Symbol'].unique()
#     stocks_company_sector = stocks['Sector'].unique()
#     stocks_company_industry = stocks['Industry'].unique()
        
#     if stoc_selection_list == 'Company name':    
#         st.text('Stocks selected by name')
#         stocks_filtered_by_name = st.sidebar.multiselect('Company name:', stocks_company_name)
#         if stocks_filtered_by_name:
#             stocks = stocks[(stocks['Company name'].isin(stocks_filtered_by_name))]
#             stocks
#             return stocks
        
#     elif stoc_selection_list == 'Company sector':    
#         st.text('Stocks selected by sector')
#         stocks_filtered_by_sector = st.sidebar.multiselect('Company sector:', stocks_company_sector)
#         if stocks_filtered_by_sector:
#             stocks = stocks[(stocks['Sector'].isin(stocks_filtered_by_sector))]
#             stocks 
#             return stocks 
    
#     elif stoc_selection_list == 'Company industry':    
#         st.text('Stocks selected by industry')
#         stocks_filtered_by_industry = st.sidebar.multiselect('Company industry:', stocks_company_industry)
#         if stocks_filtered_by_industry:
#             stocks = stocks[(stocks['Industry'].isin(stocks_filtered_by_industry))]
#             stocks
#             return stocks  
    
#     elif stoc_selection_list == 'Revolut stocks':    
#         st.text('All Revolut Stocks')
#         if stoc_selection_list:
#             stocks
#             return stocks
    
#     elif stoc_selection_list == 'Personal portfolio':    
#         st.text('Personal portfolio Stocks')        
            
            
#     else:
#         st.warning('Please load data')
        
#     return stocks


#################################################################################################################################

#Tehnical indicators
##################################################################################################################################
# st.sidebar.subheader('Tehnical indicators')
# indicators = ['RSI', 'MACD']
# tehnical_indicators = st.sidebar.multiselect('Interval:', indicators, key='tehnical_indicators')