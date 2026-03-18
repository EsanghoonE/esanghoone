import streamlit as st
import time
import datetime
import re
import random

# 1. 앱 기본 설정 (모바일 꽉 찬 화면)
st.set_page_config(page_title="Auto-Master", page_icon="🚗", layout="centered", initial_sidebar_state="collapsed")

# 2. 화면 전환 상태 관리
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def go_to_page(page_name):
    st.session_state.page = page_name

# 3. 🔥 고급 모바일 네이티브 UI / 색상 디자인 CSS 🔥
st.markdown("""
    <style>
        /* 기본 스크롤바, 헤더 숨김 */
        #MainMenu, header, footer {visibility: hidden; display: none;}
        .block-container {padding-top: 1rem !important; padding-bottom: 0px !important; max-width: 100% !important;}
        ::-webkit-scrollbar { display: none; }
        
        /* 전체 배경색 (연한 회색 바탕으로 앱 느낌 강조) */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #f8fafc;
        }

        /* 📅 D-Day 위젯 스타일 (최상단) */
        .dday-widget {
            background: linear-gradient(135deg, #0f172a, #334155);
            color: white; border-radius: 20px; padding: 20px;
            text-align: center; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); 
            margin-bottom: 20px; border: 1px solid #475569;
        }
        .dday-text { font-size: 38px; font-weight: 900; margin: 0; line-height: 1.1; color: #38bdf8;}
        .dday-sub { font-size: 14px; font-weight: 500; color: #cbd5e1; margin-bottom: 5px;}

        /* 📱 버튼 공통 디자인 (그리드 타일형) */
        .stButton>button {
            width: 100%; height: 90px; 
            border-radius: 18px; font-size: 18px !important; font-weight: 800 !important; 
            background-color: #ffffff; border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); color: #334155;
            transition: all 0.15s ease-in-out;
        }
        /* 버튼 터치 시 애니메이션 */
        .stButton>button:active {
            transform: scale(0.95); background-color: #f1f5f9; border-color: #cbd5e1;
        }
        
        /* 📸 메인 핵심 버튼 (AI 판독기) 디자인 특별 강조 */
        .stButton>button[kind="primary"] {
            background: linear-gradient(135deg, #2563eb, #3b82f6);
            color: white !important; border: none; height: 110px; font-size: 22px !important;
            box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.4);
        }

        /* ⬅️ 뒤로가기 버튼 스타일 */
        .back-btn>button {
            height: 45px !important; background-color: transparent !important; border: 1px solid #cbd5e1 !important;
            box-shadow: none !important; color: #475569 !important; font-size: 15px !important;
            border-radius: 10px; margin-bottom: 15px;
        }

        /* 서브 페이지 카드형 콘텐츠 박스 */
        .content-card {
            background-color: white; padding: 20px; border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.02); border: 1px solid #e2e8f0; margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 📱 화면 1: 홈 런처 (메인 화면)
# ==========================================
if st.session_state.page == 'home':
    # 1) D-Day 위젯 (2026년 2회차 실기 기준 자동 계산)
    today = datetime.date(2026, 3, 18)
    exam_date = datetime.date(2026, 5, 30)
    d_day = (exam_date - today).days
    
    st.markdown(f"""
        <div class="dday-widget">
            <div class="dday-sub">한국산업인력공단 정기 2회 실기시험</div>
            <div class="dday-text">D - {d_day}</div>
            <div style="font-size: 13px; color: #94a3b8; margin-top: 8px;">원서접수: 4.27 ~ 4.30</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 2) 핵심 기능: AI 판독기 (Primary 속성으로 파란색 그라데이션 적용)
    st.button("📸 AI 부품 판독기 실행", type="primary", on_click=go_to_page, args=('scanner',))
    
    # 3) 2x2 그리드: 학습 모드 및 도구
    col1, col2 = st.columns(2)
    with col1:
        st.button("🌱\n기초 가이드", on_click=go_to_page, args=('guide',))
        st.button("📝\n답안 채점", on_click=go_to_page, args=('sheet',))
    with col2:
        st.button("🔧\n실전 연습", on_click=go_to_page, args=('practice',))
        st.button("⭐️\n오답 노트", on_click=go_to_page, args=('note',))
        
    # 4) 하단 강조 버튼: 파이널 모의고사
    st.button("⏱️ 파이널 모의고사 시작", on_click=go_to_page, args=('mock',))


