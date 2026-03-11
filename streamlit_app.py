import streamlit as st
import time

# 1. 앱 기본 설정 (모바일 최적화)
st.set_page_config(page_title="Auto-Master", page_icon="🚗", layout="centered", initial_sidebar_state="collapsed")

# 2. 화면 전환을 위한 Session State 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def go_to_page(page_name):
    st.session_state.page = page_name

# 3. 모바일 네이티브 스타일 CSS 통합 적용
st.markdown("""
    <style>
        /* 기본 메뉴 및 여백 숨김 */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="collapsedControl"] {display: none;}

        /* 홈 화면 타이틀 */
        .app-title {
            text-align: center; font-size: 32px; font-weight: 900;
            color: #1e3a8a; margin-top: 30px; margin-bottom: 30px; letter-spacing: -1px;
        }

        /* 메인 런처 버튼 스타일 */
        .launcher-btn>button {
            width: 100%; border-radius: 16px; height: 75px; 
            font-size: 18px !important; font-weight: 800 !important; 
            margin-bottom: 12px; background-color: #ffffff; 
            border: 2px solid #e5e7eb; color: #374151;
            box-shadow: 0 4px 6px rgba(0,0,0,0.02); transition: all 0.2s;
        }
        .launcher-btn>button:hover, .launcher-btn>button:active {
            border-color: #3b82f6; color: #3b82f6; background-color: #f8fafc;
        }

        /* 구분선 */
        hr { margin-top: 25px; margin-bottom: 25px; border: none; border-top: 2px dashed #e5e7eb; }

        /* 판독기 화면 전용 스타일 */
        .page-title { text-align: center; color: #1e3a8a; font-weight: 800; font-size: 22px; padding: 10px 0; }
        .result-box { padding: 20px; border-radius: 15px; margin-top: 20px; text-align: center; }
        .success-box { background-color: #ecfdf5; border: 2px solid #10b981; color: #065f46; }
        .share-btn>button { background-color: #3b82f6; color: white; border-radius: 12px; font-weight: bold; width: 100%; height: 50px; }
        .back-btn>button { background-color: transparent; border: none; color: #6b7280; font-weight: bold; padding: 0; display: flex; align-items: center;}
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 📱 화면 1: 홈 화면 (메인 런처)
# ==========================================
if st.session_state.page == 'home':
    st.markdown('<div class="app-title">🚗 Auto-Master</div>', unsafe_allow_html=True)

    # 기본 학습 모드 (현재는 클릭 시 안내문구만 출력)
    st.markdown('<div class="launcher-btn">', unsafe_allow_html=True)
    if st.button("🌱 기초 가이드 (처음 해봐요)"):
        st.info("기초 가이드 기능은 개발 중입니다.")
    if st.button("🔧 실전 연습 (연습하러 왔어요)"):
        st.info("실전 연습 디지털 답안지 기능이 곧 연동됩니다.")
    if st.button("⏱️ 파이널 모의고사 (시험이 코앞이에요)"):
        st.info("모의고사 타이머 기능이 곧 연동됩니다.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # AI 판독기 진입 버튼 (클릭 시 화면 전환)
    st.markdown('<div class="launcher-btn">', unsafe_allow_html=True)
    st.button("📸 AI 부품 판독기", on_click=go_to_page, args=('scanner',))
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 📸 화면 2: AI 부품 판독기 (카메라 뷰)
# ==========================================
elif st.session_state.page == 'scanner':
    
    # 뒤로가기 버튼
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("⬅️ 홈으로 돌아가기", on_click=go_to_page, args=('home',))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="page-title">📸 AI 부품 판독기</div>', unsafe_allow_html=True)
    
    # 판독 타겟 선택
    target_part = st.selectbox(
        "어떤 과제의 부품을 검수받을까요?",
        ["선택하세요", "[12안] 발전기 (Alternator)", "[1안] 윈드 실드 와이퍼 모터", "[2안] 인젝터"]
    )

    if target_part != "선택하세요":
        st.info(f"목표 부품: **{target_part}**\n\n부품이 화면 중앙에 오도록 밝은 곳에서 촬영해 주세요.")
        
        # 스마트폰 카메라 호출
        img_file_buffer = st.camera_input("화면을 터치하여 촬영")
        
        with st.expander("또는 갤러리에서 사진 업로드"):
            uploaded_file = st.file_uploader("사진 선택", type=["jpg", "jpeg", "png"])
            if uploaded_file:
                img_file_buffer = uploaded_file

        # AI 판독 결과 시뮬레이션 로직
        if img_file_buffer is not None:
            with st.spinner("🔍 AI가 부품의 형상과 결합부를 정밀 분석 중입니다..."):
                time.sleep(2) # AI 분석 대기시간 연출
                
                # 정답 판정 UI
                st.markdown(f"""
                    <div class="result-box success-box">
                        <h3 style="margin-bottom: 5px;">✅ 판독 완료: 일치율 98%</h3>
                        <p>정확합니다! <b>{target_part.split(' ')[1]}</b>을(를) 올바르게 탈거하셨습니다.</p>
                        <p style="font-size: 14px; color: #047857;">[AI 코멘트] 연결부의 손상 없이 깔끔하게 분리되었습니다. 상태가 매우 양호합니다.</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.write("---")
                st.markdown("#### 🌟 데이터 선순환 기여하기")
                st.caption("훌륭하게 탈거된 이 부품 사진을 학교 실습 데이터베이스에 공유하여 후배들의 시각 교재로 활용되게 해주세요!")
                
                # 데이터베이스 기부 액션
                st.markdown('<div class="share-btn">', unsafe_allow_html=True)
                if st.button("🚀 내 사진을 실습 DB에 공유하기"):
                    st.balloons()
                    st.success("🎉 학교 실습 데이터베이스에 성공적으로 저장되었습니다! 후배들에게 큰 도움이 될 것입니다.")
                st.markdown('</div>', unsafe_allow_html=True)