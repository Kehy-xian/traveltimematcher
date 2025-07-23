# detective_code.py

import streamlit as st

st.title("🕵️‍♀️ 비밀 키 탐정 모드")

st.write("Streamlit Cloud의 Secrets에 저장된 'GOOGLE_APPLICATION_CREDENTIALS' 값을 확인합니다.")
st.write("---")

try:
    # Secrets에서 값을 문자열로 그대로 가져옴
    secret_value = st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]
    
    st.success("Secrets 값을 성공적으로 불러왔습니다! 내용은 아래와 같습니다.")
    
    # 가져온 값을 코드 블록으로 화면에 그대로 표시
    st.code(secret_value, language="json")

except Exception as e:
    st.error("Secrets 값을 불러오는 데 실패했습니다.")
    st.error(f"오류 내용: {e}")
