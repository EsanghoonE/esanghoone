import streamlit as st
import base64
from datetime import datetime

# ------------------ 1. 페이지 설정 ------------------
st.set_page_config(
    page_title="Auto-Master",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ------------------ 2. 배경 이미지 ------------------
bg_image_path = "졸업과제 어플 배경 테슬라.jpg"

def get_base64(file):
    try:
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

bg = get_base64(bg_image_path)

# ------------------ 3. CSS ------------------
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpeg;base64,{bg}");
    background-size: cover;
}}

[data-testid="stHeader"] {{
    background: transparent;
}}

.main .block-container {{
    max-width: 500px;
    margin: auto;
}}

.title {{
    text-align: center;
    font-size: 2rem;
    font-weight: 900;
    color: white;
}}

.card {{
    background: rgba(255,255,255,0.6);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    margin: 20px 0;
}}

.d {{
    font-size: 40px;
    font-weight: 900;
}}

.btn {{
    display:block;
    padding:15px;
    border-radius:15px;
    text-align:center;
    color:white;
    font-weight:bold;
    margin-bottom:10px;
    text-decoration:none;
}}

.gradient {{
    background: linear-gradient(90deg,#00c6ff,#ff007f);
}}

.blue {{
    background:#142850;
}}

.outline {{
    border:2px solid #00c6ff;
    background:rgba(20,40,80,0.4);
}}

.brown {{
    background:linear-gradient(135deg,#8B5A2B,#5C3A21);
}}

.white {{
    background:rgba(255,255,255,0.3);
}}

</style>
""", unsafe_allow_html=True)

# ------------------ 4. 상태 관리 ------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

def move(page):
    st.session_state.page = page

# ------------------ 5. D-DAY 계산 ------------------
target = datetime(2026, 5, 30)  # 시험 날짜 수정 가능
today = datetime.now()
d_day = (target - today).days

# ------------------ 6. 페이지 ------------------

# 홈 화면
if st.session_state.page == "home":

    st.markdown('<div class="title">🚗 Auto-Master</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        👤 용산철도고 학생 님의 목표: 2회차 실기
        <div class="d">D - {d_day}</div>
    </div>
    """, unsafe_allow_html=True)

    # 버튼들 (클릭 가능)
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


# ------------------ 하위 페이지 ------------------

elif st.session_state.page == "ai":
    st.title("📸 AI 부품 판독기")
    st.write("👉 카메라 / 이미지 인식 기능 연결 예정")
    if st.button("← 뒤로"):
        move("home")

elif st.session_state.page == "guide":
    st.title("🌿 기초 가이드")
    st.write("기초 이론 정리 페이지")
    if st.button("← 뒤로"):
        move("home")

elif st.session_state.page == "exam":
    st.title("⏱️ 실전 모의고사")
    st.write("시험 문제 풀기 기능")
    if st.button("← 뒤로"):
        move("home")

elif st.session_state.page == "note":
    st.title("⭐ AI 오답 노트")
    st.write("틀린 문제 자동 정리")
    if st.button("← 뒤로"):
        move("home")

elif st.session_state.page == "practice":
    st.title("🔥 실전 연습")
    st.write("반복 훈련 모드")
    if st.button("← 뒤로"):
        move("home")