import streamlit as st
from datetime import datetime
import time

# ---------------- 상태 초기화 ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "xp" not in st.session_state:
    st.session_state.xp = 0

# ---------------- 레벨 시스템 ----------------
def get_level(xp):
    if xp < 50:
        return "Lv.1 🚗 초보"
    elif xp < 150:
        return "Lv.2 🔧 견습"
    elif xp < 300:
        return "Lv.3 🏎️ 전문가"
    else:
        return "Lv.4 🔥 마스터"

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

/* 배경 */
[data-testid="stAppViewContainer"] {{
    background-image: url("{bg_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

[data-testid="stHeader"] {{
    background: transparent;
}}

.main .block-container {{
    max-width: 420px;
    margin: auto;
}}

/* 타이틀 */
.title {{
    text-align: center;
    font-size: 2.4rem;
    font-weight: 900;
    color: white;
    text-shadow: 0 0 15px rgba(0,0,0,0.8);
}}

/* 카드 */
.card {{
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(12px);
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 20px;
    color: white;
    box-shadow: 0 8px 25px rgba(0,0,0,0.4);
}}

/* ---------------- 일반 버튼 ---------------- */
div.stButton > button {{
    width: 100%;
    height: 65px;
    border-radius: 16px;
    background: rgba(30, 58, 95, 0.75);
    color: #e2e8f0;
    font-weight: 600;
    border: 1px solid rgba(255,255,255,0.2);
    transition: all 0.25s ease;
}}

div.stButton > button:hover {{
    background: rgba(59,130,246,0.7);
    transform: scale(1.04);
}}

/* ===============================
   🔥 AI 버튼 (레드 + 블루 네온)
   =============================== */
div.stButton:nth-of-type(1) > button {{

    position: relative;
    overflow: hidden;

    background: linear-gradient(135deg, #ff2a2a, #1e90ff, #ff2a2a);
    background-size: 300% 300%;

    font-size: 19px;
    font-weight: 900;
    color: white;

    border: 2px solid rgba(255,255,255,0.8);

    animation: neonMove 4s ease infinite;

    box-shadow:
        0 0 10px #ff2a2a,
        0 0 20px #1e90ff,
        0 0 40px rgba(255,42,42,0.8),
        0 0 60px rgba(30,144,255,0.7);
}}

/* 유리 효과 */
div.stButton:nth-of-type(1) > button::before {{
    content: "";
    position: absolute;
    inset: 0;
    background: rgba(255,255,255,0.15);
    border-radius: 16px;
    backdrop-filter: blur(10px);
}}

/* Hover 효과 */
div.stButton:nth-of-type(1) > button:hover {{
    transform: scale(1.1);

    box-shadow:
        0 0 20px #ff2a2a,
        0 0 40px #1e90ff,
        0 0 80px white;
}}

/* 애니메이션 */
@keyframes neonMove {{
    0% {{background-position: 0%}}
    50% {{background-position: 100%}}
    100% {{background-position: 0%}}
}}

h1,h2,h3,p {{
    color:white;
}}

</style>
""", unsafe_allow_html=True)

# ---------------- D-DAY ----------------
target = datetime(2026,5,30)
d_day = (target - datetime.now()).days
level = get_level(st.session_state.xp)

# ---------------- 홈 ----------------
if st.session_state.page == "home":

    st.markdown('<div class="title">🚗 Auto-Master</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        🎯 목표: 자동차 정비 기능사<br>
        ⏱️ D - {d_day}<br>
        ⚡ XP: {st.session_state.xp}<br>
        🏆 레벨: {level}
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
            time.sleep(2)

        st.success("판독 완료!")

        st.write("""
        🔧 부품: 점화 플러그  
        💡 상태: 양호  
        📊 신뢰도: 95%
        """)

        st.session_state.xp += 15
        st.success("🔥 +15 XP 획득!")

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
        st.session_state.xp += 30
        st.success("시험 완료! +30XP")

    if st.button("← 홈"):
        move("home")

# ---------------- 오답노트 ----------------
elif st.session_state.page == "note":

    st.title("⭐ 오답노트")

    st.info("추후 AI 기반 오답 분석 기능 추가 예정")

    if st.button("← 홈"):
        move("home")

# ---------------- 연습 ----------------
elif st.session_state.page == "practice":

    st.title("🔥 실전 연습")

    part = st.radio("파트 선택",["엔진","섀시","전기"])

    if st.button("연습 시작"):
        st.session_state.xp += 10
        st.success(f"{part} 연습 완료! +10XP")

    if st.button("← 홈"):
        move("home")