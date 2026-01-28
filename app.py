import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

st.set_page_config(page_title="기록기", layout="centered")

@st.cache_resource
def get_client():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    # GitHub에 올린 key.json을 직접 읽습니다.
    return gspread.authorize(ServiceAccountCredentials.from_json_keyfile_name('key.json', scope))

try:
    client = get_client()
    # 시트 제목을 정확하게 적어주세요! (예: 수려한치과 오버타임)
    sheet = client.open("수려한치과 오버타임").sheet1
    st.success("✅ 시스템 연결 완료!")
except Exception as e:
    st.error(f"연결 오류: {e}")

with st.form("form"):
    name = st.text_input("직원 성함")
    reason = st.text_area("사유")
    time = st.number_input("시간(분)", min_value=0, value=30, step=10)
    if st.form_submit_button("제출하기"):
        if name and reason:
            sheet.append_row([datetime.now().strftime("%Y-%m-%d"), name, f"{time}분", reason])
            st.balloons()
            st.success("기록되었습니다!")
