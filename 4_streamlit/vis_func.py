import pandas as pd
import os
import geopandas as gpd
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import mplcursors
import plotly.express as px
import plotly.graph_objects as go
import folium
import json
import math
from plotly.validators.scatter.marker import SymbolValidator

# 금액 단위를 읽기 쉽게 표현하는 함수를 만듭니다
def readNumber(n):
    # 백만 단위 보다 크면 억 단위로 표시
    if(n > 10**4):
        a = str(format(math.floor(n / 10**4),',d')) + '억'
        b = ' ' + str(format(math.floor(n % 10**4),',d'))
        c = a + b
    # 작으면 그대로 반환
    else:
        c = format(n,',d') + '만'
    return(c)
 
def vis_trade_rent(total, type_val, sig_area, year_val, month_val):
    
    # 타입 별 이름
    type_dic = {'apt':'아파트','offi':'오피스텔'}
    type_nm = type_dic[type_val]
    
    total = total.astype({'년' : int,'월' : int})
    total['mean_2'] = total['mean'].apply(lambda x : readNumber(x))
    
    
    df1 = total[(total['시도명'] == sig_area) & 
                (total['년'] == year_val) & 
                (total['월'] == month_val) & 
                (total['타입'] == type_val)]
    df1 = df1.sort_values(by = 'mean',ascending=False)
    
    # 각 거래 유형에 대한 데이터 추출
    df_sale = df1[df1['구분'] == '매매']
    df_lease = df1[df1['구분'] == '전세']
    df_monthly = df1[df1['구분'] == '월세']
    
    # 데이터 다시 합쳐주기
    combined_df = pd.concat([df_sale, df_lease, df_monthly])
    
    # 막대 그래프 그리기
    fig, ax = plt.subplots(figsize=(16, 10))
    sns.barplot(x='시군구명', y='mean', hue='구분', data=combined_df, alpha=0.7)

    # 툴팁 추가
    cursor = mplcursors.cursor(ax)
    cursor.connect("add", lambda sel: sel.annotation.set_text(f'({sel.target[0]:.1f}, {sel.target[1]:.1f})'))
    
    plt.title(f'{sig_area} 시군구별 아파트 매매(실거래가)/전월세(보증금) 평균값', pad=20, fontsize=20)
    plt.text(0.8, 1.015, '단위(만원)', ha='center', va='center', fontsize=15, color='gray', transform=plt.gca().transAxes)
    
    # x와 y 축 레이블 제거
    plt.xlabel('')
    plt.ylabel('')
    
    # 축 레이블과 범례 폰트 크기 설정
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)
    plt.legend(prop={'size': 20})  # 범례의 폰트 크기를 12로 조절
    
    plt.xticks(rotation=90)  # x축 라벨 회전
    plt.grid(axis='y')  # y축 그리드 표시
    
    return (fig) 
# plotly 사용
def vis_trade_rent2(total, type_val, sig_area, year_val, month_val):
    
    # 타입 별 이름
    type_dic = {'apt':'아파트','offi':'오피스텔'}
    type_nm = type_dic[type_val]
    
    total = total.astype({'년' : int,'월' : int})
    total['mean_2'] = total['mean'].apply(lambda x : readNumber(x))
    
    
    df1 = total[(total['시도명'] == sig_area) & 
                (total['년'] == year_val) & 
                (total['월'] == month_val) & 
                (total['타입'] == type_val)]
    df1 = df1.sort_values(by = 'mean',ascending=False)
    
    # 각 거래 유형에 대한 데이터 추출
    df_sale = df1[df1['구분'] == '매매']
    df_lease = df1[df1['구분'] == '전세']
    df_monthly = df1[df1['구분'] == '월세']
    
    # 데이터 다시 합쳐주기
    combined_df = pd.concat([df_sale, df_lease, df_monthly])
    
    # 막대 그래프 그리기 (plotly 사용)
    fig = px.bar(combined_df, x='시군구명', y='mean', color='구분', barmode='group')

    # 그래프 레이아웃 및 제목 설정
    fig.update_layout(
        title=f'{sig_area} 시군구별 아파트 매매(실거래가)/전월세(보증금) 평균값 <br><sub>단위(만원)</sup>',
        xaxis_title='',
        yaxis_title='',
        font=dict(size=14),
        legend=dict(title='구분', font=dict(size=12)),
        xaxis=dict(tickangle=90),
        yaxis=dict(title='단위(만원)', titlefont=dict(size=14)),
        bargap=0.15
    )

    return(fig)
