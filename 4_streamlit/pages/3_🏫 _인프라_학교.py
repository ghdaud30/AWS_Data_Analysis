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
    page_title="인프라",
    page_icon="🏫",
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

st.sidebar.markdown(
    """
    # Reference
    - [공공데이터](https://www.data.go.kr/)
    - [학교(나이스)](https://open.neis.go.kr/portal/data/service/selectServicePage.do?page=1&rows=10&sortColumn=&sortDirection=&infId=OPEN17020190531110010104913&infSeq=2)
    - [지역별 인구(kosis 공유서비스)](https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1B040A3&vw_cd=MT_ZTITLE&list_id=A_7&scrId=&seqNo=&lang_mode=ko&obj_var_id=&itm_id=&conn_path=MT_ZTITLE&path=%252FstatisticsList%252FstatisticsListIndex.do)
    - [지리 정보 수집(지오서비스)](http://www.gisdeveloper.co.kr/?p=2332)
"""
)

elementary_school = read_file_csv('real-estate555-bucket/0_data/streamlit_data/elementary_school.csv')
middle_shcool = read_file_csv('real-estate555-bucket/0_data/streamlit_data/middle_school.csv')
high_school = read_file_csv('real-estate555-bucket/0_data/streamlit_data/high_school.csv')

elementary_school['시도명'] = elementary_school['도로명주소'].str.split(' ').str[0]
elementary_school['시군구명'] = elementary_school['도로명주소'].str.split(' ').str[1]
middle_shcool['시도명'] = middle_shcool['도로명주소'].str.split(' ').str[0]
middle_shcool['시군구명'] = middle_shcool['도로명주소'].str.split(' ').str[1]
high_school['시도명'] = high_school['도로명주소'].str.split(' ').str[0]
high_school['시군구명'] = high_school['도로명주소'].str.split(' ').str[1]

school_vis = vis_func.school_count_plotly_type(elementary_school, sig_area,'초등학교')
school_vis2 = vis_func.school_count_plotly_type(middle_shcool, sig_area,'중학교')
school_vis3 = vis_func.school_count_plotly_type(high_school, sig_area,'고등학교')

school_vis4 = vis_func.school_count_plotly_gender(elementary_school, sig_area,'초등학교')
school_vis5 = vis_func.school_count_plotly_gender(middle_shcool, sig_area,'중학교')
school_vis6 = vis_func.school_count_plotly_gender(high_school, sig_area,'고등학교')


# school = [school_vis,school_vis2,school_vis3,school_vis4,school_vis5
#           ,school_vis6,school_vis7,school_vis8,school_vis9]

# # 표시 행
# columns = len(school) // 3

# n = 0

# for i in range(0, len(school), columns):
#     col = st.columns([1,1,1])
    
#     for j in range(len(col)):
#       if(i == 3):
#         col[j].plotly_chart(school[i + j], use_container_width = True)
#         n += 1
#         continue
#       else:
#         col[j].pyplot(school[i + j], use_container_width = True)
#         n += 1
    
col, col2, col3 = st.columns([1,1,1])
col.plotly_chart(school_vis, use_container_width = True) 
col2.plotly_chart(school_vis2, use_container_width = True)
col3.plotly_chart(school_vis3, use_container_width = True)

col4, col5, col6 = st.columns([1,1,1])
col4.plotly_chart(school_vis4, use_container_width = True) 
col5.plotly_chart(school_vis5, use_container_width = True)
col6.plotly_chart(school_vis6, use_container_width = True)

# col7, col8, col9 = st.columns([1,1,1])
# col7.pyplot(school_vis7, use_container_width = True) 
# col8.pyplot(school_vis8, use_container_width = True)
# col9.pyplot(school_vis9, use_container_width = True)


