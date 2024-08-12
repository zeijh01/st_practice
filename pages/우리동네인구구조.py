import streamlit as st
import matplotlib.pyplot as plt
import koreanize_matplotlib
import pandas as pd
import csv

#폰트
#plt.rc('font',family='Malgun Gothic')


f= open('age.csv',encoding='cp949')
data = csv.reader(f)
header = next(data)
data = list(data)

st.write("### 우리동네와 비슷한 :green[인구구조 찾기 프로젝트] :airplane:")
with st.sidebar:
    st.markdown("### :newspaper:데이터 파일 준비하기:newspaper:")
    st.markdown('사이트 접속하기 -> <a href="https://www.mois.go.kr/frt/a01/frtMain.do" target="_blank">행정안전부</a>', unsafe_allow_html=True)
    st.error("""
    1. 상단 메뉴에서 정책자료 ->   
       통계 -> 주민등록 인구통계 ->   
       연령별 인구현황   
    2. 남.여 구분 체크 해제//   
       연령 구분단위 1세//   
       만 연령구분 0 ~ 100이상     
    3. 연령별 인구현황 표시 후   
       전체읍면동현황에 체크 한 후   
       csv파일 다운   
    4. 파일 데이터 수정   
       (자릿수 , 제거)
    """)

step1,step2,step3,step4,step5,step6,step7 = st.tabs(['step1','step2','step3','step4','step5','step6','step7'])

#step1 광명고등학교가 있는 '철산3동' 이름이 포함된 지역의 인구 구조 그래프 그리기
result = []
for row in data:
    if '철산3동' in row[0]:
        for i in range(3,104) :
            result.append(int(row[i]))
fig, ax = plt.subplots(figsize=(10,2))
ax.plot(result,label='철산3동',color = 'red',linestyle='--')
ax.set_title("우리동네 그래프")
ax.legend()
with step1: 
    st.write(fig)

#step2 다른 지역과 인구 구조 비교하기
result = []
result2 = []
for row in data :
    if '철산3동' in row[0] :
        for i in range(3,len(row)) : 
            result.append(int(row[i]))
    if '부천동' in row[0] :
        for i in range(3,len(row)) : 
            result2.append(int(row[i]))
fig2, ax2 = plt.subplots(figsize=(10,3))
ax2.plot(result,label = '철산3동')
ax2.plot(result2,label = '부천동')
ax2.legend()
ax2.set_title("인구 구조 비교하기")
with step2:
    st.pyplot(fig2)

#step3 다른 지역과의 차이 비교를 위해 비율로 표현하기
result = []
result2 = []
for row in data:
    if '철산3동' in row[0]:
        for i in range(3,len(row)):
            result.append(int(row[i])/int(row[2]))
    if '부천동' in row[0]:
        for i in range(3,len(row)):
            result2.append(int(row[i])/int(row[2]))

fig3, ax3 = plt.subplots(figsize=(10,3))
ax3.plot(result, label = '철산3동')
ax3.plot(result2,label = '부천동')
ax3.legend()
ax3.set_title("비율로 비교하기")
with step3:
    st.pyplot(fig3)

#step4 오차값 계산하기
pivot = []
name = ''
for row in data:
    if row[2] == '0':
        continue
    if '철산3동' in row[0]:
        for i in range(3,len(row)):
            pivot.append(int(row[i])/int(row[2]))
mn = 99999999

for row in data:
    if row[2] == '0':
        continue
    s = 0
    for i in range(3,len(row)):
        tmp = pivot[i-3]-(int(row[i])/int(row[2]))
        s += tmp
    if s < mn:
        mn = s
        result = []
        name = row[0].split(" ")[-1]
        for i in range(3,len(row)):
            result.append(int(row[i])/int(row[2]))
        

fig4, ax4 = plt.subplots(figsize=(10,3))
ax4.plot(pivot,label = "철산3동")
ax4.plot(result,label = name)
ax4.legend()
with step4:
    st.pyplot(fig4)

#step5 오차값 정확하게 계산하기
pivot = []
name = ''
for row in data:
    if row[2] == '0':
        continue
    if '철산3동' in row[0]:
        for i in range(3,len(row)):
            pivot.append(int(row[i])/int(row[2]))
mn = 99999999

for row in data:
    if row[2] == '0':
        continue
    s = 0
    for i in range(3,len(row)):
        tmp = (pivot[i-3]-(int(row[i])/int(row[2])))**2
        s += tmp
    if s < mn:
        mn = s
        result = []
        name = row[0].split(" ")[-1]
        for i in range(3,len(row)):
            result.append(int(row[i])/int(row[2]))
        

fig5, ax5 = plt.subplots(figsize=(10,3))
ax5.plot(pivot,label = "철산3동")
ax5.plot(result,label = name)
ax5.legend()
with step5:
    st.pyplot(fig5)
    st.markdown('##### 그래프가 하나만 그려지는 이유는?')
    if st.button("정답을 알려줘"):
        st.info("자기 자신은 오차가 0으로 가장 작음")


#step6 철산3동을 제외한 인구구조가 비슷한 지역 찾기
pivot = []
name = ''
for row in data:
    if row[2] == '0':
        continue
    if '철산3동' in row[0]:
        for i in range(3,len(row)):
            pivot.append(int(row[i])/int(row[2]))
mn = 99999999

for row in data:
    if row[2] == '0':
        continue
    s = 0
    for i in range(3,len(row)):
        tmp = (pivot[i-3]-(int(row[i])/int(row[2])))**2
        s += tmp
    if s < mn and "철산3동" not in row[0]:
        mn = s
        result = []
        name = row[0].split(" ")[-1]
        for i in range(3,len(row)):
            result.append(int(row[i])/int(row[2]))

fig6, ax6 = plt.subplots(figsize=(10,3))
ax6.plot(pivot,label = "철산3동")
ax6.plot(result,label = name)
ax6.legend()
with step6:
    st.pyplot(fig6)


#step7 인구구조가 비슷한 지역 찾기
pivot = []
name = ''
with step7:
    st.markdown("### 지역 이름을 입력하세요")
    mycity = st.text_input("",placeholder="철산3동")
    if mycity:
        for row in data:
            if row[2] == '0':
                continue
            if mycity in row[0]:
                for i in range(3,len(row)):
                    pivot.append(int(row[i])/int(row[2]))
        mn = 99999999
        for row in data:
            if row[2] == '0':
                continue
            s = 0
            for i in range(3,len(row)):
                tmp = (pivot[i-3]-(int(row[i])/int(row[2])))**2
                s += tmp
            if s < mn and mycity not in row[0]:
                mn = s
                result = []
                name = row[0].split(" ")[-1]
                for i in range(3,len(row)):
                    result.append(int(row[i])/int(row[2]))

        fig7, ax7 = plt.subplots(figsize=(10,3))
        ax7.plot(pivot,label = mycity)
        ax7.plot(result,label = name)
        ax7.legend()
        st.pyplot(fig7)
