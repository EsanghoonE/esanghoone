import streamlit as st
from datetime import datetime
import os

# ------------------ 1. 페이지 설정 ------------------
# 모바일 해상도(아이폰 16 Pro Safari)에 최적화된 느낌을 주기 위해 layout="centered"로 설정
st.set_page_config(
    page_title="Auto-Master",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ------------------ 2. CSS (배경 및 스타일링) ------------------
# Imgur 링크의 '직접 이미지 주소(.jpg)'를 배경으로 사용합니다.
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

/* 모바일 화면처럼 중앙 정렬 및 폭 제한 (아이폰 해상도에 맞춰 420px로 더 좁게 조정) */
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

/* st.button 커스텀 (image_14.png 스타일 적용) */
div.stButton > button {{
    width: 100%;
    height: 70px;
    border-radius: 18px;
    background: rgba(20, 40, 80, 0.8); /* 진한 남색 반투명 (image_14.png 색상) */
    backdrop-filter: blur(5px);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.3);
    font-weight: bold;
    font-size: 17px;
    transition: all 0.3s ease;
    display: flex;
    justify-content: flex-start; /* 아이콘과 텍스트 왼쪽 정렬 */
    align-items: center;
    padding-left: 20px;
}}

/* 버튼 호버(마우스 올렸을 때) 효과: image_14.png처럼 하늘색 테두리 */
div.stButton > button:hover {{
    background: rgba(0, 198, 255, 0.9);
    border: 1px solid white;
    transform: scale(1.03);
    color: white;
}}

/* [핵심] AI 부품 판독기 버튼은 image_14.png처럼 두 줄 너비를 차지하도록 설정 */
[data-testid="column"]:first-child div.stButton > button {{
    width: 100%;
    margin-right: -10px; /* column 간격 조정 */
}}

/* 버튼 내 이모지와 텍스트 사이 간격 */
div.stButton > button span {{
    margin-right: 10px;
}}

/* 하위 페이지 텍스트 가독성 확보 */
h1, h2, h3, h4, h5, h6, p, li, div[data-testid="stMarkdownContainer"] > p {{
    color: white;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
}}

/* 탭 스타일 조정 (기초 가이드 페이지) */
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

# ------------------ 3. 상태 관리 (페이지 이동) ------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

def move(page):
    st.session_state.page = page

# ------------------ 4. D-DAY 계산 ------------------
# 시험 날짜 설정 (원하는 날짜로 수정하세요)
target_date = datetime(2026, 5, 30) 
today = datetime.now()
d_day_count = (target_date - today).days

# ------------------ 5. 페이지 라우팅 및 렌더링 ------------------

# --- 메인 홈 화면 ---
if st.session_state.page == "home":
    st.markdown('<div class="title">🚗 Auto-Master</div>', unsafe_allow_html=True)

    # 사용자 카드 (image_14.png처럼 D-DAY 포함)
    st.markdown(f"""
    <div class="card">
        <div class="d-day-info">
            👤 용산철도고 학생 님의 목표: 2회차 실기
        </div>
        <div class="d">D - {d_day_count}</div>
    </div>
    """, unsafe_allow_html=True)

    # 버튼 그리드 레이아웃 (image_14.png와 동일하게 2컬럼 구성)
    col1, col2 = st.columns(2)

    with col1:
        # [핵심] AI 부품 판독기 (image_14.png처럼 왼쪽 열 첫 번째)
        if st.button("📸 [핵심] AI 부품 판독기"):
            move("ai")
        
        # 🌿 기초 가이드 (왼쪽 열 두 번째)
        if st.button("🌿 기초 가이드"):
            move("guide")

    with col2:
        # ⏱️ 실전 모의고사 (오른쪽 열 첫 번째)
        if st.button("⏱️ 실전 모의고사"):
            move("exam")
            
        # ⭐ AI 오답 노트 (오른쪽 열 두 번째)
        if st.button("⭐ AI 오답 노트"):
            move("note")

    # 🔥 실전 연습 (전폭 버튼, image_14.png에는 없으나 이전 코드 기능을 위해 하단에 배치)
    if st.button("🔥 실전 연습"):
        move("practice")


# --- 하위 페이지들 ---

