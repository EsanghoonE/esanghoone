import streamlit as st
from datetime import datetime
import time
import os
import google.generativeai as genai

# ---------------- API 키 설정 (st.secrets 활용) ----------------
# Streamlit의 보안 저장소에서 키를 불러옵니다. .env 파일이 필요 없습니다!
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    # 혹시 Secret 설정이 안 되어 에러가 날 경우를 대비한 임시 하드코딩 (테스트 후 지우셔도 됩니다)
    api_key = "AIzaSyAxbvbjFk2-LU24rh6z-iS_Q66M7-BMUWI"

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------- 상태 초기화 ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "wrong_notes" not in st.session_state:
    st.session_state.wrong_notes = []

# ---------------- 페이지 이동 ----------------
def move(page):
    st.session_state.page = page
    st.rerun()

# ---------------- 페이지 설정 ----------------
st.set_page_config(
    page_title="Auto-Master",
    page_icon="🚗",
    layout="centered"
)

# ---------------- CSS ----------------
bg_url = "https://i.imgur.com/evCoCnM.jpg"

st.markdown(f"""
<style>

[data-testid="stAppViewContainer"] {{
    background-image: url("{bg_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.main .block-container {{
    max-width: 420px;
    margin: auto;
}}

.title {{
    text-align: center;
    font-size: 2.4rem;
    font-weight: 900;
    color: white;
}}

.card {{
    background: rgba(255,255,255,0.15);
    padding: 20px;
    border-radius: 20px;
    color: white;
}}

div.stButton > button {{
    width: 100%;
    height: 70px;
    border-radius: 18px;
}}

h1,h2,h3,p {{
    color:white;
}}

</style>
""", unsafe_allow_html=True)

# ---------------- D-DAY ----------------
target = datetime(2026,5,30)
d_day = (target - datetime.now()).days

# ---------------- 홈 ----------------
if st.session_state.page == "home":

    st.markdown('<div class="title">🚗 Auto-Master</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        🎯 목표: 자동차 정비 기능사<br>
        ⏱️ D - {d_day}<br>
        ⚡ 경험치: {st.session_state.xp}
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📸 AI 판독기"):
            move("ai")
        if st.button("🌿 기초 가이드"):
            move("guide")

    with col2:
        if st.button("⏱️ 모의고사"):
            move("exam")
        if st.button("⭐ 오답노트"):
            move("note")

    if st.button("🔥 실전 연습"):
        move("practice")

# ---------------- AI ----------------
elif st.session_state.page == "ai":

    st.title("📸 AI 판독기")

    img = st.camera_input("촬영")

    if img:
        st.image(img)

        with st.spinner("AI 분석중..."):
            time.sleep(1)

            try:
                response = model.generate_content([
                    "이 자동차 부품이 무엇인지 설명하고 상태를 분석해줘. (부품명 / 상태 / 이유 형식으로)",
                    img.getvalue()
                ])
                result = response.text

            except Exception as e:
                result = f"에러 발생: {e}"

        st.success("판독 완료!")
        st.write(result)

        st.session_state.xp += 10

    if st.button("← 홈"):
        move("home")

# ---------------- 가이드 ----------------
elif st.session_state.page == "guide":

    st.title("🌿 학습 가이드")

    tab1, tab2, tab3 = st.tabs(["초보","중급","고급"])

    with tab1:
        st.write("기초 이론 학습")

    with tab2:
        st.write("정비 실습")

    with tab3:
        st.write("시험 대비")

    if st.button("← 홈"):
        move("home")

# ---------------- 모의고사 ----------------
elif st.session_state.page == "exam":

    st.title("⏱️ 모의고사")

    if st.button("문제 시작"):
        st.session_state.xp += 20
        st.success("시험 완료! +20XP")

    if st.button("← 홈"):
        move("home")

# ---------------- 오답노트 ----------------
elif st.session_state.page == "note":

    st.title("⭐ 오답노트")

    if len(st.session_state.wrong_notes) == 0:
        st.info("오답 없음 👍")

    if st.button("← 홈"):
        move("home")

# ---------------- 연습 ----------------
elif st.session_state.page == "practice":

    st.title("🔥 실전 연습")

    part = st.radio("파트 선택",["엔진","섀시","전기"])

    if st.button("연습 시작"):
        st.session_state.xp += 5
        st.success(f"{part} 연습 완료! +5XP")

    if st.button("← 홈"):
        move("home")