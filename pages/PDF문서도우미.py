from langchain_community.document_loaders import PyPDFLoader #1
from langchain_text_splitters import RecursiveCharacterTextSplitter #2
from langchain_google_genai import GoogleGenerativeAIEmbeddings #3
from langchain_community.vectorstores import FAISS #4
from langchain_community.vectorstores.utils import DistanceStrategy #4
from langchain_core.runnables import RunnablePassthrough #5
from langchain_core.prompts import PromptTemplate #6
from langchain_google_genai import ChatGoogleGenerativeAI #7
from langchain_core.output_parsers import StrOutputParser #7
import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()

# 캐시 디렉토리 생성
if not os.path.exists(".cache"):
    os.mkdir(".cache")

#화면구성
st.title('PDF문서 응답📜')
st.info('''
        ##### 챗봇소개💬   
        ###### 업로드한 :green[pdf파일]에 대하여 질의하면 :blue[업로드한 파일을 참고해서] 답변합니다.
        ''')

'---'
# 파일 업로드
uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type="pdf")
'---'
st.write('#### 궁금한 것을 물어보세요')
question = st.text_input('',placeholder='pdf내용과 관련된 질문 입력')

#step1 문서로드
if uploaded_file is not None:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())  # 업로드한 파일을 임시 파일로 저장

    loader = PyPDFLoader("temp.pdf")
    pages = loader.load()

    #step2 문서분할
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400, #(['\n\n', '\n', ' ', ''])문자를 순서대로 사용하여 텍스트를  chunk_size보다 작아질 때까지 분할
        chunk_overlap=50, #분할된 텍스트 조각들 사이에서 중복으로 포함될 문자 수
        length_function = len
    )
    split_documents = text_splitter.split_documents(pages)

    #step3 임베딩
    embeddings_model = GoogleGenerativeAIEmbeddings(model='models/embedding-001')

    

    #step4 벡터 스토어
    vectorstore = FAISS.from_documents(
        documents=split_documents, 
        embedding=embeddings_model,
        distance_strategy = DistanceStrategy.COSINE #설정을 안하면 기본은 유클리드 유사도 검사 사용
    )

    #step5 검색기
    retriever = vectorstore.as_retriever()

#step6 프롬프트 생성
prompt = PromptTemplate.from_template(
    """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. 
Answer in Korean.

#Context: 
{context} 

#Question: 
{question} 

#Answer:"""
)

if 'retriever' in locals() and question != '' :
    #step7 언어모델 생성
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )
    chain = prompt | llm | StrOutputParser

    #step8 체인생성
    chain = (
        {"context":retriever, "question":RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    with st.spinner('기다려주세요...'):
        answer = chain.invoke(question)
        st.error(answer)


