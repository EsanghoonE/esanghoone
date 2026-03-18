import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="Auto-Master",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 이미지 하단의 브라우저 UI와 아이콘을 제거하고 앱 내부 스타일링에 집중하기 위해
# st.markdown을 사용하여 사용자 정의 CSS를 주입합니다.
# 특히, 배경 이미지, 사용자 카드, 버튼 그라데이션 및 테두리 스타일을 이미지와 일치시킵니다.
st.markdown(
    """
<style>
/* 전체 앱 배경 이미지 설정 */
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1579612085023-e29864299446?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MXwyMjEyMTB8MHwxfHNlYXJjaHwxfHx0ZXNsYSUyMG1vZGVsJTIwM3xlbnwwfHx8&ixlib=rb-1.2.1&q=80&w=1080");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}

/* 전체 텍스트 및 제목 스타일 */
[data-testid="stHeader"] {
    background-color: transparent;
}
[data-testid="stAppViewContainer"] .main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
.title-bar {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 2.5rem;
    color: white;
    font-weight: bold;
    margin-bottom: 1.5rem;
}
.title-bar span {
    font-size: 2rem;
    margin-right: 0.5rem;
}

/* 사용자 정보 카드 스타일 */
.user-card {
    background-color: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(5px);
    border-radius: 1.5rem;
    padding: 1rem 1.5rem;
    margin-bottom: 1.5rem;
    color: white;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}
.user-info {
    font-size: 1rem;
    margin-bottom: 0.5rem;
}
.user-info span {
    font-size: 1.2rem;
    margin-right: 0.3rem;
}
.d-day-text {
    font-size: 2rem;
    font-weight: bold;
    color: #4facfe; /* 파란색 D-Day */
    margin: 0;
}

/* 버튼 그리드 레이아웃 */
.button-container {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
}
.button-row {
    display: flex;
    gap: 1.2rem;
}

/* 버튼 기본 스타일 */
.custom-button {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    color: white;
    text-decoration: none;
    font-weight: bold;
    font-size: 1.1rem;
    border-radius: 1.2rem;
    padding: 1.2rem;
    border: none;
    cursor: pointer;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}
.custom-button span {
    font-size: 1.4rem;
    margin-right: 0.8rem;
}

/* 개별 버튼 스타일 */
.custom-button.ai-part-pred {
    background: linear-gradient(90deg, #4facfe 0%, #ee4c63 100%);
    border: 2px solid white;
}
.custom-button.basic-guide {
    background-color: #1c2a4f;
    border: 2px solid transparent;
}
.custom-button.basic-guide span {
    color: #00c851;
}
.custom-button.mock-exam {
    background-color: #1c2a4f;
    border: 2px solid #00d2ff;
}
.custom-button.mock-exam span {
    color: #00d2ff;
}
.custom-button.ai-incorrect-note {
    background-color: #6f4e37;
    border: 2px solid #ff9f43;
}
.custom-button.ai-incorrect-note span {
    color: #ff9f43;
}
.custom-button.practical-practice {
    background-color: rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(5px);
    border: 2px solid rgba(255, 255, 255, 0.5);
    color: white;
}
.custom-button.practical-practice span {
    color: white;
}

/* 하단 아이콘 */
.app-footer-icons {
    position: absolute;
    bottom: 2rem;
    right: 2rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    color: white;
    font-size: 1.5rem;
}
.icon-checkerboard {
    background-color: white;
    color: black;
    border-radius: 50%;
    width: 2rem;
    height: 2rem;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1rem;
}
.icon-crown {
    background-color: #ff4136;
    color: white;
    border-radius: 5px;
    padding: 0.2rem 0.5rem;
    font-size: 1.2rem;
}
</style>
    """,
    unsafe_allow_html=True,
)

# 앱 제목
st.markdown(
    """<div class="title-bar"><span>🚗</span>Auto-Master</div>""",
    unsafe_allow_html=True,
)

# 사용자 정보 카드
st.markdown(
    """
<div class="user-card">
    <div class="user-info"><span>👤</span>용산철도고 학생 님의 목표: 2회차 실기</div>
    <p class="d-day-text">D - 73</p>
</div>
""",
    unsafe_allow_html=True,
)

# 버튼 그리드
st.markdown(
    """
<div class="button-container">
    <a href="#" class="custom-button ai-part-pred"><span>📸</span>[핵심] AI 부품 판독기</a>
    <div class="button-row">
        <a href="#" class="custom-button basic-guide"><span>🌿</span>기초 가이드</a>
        <a href="#" class="custom-button mock-exam"><span>⏱️</span>실전 모의고사</a>
    </div>
    <div class="button-row">
        <a href="#" class="custom-button basic-guide"><span>🌿</span>기초 가이드</a>
        <a href="#" class="custom-button ai-incorrect-note"><span>⭐️</span>AI 오답 노트</a>
    </div>
    <a href="#" class="custom-button practical-practice"><span>🔧</span>실전 연습</a>
</div>
""",
    unsafe_allow_html=True,
)

# 앱 하단 아이콘 (이미지 내부 아이콘 복제)
st.markdown(
    """
<div class="app-footer-icons">
    <div class="icon-checkerboard">🏁</div>
    <div class="icon-crown">👑</div>
</div>
""",
    unsafe_allow_html=True,
)