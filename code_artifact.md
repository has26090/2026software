# ⏱️ 학생용 과목별 학습 타이머 개발 기록

## 1. 프로젝트 개요
* **목표:** 학생들이 과목별로 학습 시간을 측정하고 기록할 수 있는 웹 애플리케이션 개발
* **실행 환경:** Streamlit Cloud
* **주요 기능:** 
  * 타이머 제어 (시작, 일시정지, 초기화)
  * 과목별 학습 시간 기록 및 누적 계산
  * 직관적인 UI 표 제공

## 2. 작성된 코드

### `main.py` (메인 애플리케이션 코드)
```python
import streamlit as st
import time
import pandas as pd

# 페이지 기본 설정
st.set_page_config(page_title="학생용 학습 타이머", page_icon="⏱️")

st.title("⏱️ 학생용 과목별 학습 타이머")
st.write("학습할 과목을 입력하고 타이머를 시작해 목표를 달성해 보세요!")

# 세션 상태(Session State) 초기화
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'elapsed_time' not in st.session_state:
    st.session_state.elapsed_time = 0.0
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'records' not in st.session_state:
    st.session_state.records = {}

# 과목 입력칸
subject = st.text_input("📚 현재 학습 중인 과목을 입력하세요 (예: 수학, 영어, 프로그래밍):", "수학")

# 타이머 제어 함수
def start_timer():
    if not st.session_state.is_running:
        st.session_state.start_time = time.time()
        st.session_state.is_running = True

def pause_timer():
    if st.session_state.is_running:
        st.session_state.elapsed_time += time.time() - st.session_state.start_time
        st.session_state.is_running = False

def reset_timer():
    st.session_state.start_time = None
    st.session_state.elapsed_time = 0.0
    st.session_state.is_running = False

def record_time():
    if st.session_state.is_running:
        pause_timer()
        
    if st.session_state.elapsed_time > 0:
        if subject in st.session_state.records:
            st.session_state.records[subject] += st.session_state.elapsed_time
        else:
            st.session_state.records[subject] = st.session_state.elapsed_time
        reset_timer()
        st.success(f"🎉 '{subject}' 과목에 성공적으로 기록되었습니다!")
    else:
        st.warning("기록할 학습 시간이 없습니다. 타이머를 먼저 실행해 주세요.")

# 타이머 조작 버튼 구성
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

# 시간 계산 및 표시 로직
current_time = st.session_state.elapsed_time
if st.session_state.is_running:
    current_time += time.time() - st.session_state.start_time

hours, rem = divmod(current_time, 3600)
minutes, seconds = divmod(rem, 60)
time_formatted = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

st.metric(label=f"[{subject}] 경과 시간", value=time_formatted)

if st.session_state.is_running:
    st.info("타이머가 백그라운드에서 실행 중입니다. 화면의 빈 곳을 클릭하거나 다른 버튼을 누르면 화면의 시간이 최신화됩니다.")

st.markdown("---")
st.subheader("📊 과목별 누적 학습 기록")

# 기록된 데이터 표시
if st.session_state.records:
    df = pd.DataFrame(list(st.session_state.records.items()), columns=["과목", "총 학습 시간 (초)"])
    df["총 학습 시간"] = df["총 학습 시간 (초)"].apply(
        lambda x: f"{int(x // 3600):02d}:{int((x % 3600) // 60):02d}:{int(x % 60):02d}"
    )
    st.dataframe(df[["과목", "총 학습 시간"]], use_container_width=True)
else:
    st.write("아직 기록된 학습 내용이 없습니다. 멋진 첫 기록을 남겨보세요!")
```

### `requirements.txt` (필요 라이브러리)
```text
streamlit
pandas
```

## 3. 구현 및 배포 지침
1. **GitHub 저장소 생성:** GitHub에 새로운 Repository를 만듭니다.
2. **파일 업로드:** 위에서 작성한 `main.py`와 `requirements.txt` 파일을 커밋합니다.
3. **Streamlit 연동:** [Streamlit Community Cloud](https://share.streamlit.io/)에 접속하여 로그인합니다.
4. **배포 진행:** 'New app'을 클릭하여 GitHub 저장소를 연결하고, Main file path에 `main.py`를 지정한 후 'Deploy' 버튼을 클릭합니다.