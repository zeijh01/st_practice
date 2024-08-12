import streamlit as st
import numpy as np 
from PIL import Image
import opencv-python as cv2 

def dodgeV2(img, mask):  #두 이미지를 결합하여 하이라이트 부분을 강조
    return cv2.divide(img, 255 - mask, scale=256)

def pencilsketch(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(gray) 
    smoothing = cv2.GaussianBlur(invert, (21, 21),sigmaX=0, sigmaY=0)
    final_img = dodgeV2(gray, smoothing)
    return(final_img)
#회색조 변환 -> 이미지 반전 -> 가우시안블러 -> 하이라이트 부분 강조(회색조, 가우시안블러)

#세션 버튼 생성
if 'web_button' not in st.session_state:
    st.session_state.web_button = False
if 'upload_button' not in st.session_state:
    st.session_state.upload_button = False

img = False
st.title('연필스캐치 📷')
st.info('''
        ##### A. :green[웹캠]으로 찍은 사진을 연필스캐치로 변환해 줍니다.
        ##### B. :green[업로드한 이미지 파일]을 연필스캐치로 변환해 줍니다.
        ##### 웹캠이나 업로드를 선택해주세요
        ''')
'---'
but1, but2 = st.columns(2)
with but1:
    if st.button('웹캠사용'):
        st.session_state.web_button = True
        st.session_state.upload_button = False
with but2:
    if st.button('업로드 사용'):
        st.session_state.upload_button = True
        st.session_state.web_button = False


if st.session_state.web_button:
    st.write('#### 사진촬영하기✌️')
    img = st.camera_input('')

if st.session_state.upload_button:
    st.write('#### 사진업로드하기✌️')
    img = st.file_uploader("", type=['jpeg','jpg','png'])

    
if img:
    input_img = Image.open(img)
    final_sketch = pencilsketch(np.array(input_img)) #cvt는 백터값으로 연산처리
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("원본사진📷")
        st.image(input_img, use_column_width=True)
        
    with col2:
        st.write("연필스케치✏️")
        st.image(final_sketch, use_column_width=True)
   
st.write("[알고리즘 참고](https://github.com/amrrs/youtube-r-snippets/blob/master/Create_a_Pencil_Sketch_Portrait_with_Python_OpenCV.ipynb)")