# plotly 사용  
def vis_trade_rent3(total, type_val, sig_area, year_val, month_val):

    type_dic = {'apt':'아파트', 'rh':'연립다세대','sh':'단독-다가구','offi':'오피스텔'}
    type_nm = type_dic[type_val]
    
    total['년'] = total['년'].astype(int)
    total['월'] = total['월'].astype(int)
    total['mean'] = total['mean'].astype(int)
    total['mean_2'] = total['mean'].apply(readNumber)

    df1 = total[(total['시도명'] == sig_area) & 
                (total['년'] == year_val) & 
                (total['월'] == month_val) & 
                (total['타입'] == type_val)]


    df1 = df1.sort_values(by = 'mean',ascending=False)


    fig = go.Figure(data = [
        go.Bar(name = '매매',
               y = df1[df1['구분'] == '매매']['mean'], 
               x = df1[df1['구분'] == '매매']['시군구명'], 
               # marker_color='crimson',
               marker_color='blue',
               opacity=1,
               marker_pattern_shape="-",
               text = df1[df1['구분'] == '매매']['mean_2'],
               hovertemplate='%{text}만'
              ),
        go.Bar(name = '전세', 
               y = df1[df1['구분'] == '전세']['mean'], 
               x = df1[df1['구분'] == '전세']['시군구명'],
#                marker_color='blue',
               marker_color='red',
               opacity=0.7,
               marker_pattern_shape="x",
               text = df1[df1['구분'] == '전세']['mean_2'],
               hovertemplate='%{text}만'
              ),
        go.Bar(name = '월세',
               y = df1[df1['구분'] == '월세']['mean'], 
               x = df1[df1['구분'] == '월세']['시군구명'],
#                marker_color='green',
               marker_color='green',
               opacity=0.3,
               marker_pattern_shape="+",
               text = df1[df1['구분'] == '월세']['mean_2'],
               hovertemplate='%{text}만'
              ),
    ])



    fig.update_layout(
        title= f'{sig_area} 시군구별 {type_nm} 매매(실거래가)/전월세(보증금) 평균 <br><sup>단위(만원)</sup>',
        title_font_family="맑은고딕",
        title_font_size = 18,
        hoverlabel=dict(
            bgcolor='white',
            font_size=15,
        ),
        hovermode="x unified",
        template='plotly', 
        xaxis_tickangle=90,
        yaxis_tickformat = ',',
        legend = dict(orientation = 'h', xanchor = "center", x = 0.85, y= 1.1), #Adjust legend position
        barmode='group'
    )

    return(fig)

#  학교
def school_count_type(school, sig_area, school_name):
    # 선택한 지역을 특정해줍니다
    school2 = school[school['시도명'] == sig_area]
    school2.reset_index(drop=True, inplace = True)
    
    school2 = school2[['시군구명','설립명','학교명']].groupby(['시군구명','설립명']).describe()
    school2 = school2.reset_index()
    
    # 학교 갯수를 합쳐 줍니다
    school3 = pd.concat([school2[['시군구명','설립명']],school2['학교명'][['count']]], axis = 1)
    school3.columns = ['시군구명','설립명','count']
    
     # 각 거래 타입에 대한 데이터 추출
    school_national = school3[school3['설립명'] == '국립']
    school_public = school3[school3['설립명'] == '공립']
    school_private = school3[school3['설립명'] == '사립']
    
    # 데이터 다시 합쳐주기
    school4 = pd.concat([school_national, school_public, school_private])
    school4 = school4.sort_values(by='count',ascending=False)
    
    # 막대 그래프 그리기
    fig, ax = plt.subplots(figsize=(16, 10))
    sns.barplot(x='시군구명', y='count', hue='설립명', data=school4)
    
    # 제목 , 부제목
    plt.title(f'{sig_area} 시군구별 {school_name} 수(국공립사립 여부)', pad=20, fontsize=20)
    plt.text(0.4, 1.015, '단위(명)', ha='center', va='center', fontsize=15, color='gray', transform=plt.gca().transAxes)
    
    # 축 레이블과 범례 폰트 크기 설정
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)
    plt.xlabel('')
    plt.ylabel('')
    plt.legend(prop={'size': 20}, loc='upper right')  # 범례의 폰트 크기를 12로 조절
    
    plt.xticks(rotation=90)  # x축 라벨 회전
    plt.grid(axis='y')  # y축 그리드 표시

    plt.tight_layout()
    plt.show()
    
    return fig

