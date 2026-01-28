import streamlit as st
import gspread
from google.oauth2.service_account import Credentials # 최신형 도구
from datetime import datetime

st.set_page_config(page_title="수려한치과 오버타임", layout="centered")
st.title("🦷 수려한치과 오버타임 기록기")

@st.cache_resource
def get_client():
    # 최신 구글 보안 표준에 맞춘 연결 방식입니다
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    # key.json 파일에서 정보를 읽어옵니다
    creds = Credentials.from_service_account_file("key.json", scopes=scopes)
    return gspread.authorize(creds)

try:
    client = get_client()
    # 시트 제목 확인: '수려한치과 오버타임'
    sheet = client.open("수려한치과 오버타임").sheet1 
    st.success("✅ 시스템 정상 연결됨 (최신 보안 모드)")
except Exception as e:
    st.error(f"오류 발생: {e}")

with st.form("overtime_form", clear_on_submit=True):
    name = st.text_input("직원 성함")
    col1, col2 = st.columns(2)
    with col1:
        start_time = st.time_input("시작", value=datetime.strptime("18:30", "%H:%M").time())
    with col2:
        end_time = st.time_input("종료", value=datetime.strptime("19:00", "%H:%M").time())
    reason = st.text_area("사유")
    
    if st.form_submit_button("제출하기"):
        if name and reason:
            try:
                date_str = datetime.now().strftime("%Y-%m-%d")
                sheet.append_row([date_str, name, str(start_time), str(end_time), reason])
                st.balloons()
                st.success("저장되었습니다!")
            except Exception as e:
                st.error(f"저장 실패: {e}")
        else:
            st.warning("내용을 입력해주세요.")
