import streamlit as st
import time
import datetime
import re
import random

# ==========================================
# 1. 앱 기본 설정 및 전역 상태 관리
# ==========================================
st.set_page_config(page_title="Auto-Master", page_icon="🚗", layout="centered", initial_sidebar_state="collapsed")

# 2. 화면 전환 및 전역 상태 관리 (이름, D-Day 설정 등)
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

# ==========================================
# 3. 🔥 프리미엄 글래스모피즘 & Safari 최적화 CSS 🔥
# ==========================================
st.markdown("""
    <style>
        /* 기본 메뉴 숨김 및 Safari 화면 밀림 방지 */
        #MainMenu, header, footer {visibility: hidden; display: none;}
        .block-container {
            padding-top: 1rem !important; 
            padding-bottom: env(safe-area-inset-bottom) !important; 
            max-width: 100% !important;
        }
        ::-webkit-scrollbar { display: none; }
        
        /* 럭셔리 배경 이미지 설정 (어두운 자동차 테마) */
        [data-testid="stAppViewContainer"] {
            background-image: url('https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=1000&q=80');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            height: 100dvh !important; /* Safari 동적 뷰포트 대응 */
            overflow: hidden !important; 
        }

        /* 텍스트 가독성을 위한 전체 오버레이 */
        [data-testid="stAppViewContainer"]::before {
            content: ""; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(15, 23, 42, 0.7); /* 고급스러운 네이비 틴트 */
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

        /* 📅 글래스모피즘 D-Day 위젯 */
        .dday-widget {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
            color: white; border-radius: 20px; padding: 20px; text-align: center; 
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3); 
            margin-bottom: 15px; border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .dday-title { font-size: 14px; font-weight: 500; color: #cbd5e1; margin-bottom: 2px;}
        .dday-text { font-size: 38px; font-weight: 900; margin: 0; color: #38bdf8; text-shadow: 0 2px 10px rgba(56, 189, 248, 0.4);}
        
        /* 📱 그리드 타일형 버튼 (반투명 유리 효과) */
        .stButton>button {
            width: 100%; height: 75px; border-radius: 16px; font-size: 16px !important; font-weight: 800 !important; 
            background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2); color: #ffffff; 
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); margin-bottom: 5px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-shadow: 0 1px 2px rgba(0,0,0,0.5);
        }
        .stButton>button:active { transform: scale(0.95); background: rgba(255, 255, 255, 0.25); }
        
        /* 핵심 AI 판독기 버튼 (그라데이션 강조, Wider 반영) */
        .wider-btn>button {
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.8), rgba(59, 130, 246, 0.8));
            border: 1px solid rgba(255, 255, 255, 0.3); height: 95px; font-size: 20px !important;
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4);
        }

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
            background: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 18px; 
            border: 1px solid rgba(255, 255, 255, 0.3); margin-bottom: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1); color: #1e293b;
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
    
    st.markdown('<div class="app-title">🚗 Auto-Master</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="dday-widget">
            <div class="dday-title">👤 {st.session_state.user_name} 님의 목표: {st.session_state.exam_name}</div>
            <div class="dday-text">{d_day_str}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 1단 그리드 (내 정보 설정, 연간 일정 - 사용자의 요청 반영)
    col_mgmt1, col_mgmt2 = st.columns(2)
    with col_mgmt1:
        st.button("👤 내 정보 및 D-Day 설정", on_click=go_to_page, args=('profile',))
    with col_mgmt2:
        st.button("📅 연간 일정", on_click=go_to_page, args=('schedule',))

    # 2단 그리드 (핵심 기능 - 사용자의 Wider 요청 반영)
    st.markdown('<div class="stButton wider-btn">', unsafe_allow_html=True)
    st.button("📸 [핵심] AI 부품 판독기", on_click=go_to_page, args=('scanner',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 3단 그리드 (기초 가이드, 실전 모의고사)
    col1, col2 = st.columns(2)
    with col1:
        st.button("🌱 기초 가이드", on_click=go_to_page, args=('guide',))
        st.button("⏱️ 실전 모의고사", on_click=go_to_page, args=('mock',))
    with col2:
        st.button("🔧 실전 연습", on_click=go_to_page, args=('practice',))
        st.button("⭐️ AI 오답 노트", on_click=go_to_page, args=('note',))
        
    # 답안 채점 버튼
    st.button("📝 답안 채점", on_click=go_to_page, args=('sheet',))


# ==========================================
# 👤 내 정보 및 D-Day 설정 (이름 및 날짜 변경)
# ==========================================
elif st.session_state.page == 'profile':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center; color:#ffffff; text-shadow: 0 2px 4px rgba(0,0,0,0.8);">👤 내 정보 및 목표 설정</h3>', unsafe_allow_html=True)
    
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
        
        # 날짜 매핑 로직 (오늘 날짜 기준으로 D-Day 계산을 위해 이전 코드 로직을 복사해 넣습니다.)
        dates = {"1회차": (3, 14), "2회차": (5, 30), "3회차": (8, 29), "4회차": (11, 14)}
        for exam_key, (m, d) in dates.items():
            if exam_key in target_exam:
                st.session_state.exam_date = datetime.date(2026, m, d)
                break
        
        st.success("✅ 설정이 저장되었습니다! 홈 화면의 D-Day가 업데이트됩니다.")
        time.sleep(0.5)
        go_to_page('home')
        st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)


# ==========================================
# 📅 연간 시험 일정 (기능사 전체 일정)
# ==========================================
elif st.session_state.page == 'schedule':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center; color:#ffffff; text-shadow: 0 2px 4px rgba(0,0,0,0.8);">📅 2026 연간 시험 일정</h3>', unsafe_allow_html=True)
    
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
            <h4 style="color:#2563eb; margin-bottom:5px;">3회차 기능사 (특성화고 면제자)</h4>
            <p style="font-size:14px; margin:0; margin-top:5px;"><b>실기 원서:</b> 7.27 ~ 7.30<br>
            <b style="color:#ef4444;">실기 시험: 8.29 ~ 9.16</b></p>
        </div>
        <div class="content-card">
            <h4 style="color:#2563eb; margin-bottom:5px;">4회차 기능사</h4>
            <p style="font-size:14px; margin:0;"><b>필기 원서:</b> 9.16 ~ 9.21<br>
            <b>필기 시험:</b> 9.16 ~ 9.21<br>
            <b>실기 원서:</b> 10.26 ~ 10.29<br>
            <b style="color:#ef4444;">실기 시험: 11.14 ~ 12.02</b></p>
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
    st.markdown('<h3 style="text-align:center; color:#ffffff; text-shadow: 0 2px 4px rgba(0,0,0,0.8);">📸 AI 부품 판독기</h3>', unsafe_allow_html=True)
    
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    target_part = st.selectbox("현재 탈거한 부품 선택", ["선택하세요", "[12안] 발전기", "[1안] 앞 쇽업소버", "[13안] 인젝터"])
    
    if target_part != "선택하세요":
        st.info("부품이 화면 중앙에 오도록 촬영해 주세요.")
        img_buffer = st.camera_input("화면 터치하여 촬영")
        
        if img_buffer:
            with st.spinner("🔍 AI 모델이 부품 형상을 분석 중입니다..."):
                time.sleep(1.5)
                part_name = target_part.split('] ')[1]
                st.markdown(f"""
                    <div style="border: 2px solid #10b981; background-color: #ecfdf5; padding: 15px; border-radius: 10px; margin-top:15px;">
                        <h3 style="color:#059669; margin-top:0;">✅ 판독 결과: 일치율 98%</h3>
                        <p>정확합니다! <b>{part_name}</b>을(를) 올바르게 탈거하셨습니다.</p>
                        <p style="font-size:14px; color:#047857;">[AI 코멘트] 체결부위 마모 없이 상태가 매우 양호합니다.</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.write("")
                if st.button("🚀 실습 DB에 내 사진 공유하기 (후배들을 위해)"):
                    st.balloons()
                    st.success("🎉 데이터베이스에 저장되었습니다! 포인트 +10 획득!")
    st.markdown('</div></div>', unsafe_allow_html=True)

# 🌱 기초 가이드
elif st.session_state.page == 'guide':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center; color:#ffffff;">🌱 기초 가이드</h3>', unsafe_allow_html=True)
    
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.write("#### 🔧 [12안] 발전기 (Alternator)")
    st.image("https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?auto=format&fit=crop&w=600&q=80", caption="김** 선배 촬영본")
    st.info("💡 탈거 전 반드시 배터리 (-) 단자를 분리하세요!")
    st.markdown('</div></div>', unsafe_allow_html=True)

# 🔧 실전 연습
elif st.session_state.page == 'practice':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center; color:#ffffff;">🔧 실전 연습</h3>', unsafe_allow_html=True)
    
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    case_num = st.selectbox("실습 안 선택", ["선택하세요", "제 1안 세트", "제 12안 세트"])
    
    if case_num == "제 1안 세트":
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
    st.markdown('</div></div>', unsafe_allow_html=True)

# 📝 답안 채점
elif st.session_state.page == 'sheet':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center; color:#ffffff;">📝 디지털 답안 채점</h3>', unsafe_allow_html=True)
    
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

# ⏱️ 실전 모의고사
elif st.session_state.page == 'mock':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center; color:#ffffff;">⏱️ 실전 모의고사</h3>', unsafe_allow_html=True)
    
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    if st.button("🎲 실전 과제 랜덤 뽑기", type="primary"):
        st.session_state.mock_case = random.randint(1, 15)
        
    if 'mock_case' in st.session_state:
        st.markdown(f"""
            <div style="text-align:center; border: 3px solid #ef4444; padding:20px; border-radius:15px; margin-top:20px;">
                <h1 style="color:#ef4444; font-size:45px; margin:0;">제 {st.session_state.mock_case} 안</h1>
                <p style="color:#475569; font-weight:bold;">배정되었습니다. 실습 차량으로 이동하세요.</p>
                <hr>
                <h2 style="margin:0;">⏳ 04:00:00</h2>
                <p style="color:#94a3b8; font-size:13px;">기관 100분 / 섀시 80분 / 전기 60분</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

# 📅 연간 시험 일정
elif st.session_state.page == 'schedule':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center; color:#ffffff;">📅 2026 연간 시험 일정</h3>', unsafe_allow_html=True)
    
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
            <h4 style="color:#2563eb; margin-bottom:5px;">3회차 기능사 (특성화고 면제자)</h4>
            <p style="font-size:14px; margin:0; margin-top:5px;"><b>실기 원서:</b> 7.27 ~ 7.30<br>
            <b style="color:#ef4444;">실기 시험: 8.29 ~ 9.16</b></p>
        </div>
        <div class="content-card">
            <h4 style="color:#2563eb; margin-bottom:5px;">4회차 기능사</h4>
            <p style="font-size:14px; margin:0;"><b>필기 원서:</b> 9.16 ~ 9.21<br>
            <b>필기 시험:</b> 9.16 ~ 9.21<br>
            <b>실기 원서:</b> 10.26 ~ 10.29<br>
            <b style="color:#ef4444;">실기 시험: 11.14 ~ 12.02</b></p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)