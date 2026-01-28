import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="수려한치과 오버타임 기록기", layout="centered")
st.title("🦷 수려한치과 오버타임 기록기")

# 2. 구글 시트 연결 (key.json 파일 사용)
@st.cache_resource
def get_gspread_client():
    json_file = 'key.json' 
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
    return gspread.authorize(creds)

try:
    client = get_gspread_client()
    # 구글 시트 제목이 '수려한치과 오버타임'인지 확인하세요
    sheet = client.open("수려한치과 오버타임").sheet1 
    st.info("입력하신 데이터는 병원 관리 구글 시트에 실시간 저장됩니다.")
except Exception as e:
    st.error(f"연결 오류가 발생했습니다: {e}")

# 3. 입력 양식
with st.form("overtime_form"):
    name = st.text_input("직원 성함", placeholder="이름 입력")
    
    col1, col2 = st.columns(2)
    with col1:
        start_time = st.time_input("시작 시간", value=datetime.strptime("18:30", "%H:%M").time())
    with col2:
        end_time = st.time_input("종료 시간", value=datetime.strptime("19:00", "%H:%M").time())
    
    reason = st.text_area("사유", placeholder="사유 입력 (예: 잔류 환자 응대)")
    
    submit = st.form_submit_button("오버타임 기록 제출하기")

if submit:
    if name:
        try:
            date_str = datetime.now().strftime("%Y-%m-%d")
            new_row = [date_str, name, str(start_time), str(end_time), reason]
            sheet.append_row(new_row)
            st.balloons()
            st.success(f"{name} 님, 기록이 완료되었습니다!")
        except Exception as e:
            st.error(f"저장 오류: {e}")
    else:
        st.warning("이름을 입력해주세요.")
