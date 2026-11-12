import streamlit as st
import time
import pandas as pd

# --- Session State 초기화 (타이머용) ---
if 'running' not in st.session_state:
    st.session_state.running = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'elapsed_time' not in st.session_state:
    st.session_state.elapsed_time = 0
if 'subject_records' not in st.session_state:
    st.session_state.subject_records = {'국어': 0, '영어': 0, '수학': 0, '과학': 0, '사회': 0, '기타': 0}

# --- 현재 경과 시간 계산 함수 ---
def get_current_elapsed():
    if st.session_state.running and st.session_state.start_time is not None:
        return st.session_state.elapsed_time + (time.time() - st.session_state.start_time)
    return st.session_state.elapsed_time

# --- 시간 포맷팅 함수 ---
def format_time(seconds):
    mins, secs = divmod(int(seconds), 60)
    hours, mins = divmod(mins, 60)
    return f"{hours:02d}:{mins:02d}:{secs:02d}"

# ==========================================
# 사이드바 (메뉴 네비게이션)
# ==========================================
st.sidebar.title("📚 종합 학습 플래너")
menu = st.sidebar.radio("메뉴를 선택하세요:", ["공부타이머", "오늘 할 일", "공부회고"])

# ==========================================
# 1. 공부타이머 페이지
# ==========================================
if menu == "공부타이머":
    st.title("⏱️ 학생용 과목별 학습 타이머")
    
    # 과목 선택
    subjects = list(st.session_state.subject_records.keys())
    current_subject = st.selectbox("현재 학습할 과목을 선택하세요:", subjects)
    
    # 타이머 상태 표시
    st.markdown(f"### 현재 측정된 시간: **{format_time(get_current_elapsed())}**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("▶️ 시작", use_container_width=True):
            if not st.session_state.running:
                st.session_state.running = True
                st.session_state.start_time = time.time()
                st.rerun()
                
    with col2:
        if st.button("⏸️ 일시정지", use_container_width=True):
            if st.session_state.running:
                st.session_state.running = False
                st.session_state.elapsed_time += time.time() - st.session_state.start_time
                st.session_state.start_time = None
                st.rerun()
                
    with col3:
        if st.button("⏹️ 기록 저장 (초기화)", use_container_width=True):
            if st.session_state.running:
                st.session_state.elapsed_time += time.time() - st.session_state.start_time
                
            if st.session_state.elapsed_time > 0:
                st.session_state.subject_records[current_subject] += st.session_state.elapsed_time
                
            # 상태 리셋
            st.session_state.running = False
            st.session_state.start_time = None
            st.session_state.elapsed_time = 0
            st.rerun()
            
    st.divider()
    
    st.subheader("📚 과목별 누적 학습 시간")
    # 데이터프레임으로 변환해서 보기 좋게 출력
    records_df = pd.DataFrame(
        list(st.session_state.subject_records.items()),
        columns=['과목', '학습 시간 (초)']
    )
    records_df['포맷팅된 시간'] = records_df['학습 시간 (초)'].apply(format_time)
    
    st.dataframe(records_df[['과목', '포맷팅된 시간']], use_container_width=True)

# ==========================================
# 2. 오늘 할 일 페이지
# ==========================================
elif menu == "오늘 할 일":
    st.title("✅ 오늘 할 일")
    st.info("이곳에 오늘 해야 할 목표와 리스트를 관리하는 기능이 추가될 예정입니다!")

# ==========================================
# 3. 공부회고 페이지
# ==========================================
elif menu == "공부회고":
    st.title("📝 공부회고")
    st.info("오늘 하루 얼마나 집중했는지, 무엇을 배웠는지 기록하는 기능이 추가될 예정입니다!")
