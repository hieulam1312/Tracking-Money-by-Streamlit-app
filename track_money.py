import streamlit as st
import numpy as np
import pandas as pd 
from datetime import datetime as dt 
import gspread
import gspread_dataframe as gd
from gspread_dataframe import set_with_dataframe
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
from list_name import _list_t,_list_c,A,T,C

# Function to push data into Google Spreadsheets
def push_data(data):
    scope=['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    credentials=service_account.Credentials.from_service_account_info(
        st.secrets['gcp_service_account'],
        scopes=['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive'],)
    gc=gspread.authorize(credentials)
    sheet=gc.open('FIRE - journey').worksheet('Track_2021')
    sh_df=gd.get_as_dataframe(sheet)
    updated=sh_df.append(data)
    gd.set_with_dataframe(sheet,updated)
    st.success("Hiếu làm được rồi nè!!")

#
if 'count' not in st.session_state:
    st.session_state.count = 0

def increment_counter(increment_value=0):
    st.session_state.count += increment_value

def decrement_counter(decrement_value=0):
    st.session_state.count -= decrement_value

#Main app

c1,c2=st.columns(2)
with c1:
    a= st.selectbox('Nguồn',A)
with c2:
    L=T if a =="Thu" else C
    l=st.selectbox('Loại tiền',L)
    c=_list_c[L.index(l)] if a=="Chi" else _list_t[L.index(l)]
cc=st.selectbox('Loại chi tiêu',c)
r1,r2=st.columns(2)
with r1:
    ct=[st.text_input('Tên chi tiết')]
    for n in range(st.session_state.count):
        ct.append(st.text_input(label='', key=f'Question {n}'))
with r2:
    mn=[st.number_input('Số tiền',step=1000)]
    for n in range(st.session_state.count):
            mn.append(st.number_input(label='',step=1000, key=f'Questiosdsdn {n}'))
c1,c2,c3,c4,c5=st.columns((1,1,1,2,2))
with c1:
    st.button('Thêm dòng', on_click=increment_counter,
        kwargs=dict(increment_value=1))
with c2:
    st.button('Giảm dòng', on_click=decrement_counter,
        kwargs=dict(decrement_value=1))
with c4:
    st.write('Tổng số dòng = ', st.session_state.count+1)
h=st.session_state.count
df=[]
dict={}
if st.button('Hoàn tất'):
    dict={'Tên chi tiết':ct,'Số tiền':mn}
    df=pd.DataFrame.from_dict(dict)
    df['Nguồn']=a
    df['Nhóm']=l
    df['Danh mục']=cc
    df['Ngày']=pd.to_datetime(('today'))
    df
    push_data(df)
