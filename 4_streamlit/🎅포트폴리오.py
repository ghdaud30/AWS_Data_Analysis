import pandas as pd
import os
import glob
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import boto3
import vis_func
import folium
import json
import math
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

st.title("YeJun Hong's PortFolio 🎅🎅🎅 (Data Scientist)") 
st.markdown("---")

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
      
with st.expander("홍예준에 대해서 더 알고 싶다면?"):
  st.markdown("""
              ### 😛 취미 : 노래부르기 , 영화보기 , 야구보기
              ### 😊 MBTI : ENTP
              ### 😆 좋아하는것 : Comunication , Travelling
              ### 😑 싫어하는것 : 치과 가기 , 가지 먹기
              ### 😎 언어 : 한국어 , 영어 , 일본어
            """)
  
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
            ---
            ### 학교에서 많은 외국인 친구들을 많나며 
            ### 문화도 같이 공유하고 활동도 같이 하면서   
            ### 세상을 보는 시각을 넓힐 수 있었습니다.
            ---
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
    st.markdown("---")
    
st.markdown("""
            ### Created By Streamlit
            """)