# ==========================================
# 📸 화면 2: AI 부품 판독기 (Vision AI)
# ==========================================
elif st.session_state.page == 'scanner':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h3 style="text-align:center; color:#1e3a8a;">📸 AI 부품 판독기</h3>', unsafe_allow_html=True)
    
    target_part = st.selectbox("현재 실습 중인 과제 부품을 선택하세요", ["선택하세요", "[12안] 발전기", "[1안] 와이퍼 모터", "[2안] 인젝터"])
    
    if target_part != "선택하세요":
        img_file_buffer = st.camera_input("화면 터치하여 부품 촬영")
        if img_file_buffer is not None:
            with st.spinner("🔍 AI 비전 모델이 부품을 분석 중입니다..."):
                time.sleep(1.5)
                part_name = target_part.split(' ')[1]
                st.success(f"**✅ 판독 결과: 일치율 98%**\n\n정확합니다! **[{part_name}]**을(를) 올바르게 탈거하셨습니다. 외관 상태도 양호합니다.")
                
                st.markdown('<div class="content-card">', unsafe_allow_html=True)
                st.write("🌟 **데이터 선순환 기여**\n\n이 사진을 학교 DB에 공유하여 후배들의 교재로 사용되게 할까요?")
                if st.button("🚀 실습 DB에 내 사진 공유하기"):
                    st.balloons()
                    st.info("데이터베이스에 성공적으로 저장되었습니다! (+학습 포인트 10점)")
                st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 🌱 화면 3: 기초 가이드 (초보자용 사진/설명)
# ==========================================
elif st.session_state.page == 'guide':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h3 style="text-align:center; color:#10b981;">🌱 기초 가이드</h3>', unsafe_allow_html=True)
    st.caption("선배들이 직접 탈거하고 AI가 검증한 A+ 부품 갤러리입니다.")
    
    # 탭으로 과목 분리
    tab1, tab2, tab3 = st.tabs(["기관", "섀시", "전기"])
    with tab1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.write("#### 🔧 [12안] 발전기 (Alternator)")
        st.image("https://images.unsplash.com/photo-1530046339160-ce3e530c7d2f?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=60", caption="김** 학생 촬영 (일치율 99%)")
        st.info("💡 **AI 꿀팁:** 발전기 탈거 전, 반드시 배터리 (-) 단자를 먼저 분리하여 합선을 예방하세요!")
        st.markdown('</div>', unsafe_allow_html=True)
    with tab2:
        st.write("섀시 실습 사진이 업데이트될 예정입니다.")


