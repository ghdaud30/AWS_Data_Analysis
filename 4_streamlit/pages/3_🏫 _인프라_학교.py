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
    page_icon="🏡",
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
st.subheader(f'{sig_area} 학교 정보')
st.markdown("---")

elementary_school = read_file_csv('real-estate555-bucket/0_data/streamlit_data/elementary_school.csv')
middle_shcool = read_file_csv('real-estate555-bucket/0_data/streamlit_data/middle_school.csv')
high_school = read_file_csv('real-estate555-bucket/0_data/streamlit_data/high_school.csv')

elementary_school['시도명'] = elementary_school['도로명주소'].str.split(' ').str[0]
elementary_school['시군구명'] = elementary_school['도로명주소'].str.split(' ').str[1]
middle_shcool['시도명'] = middle_shcool['도로명주소'].str.split(' ').str[0]
middle_shcool['시군구명'] = middle_shcool['도로명주소'].str.split(' ').str[1]
high_school['시도명'] = high_school['도로명주소'].str.split(' ').str[0]
high_school['시군구명'] = high_school['도로명주소'].str.split(' ').str[1]

school_vis1 = vis_func.school_count_type(elementary_school, sig_area,'초등학교')
school_vis2 = vis_func.school_count_type(middle_shcool, sig_area,'중학교')
school_vis3 = vis_func.school_count_type(high_school, sig_area,'고등학교')

school_vis4 = vis_func.school_count_plotly(elementary_school, sig_area,'초등학교')
school_vis5 = vis_func.school_count_plotly(middle_shcool, sig_area,'중학교')
school_vis6 = vis_func.school_count_plotly(high_school, sig_area,'고등학교')

school_vis7 = vis_func.school_count_gender(elementary_school, sig_area,'초등학교')
school_vis8 = vis_func.school_count_gender(middle_shcool, sig_area,'중학교')
school_vis9 = vis_func.school_count_gender(high_school, sig_area,'고등학교')

school = ['school_vis1','school_vis2','school_vis3','school_vis4','school_vis5'
          ,'school_vis6','school_vis7','school_vis8','school_vis9']

# 표시 행
columns = len(school) // 3

n = 1

for i in range(1, len(school) + 1, columns):
    col = st.columns([1,1,1])
    
    for j in range(len(col)):
      n += 1
      if(i == 4):
        col[j].plotly_chart(f'school_vis{n}', use_container_width = True)
        continue
      else:
        col[j].pyplot(f'school_vis{n}', use_container_width = True)
    
# col1, col2, col3 = st.columns([1,1,1])
# col1.pyplot(school_vis1, use_container_width = True) 
# col2.pyplot(school_vis2, use_container_width = True)
# col3.pyplot(school_vis3, use_container_width = True)

# col4, col5, col6 = st.columns([1,1,1])
# col4.plotly_chart(school_vis4, use_container_width = True) 
# col5.plotly_chart(school_vis5, use_container_width = True)
# col6.plotly_chart(school_vis6, use_container_width = True)

# col7, col8, col9 = st.columns([1,1,1])
# col7.pyplot(school_vis7, use_container_width = True) 
# col8.pyplot(school_vis8, use_container_width = True)
# col9.pyplot(school_vis9, use_container_width = True)



st.sidebar.markdown(
    """
    # Reference
    - [데이터 분석으로 배우는 파이썬 문제 해결](https://www.aladin.co.kr/m/mproduct.aspx?ItemId=327566110)
"""
)