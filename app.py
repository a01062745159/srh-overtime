import streamlit as st
from datetime import datetime
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- [설정] 페이지 레이아웃 및 제목 ---
st.set_page_config(page_title="수려한치과 오버타임", layout="centered")

# --- [기능] 구글 시트 연결 함수 ---
@st.cache_resource
def get_google_sheet():
    # 같은 폴더에 있는 service_account.json 파일을 사용하여 인증합니다.
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(creds)
    
    # 구글 시트 제목 (반드시 시트 이름과 똑같아야 합니다)
    # 아직 시트를 안 만드셨다면 '수려한치과_오버타임_DB'라는 이름으로 만드세요.
    sheet = client.open("수려한치과_오버타임_DB").sheet1
    return sheet

st.title("🦷 수려한치과 오버타임 기록기")
st.info("입력하신 데이터는 병원 관리 구글 시트에 실시간 저장됩니다.")

# 1. 정보 입력 부분
input_name = st.text_input("직원 성함", placeholder="이름 입력", key="u_name")

st.divider()

col1, col2 = st.columns(2)
with col1:
    sh = st.number_input("시작 시", 0, 23, 18, key="sh_val")
    sm = st.number_input("시작 분", 0, 59, 30, key="sm_val")
with col2:
    eh = st.number_input("종료 시", 0, 23, 19, key="eh_val")
    em = st.number_input("종료 분", 0, 59, 0, key="em_val")

input_reason = st.text_area("사유", placeholder="사유 입력 (예: 잔류 환자 응대)", key="u_reason")

st.divider()

# 2. 계산 및 전송 로직
duration = (eh * 60 + em) - (sh * 60 + sm)

if st.button("오버타임 기록 제출하기"):
    if not input_name or not input_reason:
        st.error("성함과 사유를 모두 입력해 주세요!")
    elif duration <= 0:
        st.warning("종료 시간이 시작 시간보다 빨라 계산이 불가능합니다.")
    else:
        try:
            with st.spinner("구글 서버에 저장 중..."):
                # 구글 시트 접속 및 데이터 추가
                sheet = get_google_sheet()
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # 시트에 들어갈 행 데이터 [날짜, 이름, 시작, 종료, 분, 사유]
                row_data = [now, input_name, f"{sh}:{sm}", f"{eh}:{em}", duration, input_reason]
                sheet.append_row(row_data)
                
            st.success(f"✅ {input_name}님, {duration}분 기록이 완료되었습니다.")
            st.balloons()
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
            st.write("구글 시트 제목이 '수려한치과_오버타임_DB'인지, 그리고 로봇 이메일을 초대했는지 확인하세요.")