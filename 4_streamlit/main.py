import pandas as pd
import os
import geopandas as gpd
import glob
import plotly.express as px
import plotly.graph_objects as go
import boto3
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

# with open('real-estate555-bucket'/style.css) as f:
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

df_trade2 = df_trade[df_trade['시도명'] == sig_area]
df_rent2 = df_rent[df_rent['시도명'] == sig_area]


st.title("YeJun Hong's PortFolio 🎅🎅🎅 (Data Scientist)") 


image_col1, image_col2 = st.columns([1,4])
with image_col1:
    image = read_image_s3('hong.jpg')
    st.image(image, width=200)  
with image_col2:
    st.markdown("""
    ### 저는 카푸치노 같은 사람입니다.
    #### 놀땐 놀며 할땐 하는 구분력을 가진 사람입니다.
    #### 항상 긍정적인 마음으로 세상을 살아가고 있습니다.
    #### 주어진 일을 열심히 수행 하겠습니다.
    """)
      
with st.expander("홍예준에 대해서 더 알고 싶다면",  expanded=True):
    image_col1, image_col2 , image_col3 = st.columns([1,1,1])
    with image_col1:
      image = read_image_s3('taiwan.jpg')
      st.image(image)  
    with image_col2:
      image = read_image_s3('performance.jpg')
      st.image(image)  
    with image_col3:
      image = read_image_s3('school.jpg')
      st.image(image)
        
    st.markdown("""
                ### 학교에서 많은 외국인 친구들을 많나며 
                ### 문화도 같이 공유하고 활동도 같이 하면서   
                ### 세상을 보는 시각을 넓힐 수 있었습니다.
                """)
    
with st.container():
    st.markdown("### ✏️ 기술 스텍")
    st.markdown("#### Python , Sql , Java")
    st.markdown("---")
    
    st.markdown("### ✒️ Python 주요 활용 라이브러리")
    st.markdown("#### pandas , matplotlib , seaborn , plotly , streamlit")
    st.markdown("---")
    
    st.markdown("### 🖌️ 기술 환경")
    st.markdown("#### AWS , Linux , MySQLworkbench ,SpringBoot")
    st.markdown("---")
    
    st.markdown("### 📝 협업 툴")
    st.markdown(" - [GitHub](https://github.com/ghdaud30)")
    st.markdown(" - [Notion](https://www.notion.so/2023-9a0cd2e5323d401cab9db29c49586519)")
    st.markdown("---")
    
    st.markdown("### 🖊️ 알고리즘")
    st.markdown("#### 프로그래머스 (1471점)")
    st.markdown("---")
    
    st.markdown("### 🖋️ 어학 점수")
    st.markdown("#### TOEIC 780 (2023-11-26)")
    st.markdown("---")
    
    st.markdown("### 🖍️ 자격증")
    st.markdown(" - 컴퓨터활용능력 2급")
    st.markdown(" - 워드프로세서 1급")
    st.markdown(" - 한국사능력검정시험 1급")
    st.markdown(" - 운전면허자격증 2종 보통")

st.title('AWS 서버를 활용한 부동산 거래 정보') 
st.subheader(f'{sig_area} {type_option} {trade_option} 거래 정보(2021년)')

col1, col2, col3 , col4 = st.columns(4)

with col1:
  amount_value = st.slider(
      '매매(보증금액), 단위: 만원',
      0, 1000000, (0, 500000))

with col2:
  area_value = st.slider(
      '전용면적',
      0, 400, (0, 200))
  
with col3:
  year_value = st.slider(
      '건축년도',
      1980, 2021, (1980, 2000))
      
with col4:
  floor_value = st.slider(
      '층',
      1, 100, (0, 50))

col4, col5, = st.columns([1,1])

with col4:
    st.text(df_trade2.head(2).T)

with col5:
    st.text(df_rent2.head(2).T)