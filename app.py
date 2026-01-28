import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="수려한치과 오버타임", layout="centered")
st.title("🦷 수려한치과 오버타임 기록기")

# 구글 시트 연결 함수
@st.cache_resource
def get_client():
    # 금고(Secrets)에서 열쇠 정보를 가져옵니다.
    info = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(info)
    return gspread.authorize(creds)

try:
    client = get_client()
    # 시트 이름과 일치해야 합니다.
    sheet = client.open("수려한치과 오버타임").sheet1 
    st.success("✅ 시스템 정상 연결됨")
except Exception as e:
    st.error("⚠️ 연결 대기 중: 스트림릿 Secrets 설정을 완료해 주세요.")

# 입력 양식
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
                st.success(f"{name} 님, 기록 완료!")
            except Exception as e:
                st.error(f"저장 실패: {e}")
        else:
            st.warning("성함과 사유를 입력해 주세요.")