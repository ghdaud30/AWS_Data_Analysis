@ -0,0 +1,87 @@
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
    page_title="인프라",
    page_icon="🏞️",
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

sig_list = ['서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', '대전광역시', '울산광역시',
       '세종특별자치시', '경기도', '강원도', '충청북도', '충청남도', '전라북도', '전라남도', '경상북도',
       '경상남도', '제주특별자치도']

sig_area = st.sidebar.selectbox(
    "시군구 선택",
    sig_list
)

st.title('AWS 서버를 활용한 부동산 거래 정보') 
st.subheader(f'{sig_area} 공원 정보')
st.markdown("---")

public_city_park = read_file_csv('real-estate555-bucket/0_data/streamlit_data/public_city_park.csv')
public_city_park['시도명'] = public_city_park['소재지도로명주소'].str.split(' ').str[0]
public_city_park['시군구명'] = public_city_park['소재지도로명주소'].str.split(' ').str[1]

park_vis = vis_func.park_geo(public_city_park, sig_area)
park_vis2 = vis_func.park_count(public_city_park, sig_area)

col, col2= st.columns([1,1])
col.plotly_chart(park_vis, use_container_width = True) 
col2.plotly_chart(park_vis, use_container_width = True)


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


