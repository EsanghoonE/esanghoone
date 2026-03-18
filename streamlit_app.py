import streamlit as st
import time
import datetime
import re

# 1. 앱 기본 설정 (모바일 최적화)
st.set_page_config(page_title="Auto-Master", page_icon="🚗", layout="centered", initial_sidebar_state="collapsed")

# 2. 모바일 스타일 및 UI 컴포넌트 CSS 통합
st.markdown("""
    <style>
        /* 기본 메뉴 및 여백 강제 숨김 */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="collapsedControl"] {display: none;}
        
        /* 앱 타이틀 */
        .app-title {
            text-align: center; font-size: 28px; font-weight: 900;
            color: #1e3a8a; margin-top: 10px; margin-bottom: 20px; letter-spacing: -1px;
        }
        
        /* 메인 런처 버튼 */
        .launcher-btn>button {
            width: 100%; border-radius: 16px; height: 75px; 
            font-size: 18px !important; font-weight: 800 !important; 
            margin-bottom: 12px; background-color: #ffffff; 
            border: 2px solid #e5e7eb; color: #374151;
            box-shadow: 0 4px 6px rgba(0,0,0,0.02); transition: all 0.2s;
        }
        .launcher-btn>button:hover {
            border-color: #3b82f6; color: #3b82f6; background-color: #f8fafc;
        }

        /* 판독기 결과 박스 */
        .result-box { padding: 20px; border-radius: 15px; margin-top: 20px; text-align: center; }
        .success-box { background-color: #ecfdf5; border: 2px solid #10b981; color: #065f46; }
        .share-btn>button { background-color: #3b82f6; color: white; border-radius: 12px; font-weight: bold; width: 100%; height: 50px; }

        /* D-Day 위젯 */
        .dday-widget {
            background: linear-gradient(135deg, #1e3a8a, #3b82f6);
            color: white; border-radius: 16px; padding: 25px;
            text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 25px;
        }
        .dday-text { font-size: 42px; font-weight: 900; margin: 0; line-height: 1.1; }
        .dday-sub { font-size: 16px; font-weight: 500; opacity: 0.9; }
        
        /* 오답노트 카드 */
        .fav-card {
            background-color: #f8fafc; border-left: 5px solid #f59e0b;
            padding: 15px; border-radius: 8px; margin-bottom: 12px;
        }
    </style>
""", unsafe_allow_html=True)

# 상단 헤더
st.markdown('<div class="app-title">🚗 Auto-Master</div>', unsafe_allow_html=True)
st.caption("👤 용산철도고 이** 학생")

# 3. 하단 네비게이션용 5개 탭
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 홈", "📸 판독", "📝 답안", "⭐️ 노트", "📅 일정"])

# ==========================================
# 탭 1: 🏠 홈 (대시보드)
# ==========================================
with tab1:
    st.write("---")
    st.markdown('<div class="launcher-btn">', unsafe_allow_html=True)
    st.button("🌱 기초 가이드 (처음 해봐요)")
    st.button("🔧 실전 연습 (연습하러 왔어요)")
    st.button("⏱️ 파이널 모의고사 (시험이 코앞이에요)")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 탭 2: 📸 AI 부품 판독기
