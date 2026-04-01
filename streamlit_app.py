import streamlit as st
from datetime import datetime
import time
import os
import google.generativeai as genai
from PIL import Image

# ==========================================
# 🔑 구글 AI API 설정 (상훈쌤의 API 키 적용 완료!)
# ==========================================
# 주의: 깃허브 등 공개 저장소에 코드를 올릴 때는 이 키를 반드시 숨기세요!
genai.configure(api_key="AIzaSyAxbvbjFk2-LU24rh6z-iS_Q66M7-BMUWI") 
# Vision(이미지 인식) 기능과 속도가 뛰어난 최신 gemini-1.5-flash 모델 사용
model = genai.GenerativeModel('gemini-1.5-flash')

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

# ---------------- CSS (절대 불변의 기본 틀) ----------------
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

/* 기본 버튼 */
div.stButton > button {{
    width: 100%;
    height: 70px;
    border-radius: 18px;
    background: rgba(20,40,80,0.7);
    color: white;
    font-weight: bold;
    border: 1px solid rgba(255,255,255,0.3);
    transition: 0.3s;
}}

div.stButton > button:hover {{
    transform: scale(1.05);
}}

/* ===============================
   🌈 AI 버튼 (네온 끝판왕)
   =============================== */
div.stButton:nth-of-type(1) > button {{

    position: relative;
    overflow: hidden;

    background: linear-gradient(135deg, #ff007f, #ffd700, #00c6ff, #00e676, #ff007f);
    background-size: 400% 400%;

    font-size: 19px;
    font-weight: 900;

    animation: rainbow 6s infinite;

    box-shadow:
        0 0 10px rgba(255,255,255,0.6),
        0 0 30px rgba(0,198,255,0.7),
        0 0 60px rgba(255,0,127,0.6);

}}

div.stButton:nth-of-type(1) > button:hover {{
    transform: scale(1.1);
    box-shadow:
        0 0 20px white,
        0 0 50px #00c6ff,
        0 0 100px #ff007f;
}}

@keyframes rainbow {{
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

# ---------------- AI (진짜 모델 연동 완료!) ----------------
elif st.session_state.page == "ai":

    st.title("📸 AI 판독기")
    st.write("부품 사진을 찍거나 갤러리에서 올려주세요!")

    # 카메라와 파일 업로더 모두 제공
    img_camera = st.camera_input("촬영하기 📸")
    img_upload = st.file_uploader("사진 업로드 🖼️", type=["jpg", "jpeg", "png"])
    
    # 둘 중 하나라도 입력되면 실행
    img_data = img_camera or img_upload

    if img_data:
        st.image(img_data, caption="업로드된 이미지")

        with st.spinner("🤖 AI가 부품을 정밀 분석 중입니다..."):
            try:
                # 1. 이미지를 PIL 포맷으로 변환
                pil_image = Image.open(img_data)
                
                # 2. AI에게 내릴 프롬프트 (명령어) 설정
                prompt = """
                당신은 자동차 정비 기능사 실기 시험을 교육하는 최고의 정비 전문가입니다.
                학생이 찍은 자동차 부품 사진을 보고 아래 양식에 맞게 정확하게 판독해 주세요.
                만약 자동차 부품이 아닌 일반 사물이라면, 어떤 사물인지 밝히고 '자동차 부품을 다시 촬영해주세요'라고 친절하게 안내해 주세요.
                
                ---
                🔧 **부품명:** (정확한 명칭)
                💡 **예상 상태:** (사진상 보이는 외관 상태. 예: 양호, 마모, 오염 등)
                📊 **핵심 기능:** (이 부품이 자동차에서 하는 핵심 역할을 1~2줄로 요약)
                ---
                """
                
                # 3. Gemini API 호출
                response = model.generate_content([prompt, pil_image])
                
                # 4. 결과 출력
                st.success("✅ 판독 완료!")
                
                # 카드 형태로 AI 답변을 예쁘게 출력
                st.markdown(f"""
                <div style="background-color: rgba(0,0,0,0.5); padding: 15px; border-radius: 10px; border: 1px solid #00c6ff;">
                    {response.text}
                </div>
                """, unsafe_allow_html=True)

                # 경험치 추가
                st.session_state.xp += 10
                st.info("축하합니다! 부품 판독 완료로 +10 XP 획득! ⚡")
                
            except Exception as e:
                st.error(f"판독 중 오류가 발생했습니다. API 키나 네트워크를 확인해주세요. (에러: {e})")

    st.write("---")
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