def school_count_plotly(df_trade, sig_area,school_name):
  
    aaaa_raw = df_trade[df_trade['시도명'] == sig_area]
    aaaa_raw = aaaa_raw.reset_index(drop = True)


    aaaa_raw = aaaa_raw[['시군구명','설립명','학교명']].groupby(['시군구명','설립명']).describe()
    aaaa_raw = aaaa_raw.reset_index()

    apart_trans2 = pd.concat([aaaa_raw[['시군구명','설립명']],aaaa_raw['학교명'][['count']]], axis = 1)
    apart_trans2.columns = ['시군구명','설립명','count']
    apart_trans2 = apart_trans2.sort_values(by = 'count',ascending=False)

    
    fig = go.Figure(data=[
        go.Bar(
          name = '사립', 
          x=apart_trans2[apart_trans2['설립명'] == '사립']['시군구명'],
          y=apart_trans2[apart_trans2['설립명'] == '사립']['count'],
          hovertemplate='%{y}개'
        ),

        go.Bar(
          name = '공립', 
          x=apart_trans2[apart_trans2['설립명'] == '공립']['시군구명'],
          y=apart_trans2[apart_trans2['설립명'] == '공립']['count'],
          hovertemplate='%{y}개'
        ),

        go.Bar(
          name = '국립',
          x=apart_trans2[apart_trans2['설립명'] == '국립']['시군구명'],
          y=apart_trans2[apart_trans2['설립명'] == '국립']['count'],
          hovertemplate='%{y}개'

        )
        ])


    fig.update_layout(
            title= f'{sig_area} 시군구별 {school_name} 수 <br><sup>단위(명)</sup>',
            title_font_family="맑은고딕",
            title_font_size = 18,
            hoverlabel=dict(
                bgcolor='white',
                font_size=15,
            ),
            hovermode="x unified",
            template='plotly_white', 
            xaxis_tickangle=90,
            yaxis_tickformat = ',',
            legend = dict(orientation = 'h', xanchor = "center", x = 0.85, y= 1.1), #Adjust legend position
            barmode='group'
        )

    return(fig)

def school_count_gender(school, sig_area, school_name):
    # 선택한 지역을 특정해줍니다
    school2 = school[school['시도명'] == sig_area]
    school2.reset_index(drop=True, inplace = True)
    
    school2 = school2[['시군구명','남녀공학구분명','학교명']].groupby(['시군구명','남녀공학구분명']).describe()
    school2 = school2.reset_index()
    
    # 학교 갯수를 합쳐 줍니다
    school3 = pd.concat([school2[['시군구명','남녀공학구분명']],school2['학교명'][['count']]], axis = 1)
    school3.columns = ['시군구명','남녀공학구분명','count']
    
     # 각 거래 타입에 대한 데이터 추출
    school_dual = school3[school3['남녀공학구분명'] == '남여공학']
    school_man = school3[school3['남녀공학구분명'] == '남']
    school_girl = school3[school3['남녀공학구분명'] == '여']
    
    # 데이터 다시 합쳐주기
    school4 = pd.concat([school_dual, school_man, school_girl])
    school4 = school4.sort_values(by='count',ascending=False)
    
    # 막대 그래프 그리기
    fig, ax = plt.subplots(figsize=(16, 10))
    sns.barplot(x='시군구명', y='count', hue='남녀공학구분명', data=school4)
    
    # 제목 , 부제목
    plt.title(f'{sig_area} 시군구별 {school_name} 수(남녀공학 여부)', pad=20, fontsize=20)
    plt.text(0.4, 1.015, '단위(명)', ha='center', va='center', fontsize=15, color='gray', transform=plt.gca().transAxes)
    
    # 축 레이블과 범례 폰트 크기 설정
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)
    plt.xlabel('')
    plt.ylabel('')
    plt.legend(prop={'size': 20}, loc='upper right')  # 범례의 폰트 크기를 12로 조절
    
    plt.xticks(rotation=90)  # x축 라벨 회전
    plt.grid(axis='y')  # y축 그리드 표시

    plt.tight_layout()
    plt.show()
    
    return fig

