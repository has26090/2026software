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
if 'todos' not in st.session_state:
    st.session_state.todos = []
# 🌟 새롭게 추가: 회고 목록을 저장할 리스트
if 'retros' not in st.session_state:
    st.session_state.retros = []

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
    
    with st.form("todo_form", clear_on_submit=True):
        col1, col2 = st.columns([1, 3])
        with col1:
            new_subject = st.text_input("과목", placeholder="예: 수학")
        with col2:
            new_task = st.text_input("할 일", placeholder="예: 문제집 3쪽 풀기")
            
        submitted = st.form_submit_button("➕ 추가")
        
        if submitted:
            if new_subject and new_task:
                st.session_state.todos.append({'과목': new_subject, '할일': new_task, '완료': False})
                st.success("할 일이 추가되었습니다!")
                st.rerun()
            else:
                st.warning("과목과 할 일을 모두 입력해주세요.")
                
    st.divider()
    
    st.subheader("📋 나의 할 일 목록")
    
    if len(st.session_state.todos) == 0:
        st.info("아직 등록된 할 일이 없습니다. 위의 폼에서 할 일을 추가해보세요!")
    else:
        for i, todo in enumerate(st.session_state.todos):
            col1, col2 = st.columns([0.1, 0.9])
            
            with col1:
                is_done = st.checkbox("", key=f"check_{i}", value=todo['완료'])
                if is_done != todo['완료']:
                    st.session_state.todos[i]['완료'] = is_done
                    st.rerun()
                    
            with col2:
                if todo['완료']:
                    st.markdown(f"~~**[{todo['과목']}]** {todo['할일']}~~")
                else:
                    st.markdown(f"**[{todo['과목']}]** {todo['할일']}")

# ==========================================
# 3. 공부회고 페이지 (새로 구현된 부분!)
# ==========================================
elif menu == "공부회고":
    st.title("📝 공부회고")
    
    # 🌟 긴 글을 작성하기 좋은 text_area를 사용합니다.
    with st.form("retro_form", clear_on_submit=True):
        new_retro_subject = st.text_input("과목", placeholder="예: 영어")
        new_retro_text = st.text_area("공부 회고", placeholder="오늘 배운 내용, 어려웠던 점, 내일 보완할 점 등을 자유롭게 적어보세요.")
        
        submitted_retro = st.form_submit_button("➕ 추가")
        
        if submitted_retro:
            if new_retro_subject and new_retro_text:
                st.session_state.retros.append({'과목': new_retro_subject, '회고': new_retro_text})
                st.success("공부 회고가 추가되었습니다!")
                st.rerun()
            else:
                st.warning("과목과 회고 내용을 모두 입력해주세요.")
                
    st.divider()
    
    st.subheader("📚 나의 공부 회고록")
    
    if len(st.session_state.retros) == 0:
        st.info("아직 작성된 회고가 없습니다. 오늘 공부한 내용을 돌아보며 기록을 남겨보세요!")
    else:
        # 🌟 가장 최근에 쓴 회고가 맨 위에 오도록 reversed() 함수를 사용합니다.
        for retro in reversed(st.session_state.retros):
            # st.expander를 사용하면 클릭해서 내용을 열고 닫을 수 있어 화면이 깔끔해집니다.
            with st.expander(f"[{retro['과목']}] 회고 기록"):
                st.write(retro['회고'])
