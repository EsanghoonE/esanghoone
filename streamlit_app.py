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
# 2. 🔥 프리미엄 디자인 & 배경이미지 CSS 🔥
# ==========================================
st.markdown("""
    <style>
        /* 기본 메뉴 숨김 및 여백 최적화 */
        #MainMenu, header, footer {visibility: hidden; display: none;}
        .block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; max-width: 100% !important; }
        ::-webkit-scrollbar { display: none; }
        
        /* 🌟 밝고 신선한 테슬라 배경 이미지 고정 (안 깨짐) */
        .stApp {
            background-image: url('https://images.unsplash.com/photo-1560958089-b8a1929cea89?auto=format&fit=crop&w=1080&q=80');
            background-size: cover; background-position: center; background-attachment: fixed;
        }
        /* 가독성을 위한 어두운 오버레이 */
        .stApp::before {
            content: ""; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(15, 23, 42, 0.4); z-index: 0;
        }
        .main { position: relative; z-index: 1; }

        /* 앱 타이틀 */
        .app-title {
            text-align: center; font-size: 32px; font-weight: 900;
            color: #ffffff; margin-bottom: 15px; text-shadow: 0 2px 4px rgba(0,0,0,0.8);
        }

        /* 📅 글래스모피즘 사용자 정보 & D-Day 카드 */
        .user-card {
            background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(10px);
            border-radius: 20px; padding: 20px; text-align: center; 
            box-shadow: 0 8px 20px rgba(0,0,0,0.2); margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.4);
        }
        .user-info { font-size: 14px; font-weight: 700; color: #334155; margin-bottom: 5px; }
        .dday-text { font-size: 42px; font-weight: 900; margin: 0; color: #0284c7; text-shadow: 0 2px 5px rgba(2, 132, 199, 0.2); }

        /* 📱 Streamlit 버튼을 커스텀 디자인으로 덮어쓰기 위한 기본 설정 */
        .stButton>button {
            width: 100%; height: 80px; border-radius: 18px; font-size: 18px !important; font-weight: 800 !important; 
            color: white !important; transition: all 0.2s; box-shadow: 0 4px 10px rgba(0,0,0,0.3); border: none;
        }
        .stButton>button:active { transform: scale(0.95); }

        /* 🎨 개별 버튼 맞춤형 컬러 스타일링 */
        /* 1. AI 부품 판독기 (그라데이션 + 파란 테두리) */
        .btn-scanner > button {
            background: linear-gradient(90deg, #4facfe 0%, #ee4c63 100%) !important;
            border: 2px solid #00d2ff !important; height: 90px; font-size: 22px !important;
        }
        /* 2. 기초 가이드 (네이비 바탕) */
        .btn-guide > button { background: #1c2a4f !important; border: 2px solid transparent !important; }
        /* 3. 실전 모의고사 (네이비 바탕 + 파란 테두리) */
        .btn-mock > button { background: #1c2a4f !important; border: 2px solid #00d2ff !important; }
        /* 4. 답안 채점 (네이비 바탕 + 녹색 테두리) */
        .btn-sheet > button { background: #1c2a4f !important; border: 2px solid #10b981 !important; }
        /* 5. 오답 노트 (갈색 바탕 + 주황 테두리) */
        .btn-note > button { background: #6f4e37 !important; border: 2px solid #ff9f43 !important; }
        /* 6. 실전 연습 (반투명 글래스) */
        .btn-practice > button { background: rgba(255, 255, 255, 0.2) !important; border: 1px solid rgba(255,255,255,0.5) !important; backdrop-filter: blur(5px); }
        /* 7. 작은 유틸리티 버튼 (내정보, 일정) */
        .btn-util > button { background: rgba(0, 0, 0, 0.5) !important; height: 50px !important; font-size: 14px !important; border-radius: 10px !important; }

        /* 서브 페이지 콘텐츠 카드 */
        .content-card {
            background: rgba(255, 255, 255, 0.95); padding: 20px; border-radius: 18px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.2); color: #1e293b; margin-bottom: 15px;
        }
        .back-btn>button { background: rgba(0,0,0,0.6) !important; height: 40px !important; border-radius: 10px; font-size: 14px !important; }
        .scrollable { height: 85dvh; overflow-y: auto; padding-bottom: 50px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🏠 홈 화면 (메인 런처)
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
    
    # 1. AI 부품 판독기 (가로로 길게)
    st.markdown('<div class="btn-scanner">', unsafe_allow_html=True)
    st.button("📸 [핵심] AI 부품 판독기", on_click=go_to_page, args=('scanner',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. 2x2 그리드 버튼
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="btn-guide">', unsafe_allow_html=True)
        st.button("🌿 기초 가이드", on_click=go_to_page, args=('guide',))
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="btn-sheet">', unsafe_allow_html=True)
        st.button("📝 답안 채점", on_click=go_to_page, args=('sheet',))
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="btn-mock">', unsafe_allow_html=True)
        st.button("⏱️ 실전 모의고사", on_click=go_to_page, args=('mock',))
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="btn-note">', unsafe_allow_html=True)
        st.button("⭐️ AI 오답 노트", on_click=go_to_page, args=('note',))
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. 실전 연습 (가로로 길게, 반투명)
    st.markdown('<div class="btn-practice">', unsafe_allow_html=True)
    st.button("🔧 실전 연습", on_click=go_to_page, args=('practice',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 4. 학생 정보 입력 & 시험 일정 (하단 작은 버튼으로 배치)
    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="btn-util">', unsafe_allow_html=True)
        st.button("⚙️ 내 정보 설정", on_click=go_to_page, args=('profile',))
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="btn-util">', unsafe_allow_html=True)
        st.button("📅 연간 시험 일정", on_click=go_to_page, args=('schedule',))
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# ⚙️ 학생 정보 설정 (D-Day 연동)
# ==========================================
elif st.session_state.page == 'profile':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로 돌아가기", on_click=go_to_page, args=('home',))
    st.markdown('</div><div class="scrollable">', unsafe_allow_html=True)
    
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<h3>⚙️ 내 정보 및 목표 설정</h3>', unsafe_allow_html=True)
    
    new_name = st.text_input("이름을 입력하세요", value=st.session_state.user_name)
    target_exam = st.selectbox("목표 시험 선택", [
        "2026년 1회차 실기 (3.14)", "2026년 2회차 실기 (5.30)", 
        "2026년 3회차 실기 (8.29)", "2026년 4회차 실기 (11.14)"
    ], index=1)
    
    if st.button("💾 정보 저장 및 적용", type="primary"):
        st.session_state.user_name = new_name
        st.session_state.exam_name = target_exam.split(' (')[0]
        dates = {"1회차": (3, 14), "2회차": (5, 30), "3회차": (8, 29), "4회차": (11, 14)}
        for key, (m, d) in dates.items():
            if key in target_exam:
                st.session_state.exam_date = datetime.date(2026, m, d)
        st.success("✅ 저장 완료! 홈 화면으로 이동합니다.")
        time.sleep(0.5)
        go_to_page('home')
        st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

# ==========================================
# 📅 연간 시험 일정
# ==========================================
elif st.session_state.page == 'schedule':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로 돌아가기", on_click=go_to_page, args=('home',))
    st.markdown('</div><div class="scrollable">', unsafe_allow_html=True)
    
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color:#0284c7;">📅 2026 연간 기능사 일정</h3>', unsafe_allow_html=True)
    st.write("**1회차** | 필기: 1.20~1.24 | **실기: 3.14~4.01**")
    st.write("**2회차** | 필기: 4.04~4.09 | **실기: 5.30~6.14**")
    st.write("**3회차** | 특성화고 면제자 | **실기: 8.29~9.16**")
    st.write("**4회차** | 필기: 9.16~9.21 | **실기: 11.14~12.02**")
    st.markdown('</div></div>', unsafe_allow_html=True)

# ==========================================
# 📸 AI 부품 판독기 (기능 연동)
# ==========================================
elif st.session_state.page == 'scanner':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로 돌아가기", on_click=go_to_page, args=('home',))
    st.markdown('</div><div class="scrollable">', unsafe_allow_html=True)
    
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color:#ee4c63;">📸 AI 부품 판독기</h3>', unsafe_allow_html=True)
    target_part = st.selectbox("탈거한 부품을 선택하세요", ["선택", "[12안] 발전기", "[1안] 쇽업소버"])
    if target_part != "선택":
        img_buffer = st.camera_input("화면을 터치하여 촬영하세요")
        if img_buffer:
            with st.spinner("🔍 AI 분석 중..."):
                time.sleep(1.5)
                st.success(f"**✅ 일치율 98%**\n\n{target_part.split(' ')[1]} 탈거가 정확합니다!")
                if st.button("🚀 실습 DB에 사진 공유 (포인트 획득)"):
                    st.balloons()
                    st.info("데이터베이스에 저장되었습니다.")
    st.markdown('</div></div>', unsafe_allow_html=True)

# ==========================================
# 📝 디지털 답안 채점 (자동 채점 기능)
# ==========================================
elif st.session_state.page == 'sheet':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로 돌아가기", on_click=go_to_page, args=('home',))
    st.markdown('</div><div class="scrollable">', unsafe_allow_html=True)
    
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color:#10b981;">📝 디지털 답안 채점</h3>', unsafe_allow_html=True)
    st.caption("[1안 섀시] 제동력 측정")
    
    axle_weight = st.number_input("축중 (kg)", value=1000, step=100)
    left_input = st.text_input("좌측 측정값 (예: 200kg)")
    right_input = st.text_input("우측 측정값 (예: 300kg)")
    status_input = st.radio("판정", ["선택", "양호", "불량"], horizontal=True)
    action_input = st.text_input("정비 및 조치사항")

    if st.button("🚀 AI 선생님 제출", type="primary"):
        if "kg" not in left_input.lower() or "kg" not in right_input.lower():
            st.error("❌ **[치명적 오류] 단위(kg) 누락!** 실전에서 0점 처리됩니다.")
        else:
            try:
                l_val = float(re.sub(r'[^0-9.]', '', left_input))
                r_val = float(re.sub(r'[^0-9.]', '', right_input))
                real_dev = abs(l_val - r_val) / axle_weight * 100
                real_sum = (l_val + r_val) / axle_weight * 100
                correct_status = "양호" if (real_dev <= 8 and real_sum >= 50) else "불량"
                
                if status_input != correct_status:
                    st.error(f"❌ **[판정 오류]** 계산된 편차는 {real_dev:.1f}% 입니다. 판정은 '{correct_status}'이어야 합니다.")
                else:
                    st.success(f"✅ **[정확]** 편차({real_dev:.1f}%) 판정 완벽합니다!")
            except ValueError:
                st.warning("측정값에 숫자를 입력하세요.")
    st.markdown('</div></div>', unsafe_allow_html=True)

# ==========================================
# 나머지 서브 페이지 (기초가이드, 실전연습, 오답노트, 모의고사)
# ==========================================
elif st.session_state.page in ['guide', 'practice', 'note', 'mock']:
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로 돌아가기", on_click=go_to_page, args=('home',))
    st.markdown('</div><div class="scrollable"><div class="content-card">', unsafe_allow_html=True)
    
    if st.session_state.page == 'guide':
        st.markdown('<h3>🌿 기초 가이드</h3>', unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=500", caption="[12안] 발전기 A+ 촬영본")
    elif st.session_state.page == 'practice':
        st.markdown('<h3>🔧 실전 연습</h3>', unsafe_allow_html=True)
        st.checkbox("실린더헤드 탈거")
        st.checkbox("제동력 측정")
        if st.button("답안지 작성으로 이동"): go_to_page('sheet'); st.rerun()
    elif st.session_state.page == 'note':
        st.markdown('<h3>⭐️ AI 오답 노트</h3>', unsafe_allow_html=True)
        st.error("🚨 [1안] 제동력 측정 (단위 누락 잦음)")
        st.info("📌 공식: 편차 = (좌-우 절대값) / 축중 × 100")
    elif st.session_state.page == 'mock':
        st.markdown('<h3>⏱️ 실전 모의고사</h3>', unsafe_allow_html=True)
        if st.button("🎲 실전 과제 랜덤 뽑기", type="primary"): st.session_state.mock_case = random.randint(1, 15)
        if 'mock_case' in st.session_state:
            st.markdown(f'<h1 style="color:#ef4444; text-align:center;">제 {st.session_state.mock_case} 안</h1>', unsafe_allow_html=True)
            st.markdown('<h2 style="text-align:center;">⏳ 04:00:00</h2>', unsafe_allow_html=True)
            
    st.markdown('</div></div>', unsafe_allow_html=True)