def trade_mean_month(total, sig_area, type_val):
    
    # 타입 별 이름
    type_dic = {'apt':'아파트','offi':'오피스텔'}
    type_nm = type_dic[type_val]
    # 열 전처리
    total = total.astype({'년' : int,'월' : int})
    total['mean_2'] = total['mean'].apply(lambda x : readNumber(x))
    # 지역과 타입을 정해 줍니다
    df1 = total[(total['시도명'] == sig_area) & 
                  (total['타입'] == type_val)]
    
    df_trade = df1[df1['구분'] == '매매']
    df_year = df1[df1['구분'] == '전세']
    df_month = df1[df1['구분'] == '월세']
    
    # 데이터 다시 합쳐주기
    combined_df = pd.concat([df_trade,df_year,df_month])
    
    # 막대 그래프 그리기
    fig, ax = plt.subplots(figsize=(16, 10))
    sns.lineplot(x='거래날짜', y='mean', hue='구분', style = '구분',
                 markers=True, dashes=False, data=combined_df, alpha=0.7)

    # 툴팁 추가
    cursor = mplcursors.cursor(ax)
    cursor.connect("add", lambda sel: sel.annotation.set_text(f'({sel.target[0]:.1f}, {sel.target[1]:.1f})'))
    
    plt.title(f'{sig_area} {type_nm} 매매(실거래가)/전월세(보증금) 평균값', pad=20, fontsize=20)
    plt.text(0.3, 1.015, '단위(만원)', ha='center', va='center', fontsize=15, color='gray', transform=plt.gca().transAxes)
    
    # x와 y 축 레이블 제거
    plt.xlabel('')
    plt.ylabel('')
    
    # 축 레이블과 범례 폰트 크기 설정
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)
    plt.legend(prop={'size': 20})  # 범례의 폰트 크기를 12로 조절
    
    plt.xticks(rotation=45)  # x축 라벨 회전
    plt.grid(axis = 'x', linestyle = '--') # x축 그리드 표시
    plt.grid(axis = 'y', linestyle = '--') # y축 그리드 표시
    
    plt.tight_layout()
    plt.show()    

    return combined_df

def trade_mean(df_trade, type_val, sig_area):

    type_dic = {'apt':'아파트', 'rh':'연립다세대','sh':'단독-다가구','offi':'오피스텔'}
    type_nm = type_dic[type_val]
    
    total = df_trade
    df1 = total[(total['시도명'] == sig_area) &
                (total['타입'] == type_val)]
                
    df1['mean'] = df1['mean'].astype(int)
    df1['mean_2'] = df1['mean'].apply(readNumber)
    
    fig = go.Figure(data=[
        go.Scatter(
            name = '매매',
            x=df1[df1['구분'] == '매매']['거래날짜'],
            y=df1[df1['구분'] == '매매']['mean'],
            text = df1[df1['구분'] == '매매']['mean_2'],
            hovertemplate='%{text}만',
            marker_size=8,                
            line_shape='spline'),

        go.Scatter(
            name = '전세',
            x=df1[df1['구분'] == '전세']['거래날짜'],
            y=df1[df1['구분'] == '전세']['mean'],
            text = df1[df1['구분'] == '전세']['mean_2'],
            hovertemplate='%{text}만',
            marker_symbol='triangle-down',
            marker_size=8,                
            line_shape='spline'),

          go.Scatter(
            name = '월세',
            x=df1[df1['구분'] == '월세']['거래날짜'],
            y=df1[df1['구분'] == '월세']['mean'],
            text = df1[df1['구분'] == '월세']['mean_2'],
            hovertemplate='%{text}만',
            marker_symbol='square',
            marker_size=8,              
            line_shape='spline')
        ])

    # fig.update_traces(hoverinfo='text+name', mode='lines+markers')
    fig.update_traces(mode='lines+markers')

    fig.update_layout(
        title= f'{sig_area} {type_nm} 매매(실거래가)/전월세(보증금) 평균 <br><sup>단위(만원)</sup>',
      title_font_family="맑은고딕",
      title_font_size = 18,
      hoverlabel=dict(
        bgcolor='white',
        font_size=15,
      ),
      hovermode="x unified",
      template='plotly_white',
      xaxis_tickangle=90,
      yaxis_tickformat = ',',
      legend = dict(orientation = 'h', xanchor = "center", x = 0.85, y= 1.1), 
      barmode='group'
    )

