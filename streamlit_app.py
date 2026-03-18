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
# 2. 강력한 모바일 네이티브 CSS
# ==========================================
st.markdown("""
    <style>
        #MainMenu, header, footer {visibility: hidden; display: none;}
        .block-container {padding-top: 1rem !important; padding-bottom: 0px !important; max-width: 100% !important;}
        ::-webkit-scrollbar { display: none; }
        
        html, body, [data-testid="stAppViewContainer"] { background-color: #f8fafc; overflow: hidden !important; }

        /* D-Day 위젯 */
        .dday-widget {
            background: linear-gradient(135deg, #0f172a, #1e293b); color: white; border-radius: 18px; padding: 15px;
            text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 15px; border: 1px solid #334155;
        }
        .dday-title { font-size: 14px; font-weight: 500; color: #94a3b8; margin-bottom: 2px;}
        .dday-text { font-size: 32px; font-weight: 900; margin: 0; color: #38bdf8;}
        
        /* 메인 버튼 공통 디자인 */
        .stButton>button {
            width: 100%; height: 75px; border-radius: 16px; font-size: 16px !important; font-weight: 800 !important; 
            background-color: #ffffff; border: 1px solid #e2e8f0; color: #334155; transition: all 0.1s; margin-bottom: 5px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        }
        .stButton>button:active { transform: scale(0.95); background-color: #f1f5f9; }
        
        /* 핵심 AI 판독기 버튼 */
        .main-btn>button {
            background: linear-gradient(135deg, #2563eb, #3b82f6); color: white !important; border: none; height: 90px; font-size: 20px !important;
        }

        /* 서브 페이지 스크롤 허용 (모바일 앱 본문 느낌) */
        .scrollable-content { height: 85vh; overflow-y: auto; padding-bottom: 40px; padding-top: 5px;}
        
        /* 뒤로가기 버튼 */
        .back-btn>button {
            height: 40px !important; background-color: transparent !important; border: 1px solid #cbd5e1 !important;
            box-shadow: none !important; color: #475569 !important; border-radius: 10px; margin-bottom: 10px;
        }
        
        /* 콘텐츠 카드 */
        .content-card {
            background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #e2e8f0; margin-bottom: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 🏠 홈 화면 (런처)
# ==========================================
if st.session_state.page == 'home':
    today = datetime.date(2026, 3, 18)
    d_day = (st.session_state.exam_date - today).days
    d_day_str = f"D - {d_day}" if d_day >= 0 else f"D + {abs(d_day)}"
    
    st.markdown(f"""
        <div class="dday-widget">
            <div class="dday-title">👤 {st.session_state.user_name} 님의 목표: {st.session_state.exam_name}</div>
            <div class="dday-text">{d_day_str}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-btn">', unsafe_allow_html=True)
    st.button("📸 [핵심] AI 부품 판독기", on_click=go_to_page, args=('scanner',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("🌱 [초보]\n기초 가이드", on_click=go_to_page, args=('guide',))
        st.button("⏱️ [고수]\n모의고사", on_click=go_to_page, args=('mock',))
        st.button("⭐️ 오답 노트", on_click=go_to_page, args=('note',))
    with col2:
        st.button("🔧 [중수]\n실전 연습", on_click=go_to_page, args=('practice',))
        st.button("📝 [필수]\n답안 채점", on_click=go_to_page, args=('sheet',))
        st.button("📅 연간 일정", on_click=go_to_page, args=('schedule',))
        
    st.button("👤 내 정보 및 D-Day 설정", on_click=go_to_page, args=('profile',))


# ==========================================
# 👤 내 정보 설정
# ==========================================
elif st.session_state.page == 'profile':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center; color:#334155;">👤 내 정보 설정</h3>', unsafe_allow_html=True)
    
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    new_name = st.text_input("이름", value=st.session_state.user_name)
    target_exam = st.selectbox("목표 시험", [
        "2026년 1회차 실기 (3.14)", "2026년 2회차 실기 (5.30)", 
        "2026년 3회차 실기 (8.29)", "2026년 4회차 실기 (11.14)"
    ], index=1)
    
    if st.button("💾 설정 저장하기", type="primary"):
        st.session_state.user_name = new_name
        st.session_state.exam_name = target_exam.split(' (')[0]
        dates = {"1": (3,14), "2": (5,30), "3": (8,29), "4": (11,14)}
        m, d = dates[target_exam.split('회차')[0][-1]]
        st.session_state.exam_date = datetime.date(2026, m, d)
        
        st.success("✅ 저장 완료! 홈 화면으로 이동합니다.")
        time.sleep(0.5)
        go_to_page('home')
        st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)


# ==========================================
# 📸 AI 부품 판독기 (핵심 카메라 기능)
# ==========================================
elif st.session_state.page == 'scanner':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center; color:#1e3a8a;">📸 AI 부품 판독기</h3>', unsafe_allow_html=True)
    
    target_part = st.selectbox("현재 탈거한 부품 선택", ["선택하세요", "[12안] 발전기", "[1안] 앞 쇽업소버", "[13안] 인젝터"])
    
    if target_part != "선택하세요":
        st.info("부품이 화면 중앙에 오도록 촬영해 주세요.")
        img_buffer = st.camera_input("화면 터치하여 촬영")
        
        if img_buffer:
            with st.spinner("🔍 AI 모델이 부품 형상을 분석 중입니다..."):
                time.sleep(1.5) # AI 분석 시뮬레이션 대기
                part_name = target_part.split('] ')[1]
                st.markdown(f"""
                    <div class="content-card" style="border: 2px solid #10b981; background-color: #ecfdf5;">
                        <h3 style="color:#059669; margin-top:0;">✅ 판독 결과: 일치율 98%</h3>
                        <p>정확합니다! <b>{part_name}</b>을(를) 올바르게 탈거하셨습니다.</p>
                        <p style="font-size:14px; color:#047857;">[AI 코멘트] 체결부위 마모 없이 상태가 매우 양호합니다.</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("🚀 실습 DB에 내 사진 공유하기 (후배들을 위해)"):
                    st.balloons()
                    st.success("🎉 데이터베이스에 저장되었습니다! 포인트 +10 획득!")
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 🌱 기초 가이드
# ==========================================
elif st.session_state.page == 'guide':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center; color:#10b981;">🌱 기초 가이드</h3>', unsafe_allow_html=True)
    st.write("선배들이 남긴 A+ 실전 부품 갤러리입니다.")
    
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.write("#### 🔧 [12안] 발전기 (Alternator)")
    # 실제 발전기와 유사한 무료 이미지 플레이스홀더 사용
    st.image("https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?auto=format&fit=crop&w=600&q=80", caption="김** 선배 촬영본")
    st.info("💡 탈거 전 반드시 배터리 (-) 단자를 분리하세요!")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 🔧 실전 연습
# ==========================================
elif st.session_state.page == 'practice':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center; color:#3b82f6;">🔧 실전 연습</h3>', unsafe_allow_html=True)
    
    case_num = st.selectbox("실습 안 선택", ["선택하세요", "제 1안 세트", "제 12안 세트"])
    
    if case_num == "제 1안 세트":
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.write("#### 📋 1안 작업 지시서")
        st.checkbox("[기관] 실린더헤드와 분사노즐(1개) 탈거")
        st.checkbox("[기관] 점화회로 고장 점검 및 시동")
        st.checkbox("[섀시] 앞 쇽업소버 스프링 탈거")
        st.checkbox("[섀시] 제동력 측정 (답안 작성 필수)")
        st.checkbox("[전기] 전조등 측정")
        
        st.write("---")
        if st.button("👉 제동력 측정 답안지 작성하기", type="primary"):
            go_to_page('sheet')
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 📝 답안 채점 (자동 AI 채점 엔진)
# ==========================================
elif st.session_state.page == 'sheet':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center; color:#6366f1;">📝 디지털 답안 채점</h3>', unsafe_allow_html=True)
    
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.write("#### [1안 섀시] 제동력 측정")
    axle_weight = st.number_input("해당 축중 (kg)", value=1000, step=100)
    left_input = st.text_input("좌측 측정값 (예: 200kg)")
    right_input = st.text_input("우측 측정값 (예: 300kg)")
    status_input = st.radio("판정 체크", ["선택", "양호", "불량"], horizontal=True)
    action_input = st.text_input("정비 및 조치사항", placeholder="예: 브레이크 패드 교환 후 재점검")

    if st.button("🚀 AI 선생님 제출", type="primary"):
        st.write("---")
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
                    st.error(f"❌ **[판정 오류]** 계산된 편차는 {real_dev:.1f}% 입니다. 규정값(8% 이내)을 벗어났으므로 판정은 **'{correct_status}'**이어야 합니다.")
                else:
                    st.success(f"✅ **[계산/판정 정확]** 편차({real_dev:.1f}%)와 판정 모두 완벽합니다!")
                
                if "고침" in action_input or "바꿈" in action_input:
                    st.warning("⚠️ **[용어 교정]** '고침' 대신 '교환 후 재점검' 또는 '수리 후 재점검'을 사용하세요.")
                elif len(action_input) > 3:
                    st.success("✅ 조치사항 작성 양호!")
            except ValueError:
                st.warning("측정값에 숫자를 포함해 입력하세요.")
    st.markdown('</div></div>', unsafe_allow_html=True)


# ==========================================
# ⭐️ 오답 노트
# ==========================================
elif st.session_state.page == 'note':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center; color:#f59e0b;">⭐️ AI 오답 노트</h3>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="content-card" style="border-left: 5px solid #ef4444;">
            <b style="color:#b91c1c;">🚨 [1안] 제동력 측정 (2회 오답)</b><br>
            <span style="font-size:14px;">- 실수 패턴: 단위(kg) 습관적 누락</span><br>
            <span style="font-size:14px; color:#059669;">- AI 솔루션: 편차는 축중의 8% 이내, 앞축 합은 50% 이상!</span>
        </div>
        <div class="content-card" style="border-left: 5px solid #3b82f6;">
            <b style="color:#1d4ed8;">📌 [핵심 암기] 인젝터 코일 저항</b><br>
            <span style="font-size:14px;">- 규정값: 13 ~ 16 Ω (멀티미터로 200Ω 레인지 설정)</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# ⏱️ 파이널 모의고사
# ==========================================
elif st.session_state.page == 'mock':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center; color:#ef4444;">⏱️ 파이널 모의고사</h3>', unsafe_allow_html=True)
    
    if st.button("🎲 실전 과제 랜덤 뽑기", type="primary"):
        st.session_state.mock_case = random.randint(1, 15)
        
    if 'mock_case' in st.session_state:
        st.markdown(f"""
            <div class="content-card" style="text-align:center; border: 3px solid #ef4444;">
                <h1 style="color:#ef4444; font-size:45px; margin:0;">제 {st.session_state.mock_case} 안</h1>
                <p style="color:#475569; font-weight:bold;">배정되었습니다. 실습 차량으로 이동하세요.</p>
                <hr>
                <h2 style="margin:0;">⏳ 04:00:00</h2>
                <p style="color:#94a3b8; font-size:13px;">기관 100분 / 섀시 80분 / 전기 60분</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 📅 연간 시험 일정
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
            <p style="font-size:14px; margin:0;">필기 시험: 1.20 ~ 1.24<br><b style="color:#ef4444;">실기 시험: 3.14 ~ 4.01</b></p>
        </div>
        <div class="content-card">
            <h4 style="color:#2563eb; margin-bottom:5px;">2회차 기능사</h4>
            <p style="font-size:14px; margin:0;">필기 시험: 4.04 ~ 4.09<br><b style="color:#ef4444;">실기 시험: 5.30 ~ 6.14</b></p>
        </div>
        <div class="content-card">
            <h4 style="color:#2563eb; margin-bottom:5px;">3회차 기능사 (특성화고 면제자)</h4>
            <p style="font-size:14px; margin:0;"><b style="color:#ef4444;">실기 시험: 8.29 ~ 9.16</b></p>
        </div>
        <div class="content-card">
            <h4 style="color:#2563eb; margin-bottom:5px;">4회차 기능사</h4>
            <p style="font-size:14px; margin:0;">필기 시험: 9.16 ~ 9.21<br><b style="color:#ef4444;">실기 시험: 11.14 ~ 12.02</b></p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)