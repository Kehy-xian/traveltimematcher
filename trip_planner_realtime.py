# detective_code_v2.py

import streamlit as st

st.set_page_config(page_title="🕵️‍♀️ 비밀 키 정밀 탐정", layout="wide")
st.title("🕵️‍♀️ 비밀 키 정밀 탐정 모드")
st.write("---")

st.write("Streamlit Cloud의 Secrets에 저장된 'GOOGLE_APPLICATION_CREDENTIALS' 값을 정밀 분석합니다.")
st.info("이 작업은 문제 해결을 위한 일시적인 단계이며, 해결 즉시 원래 코드로 복구할 것입니다.")

try:
    # Secrets에서 값을 문자열로 그대로 가져옴
    secret_value = st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]
    
    st.success("Secrets 값을 성공적으로 불러왔습니다! 아래 내용을 분석해주세요.")
    
    st.write("### 1. 앱이 보는 그대로의 값 (Raw Text)")
    st.text(secret_value)

    st.write("### 2. 컴퓨터가 이해하는 내부 표현 (Representation)")
    st.code(repr(secret_value), language="python")


except Exception as e:
    st.error("Secrets 값을 불러오는 데 실패했습니다.")
    st.error(f"오류 내용: {e}")
