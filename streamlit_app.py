import streamlit as st
import base64
from datetime import datetime
import os

# ------------------ 1. 페이지 설정 ------------------
st.set_page_config(
    page_title="Auto-Master",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ------------------ 2. 배경 이미지 ------------------
bg_image_path = "졸업과제 어플 배경 테슬라.jpg"

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    else:
        st.error(f"⚠️ 이미지를 찾을 수 없습니다: {file_path}")
        return ""

bg = get_base64(bg_image_path)

# ------------------ 3. CSS ------------------
st.markdown(f"""
<style>
/* 배경 이미지 화면 전체 적용 */
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpeg;base64,{bg}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* 기본 상단 헤더 투명화 */
[data-testid="stHeader"] {{
    background: transparent;
}}

/* 모바일 화면처럼 중앙 정렬 및 폭 제한 */
.main .block-container {{
    max-width: 500px;
    margin: auto;
    padding-top: 2rem;
}}

/* 앱 제목 스타일 */
.title {{
    text-align: center;
    font-size: 2.2rem;
    font-weight: 900;
    color: white;
    text-shadow: 2px 2px 5px rgba(0,0,0,0.6);
    margin-bottom: 10px;
}

/* 사용자 정보 카드 (유리 질감) */
.card {{
    background: rgba(255, 255, 255, 0.65);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    color: #1e293b;
    font-weight: bold;
}}

.d {{
    font-size: 45px;
    font-weight: 900;
    color: #0f172a;
    margin-top: 5px;
}}

/* st.button 커스텀 (모든 버튼에 적용) */
div.stButton > button {{
    width: 100%;
    height: 60px;
    border-radius: 15px;
    background: rgba(20, 40, 80, 0.8); /* 진한 남색 반투명 */
    backdrop-filter: blur(5px);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.3);
    font-weight: bold;
    font-size: 16px;
    transition: all 0.3s ease;
}}

/* 버튼 호버(마우스 올렸을 때) 효과 */
div.stButton > button:hover {{
    background: rgba(0, 198, 255, 0.9);
    border: 1px solid white;
    transform: scale(1.02);
    color: white;
}}

/* 하위 페이지 텍스트 가독성 확보 */
h1, p, div[data-testid="stMarkdownContainer"] > p {{
    color: white;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
}}
</style>
""", unsafe_allow_html=True)

# ------------------ 4. 상태 관리 ------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

def move(page):
    st.session_state.page = page

# ------------------ 5. D-DAY 계산 ------------------
target = datetime(2026, 5, 30)  # 시험 날짜 설정
today = datetime.now()
d_day = (target - today).days

# ------------------ 6. 페이지 라우팅 ------------------

# 메인 홈 화면
if st.session_state.page == "home":
    st.markdown('<div class="title">🚗 Auto-Master</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        👤 용산철도고 학생 님의 목표: 2회차 실기
        <div class="d">D - {d_day}</div>
    </div>
    """, unsafe_allow_html=True)

    # 버튼 레이아웃
    if st.button("📸 [핵심] AI 부품 판독기"):
        move("ai")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌿 기초 가이드"):
            move("guide")
    with col2:
        if st.button("⏱️ 실전 모의고사"):
            move("exam")

    col3, col4 = st.columns(2)
    with col3:
        if st.button("🌿 기초 가이드2"):
            move("guide2")
    with col4:
        if st.button("⭐ AI 오답 노트"):
            move("note")

    if st.button("🔥 실전 연습"):
        move("practice")

# 하위 페이지들
elif st.session_state.page == "ai":
    st.title("📸 AI 부품 판독기")
    st.write("👉 카메라 / 이미지 인식 기능 연결 예정")
    if st.button("← 뒤로"):
        move("home")

elif st.session_state.page == "guide" or st.session_state.page == "guide2":
    st.title("🌿 기초 가이드")
    st.write("기초 이론 정리 페이지입니다.")
    if st.button("← 뒤로"):
        move("home")

elif st.session_state.page == "exam":
    st.title("⏱️ 실전 모의고사")
    st.write("시험 문제 풀기 기능입니다.")
    if st.button("← 뒤로"):
        move("home")

elif st.session_state.page == "note":
    st.title("⭐ AI 오답 노트")
    st.write("틀린 문제 자동 정리 페이지입니다.")
    if st.button("← 뒤로"):
        move("home")

elif st.session_state.page == "practice":
    st.title("🔥 실전 연습")
    st.write("반복 훈련 모드입니다.")
    if st.button("← 뒤로"):
        move("home")