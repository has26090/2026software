import streamlit as st
import time
import pandas as pd

# 페이지 기본 설정
st.set_page_config(page_title="학생용 학습 타이머", page_icon="⏱️")

st.title("⏱️ 학생용 과목별 학습 타이머")
st.write("학습할 과목을 입력하고 타이머를 시작해 목표를 달성해 보세요!")

# 1. 세션 상태(Session State) 초기화
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'elapsed_time' not in st.session_state:
    st.session_state.elapsed_time = 0.0
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'records' not in st.session_state:
    st.session_state.records = {}

# 2. 과목 입력칸
subject = st.text_input("📚 현재 학습 중인 과목을 입력하세요 (예: 수학, 영어, 프로그래밍):", "수학")

# 3. 타이머 제어 함수
def start_timer():
    if not st.session_state.is_running:
        st.session_state.start_time = time.time()
        st.session_state.is_running = True

def pause_timer():
    if st.session_state.is_running:
        # 현재까지 흘러간 시간을 누적
        st.session_state.elapsed_time += time.time() - st.session_state.start_time
        st.session_state.is_running = False

def reset_timer():
    st.session_state.start_time = None
    st.session_state.elapsed_time = 0.0
    st.session_state.is_running = False

def record_time():
    # 실행 중이라면 먼저 일시정지 처리하여 지금까지의 시간을 계산
    if st.session_state.is_running:
        pause_timer()
        
    if st.session_state.elapsed_time > 0:
        # 과목별 누적 시간 저장
        if subject in st.session_state.records:
            st.session_state.records[subject] += st.session_state.elapsed_time
        else:
            st.session_state.records[subject] = st.session_state.elapsed_time
        
        # 기록 후 현재 타이머 초기화
        reset_timer()
        st.success(f"🎉 '{subject}' 과목에 성공적으로 기록되었습니다!")
    else:
        st.warning("기록할 학습 시간이 없습니다. 타이머를 먼저 실행해 주세요.")

# 4. 타이머 조작 버튼 구성
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("▶️ 시작", on_click=start_timer, use_container_width=True)
with col2:
    st.button("⏸️ 일시정지", on_click=pause_timer, use_container_width=True)
with col3:
    st.button("🔄 초기화", on_click=reset_timer, use_container_width=True)
with col4:
    st.button("💾 과목에 기록", on_click=record_time, use_container_width=True)

st.markdown("---")
st.subheader("현재 진행 중인 학습 시간")

# 5. 시간 계산 및 표시 로직
current_time = st.session_state.elapsed_time
if st.session_state.is_running:
    # 타이머가 돌아가고 있다면 (현재 시간 - 시작 시간)을 더해서 보여줌
    current_time += time.time() - st.session_state.start_time

# 초 단위 시간을 시:분:초 형태로 변환
hours, rem = divmod(current_time, 3600)
minutes, seconds = divmod(rem, 60)
time_formatted = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

st.metric(label=f"[{subject}] 경과 시간", value=time_formatted)

if st.session_state.is_running:
    st.info("타이머가 백그라운드에서 실행 중입니다. 화면의 빈 곳을 클릭하거나 다른 버튼을 누르면 화면의 시간이 최신화됩니다.")

st.markdown("---")
st.subheader("📊 과목별 누적 학습 기록")

# 6. 기록된 데이터 표시
if st.session_state.records:
    # 딕셔너리를 판다스 데이터프레임으로 변환
    df = pd.DataFrame(list(st.session_state.records.items()), columns=["과목", "총 학습 시간 (초)"])
    
    # 초 단위를 시:분:초 형식 문자열로 변환하는 함수 적용
    df["총 학습 시간"] = df["총 학습 시간 (초)"].apply(
        lambda x: f"{int(x // 3600):02d}:{int((x % 3600) // 60):02d}:{int(x % 60):02d}"
    )
    
    # 보기 좋게 표 형태로 출력
    st.dataframe(df[["과목", "총 학습 시간"]], use_container_width=True)
else:
    st.write("아직 기록된 학습 내용이 없습니다. 멋진 첫 기록을 남겨보세요!")