# 1. 📸 [핵심] AI 부품 판독기 (사진 연결 기능 구현)
elif st.session_state.page == "ai":
    st.title("📸 AI 부품 판독기")
    
    st.write("### [핵심 기능] AI로 부품을 판독해 보세요!")
    
    # 두 가지 이미지 입력 방식 제공
    # 1. 카메라 입력 (모바일에서 카메라 켜짐)
    camera_image = st.camera_input("카메라로 부품 사진을 찍어주세요 📸")
    
    # 2. 파일 업로드 (갤러리에서 이미지 가져오기)
    uploaded_image = st.file_uploader("또는 갤러리에서 부품 이미지를 업로드하세요 🖼️", type=["jpg", "jpeg", "png"])
    
    # 이미지 입력에 따른 처리
    if camera_image:
        st.write("카메라에서 이미지를 성공적으로 가져왔습니다! 분석을 시작합니다...")
        # st.image(camera_image) # 가져온 이미지 표시
        # AI 판독 로직이 여기에 추가됩니다.
    
    if uploaded_image:
        st.write("이미지가 성공적으로 업로드되었습니다! 분석을 시작합니다...")
        # st.image(uploaded_image) # 업로드된 이미지 표시
        # AI 판독 로직이 여기에 추가됩니다.

    st.write("---")
    st.write("👉 분석 결과가 여기에 표시될 예정입니다.")
    
    if st.button("← 뒤로"):
        move("home")

# 2. 🌿 기초 가이드 (초보자/중급자/상급자 탭 구현)
elif st.session_state.page == "guide":
    st.title("🌿 기초 가이드")
    
    # 초보자, 중급자, 상급자 탭 다시 살리기
    tab_basic, tab_inter, tab_adv = st.tabs(["초보자 (1~2주)", "중급자 (3~4주)", "상급자 (시험 직전)"])
    
    with tab_basic:
        st.header("1단계: 초보자 가이드")
        st.write("""
        - **주요 목표:** 핵심 이론 및 부품 명칭 익히기
        - **학습 내용:**
            - 엔진 시스템 기초 (4행정 사이클)
            - 섀시 기초 및 주요 부품 명칭
            - 전기 장치 기초 및 기본 멀티미터 사용법
        - **활용 팁:** [핵심] AI 부품 판독기를 활용하여 부품 이름을 맞춰보며 공부하세요.
        """)
    
    with tab_inter:
        st.header("2단계: 중급자 가이드")
        st.write("""
        - **주요 목표:** 실제 정비 절차 및 회로도 분석
        - **학습 내용:**
            - 엔진 튠업 및 스캐너 활용법
            - 섀시 얼라이먼트 및 브레이크 시스템 정비
            - 복잡한 전장 회로도 읽는 법 및 고장 진단
        - **활용 팁:** 기초 가이드 내용을 심화하고 실전 모의고사를 시작해 보세요.
        """)
        
    with tab_adv:
        st.header("3단계: 상급자 가이드")
        st.write("""
        - **주요 목표:** 문제 해결 능력 및 실전 감각 키우기
        - **학습 내용:**
            - 실제 차량을 활용한 고장 진단 시뮬레이션
            - 실전 모의고사 무한 반복 풀이
            - ⭐ AI 오답 노트를 활용한 약점 분석 및 극복
        - **활용 팁:** 실전 연습 모드를 통해 실제 시험 시간과 동일하게 훈련하세요.
        """)

    if st.button("← 뒤로"):
        move("home")

# 3. ⏱️ 실전 모의고사
elif st.session_state.page == "exam":
    st.title("⏱️ 실전 모의고사")
    st.write("👉 시험 문제 풀기 및 채점 기능이 연결될 예정입니다.")
    
    # 모의고사 목록 예시
    with st.expander("2024년 2회차 실기 모의고사", expanded=True):
        st.write("- [핵심] AI 부품 판독 문제 (10문항)")
        st.write("- 엔진 고장 진단 (2문항)")
        st.write("- 섀시 전장 회로 분석 (2문항)")
        if st.button("시험 시작 🔥"):
            st.write("👉 시험이 곧 시작됩니다.")

    if st.button("← 뒤로"):
        move("home")

# 4. ⭐ AI 오답 노트
elif st.session_state.page == "note":
    st.title("⭐ AI 오답 노트")
    st.write("👉 틀린 문제를 자동으로 정리하여 보여줍니다.")
    
    st.write("### ⭐ 당신의 약점, AI가 분석했습니다.")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="최다 오답 분야", value="전기 장치 (회로 분석)")
    with col2:
        st.metric(label="틀린 문제 수", value="25개", delta="-5개")
        
    st.write("오답 내용을 분석하여 취약한 부분의 기초 가이드를 추천해 드립니다.")
    if st.button("전기 장치 기초 가이드 보러 가기"):
        st.write("👉 전기 장치 가이드로 이동합니다.")

    if st.button("← 뒤로"):
        move("home")

# 5. 🔥 실전 연습
elif st.session_state.page == "practice":
    st.title("🔥 실전 연습")
    st.write("👉 반복 훈련 모드입니다. 특정 파트만 집중적으로 연습할 수 있습니다.")
    
    st.radio("연습할 파트를 선택하세요", ["엔진", "섀시", "전기", "전장 회로"])
    
    if st.button("연습 시작 🚀"):
        st.write("👉 연습 모드가 시작됩니다.")

    if st.button("← 뒤로"):
        move("home")