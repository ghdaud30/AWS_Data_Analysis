import pandas as pd
import os
import geopandas as gpd
import glob
import plotly.express as px
import plotly.graph_objects as go
import folium
import json
import math
import boto3
import vis_func
import streamlit as st
from datetime import datetime

from st_files_connection import FilesConnection
from PIL import Image


st.set_page_config(
    page_title="아파트 대시보드",
    page_icon="🏬",
    layout="wide",
    initial_sidebar_state="expanded"
)

conn = st.connection('s3', type=FilesConnection)

@st.cache_data(ttl=3600)
def read_file_csv(filename):
  df = conn.read(filename, input_format="csv", ttl=600)
  return df 
@st.cache_data(ttl=3600)
def read_file_json(filename):
  df = conn.read(filename, input_format="json", ttl=600)
  return df

s3 = boto3.resource('s3')

# s3에서 이미지 가져오는 함수
def read_image_s3(filename):
    bucket = s3.Bucket('real-estate555-bucket')
    object = bucket.Object(filename)
    response = object.get()
    file_stream = response['Body']
    img = Image.open(file_stream)
    return img

# with open('4_streamlit/style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
  
type_option = 'apt'

sig_list = ['서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', '대전광역시', '울산광역시',
       '세종특별자치시', '경기도', '강원도', '충청북도', '충청남도', '전라북도', '전라남도', '경상북도',
       '경상남도', '제주특별자치도']

sig_area = st.sidebar.selectbox(
    "시군구 선택",
    sig_list
)

year_list = [2021]
year_option = st.sidebar.selectbox(
 'year',
 year_list
)

month_list = range(1,13)
month_option = st.sidebar.selectbox(
 'month',
 month_list
)

st.title('AWS 서버를 활용한 부동산 거래 정보') 
st.subheader(f'{sig_area} 아파트 거래 정보(2021년)')
st.markdown("---")

# trade_count_df = read_file_csv('real-estate555-bucket/0_data/streamlit_data/trade_count.csv')
vis_trade_rent_df = read_file_csv('real-estate555-bucket/0_data/streamlit_data/vis_trade_rent.csv')
# apart_trans4 = read_file_csv('real-estate555-bucket/0_data/streamlit_data/map_csv.csv')
# sig_lat_lon = read_file_csv('real-estate555-bucketreal-estate555-bucket/0_data/streamlit_data/sig_lat_lon.csv')

geo_json = read_file_json(f'real-estate555-bucket/0_data/streamlit_data/geo_sig_{sig_area}_json.geojson')

# 막대그래프 seaborn
vis_trade_rent1 = vis_func.vis_trade_rent(vis_trade_rent_df,
                          type_option,
                          sig_area,
                          year_option,
                          month_option)
# plotly
vis_trade_rent2 = vis_func.vis_trade_rent2(vis_trade_rent_df,
                          type_option,
                          sig_area,
                          year_option,
                          month_option)

# 2021년 월에 따른 지역별 부동산 실거래가 평균
trade_mean_month = vis_func.trade_mean_month(vis_trade_rent_df,
                          type_option,
                          sig_area)
# 실거래가
trade_mean = vis_func.trade_mean(vis_trade_rent_df,
                          type_option,
                          sig_area)
# 2021년 월에 따른 지역별 부동산 거래량 평균
trade_count_month = vis_func.trade_count_month(vis_trade_rent_df,
                          type_option,
                          sig_area)
# 거래량
trade_count = vis_func.trade_mean(vis_trade_rent_df,
                          type_option,
                          sig_area)

col, col2 = st.columns([1,1])
col.pyplot(vis_trade_rent1, use_container_width = True) 
col2.plotly_chart(vis_trade_rent2, use_container_width = True)

col3, col4 = st.columns([1,1])
col3.pyplot(trade_mean_month, use_container_width = True) 
col4.plotly_chart(trade_mean, use_container_width = True)

col4, col5 = st.columns([1,1])
col4.pyplot(trade_count_month, use_container_width = True) 
col5.plotly_chart(trade_count, use_container_width = True)


# trade_count1 = vis_func.trade_count(trade_count_df,
#                           type_option,
#                           sig_area)

# trade_mean1 = vis_func.trade_mean(trade_count_df,
#                           type_option,
#                           sig_area)
                          
                          
                          
# trade_mean_map1 = vis_func.trade_mean_map(apart_trans4,
#                           geo_json_seoul,
#                           sig_lat_lon,
#                           sig_area, 
#                           type_option)

# col1, col2 = st.columns([1,1])
# col1.plotly_chart(trade_mean1, use_container_width = True)
# col2.plotly_chart(trade_count1, use_container_width = True)

st.sidebar.markdown(
    """
    # Reference
    - [데이터 분석으로 배우는 파이썬 문제 해결](https://www.aladin.co.kr/m/mproduct.aspx?ItemId=327566110)
"""
)