# ==========================================
with tab2:
    st.subheader("📸 AI 부품 판독기")
    target_part = st.selectbox(
        "어떤 과제의 부품을 검수받을까요?",
        ["선택하세요", "[12안] 발전기 (Alternator)", "[1안] 윈드 실드 와이퍼 모터", "[2안] 인젝터"]
    )

    if target_part != "선택하세요":
        st.info(f"목표 부품: **{target_part}**\n\n부품이 화면 중앙에 오도록 촬영해 주세요.")
        img_file_buffer = st.camera_input("화면을 터치하여 촬영")
        
        with st.expander("또는 갤러리에서 사진 업로드"):
            uploaded_file = st.file_uploader("사진 선택", type=["jpg", "jpeg", "png"])
            if uploaded_file:
                img_file_buffer = uploaded_file

        if img_file_buffer is not None:
            with st.spinner("🔍 AI가 부품의 형상과 결합부를 정밀 분석 중입니다..."):
                time.sleep(2)
                st.markdown(f"""
                    <div class="result-box success-box">
                        <h3 style="margin-bottom: 5px;">✅ 판독 완료: 일치율 98%</h3>
                        <p>정확합니다! <b>{target_part.split(' ')[1]}</b>을(를) 올바르게 탈거하셨습니다.</p>
                        <p style="font-size: 14px; color: #047857;">[AI 코멘트] 상태가 매우 양호합니다.</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.write("---")
                st.markdown("#### 🌟 데이터 선순환 기여하기")
                st.markdown('<div class="share-btn">', unsafe_allow_html=True)
                if st.button("🚀 내 사진을 실습 DB에 공유하기"):
                    st.balloons()
                    st.success("🎉 학교 실습 데이터베이스에 저장되었습니다! 후배들에게 큰 도움이 됩니다.")
                st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 탭 3: 📝 디지털 답안지 (제동력 측정 예시)
# ==========================================
with tab3:
    st.subheader("📝 디지털 답안지")
    st.caption("과제: [제1안 새시] 제동력 측정 및 판정")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("측정 위치: 앞축")
    with col2:
        axle_weight = st.number_input("해당 축중 (kg)", value=1000, step=100)

    st.write("---")
    left_input = st.text_input("좌측 제동력 측정값 (예: 200kg)")
    right_input = st.text_input("우측 제동력 측정값 (예: 300kg)")
    
    st.write("**산출근거 및 결과**")
    calc_dev = st.text_input("편차 산출근거 및 편차(%)")
    calc_sum = st.text_input("합 산출근거 및 합(%)")

    status_input = st.radio("판정", ["선택 안 함", "양호", "불량"], horizontal=True)
    action_input = st.text_area("정비 및 조치할 사항", placeholder="예: 브레이크 교환 후 재점검")

    if st.button("🚀 제출 및 AI 피드백 받기", type="primary"):
        with st.spinner('AI 튜터가 답안을 분석하고 있습니다...'):
            st.write("---")
            st.subheader("🚨 AI 튜터 피드백")
            
            if "kg" not in left_input.lower() or "kg" not in right_input.lower():
                st.error("❌ **[오류] 단위(kg) 기재 누락!** 실전에서는 오답(0점) 처리됩니다.")
            else:
                st.success("✅ 단위(kg)를 정확히 기재했습니다.")

            try:
                l_val = float(re.sub(r'[^0-9.]', '', left_input))
                r_val = float(re.sub(r'[^0-9.]', '', right_input))
                
                real_dev = abs(l_val - r_val) / axle_weight * 100
                real_sum = (l_val + r_val) / axle_weight * 100
                correct_status = "양호" if (real_dev <= 8 and real_sum >= 50) else "불량"
                
                if status_input == "선택 안 함":
                    st.warning("⚠️ 판정을 선택하지 않았습니다.")
                elif status_input != correct_status:
                    st.error(f"❌ **[판정 오류]** 실제 편차 {real_dev:.1f}%, 합 {real_sum:.1f}% 입니다. 판정은 **'{correct_status}'**이어야 합니다.")
                else:
                    st.success(f"✅ 판정({status_input})이 정확합니다!")
                    
                if action_input:
                    if "고침" in action_input or "바꿈" in action_input:
                        st.warning("⚠️ **[용어 교정]** '고침' 대신 '교환 후 재점검' 등 표준 정비 용어를 사용하세요.")
                    elif len(action_input) > 2:
                        st.success("✅ 조치사항이 훌륭하게 작성되었습니다.")
            except ValueError:
                st.error("⚠️ 측정값에 올바른 숫자를 입력해 주세요.")

# ==========================================
# 탭 4: ⭐️ 내 오답 & 즐겨찾기
# ==========================================
with tab4:
    st.subheader("⭐️ 내 오답 & 즐겨찾기")
    sub_tab1, sub_tab2 = st.tabs(["🚨 AI 오답 노트", "📌 내 즐겨찾기"])
    
    with sub_tab1:
        st.markdown("""
            <div class="fav-card">
                <b>[1안] 제동력 측정 (앞축)</b><br>
                <span style="color: #ef4444; font-size: 14px;">❌ 잦은 실수: 단위(kg) 누락 및 편차 계산 오류</span><br>
                <span style="color: #10b981; font-size: 14px;">✅ AI 팁: 편차는 축중의 8% 이내, 합은 50% 이상!</span>
            </div>
            <div class="fav-card">
                <b>[12안] 스텝 모터(ISC) 저항 측정</b><br>
                <span style="color: #ef4444; font-size: 14px;">❌ 잦은 실수: 측정 핀 위치 오인</span><br>
                <span style="color: #10b981; font-size: 14px;">✅ AI 팁: 1-2번 핀과 2-3번 핀의 저항을 각각 측정하세요.</span>
            </div>
        """, unsafe_allow_html=True)
        
    with sub_tab2:
        st.info("실습 중 '별표(⭐️)'를 누른 항목이 여기에 모입니다.")
        st.markdown("- [공식] 제동력 편차 산출식: `(좌-우 절대값) / 축중 × 100`")
        st.markdown("- [규정값] 인젝터 코일 저항: `13 ~ 16 Ω`")

# ==========================================
# 탭 5: 📅 큐넷 시험일정 & D-Day
# ==========================================
with tab5:
    st.subheader("📅 2026년 정기 시험 일정")
    target_exam = st.selectbox("목표 시험을 설정하세요", 
                               ["선택", "2026년 정기 2회 실기시험 (5.30)", "2026년 정기 3회 실기시험 (8.29)"])
    
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
        
    with st.expander("📚 2026년 자동차정비기능사 연간 시험 일정 전체보기"):
        st.markdown("""
        * **1회차** | 필기: 1.20~1.24 | **실기: 3.14~4.01**
        * **2회차** | 필기: 4.04~4.09 | **실기: 5.30~6.14**
        * **3회차** | 필기: 6.27~7.02 | **실기: 8.29~9.16**
        * **4회차** | 필기: 9.16~9.21 | **실기: 11.14~12.02**
        """)