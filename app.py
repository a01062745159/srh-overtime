import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="수려한치과 오버타임 기록기", layout="centered")
st.title("🦷 수려한치과 오버타임 기록기")

# 2. 구글 시트 연결 (가장 안전한 파일 직접 읽기 방식)
@st.cache_resource
def get_gspread_client():
    # 깃허브에 올리신 파일 이름과 정확히 일치해야 합니다.
    json_file = 'service_account.json'
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
    return gspread.authorize(creds)

try:
    client = get_gspread_client()
    # 구글 시트 이름을 원장님이 만드신 이름으로 정확히 적어주세요.
    # 만약 시트 이름이 다르면 여기서 에러가 납니다.
    sheet = client.open("수려한치과 오버타임").sheet1 
    st.info("입력하신 데이터는 병원 관리 구글 시트에 실시간 저장됩니다.")
except Exception as e:
    st.error(f"연결 오류가 발생했습니다: {e}")
    st.write("구글 시트 제목이 '수려한치과 오버타임'인지 확인하세요.")

# 3. 입력 양식
with st.form("overtime_form"):
    name = st.text_input("직원 성함", placeholder="이름 입력")
    
    col1, col2 = st.columns(2)
    with col1:
        start_hour = st.number_input("시작 시", min_value=0, max_value=23, value=18)
        start_min = st.number_input("시작 분", min_value=0, max_value=59, value=30, step=10)
    with col2:
        end_hour = st.number_input("종료 시", min_value=0, max_value=23, value=19)
        end_min = st.number_input("종료 분", min_value=0, max_value=59, value=0, step=10)
    
    reason = st.text_area("사유", placeholder="사유 입력 (예: 잔류 환자 응대)")
    
    submit = st.form_submit_button("오버타임 기록 제출하기")

if submit:
    if name:
        try:
            # 시간 계산 및 데이터 정리
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            start_time = f"{start_hour:02d}:{start_min:02d}"
            end_time = f"{end_hour:02d}:{end_min:02d}"
            
            # 구글 시트에 한 줄 추가
            new_row = [date_str, name, start_time, end_time, reason]
            sheet.append_row(new_row)
            
            st.balloons()
            st.success(f"{name} 님, 기록이 완료되었습니다!")
        except Exception as e:
            st.error(f"저장 중 오류 발생: {e}")
    else:
        st.warning("이름을 입력해주세요.")
