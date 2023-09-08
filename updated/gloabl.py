import streamlit as st
from css import get_custom_css

st.set_page_config(layout="wide", page_icon="🌨")
PAGES = { 
           "Hi There": 0,
           "Data": 1,
           "Dashboard": 2
         }

st.markdown(get_custom_css(), unsafe_allow_html=True)
storage_cost_per_tb = 0.023  
cost_per_node_per_hour = 3.00
YOUTUBE_API_KEY = 'AIzaSyD55GaZk1Ggv9TFaONa4-Z4eGnaN23cGN0'  
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
roles=["ACCOUNTADMIN","SYSADMIN","SECURITYADMIN","USER", "PUBLIC", "ORGADMIN"]
