import streamlit as st
import time
import pandas as pd

# --- Session State 초기화 ---
if 'running' not in st.session_state:
    st.session_state.running = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'elapsed_time' not in st.session_state:
    st.session_state.elapsed_time = 0
if 'subject_records' not in st.session_state:
    st.session_state.subject_records = {'국어': 0, '영어': 0, '수학': 0, '과학': 0, '사회': 0, '기타': 0}
# 새롭게 추가: 할 일 목록을 저장할 리스트
if 'todos' not in st.session_state:
    st.session_state.todos = []

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
    
    subjects = list(st.session_state.subject_records.keys())
    current_subject = st.selectbox("현재 학습할 과목을 선택하세요:", subjects)
    
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
                
            st.session_state.running = False
            st.session_state.start_time = None
            st.session_state.elapsed_time = 0
            st.rerun()
            
    st.divider()
    
    st.subheader("📚 과목별 누적 학습 시간")
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
    
    # 할 일 입력 폼
    with st.form("todo_form", clear_on_submit=True):
        col1, col2 = st.columns([1, 3])
        with col1:
            new_subject = st.text_input("과목", placeholder="예: 수학")
        with col2:
            new_task = st.text_input("할 일", placeholder="예: 문제집 3쪽 풀기")
            
        submitted = st.form_submit_button("➕ 추가")
        
        if submitted:
            if new_subject and new_task:
                # 새로운 할 일을 리스트에 추가
                st.session_state.todos.append({'과목': new_subject, '할일': new_task, '완료': False})
                st.success("할 일이 추가되었습니다!")
                st.rerun() # 화면 새로고침
            else:
                st.warning("과목과 할 일을 모두 입력해주세요.")
                
    st.divider()
    
    # 할 일 목록 출력
    st.subheader("📋 나의 할 일 목록")
    
    if not st.session_state.todos:
        st.info("아직 등록된 할 일이 없습니다. 위의 폼에서 할 일을 추가해보세요!")
    else:
        for i, todo in enumerate(st.session_state.todos):
            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                # 완료 체크박스
                is_done = st.checkbox("", key=f"check_{i}", value=todo['완료'])
                if is_done != todo['완료']:
                    st.session_state.todos[i]['완료'] = is_done
                    st.rerun()
            with col2:
                # 완료 여부에 따라 취소선 표시
                if todo['완료']:
                    st.markdown(f"~~**[{todo['과목']}]** {todo['할일']}~~")
                else:
                    st.markdown(f"**[{todo['과목']}]** {todo['할일']}")

# ==========================================
# 3. 공부회고 페이지
# ==========================================
elif menu == "공부회고":
    st.title("📝 공부회고")
    st.info("오늘 하루 얼마나 집중했는지, 무엇을 배웠는지 기록하는 기능이 추가될 예정입니다!")
