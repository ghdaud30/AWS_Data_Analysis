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
 '년도',
 year_list
)

year_list_str = ['2021','2022']
selected_year_index = year_list.index(year_option)  # 선택한 연도의 인덱스를 가져옵니다
selected_year_str = year_list_str[selected_year_index]  # year_list_str에서 해당 연도의 문자열 값을 가져옵니다

month_list = range(1,13)
month_option = st.sidebar.selectbox(
 '월',
 month_list
)

month_list_str = ['01','02','03','04','05','06',
                  '07','08','09','10','11','12']
selected_month_index = month_option - 1  # 선택한 월의 인덱스를 가져옵니다 (0부터 시작하므로 -1)
selected_month_str = month_list_str[selected_month_index]  # month_list_str에서 해당 월의 문자열 값을 가져옵니다

st.title('AWS 서버를 활용한 부동산 거래 정보') 
st.subheader(f'{sig_area} 아파트 거래 정보 {year_option}년 {month_option}월')
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
  amount_value = st.slider(
      '보증금액, 단위: 만원',
      0, 1000000, (0, 10000000))

with col2:
  area_value = st.slider(
      '전용면적',
      0, 400, (0, 200))
      
with col3:
  year_value = st.slider(
      '건축년도',
      1980, 2022, (1980, 2000))
      
with col4:
  floor_value = st.slider(
      '층',
      1, 100, (0, 100))

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

legal_info_b = read_file_csv('real-estate555-bucket/0_data/streamlit_data/legal_info_b.csv')

apart_trans = read_file_csv('real-estate555-bucket/0_data/streamlit_data/geoservice/property_trade_map.csv')
sig_lat_lon = read_file_csv('real-estate555-bucket/0_data/streamlit_data/geoservice/sig_lat_lon.csv')

vis_trade_rent_df = read_file_csv('real-estate555-bucket/0_data/streamlit_data/vis_trade_rent.csv')
geo_json = read_file_json(f'real-estate555-bucket/0_data/streamlit_data/geoservice/geo_sig_{sig_area}_json.geojson')

df_lat_lon = read_file_csv(f'real-estate555-bucket/0_data/streamlit_data/df_lat_lon.csv')

df_trade = read_file_csv(f'real-estate555-bucket/0_data/streamlit_data/{type_option}_trade/{type_option}_trade_{selected_year_str}{selected_month_str}.csv')
df_rent = read_file_csv(f'real-estate555-bucket/0_data/streamlit_data/{type_option}_rent/{type_option}_rent_{selected_year_str}{selected_month_str}.csv')
df_trade_2 = df_trade[df_trade['시도명'] == sig_area]
df_rent_2 = df_rent[df_rent['시도명'] == sig_area]

df_trade_3 = pd.merge(df_trade_2,legal_info_b,
                    on = ['법정동코드','시도명','시군구명','동리명'],
                    how = 'left')

df_trade_4 = pd.merge(df_trade_3,df_lat_lon,
                      on = '주소',
                      how = 'left')
df_rent_3 = pd.merge(df_rent_2,df_lat_lon,
                      on = '주소',
                      how = 'left')



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

# 각 시군구별 평균 거래 금액 지도로 표현
trade_mean_map = vis_func.trade_mean_map(apart_trans,
                        geo_json,
                        sig_lat_lon,
                        sig_area,
                        year_option,
                        month_option,
                        type_val,
                        type_option)

# 각 시도별 거래량 지도로 표현
if type_val == '매매':
    map_trade = vis_func.map_trade(df_trade_4,
                              type_val,
                              amount_value[0],
                              amount_value[1],
                              area_value[0],
                              area_value[1],
                              year_value[0],
                              year_value[1],
                              floor_value[0],
                              floor_value[1])
    st.plotly_chart(map_trade, use_container_width = True)
    st.markdown("---")
    
if type_val == '전세':
    map_trade = vis_func.map_trade(df_rent_3,
                              type_val,
                              amount_value[0],
                              amount_value[1],
                              area_value[0],
                              area_value[1],
                              year_value[0],
                              year_value[1],
                              floor_value[0],
                              floor_value[1])
    st.plotly_chart(map_trade, use_container_width = True)
    st.markdown("---")
    
if type_val == '월세':
    map_trade = vis_func.map_trade(df_rent_3,
                              type_val,
                              amount_value[0],
                              amount_value[1],
                              area_value[0],
                              area_value[1],
                              year_value[0],
                              year_value[1],
                              floor_value[0],
                              floor_value[1])
    st.plotly_chart(map_trade, use_container_width = True)
    st.markdown("---")

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