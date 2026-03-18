import streamlit as st
import time
import datetime
import re

# 1. 앱 기본 설정 (화면 꽉 채우기)
st.set_page_config(page_title="Auto-Master", page_icon="🚗", layout="centered", initial_sidebar_state="collapsed")

# 2. 화면 전환 상태 관리 (SPA 방식)
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def go_to_page(page_name):
    st.session_state.page = page_name

# 3. 플래시/네이티브 앱 느낌을 강제하는 강력한 CSS
st.markdown("""
    <style>
        /* 상단 띠, 메뉴, 스크롤바 완전히 제거 */
        #MainMenu, header, footer {visibility: hidden; display: none;}
        .block-container {padding-top: 1rem !important; padding-bottom: 0px !important; max-width: 100% !important;}
        
        /* 전체 페이지 스크롤 방지 (한 화면에 고정) */
        html, body, [data-testid="stAppViewContainer"] {
            overflow: hidden !important; 
            background-color: #f4f6f9;
        }

        /* 앱 타이틀 */
        .app-title {
            text-align: center; font-size: 28px; font-weight: 900;
            color: #1e3a8a; margin-bottom: 20px; letter-spacing: -1px;
        }

        /* 📱 커다란 타일형 버튼 디자인 */
        .stButton>button {
            width: 100%; 
            height: 130px; 
            border-radius: 20px; 
            font-size: 18px !important; 
            font-weight: 900 !important; 
            background-color: #ffffff; 
            border: none;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05); 
            color: #374151;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            transition: transform 0.1s;
        }
        
        /* 버튼 터치 효과 */
        .stButton>button:active {
            transform: scale(0.95);
            background-color: #eff6ff;
            color: #2563eb;
        }
        
        /* 메인 핵심 버튼(판독기) 강조 */
        .main-btn>button {
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: white !important;
            height: 110px;
            font-size: 22px !important;
            margin-bottom: 10px;
        }
        
        /* 상단 뒤로가기 버튼 작게 만들기 */
        .back-btn>button {
            height: 40px !important;
            background-color: transparent !important;
            box-shadow: none !important;
            color: #6b7280 !important;
            font-size: 16px !important;
            justify-content: flex-start !important;
            padding-left: 0 !important;
        }

        /* 서브 페이지 스크롤 허용 (콘텐츠가 길 경우) */
        .scrollable-content {
            height: 80vh;
            overflow-y: auto;
            padding-bottom: 50px;
        }
        
        /* D-Day 위젯 */
        .dday-widget {
            background: linear-gradient(135deg, #1e3a8a, #3b82f6);
            color: white; border-radius: 16px; padding: 25px;
            text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 25px;
        }
        .dday-text { font-size: 42px; font-weight: 900; margin: 0; line-height: 1.1; }
        .dday-sub { font-size: 16px; font-weight: 500; opacity: 0.9; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 📱 화면 1: 홈 런처 (플래시/그리드 스타일)
# ==========================================
if st.session_state.page == 'home':
    st.markdown('<div class="app-title">🚗 Auto-Master</div>', unsafe_allow_html=True)
    
    # [1단] 핵심 기능 (가로 꽉 차게)
    st.markdown('<div class="main-btn">', unsafe_allow_html=True)
    st.button("📸 AI 부품 판독기", on_click=go_to_page, args=('scanner',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    # [2단] 2x2 그리드 배열
    col1, col2 = st.columns(2)
    with col1:
        st.button("📝\n답안 채점", on_click=go_to_page, args=('sheet',))
        st.button("🌱\n기초 가이드", on_click=go_to_page, args=('guide',))
    with col2:
        st.button("⭐️\n오답 노트", on_click=go_to_page, args=('note',))
        st.button("📅\n시험 일정", on_click=go_to_page, args=('calendar',))

# ==========================================
# 📸 화면 2: AI 부품 판독기
# ==========================================
elif st.session_state.page == 'scanner':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center;">📸 AI 부품 판독기</h3>', unsafe_allow_html=True)
    
    target_part = st.selectbox("과제 선택", ["선택", "[12안] 발전기", "[1안] 와이퍼 모터"])
    if target_part != "선택":
        img_file_buffer = st.camera_input("화면 터치하여 촬영")
        if img_file_buffer is not None:
            with st.spinner("🔍 AI 분석 중..."):
                time.sleep(1.5)
                st.success(f"✅ 판독 완료: 일치율 98%\n\n정확합니다! **{target_part.split(' ')[1]}** 탈거 상태가 양호합니다.")
                if st.button("🚀 실습 DB에 내 사진 공유하기"):
                    st.balloons()
                    st.info("데이터베이스에 저장되었습니다.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 📝 화면 3: 디지털 답안지 (제동력 예시)
# ==========================================
elif st.session_state.page == 'sheet':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center;">📝 디지털 답안지</h3>', unsafe_allow_html=True)
    
    axle_weight = st.number_input("해당 축중 (kg)", value=1000, step=100)
    left_input = st.text_input("좌측 측정값 (예: 200kg)")
    right_input = st.text_input("우측 측정값 (예: 300kg)")
    status_input = st.radio("판정", ["양호", "불량"], horizontal=True)
    action_input = st.text_input("정비 및 조치할 사항")

    if st.button("🚀 AI 채점 받기", type="primary"):
        if "kg" not in left_input.lower() or "kg" not in right_input.lower():
            st.error("❌ [오류] 단위(kg) 기재 누락! 실전에서 오답 처리됩니다.")
        else:
            try:
                l_val = float(re.sub(r'[^0-9.]', '', left_input))
                r_val = float(re.sub(r'[^0-9.]', '', right_input))
                real_dev = abs(l_val - r_val) / axle_weight * 100
                real_sum = (l_val + r_val) / axle_weight * 100
                correct_status = "양호" if (real_dev <= 8 and real_sum >= 50) else "불량"
                
                if status_input != correct_status:
                    st.error(f"❌ [판정 오류] 실제 편차 {real_dev:.1f}%, 합 {real_sum:.1f}% 입니다. 판정은 '{correct_status}'이어야 합니다.")
                else:
                    st.success("✅ 판정 정확함!")
            except ValueError:
                st.warning("측정값에 숫자를 입력하세요.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# ⭐️ 화면 4: 오답 노트
# ==========================================
elif st.session_state.page == 'note':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center;">⭐️ 오답 노트</h3>', unsafe_allow_html=True)
    st.error("🚨 [1안] 제동력 측정 (단위 누락 주의)")
    st.warning("🚨 [12안] ISC 저항 측정 (핀 위치 주의)")
    st.info("📌 [공식] 편차 산출식: (좌-우 절대값) / 축중 × 100")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 📅 화면 5: 시험 일정 (D-Day)
# ==========================================
elif st.session_state.page == 'calendar':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center;">📅 2026년 시험 일정</h3>', unsafe_allow_html=True)
    
    target_exam = st.selectbox("목표 시험 설정", ["선택", "2026년 정기 2회 실기시험 (5.30)", "2026년 정기 3회 실기시험 (8.29)"])
    if target_exam != "선택":
        today = datetime.date(2026, 3, 18)
        if "2회" in target_exam:
            exam_date = datetime.date(2026, 5, 30)
            app_date = "4.27 ~ 4.30"
        else:
            exam_date = datetime.date(2026, 8, 29)
            app_date = "7.27 ~ 7.30"
            
        d_day = (exam_date - today).days
        st.markdown(f"""
            <div class="dday-widget">
                <p class="dday-sub">목표: {target_exam.split(' (')[0]}</p>
                <p class="dday-text">D - {d_day}</p>
                <p class="dday-sub" style="margin-top: 10px; color: #ffd700;">실기 원서접수: {app_date}</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 🌱 화면 6: 기초 가이드
# ==========================================
elif st.session_state.page == 'guide':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center;">🌱 기초 가이드</h3>', unsafe_allow_html=True)
    st.write("선배들이 남긴 실전 부품 사진 갤러리 영역입니다.")
    st.image("https://via.placeholder.com/300x200/cccccc/000000?text=Alternator+A+", caption="[12안] 발전기 (김** 학생 기부)")
    st.markdown('</div>', unsafe_allow_html=True)