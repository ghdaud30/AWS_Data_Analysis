import pandas as pd
import os
import glob
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import boto3
import folium
import json
import math
import streamlit as st
from datetime import datetime

from st_files_connection import FilesConnection
from PIL import Image


# 웹 페이지의 기본 설정
st.set_page_config(
    page_title="Contact",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("연락처 정보")
st.markdown(" - 이메일 : ghdaud3093@gmail.com")
st.markdown("---")