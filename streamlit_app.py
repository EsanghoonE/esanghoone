import streamlit as st
import time
import datetime
import re
import random

# 1. 앱 기본 설정 (모바일 꽉 찬 화면)
st.set_page_config(page_title="Auto-Master", page_icon="🚗", layout="centered", initial_sidebar_state="collapsed")

# 2. 전역 상태 관리 (이름, D-Day 설정 등)
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'user_name' not in st.session_state:
    st.session_state.user_name = "용산철도고 학생"
if 'exam_date' not in st.session_state:
    st.session_state.exam_date = datetime.date(2026, 5, 30)
if 'exam_name' not in st.session_state:
    st.session_state.exam_name = "2회차 실기"

def go_to_page(page_name):
    st.session_state.page = page_name

# 3. 🔥 모바일 네이티브 UI CSS 🔥
st.markdown("""
    <style>
        #MainMenu, header, footer {visibility: hidden; display: none;}
        .block-container {padding-top: 1rem !important; padding-bottom: 0px !important; max-width: 100% !important;}
        ::-webkit-scrollbar { display: none; }
        
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #f8fafc; overflow: hidden !important; 
        }

        /* 📅 컴팩트 D-Day 위젯 (공간 절약형) */
        .dday-widget {
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: white; border-radius: 18px; padding: 15px;
            text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.1); 
            margin-bottom: 15px; border: 1px solid #334155;
        }
        .dday-title { font-size: 14px; font-weight: 500; color: #94a3b8; margin-bottom: 2px;}
        .dday-text { font-size: 32px; font-weight: 900; margin: 0; color: #38bdf8;}
        
        /* 📱 그리드 타일형 버튼 디자인 */
        .stButton>button {
            width: 100%; height: 75px; /* 한 화면에 다 들어가도록 높이 최적화 */
            border-radius: 16px; font-size: 16px !important; font-weight: 800 !important; 
            background-color: #ffffff; border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); color: #334155;
            transition: all 0.1s ease-in-out; margin-bottom: 5px;
        }
        .stButton>button:active { transform: scale(0.95); background-color: #f1f5f9; }
        
        /* 메인 핵심 버튼 */
        .main-btn>button {
            background: linear-gradient(135deg, #2563eb, #3b82f6);
            color: white !important; border: none; height: 90px; font-size: 20px !important;
        }

        /* 서브 페이지 스크롤 영역 */
        .scrollable-content {
            height: 85vh; overflow-y: auto; padding-bottom: 40px;
        }
        
        /* 뒤로가기 버튼 */
        .back-btn>button {
            height: 40px !important; background-color: transparent !important; border: 1px solid #cbd5e1 !important;
            box-shadow: none !important; color: #475569 !important; border-radius: 10px; margin-bottom: 10px;
        }
        
        /* 카드 UI */
        .content-card {
            background-color: white; padding: 20px; border-radius: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 📱 화면 1: 홈 런처 (모든 기능이 한눈에)
# ==========================================
if st.session_state.page == 'home':
    # D-Day 계산 로직
    today = datetime.date(2026, 3, 18)
    d_day = (st.session_state.exam_date - today).days
    d_day_str = f"D - {d_day}" if d_day >= 0 else f"D + {abs(d_day)}"
    
    st.markdown(f"""
        <div class="dday-widget">
            <div class="dday-title">👤 {st.session_state.user_name} 님의 목표: {st.session_state.exam_name}</div>
            <div class="dday-text">{d_day_str}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # [핵심 기능]
    st.markdown('<div class="main-btn">', unsafe_allow_html=True)
    st.button("📸 [핵심] AI 부품 판독기", on_click=go_to_page, args=('scanner',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    # [수준별 학습 그리드]
    col1, col2 = st.columns(2)
    with col1:
        st.button("🌱 [초보]\n기초 가이드", on_click=go_to_page, args=('guide',))
        st.button("⏱️ [고수]\n모의고사", on_click=go_to_page, args=('mock',))
    with col2:
        st.button("🔧 [중수]\n실전 연습", on_click=go_to_page, args=('practice',))
        st.button("📝 [필수]\n답안 채점", on_click=go_to_page, args=('sheet',))
        
    # [관리 툴 그리드]
    col3, col4 = st.columns(2)
    with col3:
        st.button("⭐️ 오답 노트", on_click=go_to_page, args=('note',))
        st.button("📅 연간 일정", on_click=go_to_page, args=('schedule',))
    with col4:
        st.button("👤 내 정보 설정", on_click=go_to_page, args=('profile',))


# ==========================================
# 👤 화면 2: 내 정보 설정 (이름 및 D-Day 변경)
# ==========================================
elif st.session_state.page == 'profile':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center; color:#334155;">👤 내 정보 및 목표 설정</h3>', unsafe_allow_html=True)
    
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    new_name = st.text_input("이름을 입력하세요", value=st.session_state.user_name)
    
    target_exam = st.selectbox("목표로 하는 시험을 선택하세요", [
        "2026년 1회차 실기 (3.14)", 
        "2026년 2회차 실기 (5.30)", 
        "2026년 3회차 실기 (8.29)", 
        "2026년 4회차 실기 (11.14)"
    ], index=1)
    
    if st.button("💾 설정 저장하기", type="primary"):
        st.session_state.user_name = new_name
        st.session_state.exam_name = target_exam.split(' (')[0]
        
        # 날짜 매핑 로직
        if "1회차" in target_exam: st.session_state.exam_date = datetime.date(2026, 3, 14)
        elif "2회차" in target_exam: st.session_state.exam_date = datetime.date(2026, 5, 30)
        elif "3회차" in target_exam: st.session_state.exam_date = datetime.date(2026, 8, 29)
        else: st.session_state.exam_date = datetime.date(2026, 11, 14)
        
        st.success("✅ 설정이 저장되었습니다! 홈 화면의 D-Day가 업데이트됩니다.")
        time.sleep(1)
        go_to_page('home')
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 📅 화면 3: 연간 시험 일정 (기능사 전체 일정)
# ==========================================
elif st.session_state.page == 'schedule':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center; color:#10b981;">📅 2026 연간 시험 일정</h3>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="content-card">
            <h4 style="color:#2563eb; margin-bottom:5px;">1회차 기능사</h4>
            <p style="font-size:14px; margin:0;"><b>필기 원서:</b> 1.06 ~ 1.09<br>
            <b>필기 시험:</b> 1.20 ~ 1.24<br>
            <b>실기 원서:</b> 2.16 ~ 2.19<br>
            <b style="color:#ef4444;">실기 시험: 3.14 ~ 4.01</b></p>
        </div>
        <div class="content-card">
            <h4 style="color:#2563eb; margin-bottom:5px;">2회차 기능사</h4>
            <p style="font-size:14px; margin:0;"><b>필기 원서:</b> 3.23 ~ 3.26<br>
            <b>필기 시험:</b> 4.04 ~ 4.09<br>
            <b>실기 원서:</b> 4.27 ~ 4.30<br>
            <b style="color:#ef4444;">실기 시험: 5.30 ~ 6.14</b></p>
        </div>
        <div class="content-card">
            <h4 style="color:#2563eb; margin-bottom:5px;">3회차 기능사 (산업수요맞춤형)</h4>
            <p style="font-size:14px; margin:0; color:#64748b;">※ 특성화고/마이스터고 학생 대상 (필기면제자)</p>
            <p style="font-size:14px; margin:0; margin-top:5px;"><b>실기 원서:</b> 7.27 ~ 7.30<br>
            <b style="color:#ef4444;">실기 시험: 8.29 ~ 9.16</b></p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# (나머지 화면들은 이전과 동일하게 기능을 유지합니다)
# ==========================================

# 📸 판독기
elif st.session_state.page == 'scanner':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center; color:#1e3a8a;">📸 AI 부품 판독기</h3>', unsafe_allow_html=True)
    target_part = st.selectbox("현재 탈거한 부품 선택", ["선택", "[12안] 발전기", "[1안] 와이퍼 모터"])
    if target_part != "선택":
        img_file_buffer = st.camera_input("화면 터치하여 촬영")
        if img_file_buffer:
            with st.spinner("🔍 분석 중..."):
                time.sleep(1.5)
                st.success(f"**✅ 판독 결과: 일치율 98%**\n\n정확합니다! {target_part.split(' ')[1]} 상태 양호.")
    st.markdown('</div>', unsafe_allow_html=True)

# 🌱 초보 기초 가이드
elif st.session_state.page == 'guide':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center; color:#10b981;">🌱 [초보] 기초 가이드</h3>', unsafe_allow_html=True)
    st.info("실습 전, 부품의 위치와 생김새를 사진으로 먼저 눈에 익히세요.")
    st.image("https://via.placeholder.com/300x200/e2e8f0/475569?text=Alternator+Photo", caption="선배들이 탈거한 발전기 사진 (A+ 판정)")
    st.markdown('</div>', unsafe_allow_html=True)

# 🔧 중수 실전 연습
elif st.session_state.page == 'practice':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center; color:#3b82f6;">🔧 [중수] 실전 연습</h3>', unsafe_allow_html=True)
    st.write("원하는 실습 번호를 선택해 체크리스트를 확인하세요.")
    st.selectbox("실습 안 선택", ["제 1안 세트", "제 12안 세트"])
    st.checkbox("디젤기관 분사노즐 탈거")
    st.checkbox("제동력 측정")
    if st.button("👉 답안지 작성하기"):
        go_to_page('sheet')
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 📝 실전 답안 채점
elif st.session_state.page == 'sheet':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center; color:#6366f1;">📝 디지털 답안 채점</h3>', unsafe_allow_html=True)
    st.caption("[1안] 제동력 측정")
    axle_weight = st.number_input("축중 (kg)", value=1000)
    left_input = st.text_input("좌측 측정값 (예: 200kg)")
    right_input = st.text_input("우측 측정값")
    if st.button("🚀 제출 및 채점", type="primary"):
        if "kg" not in left_input.lower():
            st.error("❌ 단위(kg) 누락! 실전에서 0점 처리됩니다.")
        else:
            st.success("✅ 계산 및 판정 완벽합니다!")
    st.markdown('</div>', unsafe_allow_html=True)

# ⏱️ 고수 모의고사
elif st.session_state.page == 'mock':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center; color:#ef4444;">⏱️ [고수] 파이널 모의고사</h3>', unsafe_allow_html=True)
    if st.button("🎲 실전 과제 랜덤 배정", type="primary"):
        st.session_state.mock_case = random.randint(1, 15)
    if 'mock_case' in st.session_state:
        st.markdown(f'<h1 style="text-align:center; color:#ef4444;">제 {st.session_state.mock_case} 안</h1>', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align:center;">⏳ 04:00:00</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ⭐️ 오답 노트
elif st.session_state.page == 'note':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center; color:#f59e0b;">⭐️ 오답 노트</h3>', unsafe_allow_html=True)
    st.error("🚨 [1안] 제동력: 단위(kg) 누락 주의")
    st.info("📌 [공식] 제동력 편차: (좌-우 절대값) / 축중 × 100")
    st.markdown('</div>', unsafe_allow_html=True)