import streamlit as st

st.set_page_config("HOME")

st.header("Equity Support and Resistances",width='content')

text1 = """
1. This application gives analysis for NIFTY 500 equity stocks.
2. This application gives 
    2.1 Support Levels
    2.2 Resistance Levels
    2.3 Significance Levels (Most traded levels)
for a selected data window
"""
st.text(text1)

if st.button("Application >>"):
    st.switch_page('pages/1_App.py')