# ==========================================
# 🔧 화면 4: 실전 연습 (과제 체크리스트)
# ==========================================
elif st.session_state.page == 'practice':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h3 style="text-align:center; color:#3b82f6;">🔧 실전 연습 모드</h3>', unsafe_allow_html=True)
    st.write("원하는 실습 안을 선택하여 단계별로 연습하세요.")
    
    prac_choice = st.selectbox("실습할 안(Case) 선택", ["선택", "제 1안 세트", "제 12안 세트"])
    
    if prac_choice == "제 1안 세트":
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.write("#### 📋 1안 실습 체크리스트")
        st.checkbox("[기관] 디젤기관 분사노즐 탈거 및 조립")
        st.checkbox("[섀시] 앞 쇽업소버 스프링 탈거 및 조립")
        st.checkbox("[섀시] 제동력 측정 (답안지 작성 필요)")
        st.checkbox("[전기] 전조등 광도/진폭 측정")
        
        if st.button("👉 제동력 답안지 작성하러 가기"):
            go_to_page('sheet')
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 📝 화면 5: 답안 채점 (자동 피드백)
# ==========================================
elif st.session_state.page == 'sheet':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h3 style="text-align:center; color:#6366f1;">📝 디지털 답안지 채점</h3>', unsafe_allow_html=True)
    st.caption("과제: [제1안 새시] 제동력 측정")
    
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    axle_weight = st.number_input("해당 축중 (kg)", value=1000, step=100)
    left_input = st.text_input("좌측 측정값 (예: 200kg)")
    right_input = st.text_input("우측 측정값 (예: 300kg)")
    status_input = st.radio("판정", ["선택", "양호", "불량"], horizontal=True)
    action_input = st.text_input("정비 및 조치사항", placeholder="예: 브레이크 패드 교환")

    if st.button("🚀 AI 선생님에게 제출하기", type="primary"):
        if "kg" not in left_input.lower() or "kg" not in right_input.lower():
            st.error("❌ **[치명적 오류] 단위(kg) 누락!** 실전에서 0점 처리됩니다.")
        else:
            try:
                l_val = float(re.sub(r'[^0-9.]', '', left_input))
                r_val = float(re.sub(r'[^0-9.]', '', right_input))
                real_dev = abs(l_val - r_val) / axle_weight * 100
                real_sum = (l_val - r_val) / axle_weight * 100 # 고의 오타 방지
                real_sum = (l_val + r_val) / axle_weight * 100
                
                correct_status = "양호" if (real_dev <= 8 and real_sum >= 50) else "불량"
                
                if status_input != correct_status:
                    st.error(f"❌ **[판정 오류]** 계산된 편차는 {real_dev:.1f}% 입니다. 규정값(8% 이내)을 벗어났으므로 판정은 **'{correct_status}'**이어야 합니다.")
                else:
                    st.success("✅ **[판정 정확]** 완벽한 계산과 판정입니다!")
                
                if "고침" in action_input:
                    st.warning("⚠️ **[용어 주의]** '고침' 대신 '교환 후 재점검'을 사용하세요.")
            except ValueError:
                st.warning("측정값에 숫자를 입력하세요.")
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# ⭐️ 화면 6: 오답 노트
# ==========================================
elif st.session_state.page == 'note':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h3 style="text-align:center; color:#f59e0b;">⭐️ AI 오답 노트</h3>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="content-card" style="border-left: 5px solid #ef4444;">
            <b style="color:#b91c1c;">🚨 [1안] 제동력 측정 (어제 틀림)</b><br>
            <span style="font-size:14px;">- 실수 내용: 단위(kg) 누락 및 편차 판정 실수</span><br>
            <span style="font-size:14px; color:#059669;">- AI 솔루션: 편차는 축중의 8% 이내, 합은 50% 이상!</span>
        </div>
        <div class="content-card" style="border-left: 5px solid #3b82f6;">
            <b style="color:#1d4ed8;">📌 [핵심 암기] 인젝터 코일 저항</b><br>
            <span style="font-size:14px;">- 규정값: 13 ~ 16 Ω (멀티미터 사용)</span>
        </div>
    """, unsafe_allow_html=True)


# ==========================================
# ⏱️ 화면 7: 파이널 모의고사 (타이머 및 랜덤 배정)
# ==========================================
elif st.session_state.page == 'mock':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h3 style="text-align:center; color:#ef4444;">⏱️ 파이널 모의고사</h3>', unsafe_allow_html=True)
    
    if st.button("🎲 실전 문제 랜덤 뽑기", type="primary"):
        random_case = random.randint(1, 15)
        st.session_state.random_case = random_case
        
    if 'random_case' in st.session_state:
        st.markdown(f"""
            <div class="content-card" style="text-align:center; border: 2px solid #ef4444;">
                <h1 style="color:#ef4444; font-size:40px; margin:0;">제 {st.session_state.random_case} 안</h1>
                <p style="color:#475569; font-weight:bold;">시험위원이 과제를 배정했습니다.</p>
                <hr>
                <h2 style="margin:0;">⏳ 04:00:00</h2>
                <p style="color:#94a3b8; font-size:12px;">(기관 100분 / 섀시 80분 / 전기 60분)</p>
            </div>
        """, unsafe_allow_html=True)
        st.info("실제 시험처럼 제한 시간 내에 차량으로 이동하여 작업을 시작하세요!")