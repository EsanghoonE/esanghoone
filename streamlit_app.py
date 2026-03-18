import streamlit as st
from datetime import datetime
import time  # AI 판독 로딩 연출을 위해 추가

# ------------------ 1. 페이지 설정 ------------------
st.set_page_config(
    page_title="Auto-Master",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ------------------ 2. CSS (배경 및 스타일링) ------------------
bg_url = "https://i.imgur.com/evCoCnM.jpg"

st.markdown(f"""
<style>
/* 배경 이미지 화면 전체 적용 */
[data-testid="stAppViewContainer"] {{
    background-image: url("{bg_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* 기본 상단 헤더 투명화 */
[data-testid="stHeader"] {{
    background: transparent;
}}

/* 모바일 화면처럼 중앙 정렬 및 폭 제한 (아이폰 해상도에 맞춰 420px) */
.main .block-container {{
    max-width: 420px;
    margin: auto;
    padding-top: 2rem;
}}

/* 앱 제목 스타일 */
.title {{
    text-align: center;
    font-size: 2.3rem;
    font-weight: 900;
    color: white;
    text-shadow: 2px 2px 5px rgba(0,0,0,0.6);
    margin-bottom: 10px;
}}

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
    font-size: 1.1rem;
}}

.d-day-info {{
    margin-bottom: 15px;
}}

.d {{
    font-size: 48px;
    font-weight: 900;
    color: #0f172a;
    margin-top: 5px;
}}

/* st.button 커스텀 */
div.stButton > button {{
    width: 100%;
    height: 70px;
    border-radius: 18px;
    background: rgba(20, 40, 80, 0.8);
    backdrop-filter: blur(5px);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.3);
    font-weight: bold;
    font-size: 17px;
    transition: all 0.3s ease;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    padding-left: 20px;
}}

/* 버튼 호버 효과 */
div.stButton > button:hover {{
    background: rgba(0, 198, 255, 0.9);
    border: 1px solid white;
    transform: scale(1.03);
    color: white;
}}

/* [핵심] AI 부품 판독기 버튼 좌측 여백 조정 */
[data-testid="column"]:first-child div.stButton > button {{
    width: 100%;
    margin-right: -10px;
}}

div.stButton > button span {{
    margin-right: 10px;
}}

h1, h2, h3, h4, h5, h6, p, li, div[data-testid="stMarkdownContainer"] > p {{
    color: white;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
}}

/* 탭 스타일 조정 */
[data-testid="stTabs"] [data-baseweb="tab"] {{
    background-color: rgba(20, 40, 80, 0.6);
    color: white;
    border-radius: 10px 10px 0 0;
    margin-right: 5px;
    font-weight: bold;
}}
[data-testid="stTabs"] [data-baseweb="tab"]:focus {{
    outline: none;
}}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {{
    background-color: #00c6ff;
}}
</style>
""", unsafe_allow_html=True)

# ------------------ 3. 상태 관리 (더블 클릭 해결 핵심!) ------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

def move(page):
    st.session_state.page = page
    st.rerun()  # <--- 이 한 줄이 버튼을 한 번만 눌러도 바로 넘어가게 해줍니다!

# ------------------ 4. D-DAY 계산 ------------------
target_date = datetime(2026, 5, 30) 
today = datetime.now()
d_day_count = (target_date - today).days

# ------------------ 5. 페이지 라우팅 및 렌더링 ------------------

# --- 메인 홈 화면 ---
if st.session_state.page == "home":
    st.markdown('<div class="title">🚗 Auto-Master</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <div class="d-day-info">
            👤 용산철도고 학생 님의 목표: 2회차 실기
        </div>
        <div class="d">D - {d_day_count}</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📸 [핵심] AI 판독기"):
            move("ai")
        if st.button("🌿 기초 가이드"):
            move("guide")

    with col2:
        if st.button("⏱️ 실전 모의고사"):
            move("exam")
        if st.button("⭐ AI 오답 노트"):
            move("note")

    if st.button("🔥 실전 연습"):
        move("practice")


# --- 1. 📸 [핵심] AI 부품 판독기 (사진 찍으면 바로 판독!) ---
elif st.session_state.page == "ai":
    st.title("📸 AI 부품 판독기")
    st.write("### 부품 사진을 찍거나 올려주세요!")
    
    # 카메라 입력 & 파일 업로드
    camera_image = st.camera_input("카메라로 촬영하기 📸")
    uploaded_image = st.file_uploader("또는 갤러리에서 선택하기 🖼️", type=["jpg", "jpeg", "png"])
    
    # 두 입력 중 하나라도 들어오면 image_to_process에 저장
    image_to_process = camera_image or uploaded_image

    if image_to_process:
        st.write("---")
        # 1. 입력받은 이미지 화면에 표시
        st.image(image_to_process, caption="입력된 부품 이미지", use_container_width=True)
        
        # 2. AI 판독 로딩 연출 (spinner 사용)
        with st.spinner('AI가 부품을 정밀하게 분석 중입니다... 🔍'):
            time.sleep(2) # 2초 동안 분석하는 척 대기 (실제 모델 연동 시 이 부분에 모델 코드 삽입)
            
        # 3. 판독 결과 출력
        st.success("✅ 판독 완료!")
        st.info("""
        💡 **AI 분석 결과:**
        - **부품명:** 점화 플러그 (Spark Plug)
        - **상태:** 양호 (카본 퇴적물 적음)
        - **설명:** 엔진 실린더 내의 압축된 혼합기에 불꽃을 튀겨 점화시키는 핵심 부품입니다.
        """)
        
        # 다시하기 버튼
        if st.button("🔄 다른 부품 판독하기"):
            st.rerun()

    st.write("---")
    if st.button("← 홈으로 돌아가기"):
        move("home")

# --- 2. 🌿 기초 가이드 ---
elif st.session_state.page == "guide":
    st.title("🌿 기초 가이드")
    
    tab_basic, tab_inter, tab_adv = st.tabs(["초보자 (1~2주)", "중급자 (3~4주)", "상급자 (시험 직전)"])
    
    with tab_basic:
        st.header("1단계: 초보자 가이드")
        st.write("""
        - **주요 목표:** 핵심 이론 및 부품 명칭 익히기
        - **학습 내용:** 엔진 시스템 기초, 섀시 기초, 전기 장치 기초
        - **활용 팁:** AI 부품 판독기를 적극 활용하세요.
        """)
    
    with tab_inter:
        st.header("2단계: 중급자 가이드")
        st.write("""
        - **주요 목표:** 실제 정비 절차 및 회로도 분석
        - **학습 내용:** 엔진 튠업, 섀시 얼라이먼트, 전장 회로도 읽는 법
        """)
        
    with tab_adv:
        st.header("3단계: 상급자 가이드")
        st.write("""
        - **주요 목표:** 문제 해결 능력 및 실전 감각 키우기
        - **학습 내용:** 실제 차량 고장 진단 시뮬레이션, 오답 노트 분석
        """)

    st.write("---")
    if st.button("← 홈으로 돌아가기"):
        move("home")

# --- 3. ⏱️ 실전 모의고사 ---
elif st.session_state.page == "exam":
    st.title("⏱️ 실전 모의고사")
    st.write("👉 시험 문제 풀기 및 채점 기능")
    with st.expander("2024년 2회차 실기 모의고사", expanded=True):
        st.write("- [핵심] AI 부품 판독 문제 (10문항)")
        st.write("- 엔진 고장 진단 (2문항)")
        if st.button("시험 시작 🔥"):
            st.success("시험이 시작되었습니다!")

    st.write("---")
    if st.button("← 홈으로 돌아가기"):
        move("home")

# --- 4. ⭐ AI 오답 노트 ---
elif st.session_state.page == "note":
    st.title("⭐ AI 오답 노트")
    st.write("### ⭐ 당신의 약점, AI가 분석했습니다.")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="최다 오답 분야", value="전기 장치")
    with col2:
        st.metric(label="틀린 문제 수", value="25개", delta="-5개")
        
    st.write("---")
    if st.button("← 홈으로 돌아가기"):
        move("home")

# --- 5. 🔥 실전 연습 ---
elif st.session_state.page == "practice":
    st.title("🔥 실전 연습")
    st.radio("연습할 파트를 선택하세요", ["엔진", "섀시", "전기", "전장 회로"])
    if st.button("연습 시작 🚀"):
        st.success("연습 모드가 시작됩니다.")

    st.write("---")
    if st.button("← 홈으로 돌아가기"):
        move("home")