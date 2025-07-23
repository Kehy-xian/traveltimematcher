# trip_planner_realtime.py (진짜 최종본)

import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from streamlit_calendar import calendar
import datetime
import os

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="👑 실시간 여행 작전 보드", page_icon="👑", layout="wide")

# --- Firebase 연결 (가장 간단한 공식 방법!) ---
try:
    # GOOGLE_APPLICATION_CREDENTIALS는 Streamlit Cloud Secrets에서 설정할 예정
    # 이 코드는 주변에 비밀 목걸이(환경 변수)가 있는지 자동으로 찾아서 연결해요!
    if not firebase_admin._apps:
        firebase_admin.initialize_app()

except Exception as e:
    # 로컬에서 실행할 때는 GOOGLE_APPLICATION_CREDENTIALS를 직접 설정해야 함
    st.error("앗! Firebase 연결에 실패했어요. Streamlit Cloud에 Secret을 올바르게 설정했는지 확인해주세요!")
    st.error(f"자세한 오류: {e}")
    st.stop()

# Firestore 클라이언트 초기화
db = firestore.client()
events_ref = db.collection('schedules')

# --- (이하 나머지 코드는 이전과 동일) ---

# --- 함수 정의 ---
def load_events():
    docs = events_ref.stream()
    return [doc.to_dict() for doc in docs]

# --- 사이드바 UI ---
with st.sidebar:
    st.header("✨ 작전 준비")
    st.subheader("🗓️ '안 되는 날' 표시하기")
    
    selected_user = st.text_input("이름을 적어주세요", placeholder="예: 케이")
    unavailable_date = st.date_input("안 되는 날짜", datetime.date.today())
    
    if st.button("❌ 달력에 표시하기"):
        if not selected_user:
            st.warning("이름을 꼭 적어주셔야 해요!")
        else:
            event_id = f"{unavailable_date.isoformat()}-{selected_user}"
            event_doc = events_ref.document(event_id)
            
            if event_doc.get().exists:
                st.warning(f"{selected_user}님은 해당 날짜에 이미 안된다고 표시했어요!")
            else:
                new_event = {
                    "title": f"❌ {selected_user}", "color": "#FF6F6F",
                    "start": str(unavailable_date), "end": str(unavailable_date),
                    "allDay": True,
                }
                event_doc.set(new_event)
                st.success(f"{selected_user}님의 안 되는 날을 표시했어요!")
                st.rerun()

# --- 메인 화면 ---
st.title("👑 실시간 여행 작전 보드")
st.markdown("모두의 '안 되는 날'을 실시간으로 확인해요!")

events = load_events()
calendar(events=events, options={"locale": "ko"})

if st.button("🔄 새로고침"):
    st.rerun()