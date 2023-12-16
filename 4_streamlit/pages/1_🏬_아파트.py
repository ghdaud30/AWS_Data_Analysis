import pandas as pd
import os
import geopandas as gpd
import glob
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import folium
import json
import math
import boto3
import vis_func
import streamlit as st
from datetime import datetime

from st_files_connection import FilesConnection
from PIL import Image

import matplotlib.font_manager as fm  # 한글 폰트

st.set_page_config(
    page_title="아파트 대시보드",
    page_icon="🏬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 현재 디렉토리 경로
current_directory = os.path.dirname(__file__)

# 나눔고딕 폰트 경로 설정
font_path = os.path.join(current_directory, 'customFonts', 'NanumGothic-Regular.ttf')

# 폰트 추가 및 적용
fm.fontManager.addfont(font_path)
plt.rc('font', family='NanumGothic')

  

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

type_list = ['매매','전세','월세']
type_val = st.sidebar.selectbox(
    "거래 타입 선택",
    type_list
)

year_list = [2021,2022]
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
st.subheader(f'{sig_area} 아파트 거래 정보 {year_option}년')
st.markdown("---")

st.sidebar.markdown(
    """
    # Reference
    - [아파트](https://www.data.go.kr/data/15058017/openapi.do)
    - [오피스텔](https://www.data.go.kr/data/15059249/openapi.do)
    - [학교(나이스)](https://open.neis.go.kr/portal/data/service/selectServicePage.do?page=1&rows=10&sortColumn=&sortDirection=&infId=OPEN17020190531110010104913&infSeq=2)
    - [지역별 공원](https://www.data.go.kr/data/15012890/standard.do)
    - [지역별 인구(kosis 공유서비스)](https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1B040A3&vw_cd=MT_ZTITLE&list_id=A_7&scrId=&seqNo=&lang_mode=ko&obj_var_id=&itm_id=&conn_path=MT_ZTITLE&path=%252FstatisticsList%252FstatisticsListIndex.do)
    - [지리 정보 수집(지오서비스)](http://www.gisdeveloper.co.kr/?p=2332)
"""
)

apart_trans = read_file_csv('real-estate555-bucket/0_data/streamlit_data/geoservice/property_trade_map.csv')
apart_trans2 = apart_trans[apart_trans['시도명'] == sig_area]

sig_lat_lon = read_file_csv('real-estate555-bucket/0_data/streamlit_data/geoservice/sig_lat_lon.csv')
sig_lat_lon2 = sig_lat_lon[sig_lat_lon['sig_nm'] == sig_area].reset_index(drop = True)

vis_trade_rent_df = read_file_csv('real-estate555-bucket/0_data/streamlit_data/vis_trade_rent.csv')
geo_json = read_file_json(f'real-estate555-bucket/0_data/streamlit_data/geoservice/geo_sig_{sig_area}_json.geojson')

# 막대그래프 seaborn
vis_trade_rent = vis_func.vis_trade_rent(vis_trade_rent_df,
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
                        sig_area,
                        type_option)
# 실거래가
trade_mean = vis_func.trade_mean(vis_trade_rent_df,
                        sig_area,
                        type_option)
# 2021년 월에 따른 지역별 부동산 거래량 평균
trade_count_month = vis_func.trade_count_month(vis_trade_rent_df,
                        sig_area,
                        type_option)
# 거래량
trade_count = vis_func.trade_count(vis_trade_rent_df,
                        sig_area,
                        type_option)

# 각 구별 평균 거래 금액
trade_mean_map = vis_func.trade_mean_map(apart_trans2,
                        geo_json,
                        sig_lat_lon2,
                        sig_area,
                        type_val,
                        type_option)


col555 = st.columns([1])
with col555[0]:
    st.plotly_chart(trade_mean_map, use_container_width=True)
st.markdown("---")

col, col2 = st.columns([1,1])
col.pyplot(vis_trade_rent, use_container_width = True) 
col2.plotly_chart(vis_trade_rent2, use_container_width = True)
st.markdown("---")

col3, col4 = st.columns([1,1])
col3.pyplot(trade_mean_month, use_container_width = True) 
col4.plotly_chart(trade_mean, use_container_width = True)
st.markdown("---")

col4, col5 = st.columns([1,1])
col4.pyplot(trade_count_month, use_container_width = True) 
col5.plotly_chart(trade_count, use_container_width = True)
st.markdown("---")

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