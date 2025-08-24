# Import packages
import pandas as pd
import yfinance as yf
import streamlit as st
from datetime import datetime
import numpy as np

# Header
st.header("Equity Resistance-Support Levels")

script = pd.read_csv('nifty500.csv')

script = st.multiselect("Select Script : ",options=script['Tickers'],
                        default=None,
                        max_selections=1)

st.write("Select Data Window")
col1,col2 = st.columns(spec=2)
formatted_start = col1.date_input("From : [inclusive]")
formatted_end = col2.date_input("To : [exclusive]")

day_diff = (formatted_end-formatted_start).days

if day_diff>=365:
    st.write("Reduce data window to less than 365 days")
    st.stop()
else:
    pass

timeframe = st.radio(label="Select timeframe : ",options=['1d','60m','15m','5m'])

start = datetime.strftime(formatted_start,format="%Y-%m-%d")
end = datetime.strftime(formatted_end,format="%Y-%m-%d")

df = yf.download(tickers=script,
                 start=start,
                 end=end,
                 multi_level_index=False,
                 interval=timeframe,
                 ignore_tz=True)

df.drop('Volume',axis=1,inplace=True)

text2 = """
Say 
1. Price is 768 and you select nearest 5
2. 768 is converted to 770
3. and so on for the rest of the multiples
"""
nearest = st.radio("Select price level multiple of : ",options=[5,10,25,50,100],
                   help = text2,
                   label_visibility='visible')    

for i in df:
    df[i] = round(df[i]/nearest)*nearest

text = """
1. Selcting Low will give you support levels
2. Selecting High will give you resistance levels
3. Selecting Close will give you significant levels with its classification on both side of
CMP
"""
olhc = st.radio("Select OLHC : ", options=['Levels','Supports','Resistances'],
                help=text,
                label_visibility='visible')

d = {'Levels' : 'Close'
    ,'Supports' : 'Low',
     'Resistances' : 'High'}

data = df[d[olhc]].value_counts().reset_index()

l1 = np.percentile(data['count'],25)
l2 = np.percentile(data['count'],50)
l3 = np.percentile(data['count'],75)

def classes(i):
    if i <= l1:
        return 'WEAK'
    elif i>l1 and i<=l2:
        return "MODERATE"
    elif i>l2 and i<=l3:
        return "STRONG"
    else:
        return "POWERFUL"
    
data['Class'] = data['count'].apply(classes)

current_price = df[d[olhc]].iloc[-1]

if olhc == 'Supports':
    data = data[data['Low']<current_price]
elif olhc == 'Resistances':
    data = data[data['High']>current_price]
else :
    pass

text3 = """
1. This show how important the level is.
2. This level can be resistance,support [based on viz. high and low] 
3. or just a level[based on close].
"""
significance = st.multiselect(label='Select significance : ',
                                options=['WEAK','MODERATE','STRONG','POWERFUL'],
                                default='POWERFUL',
                                help = text3,
                                label_visibility='visible')

if st.button("SUBMIT"):
    st.subheader("RESULTS",divider=True)
    data = data[data['Class'].isin(significance)]
    st.write(data)
