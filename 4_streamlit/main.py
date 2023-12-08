import pandas as pd
import os
import geopandas as gpd
import glob
import plotly.express as px
import plotly.graph_objects as go
# import folium
import json
# import math
import streamlit as st
from datetime import datetime

from st_files_connection import FilesConnection
from PIL import Image

# 웹 페이지의 기본 설정
st.set_page_config(
    page_title="홍예준 PortfFolio",
    page_icon="🎅",
    layout="wide",
    initial_sidebar_state="expanded"
)

conn = st.connection('s3', type=FilesConnection)

# conn = st.experimental_connection('s3', type=FilesConnection)

@st.cache_data(ttl=3600)
def read_file_csv(filename):
  df = conn.read(filename, input_format="csv", ttl=600)
  return df 
@st.cache_data(ttl=3600)
def read_file_json(filename):
  df = conn.read(filename, input_format="json", ttl=600)
  return df

# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
sig_list = ['서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', '대전광역시', '울산광역시',
       '세종특별자치시', '경기도', '강원도', '충청북도', '충청남도', '전라북도', '전라남도', '경상북도',
       '경상남도', '제주특별자치도']

type_list = ["아파트", "오피스텔"]
type_dic = {'아파트':'apt', '오피스텔':'offi'}
trade_list = ['매매','전세','월세']  
trade_days = ['202101','202102','202103','202104','202105','202106',
              '202107','202108','202109','202110','202111','202112']

sig_area = st.sidebar.selectbox(
    "시군구 선택",
    sig_list
)

type_option = st.sidebar.selectbox(
    "아파트/오피스텔 선택",
    type_list
)

trade_option = st.sidebar.selectbox(
    '거래 타입 선택',
    trade_list
)  

trade_month = st.sidebar.selectbox(
    '거래 월 선택',
    trade_days
)

type_cd = type_dic[type_option]

df_trade = read_file_csv(f'real-estate555-bucket/0_data/streamlit_data/{type_cd}_trade/{type_cd}_trade_{trade_month}.csv')
df_rent = read_file_csv(f'real-estate555-bucket/0_data/streamlit_data/{type_cd}_rent/{type_cd}_rent_{trade_month}.csv')

df_trade = df_trade[df_trade['시도명'] == sig_area]
df_rent = df_rent[df_rent['시도명'] == sig_area]

# df_trade['사용승인일'] = 2021 - df_trade['건축년도']
# df_rent['사용승인일'] = 2021 - df_rent['건축년도']

# st.text(df_trade[['사용승인일','건축년도']])
# st.text(df_rent[['사용승인일','건축년도']])

st.title("부동산 대시보드")

st.text(df_trade)
st.text(df_rent)
