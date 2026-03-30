import streamlit as st
from datetime import datetime
import time  # 로딩 연출용
import os    # 파일 경로 확인용

# ========================================================
# [고도화 준비] 1. 진짜 AI 모델 연결을 위한 설정 (가이드)
# ========================================================
# 실제 모델 연결 시 이 부분의 주석을 해제하고 라이브러리를 임포트하세요.
# import tensorflow as tf
# from PIL import Image, ImageOps
# import numpy as np

# 가상의 모델 로드 함수 (실제 연결 시 구현 필요)
@st.cache_resource # 모델을 한 번만 로드하여 세션 간 공유
def load_car_part_model():
    # ---------------------------------------------------------
    # [설명] 여기에 실제 모델 파일(.h5, .pth 등) 로드 코드를 작성합니다.
    # 예: model = tf.keras.models.load_model('my_car_part_model.h5')
    # 현재는 모델 파일이 없으므로 Dummy(Fake) 모델을 반환한다고 가정합니다.
    # ---------------------------------------------------------
    class DummyModel:
        def predict(self, img_array):
            # 가상의 예측 결과 반환 (0: 점화플러그, 1: 브레이크패드, 2: 에어필터)
            return [[0.95, 0.03, 0.02]] # 점화플러그일 확률 95%
    return DummyModel()

# Fake 모델 로드 (앱 실행 시 뼈대 구성)
model = load_car_part_model()

# ========================================================
# [고도화 준비] 2. 실전 모의고사 DB 구조 구축 (가이드)
# ========================================================
# 실제 상용 앱에서는 SQL DB를 쓰지만, 시연용/졸업과제용으로는 Python Dictionary가 가장 빠르고 쉽습니다.
# 필요에 따라 이 구조를 확장하여 더 많은 문제를 추가하세요.
mock_exams_db = {
    "2024년 2회차 실기 모의고사": [
        {
            "id": 1,
            "type": "AI 판독",
            "question": "다음 부품의 사진을 찍고 정확한 명칭과 상태(양호/불량)를 판독하시오.",
            "correct_part_name": "점화 플러그",
            "image_path": "placeholder_spark_plug.jpg" # 실제 이미지를 부록 폴더에 넣고 경로 수정 필요
        },
        {
            "id": 2,
            "type": "엔진 고장진단",
            "question": "엔진 부조 현상이 발생합니다. 스캐너 데이터와 점화 장치를 점검하여 고장 원인을 찾아내고 정비 하시오.",
            "image_path": "placeholder_engine_scanner.jpg"
        }
    ],
    "2024년 1회차 실기 모의고사": [
        {
            "id": 1,
            "type": "섀시 정비",
            "question": "브레이크 패드를 탈거하고 마모 한계를 측정하여 규정값과 비교 판단 하시오."
        }
    ]
}


