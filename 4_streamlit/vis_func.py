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
    return c
 
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
    plt.text(0.25, 1.015, '단위(만원)', ha='center', va='center', fontsize=15, color='gray', transform=plt.gca().transAxes)
    
    # x와 y 축 레이블 제거
    plt.xlabel('')
    plt.ylabel('')
    
    # 축 레이블과 범례 폰트 크기 설정
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)
    plt.legend(prop={'size': 20})  # 범례의 폰트 크기를 12로 조절
    
    plt.xticks(rotation=90)  # x축 라벨 회전
    plt.grid(axis='y')  # y축 그리드 표시
    
    return fig
 
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

    return fig

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

    return fig

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

def school_count_plotly_type(df_trade, sig_area,school_name):
  
    df = df_trade[df_trade['시도명'] == sig_area]
    df = df.reset_index(drop = True)


    df = df[['시군구명','설립명','학교명']].groupby(['시군구명','설립명']).describe()
    df = df.reset_index()

    df2 = pd.concat([df[['시군구명','설립명']],df['학교명'][['count']]], axis = 1)
    df2.columns = ['시군구명','설립명','count']
    df2 = df2.sort_values(by = 'count',ascending=False)

    
    fig = go.Figure(data=[
        go.Bar(
          name = '사립', 
          x=df2[df2['설립명'] == '사립']['시군구명'],
          y=df2[df2['설립명'] == '사립']['count'],
          hovertemplate='%{y}개'
        ),

        go.Bar(
          name = '공립', 
          x=df2[df2['설립명'] == '공립']['시군구명'],
          y=df2[df2['설립명'] == '공립']['count'],
          hovertemplate='%{y}개'
        ),

        go.Bar(
          name = '국립',
          x=df2[df2['설립명'] == '국립']['시군구명'],
          y=df2[df2['설립명'] == '국립']['count'],
          hovertemplate='%{y}개'

        )
        ])


    fig.update_layout(
            title= f'{sig_area} 시군구별 {school_name} 수 (국공립사립 여부) <br><sup>단위(명)</sup>',
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

def school_count_plotly_gender(df_trade, sig_area,school_name):
  
    df = df_trade[df_trade['시도명'] == sig_area]
    df = df.reset_index(drop = True)


    df = df[['시군구명','남녀공학구분명','학교명']].groupby(['시군구명','남녀공학구분명']).describe()
    df = df.reset_index()

    df2 = pd.concat([df[['시군구명','남녀공학구분명']],df['학교명'][['count']]], axis = 1)
    df2.columns = ['시군구명','남녀공학구분명','count']
    df2 = df2.sort_values(by = 'count',ascending=False)

    
    fig = go.Figure(data=[
        go.Bar(
          name = '남여공학', 
          x=df2[df2['남녀공학구분명'] == '남여공학']['시군구명'],
          y=df2[df2['남녀공학구분명'] == '남여공학']['count'],
          hovertemplate='%{y}개'
        ),

        go.Bar(
          name = '남', 
          x=df2[df2['남녀공학구분명'] == '남']['시군구명'],
          y=df2[df2['남녀공학구분명'] == '남']['count'],
          hovertemplate='%{y}개'
        ),

        go.Bar(
          name = '여',
          x=df2[df2['남녀공학구분명'] == '여']['시군구명'],
          y=df2[df2['남녀공학구분명'] == '여']['count'],
          hovertemplate='%{y}개'

        )
        ])

    fig.update_layout(
            title= f'{sig_area} 시군구별 {school_name} 수 (남녀공학 여부) <br><sup>단위(명)</sup>',
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

# 2021년 월에 따른 지역별 부동산 실거래가 평균
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
    
    # '거래날짜' 열을 날짜 형식으로 변환
    combined_df['거래날짜'] = pd.to_datetime(combined_df['거래날짜'])

    # '거래날짜'를 기준으로 데이터 정렬
    combined_df = combined_df.sort_values(by='거래날짜')
    
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

    return fig
# 실거래가
def trade_mean(df_trade, sig_area, type_val):

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
        title= f'{sig_area} {type_nm} 매매(실거래가)/전월세(보증금) 평균값 <br><sup>단위(만원)</sup>',
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
# 2021년 월에 따른 지역별 부동산 거래량 평균
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
    
    # '거래날짜' 열을 날짜 형식으로 변환
    combined_df['거래날짜'] = pd.to_datetime(combined_df['거래날짜'])

    # '거래날짜'를 기준으로 데이터 정렬
    combined_df = combined_df.sort_values(by='거래날짜')
    
    # 막대 그래프 그리기
    fig, ax = plt.subplots(figsize=(16, 10))
    sns.lineplot(x='거래날짜', y='count', hue='구분',style='구분',
                 markers=True, dashes=False , data=combined_df, alpha=0.7)

    # 툴팁 추가
    cursor = mplcursors.cursor(ax)
    cursor.connect("add", lambda sel: sel.annotation.set_text(f'({sel.target[0]:.1f}, {sel.target[1]:.1f})'))
    
    plt.title(f'{sig_area} {type_nm} 매매(실거래가)/전월세(보증금) 거래량', pad=20, fontsize=20)
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

    return fig
# 거래량
def trade_count(df_trade, sig_area, type_val):
    
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
    return fig

# 공원 갯수
def park_count(park_raw, sig_area):
    
    public_park_df = park_raw[park_raw['시도명'] == sig_area]
    public_park_df = public_park_df.reset_index(drop=True)        
    
    public_park_df = public_park_df[['시군구명','공원구분','공원명']].groupby(['시군구명','공원구분']).describe()
    public_park_df = public_park_df.reset_index()
    
    public_park_df2 = pd.concat([public_park_df[['시군구명','공원구분']],public_park_df['공원명'][['count']]], axis = 1)
    public_park_df2.columns = ['시군구명','공원구분','count']
    
    fig = go.Figure()
    
    key_list = public_park_df2['공원구분'].unique()
    
    for key in key_list:
        fig.add_trace(go.Bar(
          name = key,
          x=public_park_df2[public_park_df2['공원구분'] == key]['시군구명'],
          y=public_park_df2[public_park_df2['공원구분'] == key]['count'],
          hovertemplate='%{y}개'
            )
        )

    fig.update_layout(
        title= f'{sig_area} 시군구별 도시 공원 개수 <br><sup>단위(개)</sup>',
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
        barmode='stack'
    )

    return fig
# 공원 지도
def park_geo(park_raw, sig_area):
    
    public_park_df = park_raw[park_raw['시도명'] == sig_area]
    
    fig = px.scatter_mapbox(public_park_df,
                            lat="위도",
                            lon="경도",
                            color="공원구분",
                            hover_data={
                                "위도" : False,
                                "경도" : False,
                              "공원명" : True,
                              "공원구분": True,
                              "소재지도로명주소": True,
                                "관리기관명" : True,
                                "전화번호" : True
                              },
                            zoom = 10,
                            title = f'{sig_area} 시군구별 도시 공원 위치',
                              )

    fig.update_layout(
      mapbox_style="carto-positron",
      margin={"r":0,"t":50,"l":0,"b":0},
      hoverlabel=dict(
        bgcolor='white',
        font_size=15,
        ),
        template='plotly_white'
      )
        
    return fig

# 각 시군구별 평균 거래 금액 지도로 표현
def trade_mean_map(apart_trans, geo_json ,sig_lat_lon, sig_area, year_option, month_option ,type_val, type_option):
  
    # 타입 별 이름
    type_dic = {'apt':'아파트','offi':'오피스텔'}
    type_nm = type_dic[type_option]

    apart_trans2 = apart_trans[apart_trans['시도명'] == sig_area]
    apart_trans2 = apart_trans2[apart_trans2['년'] == year_option]
    apart_trans2 = apart_trans2[apart_trans2['월'] == month_option]
    apart_trans3 = apart_trans2[apart_trans2['구분'] == type_val]
    apart_trans4 = apart_trans3[apart_trans2['타입'] == type_option].reset_index(drop = True)
    
    sig_lat_lon2 = sig_lat_lon[sig_lat_lon['sig_nm'] == sig_area].reset_index(drop = True)
    
    apart_trans4['거래금액_int'] = apart_trans4['거래금액'].astype(int)
    apart_trans4['거래금액'] = apart_trans4['거래금액_int'].apply(readNumber)
        
    fig = px.choropleth_mapbox(apart_trans4, 
                               geojson=geo_json, 
                               color="거래금액_int",
                               color_continuous_scale="Reds",
                               hover_data={
                                   "SIG_CD" : False,
                                   "시도명" : True,
                                   "시군구명" : True,
                                   "구분": False,
                                   "타입": False,
                                   "거래금액": True,
                                   "거래금액_int": False
                               },
                               locations="SIG_CD", 
                               featureidkey="properties.SIG_CD",
                               center={"lat":sig_lat_lon2['long'][0], 
                                       "lon":sig_lat_lon2['lat'][0]},
                               mapbox_style="carto-positron",
                               zoom=9)
    
    fig.update_layout(
      margin={"r":0,"t":50,"l":0,"b":0},
      title = f'{sig_area} 시군구별 {type_nm} {type_val} 거래금액 지도 ({year_option}년 {month_option}월 기준)',
      title_font_family="맑은고딕",
      title_font_size = 18,
      hoverlabel=dict(
        bgcolor='white',
        font_size=15,
        ),
        template='plotly_white'
      )
      
    return fig  

# 각 시도별 거래량 지도로 표현
def map_trade(df_total, trade_option,
              amount_value_0,amount_value_1, 
              area_value_0, area_value_1, 
              year_value_0, year_value_1,
              floor_value_0, floor_value_1,
              sig_area, type_option,
              year_option, month_option):
    
    # 타입 별 이름
    type_dic = {'apt':'아파트','offi':'오피스텔'}
    type_nm = type_dic[type_option]
    
     # '건축년도' 열(column)의 '없음' 값을 NaN(누락된 값)으로 대체
    df_total['건축년도'] = pd.to_numeric(df_total['건축년도'], errors='coerce')
    # NaN 값이 있는 행 제거
    df_total.dropna(subset=['건축년도'], inplace=True)
    # '건축년도' 열(column)의 데이터 타입을 정수형(int)으로 변경
    df_total['건축년도'] = df_total['건축년도'].astype('int')
    
    
    if(trade_option == '매매'):
           
        df_total_2 = df_total[
          (df_total['거래금액'] >= amount_value_0) & 
          (df_total['거래금액'] <= amount_value_1) &
          (df_total['전용면적'] >= area_value_0) & 
          (df_total['전용면적'] <= area_value_1) &
          (df_total['건축년도'] >= year_value_0) & 
          (df_total['건축년도'] <= year_value_1) & 
          (df_total['층'] >= floor_value_0) & 
          (df_total['층'] <= floor_value_1)
          ]
        df_total_2['거래금액_int'] = df_total_2['거래금액'].astype(int)
        df_total_2['거래금액'] = df_total_2['거래금액_int'].apply(readNumber)
        
        if('아파트' in df_total.columns):
            df_total_2['이름'] = df_total_2['아파트']
            fig = px.scatter_mapbox(df_total_2,
                                    lat="lat",
                                    lon="lon",
                                    hover_data={
                                      "lat" : False,
                                      "lon" : False,
                                      "이름" : True,
                                      "법정동": True,
                                      "거래금액": True,
                                      "거래금액_int": False,
                                      "전용면적":True,
                                      },
                                    color = '시군구명',
                                    size = '거래금액_int',
                                    height = 600,
                                    zoom=10)
        else:
            df_total_2['법정동'] = df_total_2['동리명']
            fig = px.scatter_mapbox(df_total_2,
                                    lat="lat",
                                    lon="lon",
                                    hover_data={
                                      "lat" : False,
                                      "lon" : False,
                                      "단지" : True,
                                      "동리명": True,
                                      "거래금액": True,
                                      "거래금액_int": False,
                                      "전용면적":True,
                                      },
                                    color = '시군구명',
                                    size = '거래금액_int',
                                    height = 600,
                                    zoom=10)            
        
    # 전세
    elif(trade_option == '전세') :
        
        if('아파트' in df_total.columns):
            df_total = df_total[df_total['월세금액'] == 0]   
            
            df_total_2 = df_total[
              (df_total['보증금액'] >= amount_value_0) & 
              (df_total['보증금액'] <= amount_value_1) &
              (df_total['전용면적'] >= area_value_0) & 
              (df_total['전용면적'] <= area_value_1) &
              (df_total['건축년도'] >= year_value_0) & 
              (df_total['건축년도'] <= year_value_1) & 
              (df_total['층'] >= floor_value_0) & 
              (df_total['층'] <= floor_value_1)
              ]

            df_total_2['보증금액_int'] = df_total_2['보증금액'].astype(int)
            df_total_2['보증금액'] = df_total_2['보증금액_int'].apply(readNumber)            
            
            df_total_2['이름'] = df_total_2['아파트']
            df_total_2['법정동'] = df_total_2['동리명']
        
            fig = px.scatter_mapbox(df_total_2,
                                    lat="lat",
                                    lon="lon",
                                    hover_data={
                                      "lat" : False,
                                      "lon" : False,
                                      "이름" : True,
                                      "법정동": True,
                                      '건축년도': True,
                                      "보증금액": True,
                                      "보증금액_int": False,
                                      "전용면적":True,
                                      },
                                    color = '시군구명',
                                    size = '보증금액_int',
                                    height = 600,
                                    zoom=10)
        else:     
            df_total = df_total[df_total['월세'] == 0]   
            
            df_total_2 = df_total[
              (df_total['보증금'] >= amount_value_0) & 
              (df_total['보증금'] <= amount_value_1) &
              (df_total['전용면적'] >= area_value_0) & 
              (df_total['전용면적'] <= area_value_1) &
              (df_total['건축년도'] >= year_value_0) & 
              (df_total['건축년도'] <= year_value_1) & 
              (df_total['층'] >= floor_value_0) & 
              (df_total['층'] <= floor_value_1)
              ]

            df_total_2['보증금_int'] = df_total_2['보증금'].astype(int)
            df_total_2['보증금'] = df_total_2['보증금_int'].apply(readNumber)
            
            df_total_2['법정동'] = df_total_2['동리명']
            fig = px.scatter_mapbox(df_total_2,
                                lat="lat",
                                lon="lon",
                                hover_data={
                                  "lat" : False,
                                  "lon" : False,
                                  "단지" : True,
                                  "법정동": True,
                                  '건축년도': True,
                                  "보증금": True,
                                  "보증금_int": False,
                                  "전용면적":True,
                                  },
                                color = '시군구명',
                                size = '보증금_int',
                                height = 600,
                                zoom=10)           
        
    elif(trade_option == '월세') :
        
        if('아파트' in df_total.columns):
            df_total = df_total[df_total['월세금액'] != 0]   
            
            df_total_2 = df_total[
              (df_total['보증금액'] >= amount_value_0) & 
              (df_total['보증금액'] <= amount_value_1) &
              (df_total['전용면적'] >= area_value_0) & 
              (df_total['전용면적'] <= area_value_1) &
              (df_total['건축년도'] >= year_value_0) & 
              (df_total['건축년도'] <= year_value_1) & 
              (df_total['층'] >= floor_value_0) & 
              (df_total['층'] <= floor_value_1)
              ]

            df_total_2['보증금액_int'] = df_total_2['보증금액'].astype(int)
            df_total_2['보증금액'] = df_total_2['보증금액_int'].apply(readNumber)              
            
            df_total_2['이름'] = df_total_2['아파트']
            df_total_2['법정동'] = df_total_2['동리명']
        
            fig = px.scatter_mapbox(df_total_2,
                                    lat="lat",
                                    lon="lon",
                                    hover_data={
                                      "lat" : False,
                                      "lon" : False,
                                      "이름" : True,
                                      "법정동": True,
                                      '건축년도': True,
                                      "보증금액": True,
                                      "월세금액": True,
                                      "보증금액_int": False,
                                      "전용면적":True,
                                      },
                                    color = '시군구명',
                                    size = '보증금액_int',
                                    height = 600,
                                    zoom=10)
        else:
            df_total = df_total[df_total['월세'] != 0]   
            
            df_total_2 = df_total[
              (df_total['보증금'] >= amount_value_0) & 
              (df_total['보증금'] <= amount_value_1) &
              (df_total['전용면적'] >= area_value_0) & 
              (df_total['전용면적'] <= area_value_1) &
              (df_total['건축년도'] >= year_value_0) & 
              (df_total['건축년도'] <= year_value_1) & 
              (df_total['층'] >= floor_value_0) & 
              (df_total['층'] <= floor_value_1)
              ]

            df_total_2['보증금_int'] = df_total_2['보증금'].astype(int)
            df_total_2['보증금'] = df_total_2['보증금_int'].apply(readNumber)
            
            df_total_2['법정동'] = df_total_2['동리명']
            fig = px.scatter_mapbox(df_total_2,
                                lat="lat",
                                lon="lon",
                                hover_data={
                                  "lat" : False,
                                  "lon" : False,
                                  "단지" : True,
                                  "법정동": True,
                                  '건축년도': True,
                                  "보증금": True,
                                  "월세" : True,
                                  "보증금_int": False,
                                  "전용면적":True,
                                  },
                                color = '시군구명',
                                size = '보증금_int',
                                height = 600,
                                zoom=10)
        
    fig.update_layout(
      margin={"r":0,"t":50,"l":0,"b":0},
      title = f'{sig_area} 시군구별 {type_nm} {trade_option} 거래 데이터 지도 ({year_option}년 {month_option}월 기준)',
      title_font_family="맑은고딕",
      title_font_size = 18,
      mapbox_style="carto-positron",
      coloraxis_showscale=False,
      showlegend=False,
      hoverlabel=dict(
        bgcolor='white',
        font_size=15,
        ),
        template='plotly_white'
      )
      
    return fig