import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

st.title("멀티턴 챗봇📢")
#인공지능 모델 설정
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-pro')

#mturn을 위한 대화 저장
if 'history' not in st.session_state:
    st.session_state.history = []

#기존 대화를 위한 저장
if 'talk' not in st.session_state:
    st.session_state.talk = []

#기존의 대화 출력
for message in st.session_state.talk:
    with st.chat_message(message['role']):
        st.write(message['parts'])

#새로운 메시지 생성
prompt = st.chat_input("메시지를 입력하세요 : ")
if prompt:
    with st.chat_message("user"):
        st.session_state.history.append({
            'role':"user",
            'parts':prompt
        }) #새로운 대화를 위한 세션
        st.session_state.talk.append({
            'role':'user',
            'parts':prompt
        }) #기존 대화를 출력하기 위한 세션
        st.write(prompt)
    response = model.generate_content(st.session_state.history)
    st.session_state.history.append(response.candidates[0].content)

    with st.chat_message('ai'):
        st.session_state.talk.append({
            'role':"ai",
            'parts':response.text
            })
        st.write(response.text)
