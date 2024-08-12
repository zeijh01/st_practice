import streamlit as st
import json
import requests
import time, datetime
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

url = 'https://open.neis.go.kr/hub/'
service_key = os.getenv('EDU_API_KEY')
office_Education_list = ['강원특별자치도교육청','경기도교육청','경상남도교육청',
                         '경상북도교육청','광주광역시교육청','대구광역시교육청',
                         '대전광역시교육청','부산광역시교육청','서울특별시교육청',
                         '세종특별자치시교육청','울산광역시교육청','인천광역시교육청',
                         '재외교육지원담당관실','재외한국학교교육청','전라남도교육청',
                         '전라북도교육청','전북특별자치도교육청','제주특별자치도교육청',
                         '충청남도교육청','충청북도교육청'
                         ]
# def get_office_Education():
#     office_Educations = set()
    
#     for pIndex in range(1, 15):
#         params = {
#             'KEY' : service_key,
#             'Type' : 'json',
#             'pSize' : 1000,
#             'pIndex' : pIndex
#         }
        
#         response = requests.get(url+'schoolInfo', params=params)
#         if response.status_code != 200:
#             print(f"Failed to get data for pIndex {pIndex}")
#             continue
        
#         data = json.loads(response.text)
#         if 'schoolInfo' not in data:
#             print(f"No schoolInfo found in response for pIndex {pIndex}")
#             continue

#         for schoolInfo in data['schoolInfo'][1]['row']:
#             office_Educations.add(schoolInfo['ATPT_OFCDC_SC_NM'])
            
#     office_Educations = list(office_Educations)
#     office_Educations.sort()
#     return office_Educations


def get_menus(school_name, office_Education,day=datetime.date.today().strftime('%Y%m%d')):
    
    params = {
    'KEY' : service_key,
    'Type' : 'json',
    }

    info_url = url+'schoolInfo'

    params.update({'SCHUL_NM':school_name})
    params.update({'MLSV_YMD':day})
    response = requests.get(info_url,params=params)
    
    s_code= json.loads(response.text)
    for schoolinfo in s_code['schoolInfo'][1]['row']:
        if schoolinfo['ATPT_OFCDC_SC_NM'] == office_Education:
            params.update({'ATPT_OFCDC_SC_CODE':schoolinfo['ATPT_OFCDC_SC_CODE']})
            params.update({'SD_SCHUL_CODE':schoolinfo['SD_SCHUL_CODE']})

    response = requests.get(url+'mealServiceDietInfo',params=params)
    menus= json.loads(response.text)
    menu = []
    for i in menus['mealServiceDietInfo'][1]['row'][0]['DDISH_NM'].split('<br/>'):
        menu.append(i.split(' ')[0])

    return menu


#streamlit 화면구성
con1,con2 = st.columns([3,1])
with con1 :
    st.title('우리학교 급식 알리미🍙')
with con2 :
    ''
    ''
    start_button = st.button('급식 알려줘!')
st.info('''
        ##### 1. 소속 교육청을 선택하세요😊   
        ##### 2. 소속학교를 입력하세요🏫   
        ##### 3. 궁금한 날짜를 입력하세요📆   
        ##### 4. :blue[우리학교 급식 알리미] 옆 :red[버튼]을 누르세요🙏   
        ''')
'---'    
office_Education = st.selectbox(
    '소속 교육청을 선택하세요 : ',
    office_Education_list,
#    (get_office_Education()),
    index=None,
    placeholder='교육청을 선택하세요'
    )
school_name = st.text_input('소속학교를 입력하세요',placeholder='학교명을 입력하세요')
meal_date = st.date_input('원하는 급식 날짜')
'---'
if start_button:
    st.write(f'#### :green[{meal_date}] :blue[{school_name}] 의 급식메뉴')
    df = pd.DataFrame(get_menus(school_name,office_Education,day=meal_date.strftime('%Y%m%d')))
    st.dataframe(df)