#     for i in range(2019, 2023):
#         fig.add_vline(x=f'{i}-01-01', line_width=1, line_dash="dash", line_color="green")
    return(fig)

def trade_count_month(total, sig_area, type_val):
    
    # 타입 별 이름
    type_dic = {'apt':'아파트','offi':'오피스텔'}
    type_nm = type_dic[type_val]
    # 열 전처리
    total = total.astype({'년' : int,'월' : int})
    # 지역과 타입을 정해 줍니다
    df1 = total[(total['시도명'] == sig_area) & 
                  (total['타입'] == type_val)]
    
    df_trade = df1[df1['구분'] == '매매']
    df_year = df1[df1['구분'] == '전세']
    df_month = df1[df1['구분'] == '월세']
    
    # 데이터 다시 합쳐주기
    combined_df = pd.concat([df_trade,df_year,df_month])
    
    # 막대 그래프 그리기
    fig, ax = plt.subplots(figsize=(16, 10))
    sns.lineplot(x='거래날짜', y='count', hue='구분',style='구분',
                 markers=True, dashes=False , data=combined_df, alpha=0.7)

    # 툴팁 추가
    cursor = mplcursors.cursor(ax)
    cursor.connect("add", lambda sel: sel.annotation.set_text(f'({sel.target[0]:.1f}, {sel.target[1]:.1f})'))
    
    plt.title(f'{sig_area} {type_nm} 매매(실거래가)/전월세(보증금) 거래량', pad=20, fontsize=20)

    
    # x와 y 축 레이블 제거
    plt.xlabel('')
    plt.ylabel('')
    
    # 축 레이블과 범례 폰트 크기 설정
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)
    plt.legend(prop={'size': 20})  # 범례의 폰트 크기를 12로 조절
    
    plt.xticks(rotation=45)  # x축 라벨 회전
    plt.grid(axis = 'x', linestyle = '--') # x축 그리드 표시
    plt.grid(axis = 'y', linestyle = '--') # y축 그리드 표시
    
    plt.tight_layout()
    plt.show()    

    return combined_df
  
def trade_count(df_trade, type_val, sig_area):
    
    type_dic = {'apt':'아파트', 'rh':'연립다세대','sh':'단독-다가구','offi':'오피스텔'}
    type_nm = type_dic[type_val]

    total = df_trade
    df1 = total[(total['시도명'] == sig_area) & 
                (total['타입'] == type_val)]
    fig = go.Figure(data=[
        go.Scatter(
            name = '매매', 
            x=df1[df1['구분'] == '매매']['거래날짜'],
            y=df1[df1['구분'] == '매매']['count'],
            hovertemplate='%{y}건',
            marker_size=8,                   
            line_shape='spline'),

        go.Scatter(
            name = '전세', 
            x=df1[df1['구분'] == '전세']['거래날짜'],
            y=df1[df1['구분'] == '전세']['count'],
            hovertemplate='%{y}건',
            marker_symbol='triangle-down',
            marker_size=8,                 
            line_shape='spline'),

          go.Scatter(
            name = '월세',
            x=df1[df1['구분'] == '월세']['거래날짜'],
            y=df1[df1['구분'] == '월세']['count'],
            hovertemplate='%{y}건',
            marker_symbol='square',
            marker_size=8,
            line_shape='spline')
        ])

    fig.update_traces(mode='lines+markers')

    fig.update_layout(
        title= f'{sig_area} {type_nm} 매매(실거래가)/전월세(보증금) 거래량',
      title_font_family="맑은고딕",
      title_font_size = 18,
      hoverlabel=dict(
        bgcolor='white',
        font_size=15,
      ),
      hovermode="x unified",
      template='plotly_white', 
      xaxis_tickangle=90,
      yaxis_tickformat = ',',
      legend = dict(orientation = 'h', xanchor = "center", x = 0.85, y= 1.1), 
      barmode='group'
    )

#     for i in range(2019, 2023):
#         fig.add_vline(x=f'{i}-01-01', line_width=1, line_dash="dash", line_color="green")
    return(fig)  

