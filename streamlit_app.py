import streamlit as st
import time
import datetime
import re
import random

# ==========================================
# 1. 앱 기본 설정 및 전역 상태 관리
# ==========================================
st.set_page_config(page_title="Auto-Master", page_icon="🚗", layout="centered", initial_sidebar_state="collapsed")

if 'page' not in st.session_state: st.session_state.page = 'home'
if 'user_name' not in st.session_state: st.session_state.user_name = "용산철도고 학생"
if 'exam_date' not in st.session_state: st.session_state.exam_date = datetime.date(2026, 5, 30)
if 'exam_name' not in st.session_state: st.session_state.exam_name = "2회차 실기"

def go_to_page(page_name):
    st.session_state.page = page_name

# ==========================================
# 2. 🔥 스크린샷과 완벽히 일치하는 CSS 🔥
# ==========================================
st.markdown("""
    <style>
        /* 기본 메뉴 숨김 및 Safari 화면 밀림 방지 */
        #MainMenu, header, footer {visibility: hidden; display: none;}
        .block-container {
            padding-top: 1.5rem !important; 
            padding-bottom: env(safe-area-inset-bottom) !important; 
            max-width: 100% !important;
        }
        ::-webkit-scrollbar { display: none; }
        
        /* 🌟 스크롤 불가, 사진 속 밝고 깨끗한 그림 배경 이미지 고정 🌟 */
        [data-testid="stAppViewContainer"] {
            background-image: url('https://images.unsplash.com/photo-1579612085023-e29864299446?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MXwyMjEyMTB8MHwxfHNlYXJjaHwxfHx0ZXNsYSUyMG1vZGVsJTIwM3xlbnwwfHx8&ixlib=rb-1.2.1&q=80&w=1080');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            height: 100dvh !important;
            overflow: hidden !important; 
        }

        /* 텍스트 가독성을 위한 전체 오버레이 */
        [data-testid="stAppViewContainer"]::before {
            content: ""; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(15, 23, 42, 0.4); /* 네이비 틴트 완화 */
            z-index: 0;
        }
        
        /* 모든 콘텐츠를 오버레이 위로 올림 */
        .main { position: relative; z-index: 1; }

        /* 앱 타이틀 */
        .app-title {
            text-align: center; font-size: 28px; font-weight: 900;
            color: #ffffff; margin-bottom: 15px; letter-spacing: -1px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }

        /* 📅 글래스모피즘 D-Day 위젯 (사진 속 남색 텍스트 반영) */
        .dday-widget {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
            color: white; border-radius: 20px; padding: 20px; text-align: center; 
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2); 
            margin-bottom: 15px; border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .dday-title { font-size: 14px; font-weight: 500; color: #334155; margin-bottom: 2px;}
        .dday-text { font-size: 38px; font-weight: 900; margin: 0; color: #1e293b; text-shadow: 0 2px 10px rgba(30, 41, 59, 0.1);}
        
        /* 📱 그리드 타일형 버튼 디자인 */
        .stButton>button {
            width: 100%; height: 75px; border-radius: 16px; font-size: 16px !important; font-weight: 800 !important; 
            background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2); color: #ffffff; 
            transition: all 0.2s; margin-bottom: 5px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-shadow: 0 1px 2px rgba(0,0,0,0.5);
        }
        .stButton>button:active { transform: scale(0.95); background: rgba(255, 255, 255, 0.25); }
        
        /* 📸 핵심 AI 판독기 버튼 (그라데이션 광선 테두리 반영) */
        .btn-primary-highlight>button {
            background: rgba(30, 41, 59, 0.8) !important;
            border: 2px solid transparent !important;
            height: 95px; font-size: 20px !important;
            box-shadow: 0 0 15px #ee4c63, 0 0 15px #3b82f6 !important;
        }

        /* 서브 버튼 맞춤 컬러 */
        .btn-navy-green>button { background: rgba(30, 41, 59, 0.8) !important; border: 1px solid rgba(255,255,255,0.1) !important;}
        .btn-navy-green>button[data-testid="stMarkdownContainer"] { color: #10b981 !important; }
        
        .btn-navy-blue>button { background: rgba(30, 41, 59, 0.8) !important; border: 2px solid #00d2ff !important;}
        .btn-navy-blue>button[data-testid="stMarkdownContainer"] { color: #00d2ff !important; }
        
        .btn-brown-orange>button { background: rgba(111, 78, 55, 0.8) !important; border: 1px solid rgba(255,255,255,0.1) !important;}
        .btn-brown-orange>button[data-testid="stMarkdownContainer"] { color: #f59e0b !important; }

        /* 하단 Wider 버튼 (실전 연습) */
        .btn-practice-transparent>button { 
            background: rgba(255, 255, 255, 0.2) !important; 
            backdrop-filter: blur(10px) !important; -webkit-backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255,255,255,0.5) !important; 
            color: #ffffff !important; text-shadow: none !important;
        }

        /* 하단 아이콘들 */
        .app-footer-icons {
            position: absolute; bottom: 2rem; right: 2rem; display: flex; align-items: center; gap: 1rem; color: white; font-size: 1.5rem;
        }
        .icon-checkerboard { background-color: white; color: black; border-radius: 50%; width: 2rem; height: 2rem; display: flex; justify-content: center; align-items: center; font-size: 1rem; }
        .icon-crown { background-color: #ff4136; color: white; border-radius: 5px; padding: 0.2rem 0.5rem; font-size: 1.2rem; }

        /* 서브 페이지 스크롤 영역 */
        .scrollable-content { height: 82dvh; overflow-y: auto; padding-bottom: env(safe-area-inset-bottom); padding-top: 5px; }
        
        /* 뒤로가기 버튼 */
        .back-btn>button {
            height: 40px !important; background: rgba(255, 255, 255, 0.1) !important; 
            border: 1px solid rgba(255, 255, 255, 0.2) !important; color: #ffffff !important; 
            border-radius: 10px; margin-bottom: 10px; text-shadow: none;
        }
        
        /* 서브페이지 콘텐츠 카드 */
        .content-card {
            background: rgba(255, 255, 255, 0.95); padding: 20px; border-radius: 18px; 
            border: 1px solid rgba(255, 255, 255, 0.3); margin-bottom: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1); color: #1e293b;
        }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 🏠 홈 화면 (런처 - 시연용 완벽 기능 통합)
# ==========================================
if st.session_state.page == 'home':
    # D-Day 계산
    today = datetime.date(2026, 3, 18)
    d_day = (st.session_state.exam_date - today).days
    d_day_str = f"D - {d_day}" if d_day >= 0 else f"D + {abs(d_day)}"
    
    st.markdown('<div class="app-title">🚗 Auto-Master</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="user-card">
            <div class="user-info">👤 {st.session_state.user_name} 님의 목표: {st.session_state.exam_name}</div>
            <div class="dday-text">{d_day_str}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # [핵심] 1. AI 부품 판독기 (그라데이션 광선 테두리)
    st.markdown('<div class="stButton btn-primary-highlight">', unsafe_allow_html=True)
    st.button("📸 [핵심] AI 부품 판독기", on_click=go_to_page, args=('scanner',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. 2x2 그리드 버튼
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="stButton btn-navy-green">', unsafe_allow_html=True)
        st.button("🌿 기초 가이드", on_click=go_to_page, args=('guide',))
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 답안 채점 버튼 (사진 속 녹색 나뭇잎 - 2개 배치된 것 반영)
        st.markdown('<div class="stButton btn-navy-green">', unsafe_allow_html=True)
        st.button("🌿 답안 채점", on_click=go_to_page, args=('sheet',))
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        # 실전 모의고사 (파란색 테두리)
        st.markdown('<div class="stButton btn-navy-blue">', unsafe_allow_html=True)
        st.button("⏱️ 실전 모의고사", on_click=go_to_page, args=('mock',))
        st.markdown('</div>', unsafe_allow_html=True)
        
        # AI 오답 노트 (갈색 바탕)
        st.markdown('<div class="stButton btn-brown-orange">', unsafe_allow_html=True)
        st.button("⭐️ AI 오답 노트", on_click=go_to_page, args=('note',))
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. 실전 연습 (가로 Wider, 반투명)
    st.markdown('<div class="stButton btn-practice-transparent">', unsafe_allow_html=True)
    st.button("🔧 실전 연습", on_click=go_to_page, args=('practice',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 4. 내 정보 설정 (작은 유틸리티 버튼)
    st.button("👤 내 정보 및 D-Day 설정", on_click=go_to_page, args=('profile',))

# ==========================================
# (이하 서브 페이지는 사진 속 디자인을 유지하며 기능을 채워 넣습니다)
# ==========================================

# 📸 AI 부품 판독기 (실제 카메라 구동 연동)
elif st.session_state.page == 'scanner':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div><div class="scrollable-content">', unsafe_allow_html=True)
    
    st.markdown('<h3 style="text-align:center; color:#ffffff;">📸 AI 부품 판독기</h3>', unsafe_allow_html=True)
    
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    target_part = st.selectbox("현재 탈거한 부품 선택", ["선택하세요", "[12안] 발전기", "[1안] 앞 쇽업소버"])
    
    if target_part != "선택하세요":
        st.info("부품이 화면 중앙에 오도록 촬영해 주세요.")
        img_buffer = st.camera_input("화면 터치하여 촬영")
        
        if img_buffer:
            with st.spinner("🔍 AI 분석 중..."):
                time.sleep(1.5)
                part_name = target_part.split('] ')[1]
                st.markdown(f"""
                    <div style="border: 2px solid #10b981; background-color: #ecfdf5; padding: 15px; border-radius: 10px; margin-top:15px;">
                        <h3 style="color:#059669; margin-top:0;">✅ 판독 결과: 일치율 98%</h3>
                        <p>정확합니다! <b>{part_name}</b>을(를) 올바르게 탈거하셨습니다.</p>
                        <p style="font-size:14px; color:#047857;">[AI 코멘트] 상태가 매우 양호합니다.</p>
                    </div>
                """, unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)


# 📝 답안 채점 (자동 채점 기능 연동)
elif st.session_state.page == 'sheet':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div><div class="scrollable-content">', unsafe_allow_html=True)
    
    st.markdown('<h3 style="text-align:center; color:#ffffff;">📝 디지털 답안 채점</h3>', unsafe_allow_html=True)
    
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.write("#### [1안 섀시] 제동력 측정")
    axle_weight = st.number_input("해당 축중 (kg)", value=1000, step=100)
    left_input = st.text_input("좌측 측정값 (예: 200kg)")
    right_input = st.text_input("우측 측정값 (예: 300kg)")
    status_input = st.radio("판정 체크", ["선택", "양호", "불량"], horizontal=True)
    action_input = st.text_input("정비 및 조치사항")

    if st.button("🚀 AI 선생님 제출", type="primary"):
        if "kg" not in left_input.lower() or "kg" not in right_input.lower():
            st.error("❌ **[치명적 오류] 단위(kg) 누락!** 산업인력공단 규정상 0점 처리됩니다.")
        else:
            try:
                l_val = float(re.sub(r'[^0-9.]', '', left_input))
                r_val = float(re.sub(r'[^0-9.]', '', right_input))
                real_dev = abs(l_val - r_val) / axle_weight * 100
                real_sum = (l_val + r_val) / axle_weight * 100
                correct_status = "양호" if (real_dev <= 8 and real_sum >= 50) else "불량"
                
                if status_input != correct_status:
                    st.error(f"❌ **[판정 오류]** 실제 편차 {real_dev:.1f}%, 합 {real_sum:.1f}% 입니다. 판정은 **'{correct_status}'**이어야 합니다.")
                else:
                    st.success("✅ **[계산/판정 정확]** 완벽합니다!")
            except ValueError:
                st.warning("측정값에 숫자를 포함해 입력하세요.")
    st.markdown('</div></div>', unsafe_allow_html=True)

# 👤 내 정보 설정 (D-Day 연동)
elif st.session_state.page == 'profile':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로 돌아가기", on_click=go_to_page, args=('home',))
    st.markdown('</div><div class="scrollable-content">', unsafe_allow_html=True)
    
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<h3>⚙️ 내 정보 및 목표 설정</h3>', unsafe_allow_html=True)
    new_name = st.text_input("이름을 입력하세요", value=st.session_state.user_name)
    target_exam = st.selectbox("목표 시험 선택", ["2026년 2회차 실기 (5.30)", "2026년 3회차 실기 (8.29)"])
    
    if st.button("💾 정보 저장 및 적용", type="primary"):
        st.session_state.user_name = new_name
        st.session_state.exam_name = target_exam.split(' (')[0]
        st.session_state.exam_date = datetime.date(2026, 5, 30) if "2회차" in target_exam else datetime.date(2026, 8, 29)
        st.success("✅ 저장 완료! 홈 화면으로 이동합니다.")
        time.sleep(0.5); go_to_page('home'); st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)


# (기타 서브 페이지는 디자인 유지)
elif st.session_state.page in ['guide', 'practice', 'note', 'mock']:
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로 돌아가기", on_click=go_to_page, args=('home',))
    st.markdown('</div><div class="scrollable-content"><div class="content-card">', unsafe_allow_html=True)
    
    if st.session_state.page == 'guide':
        st.markdown('<h3>🌿 기초 가이드</h3>', unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=500", caption="[12안] 발전기 A+ 촬영본")
    elif st.session_state.page == 'practice':
        st.markdown('<h3>🔧 실전 연습</h3>', unsafe_allow_html=True)
        st.write("체크리스트와 작업지시서가 나타납니다.")
    elif st.session_state.page == 'note':
        st.markdown('<h3>⭐️ AI 오답 노트</h3>', unsafe_allow_html=True)
        st.error("🚨 제동력 측정 (단위 누락 주의)")
    elif st.session_state.page == 'mock':
        st.markdown('<h3>⏱️ 실전 모의고사</h3>', unsafe_allow_html=True)
        if st.button("🎲 실전 과제 랜덤 뽑기"): st.session_state.mock_case = random.randint(1, 15)
        if 'mock_case' in st.session_state: st.markdown(f'<h1 style="color:#ef4444; text-align:center;">제 {st.session_state.mock_case} 안</h1>', unsafe_allow_html=True)
            
    st.markdown('</div></div>', unsafe_allow_html=True)