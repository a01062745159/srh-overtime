import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- Google Sheets 연결 ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

gc = gspread.authorize(credentials)
spreadsheet = gc.open_by_key("스프레드시트_ID")
worksheet = spreadsheet.sheet1

# --- 화면 ---
st.title("오버타임 기록 입력")

name = st.text_input("직원 이름")

col1, col2 = st.columns(2)
with col1:
    start_hour = st.number_input("시작 시간", min_value=0, max_value=23, step=1)
    start_min = st.number_input("시작 분", min_value=0, max_value=59, step=1)

with col2:
    end_hour = st.number_input("종료 시간", min_value=0, max_value=23, step=1)
    end_min = st.number_input("종료 분", min_value=0, max_value=59, step=1)

reason = st.text_area("오버타임 사유")

if st.button("제출"):
    if name and reason:
        start_time = f"{start_hour:02d}:{start_min:02d}"
        end_time = f"{end_hour:02d}:{end_min:02d}"

        worksheet.append_row([
            datetime.now().strftime("%Y-%m-%d"),
            name,
            start_time,
            end_time,
            reason,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])

        st.success("기록이 저장되었습니다 ✅")
    else:
        st.warning("직원 이름과 사유는 필수입니다")
