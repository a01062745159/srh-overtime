import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

st.set_page_config(page_title="수려한치과 기록기", layout="centered")
st.title("🦷 수려한치과 오버타임 기록기")

@st.cache_resource
def get_client():
    # 파일명이 정확히 key.json 이어야 함
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)
    return gspread.authorize(creds)

try:
    client = get_client()
    # 시트 제목이 정확히 일치해야 함
    sheet = client.open("수려한치과 오버타임").sheet1
    st.success("✅ 시스템 연결 완료!")
except Exception as e:
    st.error(f"연결 오류: {e}")

with st.form("my_form"):
    name = st.text_input("직원 성함")
    reason = st.text_area("사유")
    # 시간 입력은 간단하게 숫자로
    over_min = st.number_input("추가 근무 시간(분)", min_value=0, step=10, value=30)
    
    submitted = st.form_submit_button("제출하기")
    if submitted:
        if name and reason:
            try:
                date_str = datetime.now().strftime("%Y-%m-%d")
                sheet.append_row([date_str, name, f"{over_min}분", reason])
                st.balloons()
                st.success("기록되었습니다!")
            except Exception as e:
                st.error(f"저장 실패: {e}")
        else:
            st.warning("이름과 사유를 입력하세요.")
