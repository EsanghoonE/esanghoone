import streamlit as st
import base64

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="Auto-Master",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- 2. 로컬 배경 이미지를 Base64로 변환하는 함수 ---
# '졸업과제 어플 배경 테슬라.jpg' 파일이 app.py와 같은 폴더에 있어야 합니다.
bg_image_path = "졸업과제 어플 배경 테슬라.jpg" 

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return "" # 파일이 없을 경우 빈 문자열 반환

bg_base64 = get_base64_of_bin_file(bg_image_path)

# --- 3. 사용자 정의 CSS 주입 ---
st.markdown(
    f"""
    <style>
    /* 전체 앱 배경 이미지 설정 */
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}

    /* Streamlit 기본 헤더 및 여백 투명화/최소화 */
    [data-testid="stHeader"] {{
        background-color: transparent;
    }}
    [data-testid="stAppViewContainer"] .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 500px; /* 모바일 화면처럼 좁게 보이도록 최대 너비 설정 */
        margin: 0 auto;
    }}

    /* 제목 스타일 */
    .title-bar {{
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 2rem;
        color: white;
        font-weight: 900;
        margin-bottom: 1rem;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.5);
    }}
    .title-bar span {{
        font-size: 1.8rem;
        margin-right: 0.5rem;
    }}

    /* 사용자 정보 투명 카드 (Glassmorphism) */
    .user-card {{
        background-color: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 1.2rem;
        padding: 1.5rem;
        margin-bottom: 2rem;
        color: #2c3e50;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }}
    .user-info {{
        font-size: 0.95rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }}
    .d-day-text {{
        font-size: 2.5rem;
        font-weight: 900;
        color: #2c3e50;
        margin: 0;
    }}

    /* 버튼 레이아웃 */
    .button-container {{
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }}
    .button-row {{
        display: flex;
        gap: 1rem;
    }}

    /* 버튼 공통 스타일 */
    .custom-button {{
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        text-decoration: none;
        font-weight: bold;
        font-size: 1rem;
        border-radius: 1rem;
        padding: 1.2rem 1rem;
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s;
    }}
    .custom-button:hover {{
        transform: scale(1.02);
    }}
    .custom-button span {{
        font-size: 1.2rem;
        margin-right: 0.5rem;
    }}

    /* 개별 버튼 세부 스타일 */
    .ai-part-pred {{
        background: linear-gradient(90deg, #00c6ff 0%, #ff007f 100%);
        width: 48%; /* 절반 너비만 차지하도록 설정 */
        justify-content: flex-start; /* 왼쪽 정렬 */
    }}
    
    .half-btn {{
        flex: 1;
        justify-content: flex-start;
    }}
    
    .basic-guide {{
        background-color: #142850; /* 진한 남색 */
    }}
    
    .mock-exam {{
        background-color: rgba(20, 40, 80, 0.4);
        border: 2px solid #00c6ff; /* 하늘색 테두리 */
        backdrop-filter: blur(5px);
    }}
    
    .ai-incorrect-note {{
        background: linear-gradient(135deg, #8B5A2B 0%, #5C3A21 100%); /* 갈색 그라데이션 */
    }}
    
    .practical-practice {{
        background-color: rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        color: white;
        width: 100%; /* 전체 너비 */
    }}

    /* 하단 우측 아이콘 */
    .app-footer-icons {{
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        z-index: 100;
    }}
    .icon-checkerboard {{
        background-color: white;
        color: black;
        border-radius: 50%;
        width: 2.5rem;
        height: 2.5rem;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 1.2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }}
    .icon-crown {{
        background-color: #ff4757;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 0.6rem;
        font-size: 1.2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- 4. HTML 요소 렌더링 ---

# 제목
st.markdown("""<div class="title-bar"><span>🚗</span>Auto-Master</div>""", unsafe_allow_html=True)

# 카드
st.markdown("""
<div class="user-card">
    <div class="user-info">👤 용산철도고 학생 님의 목표: 2회차 실기</div>
    <p class="d-day-text">D - 73</p>
</div>
""", unsafe_allow_html=True)

# 버튼 그리드
st.markdown("""
<div class="button-container">
    <a href="#" class="custom-button ai-part-pred"><span>📸</span>[핵심] AI 부품 판독기</a>
    
    <div class="button-row">
        <a href="#" class="custom-button half-btn basic-guide"><span>🌿</span>기초 가이드</a>
        <a href="#" class="custom-button half-btn mock-exam"><span>⏱️</span>실전 모의고사</a>
    </div>
    
    <div class="button-row">
        <a href="#" class="custom-button half-btn basic-guide"><span>🌿</span>기초 가이드</a>
        <a href="#" class="custom-button half-btn ai-incorrect-note"><span>⭐</span>AI 오답 노트</a>
    </div>
    
    <a href="#" class="custom-button practical-practice">실전 연습</a>
</div>
""", unsafe_allow_html=True)

# 하단 우측 플로팅 아이콘
st.markdown("""
<div class="app-footer-icons">
    <div class="icon-checkerboard">🏁</div>
    <div class="icon-crown">👑</div>
</div>
""", unsafe_allow_html=True)