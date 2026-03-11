import streamlit as st

# 1. 앱 기본 설정 (화면을 넓게 쓰고, 메뉴바를 기본으로 열어둠)
st.set_page_config(page_title="Auto-Master AI", page_icon="🔧", layout="wide", initial_sidebar_state="expanded")

# 2. 커스텀 CSS (설문지 느낌을 없애고 앱 느낌을 주는 핵심 마법)
st.markdown("""
    <style>
        /* 기본 Streamlit 헤더와 푸터 숨기기 (앱처럼 보이게) */
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* 앱 스타일의 카드(Card) UI 디자인 */
        .app-card {
            background-color: #ffffff;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08); /* 그림자 효과 */
            margin-bottom: 20px;
            border-left: 6px solid #1f77b4; /* 좌측 포인트 컬러 */
            transition: transform 0.2s; /* 마우스 올렸을 때 애니메이션 */
        }
        .app-card:hover {
            transform: translateY(-5px);
        }
        .card-title {
            color: #2c3e50;
            font-size: 18px;
            font-weight: 800;
            margin-bottom: 10px;
        }
        .card-text {
            color: #7f8c8d;
            font-size: 14px;
        }
    </style>
""", unsafe_allow_html=True)

# 3. 좌측 사이드바 (App 네비게이션 메뉴)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3204/3204003.png", width=80) # 자동차 정비 아이콘
    st.title("Auto-Master")
    st.write("👤 **학생:** 용산철도고 2학년")
    
    # 앱 스타일의 진행률 바
    st.progress(0.65, text="🏆 전체 마스터 진행률: 65%")
    st.write("---")
    
    # 탭 대신 라디오 버튼으로 앱 메뉴 이동 구현
    menu = st.radio("메뉴 이동", [
        "🏠 홈 (대시보드)", 
        "🌱 기초 가이드 (초보)", 
        "🔧 실전 연습 (AI 채점)", 
        "📸 AI 부품 판독기 (Vision)",
        "⏱️ 파이널 모의고사"
    ])
    
    st.write("---")
    st.caption("Ver 1.0 (Prof. Review Demo)")

# 4. 메인 화면 구성 (선택한 메뉴에 따라 화면이 앱처럼 바뀜)

if menu == "🏠 홈 (대시보드)":
    st.title("반가워요! 오늘의 학습 현황입니다.")
    st.write("---")
    
    # 앱 스타일의 핵심 지표(Metrics) 대시보드
    col1, col2, col3 = st.columns(3)
    col1.metric(label="완료한 실습 안", value="8 / 15", delta="이번 주 2건 증가")
    col2.metric(label="AI 채점 평균", value="85점", delta="3점 상승")
    col3.metric(label="최다 취약 파트", value="전기 (전조등)", delta="-", delta_color="off")
    
    st.write("---")
    st.subheader("🚀 AI 맞춤형 오늘의 추천 학습")
    
    # 커스텀 CSS를 적용한 카드형 UI
    st.markdown("""
        <div class="app-card">
            <div class="card-title">⚠️ [1안] 전기 - 전조등 회로 점검 복습 요망</div>
            <div class="card-text">최근 실전 연습에서 '전조등 광도 판정' 오답이 발생했습니다. 실습장에 방문하여 스위치를 켜고 다시 측정해 보세요.</div>
        </div>
        <div class="app-card" style="border-left-color: #2ca02c;">
            <div class="card-title">✨ 새로운 선배들의 꿀팁 사진 도착!</div>
            <div class="card-text">[12안] 발전기 탈거 미션에 3장의 A+ 판독 사진이 업데이트되었습니다. 기초 가이드에서 확인하세요.</div>
        </div>
    """, unsafe_allow_html=True)

elif menu == "📸 AI 부품 판독기 (Vision)":
    st.title("📸 AI 부품 판독 및 업로드")
    st.info("실습장에서 직접 탈거한 부품을 촬영하여 업로드하면 AI가 즉시 판독합니다.")
    
    # 앱의 파일 업로드 기능 느낌
    uploaded_file = st.file_uploader("여기를 눌러 사진을 촬영하거나 갤러리에서 선택하세요.", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        st.success("사진이 성공적으로 업로드되었습니다! AI가 분석 중입니다...")
        # (다음 단계에 들어갈 AI 분석 시뮬레이션 코드 자리)

elif menu == "🔧 실전 연습 (AI 채점)":
    st.title("🔧 실전 연습 모드")
    # Streamlit의 탭 기능을 사용하여 앱 화면 분할
    tab1, tab2, tab3 = st.tabs(["기관 (Engine)", "새시 (Chassis)", "전기 (Electric)"])
    
    with tab2:
        st.subheader("[1안] 제동력 측정")
        st.write("여기에 아까 만든 디지털 답안지 폼이 들어갑니다.")
        st.button("답안지 열기", type="primary")

else:
    st.title(menu)
    st.write("해당 메뉴의 기능은 현재 개발 중입니다.")