# ------------------ 1. 페이지 설정 (고정) ------------------
st.set_page_config(
    page_title="Auto-Master",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ------------------ 2. CSS (배경 및 UI/UX 고정, AI 버튼 특별화) ------------------
bg_url = "https://i.imgur.com/evCoCnM.jpg"

st.markdown(f"""
<style>
/* 배경 및 전체 레이아웃 (고정) */
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
    padding-top: 2rem;
}}

.title {{
    text-align: center;
    font-size: 2.3rem;
    font-weight: 900;
    color: white;
    text-shadow: 2px 2px 5px rgba(0,0,0,0.6);
    margin-bottom: 10px;
}}

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

.d-day-info {{ margin-bottom: 15px; }}

.d {{
    font-size: 48px;
    font-weight: 900;
    color: #0f172a;
    margin-top: 5px;
}}

/* 기본 st.button 유리 질감 (고정) */
div.stButton > button {{
    width: 100%;
    height: 70px;
    border-radius: 18px;
    background: rgba(20, 40, 80, 0.8); /* 진한 남색 반투명 */
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

/* 기본 버튼 호버 효과 (고정) */
div.stButton > button:hover {{
    background: rgba(0, 198, 255, 0.9);
    border: 1px solid white;
    transform: scale(1.03);
    color: white;
}}

/* ========================================================
   [UI/UX 차별화] 💡 핵심 기능: AI 판독기 버튼 '무지개색' 특별화
   ======================================================== */
/* Home 페이지의 첫 번째 컬럼(AI 판독기) 버튼만 무지개 그라데이션 적용 */
[data-testid="column"]:first-child div.stButton > button {{
    background: linear-gradient(135deg, #FF007F, #FFD700, #00C6FF, #00E676, #FF007F);
    background-size: 400% 400%; /* 움직이는 애니메이션 효과 */
    border: 3px solid white;
    box-shadow: 0 0 15px rgba(255, 255, 255, 0.7);
    color: white !important;
    font-size: 19px; /* 조금 더 크게 */
    width: 100%;
    margin-right: -10px;
    animation: rainbow 5s ease infinite; /* 부드러운 애니메이션 */
}}

/* 무지개 그라데이션 움직임 정의 */
@keyframes rainbow {{ 
    0%{{background-position:0% 50%}}
    50%{{background-position:100% 50%}}
    100%{{background-position:0% 50%}}
}}

/* 무지개 버튼 호버 효과: 더 밝게 빛남 */
[data-testid="column"]:first-child div.stButton > button:hover {{
    transform: scale(1.05); /* 조금 더 크게 */
    box-shadow: 0 0 25px rgba(255, 255, 255, 1);
    background: linear-gradient(135deg, #FF007F, #FFD700, #00C6FF, #00E676, #FF007F);
    border: 3px solid white;
}}

div.stButton > button span {{
    margin-right: 10px;
}}

h1, h2, h3, h4, h5, h6, p, li, div[data-testid="stMarkdownContainer"] > p {{
    color: white;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
}}

[data-testid="stTabs"] [data-baseweb="tab"] {{
    background-color: rgba(20, 40, 80, 0.6);
    color: white;
    border-radius: 10px 10px 0 0;
    margin-right: 5px;
    font-weight: bold;
}}
[data-testid="stTabs"] [data-baseweb="tab"]:focus {{ outline: none; }}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {{ background-color: #00c6ff; }}
</style>
""", unsafe_allow_html=True)

# ------------------ 3. 상태 관리 (더블 클릭 해결, 고정) ------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

def move(page):
    st.session_state.page = page
    st.rerun()

# ------------------ 4. D-DAY 계산 (고정) ------------------
target_date = datetime(2026, 5, 30) 
today = datetime.now()
d_day_count = (target_date - today).days

# ------------------ 5. 페이지 라우팅 및 렌더링 (고도화 반영) ------------------

# --- 메인 홈 화면 (UI 고정, AI 버튼만 특별화됨) ---
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
        # 이 버튼이 CSS에서 무지개색으로 특별 스타일링됩니다.
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


# --- 1. 📸 [핵심] AI 부품 판독기 (진짜 모델 연결 뼈대) ---
elif st.session_state.page == "ai":
    st.title("📸 AI 부품 판독기")
    st.write("### 부품 사진을 찍거나 올려주세요!")
    
    camera_image = st.camera_input("카메라로 촬영하기 📸")
    uploaded_image = st.file_uploader("ギャラリ에서 선택하기 🖼️", type=["jpg", "jpeg", "png"])
    
    image_to_process = camera_image or uploaded_image

    if image_to_process:
        st.write("---")
        st.image(image_to_process, caption="입력된 부품 이미지", use_container_width=True)
        
        with st.spinner('AI가 실제 모델 기반으로 부품을 정밀 분석 중입니다... 🔍'):
            # ========================================================
            # [고도화 반영] 진짜 AI 모델 연결 및 예측 로직 삽입 위치
            # ========================================================
            # 1. 실제 예측을 위한 데이터 전처리 (주석 해제 필요)
            # image = Image.open(image_to_process).convert('RGB')
            # size = (224, 224) # 모델에 맞는 해상도로 조정
            # image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
            # img_array = np.asarray(image)
            # normalized_img_array = (img_array.astype(np.float32) / 127.0) - 1 # 정규화
            # data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            # data[0] = normalized_img_array

            # 2. 실제 모델 예측 호출 (주석 해제 필요)
            # prediction = model.predict(data)
            # index = np.argmax(prediction) # 가장 확률 높은 클래스 인덱스
            # class_name = ["점화 플러그", "브레이크 패드", "에어 필터"][index]
            # confidence_score = prediction[0][index]

            # ---------------------------------------------------------
            # Dummy 모델 결과 시뮬레이션 (실제 연결 시 위 주석 사용)
            prediction_Dummy = model.predict(None)
            index_Dummy = 0 # 점화플러그
            class_name_Dummy = ["점화 플러그", "브레이크 패드", "에어 필터"][index_Dummy]
            confidence_Dummy = prediction_Dummy[0][index_Dummy]
            # ---------------------------------------------------------

            time.sleep(2) # 로딩 연출용 대기
            
        # 3. 모델 기반 실제 결과 출력
        st.success("✅ 판독 완료!")
        st.info(f"""
        💡 **AI 분석 결과 (가상 모델 가동):**
        - **판독 부품명:** **{class_name_Dummy}**
        - **판독 신뢰도:** **{confidence_Dummy*100:.1f}%**
        - **설명:** 엔진 실린더 내의 압축된 혼합기에 불꽃을 튀겨 점화시키는 핵심 부품입니다. 카본 퇴적물이 적고 간극이 양호합니다.
        """)
        
        if st.button("🔄 다른 부품 판독하기"):
            st.rerun()

    st.write("---")
    if st.button("← 홈으로 돌아가기"):
        move("home")

# --- 2. 🌿 기초 가이드 (고정) ---
elif st.session_state.page == "guide":
    st.title("🌿 기초 가이드")
    tab_basic, tab_inter, tab_adv = st.tabs(["초보자 (1~2주)", "중급자 (3~4주)", "상급자 (시험 직전)"])
    
    with tab_basic:
        st.header("1단계: 초보자 가이드")
        st.write("- 핵심 이론 및 부품 명칭 익히기, 엔진 기초")
    with tab_inter:
        st.header("2단계: 중급자 가이드")
        st.write("- 정비 절차 및 회로도 분석, 엔진 튠업, 섀시 얼라이먼트")
    with tab_adv:
        st.header("3단계: 상급자 가이드")
        st.write("- 차량 고장 진단 시뮬레이션, 오답 노트 분석")

    st.write("---")
    if st.button("← 홈으로 돌아가기"):
        move("home")

# --- 3. ⏱️ 실전 모의고사 (DB 구조 반영) ---
elif st.session_state.page == "exam":
    st.title("⏱️ 실전 모의고사")
    st.write("👉 시험 문제 풀기 및 채점 기능")

    # ========================================================
    # [고도화 반영] 모의고사 DB 동적 로드
    # ========================================================
    # DB에서 모의고사 목록 가져와 선택하게 함
    exam_names = list(mock_exams_db.keys())
    selected_exam = st.selectbox("연습할 모의차수를 선택하세요", exam_names)
    
    questions = mock_exams_db[selected_exam]
    st.write(f"### 📋 {selected_exam}")
    
    for q in questions:
        # st.expander를 통해 각 문제를 깔끔하게 펼쳐보게 함
        with st.expander(f"문제 {q['id']} - [{q['type']}]", expanded=(q['id']==1)):
            st.write(q['question'])
            if 'image_path' in q:
                # 시연 시 이미지가 없다면 경로 오류 방지
                if os.path.exists(q['image_path']):
                    st.image(q['image_path'], use_container_width=True)
                else:
                    st.warning(f"🏞️ 부록 이미지가 없습니다. (경로 확인: {q['image_path']})")
            if q['type'] == "AI 판독":
                if st.button(f"📸 {q['correct_part_name']} 판독하기"):
                    # 실제 시나리오에서는 이 버튼 누르면 판독기 탭으로 이동하거나 즉시 판독 기능 호출
                    move("ai")
            
    if st.button("시험 전체 종료 🏁"):
        st.success("모의고사가 종료되었습니다. 수고하셨습니다!")

    st.write("---")
    if st.button("← 홈으로 돌아가기"):
        move("home")

# --- 4. ⭐ AI 오답 노트 (고정) ---
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

# --- 5. 🔥 실전 연습 (고정) ---
elif st.session_state.page == "practice":
    st.title("🔥 실전 연습")
    st.radio("연습할 파트를 선택하세요", ["엔진", "섀시", "전기", "전장 회로"])
    if st.button("연습 시작 🚀"):
        st.success("연습 모드가 시작됩니다.")
    st.write("---")
    if st.button("← 홈으로 돌아가기"):
        move("home")