# trip_planner_realtime.py (진짜진짜 최종본)

import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from streamlit_calendar import calendar
import datetime
import json

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="실시간 여행 작전 보드", page_icon="👑", layout="wide")

# --- Firebase 연결 (줄바꿈 오류 해결!) ---
try:
    creds_json_str = st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]
    creds_dict = json.loads(creds_json_str)

    if not firebase_admin._apps:
        cred = credentials.Certificate(creds_dict)
        firebase_admin.initialize_app(cred)

except Exception as e:
    st.error("앗! Firebase 연결에 실패했어요. Streamlit Cloud의 Secrets 설정을 다시 확인해주세요.")
    st.error(f"자세한 오류: {e}")
    st.stop()

# Firestore 클라이언트 초기화
db = firestore.client()
events_ref = db.collection('schedules')

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
