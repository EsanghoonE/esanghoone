import streamlit as st
import time

# 1. 모바일 앱 환경 설정
st.set_page_config(page_title="Auto-Master AI 판독기", page_icon="📸", layout="centered")

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .title-text { text-align: center; color: #1e3a8a; font-weight: 800; font-size: 24px; padding: 20px 0; }
        .result-box { padding: 20px; border-radius: 15px; margin-top: 20px; text-align: center; }
        .success-box { background-color: #ecfdf5; border: 2px solid #10b981; color: #065f46; }
        .fail-box { background-color: #fef2f2; border: 2px solid #ef4444; color: #991b1b; }
        .share-btn>button { background-color: #3b82f6; color: white; border-radius: 12px; font-weight: bold; width: 100%; height: 50px; }
    </style>
""", unsafe_allow_html=True)

# 상단 네비게이션 (뒤로가기 버튼 느낌)
if st.button("⬅️ 홈으로 돌아가기"):
    st.warning("메인 화면 로직은 여기에 연결됩니다.")

st.markdown('<div class="title-text">📸 AI 부품 판독기</div>', unsafe_allow_html=True)

# 2. 판독할 부품 선택
target_part = st.selectbox(
    "어떤 과제의 부품을 검수받을까요?",
    ["선택하세요", "[12안] 발전기 (Alternator)", "[1안] 윈드 실드 와이퍼 모터", "[2안] 인젝터"]
)

if target_part != "선택하세요":
    st.info(f"목표 부품: **{target_part}**\n\n부품이 잘 보이도록 밝은 곳에서 촬영해 주세요.")
    
    # 3. 실제 카메라 호출 기능 (Streamlit 핵심 기능)
    # 스마트폰으로 접속하면 전면/후면 카메라를 켤 수 있습니다!
    img_file_buffer = st.camera_input("카메라로 부품 촬영하기")
    
    # 또는 갤러리에서 올리기 옵션
    with st.expander("또는 갤러리에서 사진 업로드"):
        uploaded_file = st.file_uploader("사진 선택", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            img_file_buffer = uploaded_file

    # 4. AI 판독 시뮬레이션
    if img_file_buffer is not None:
        with st.spinner("🔍 AI가 부품의 형상과 결합부를 정밀 분석 중입니다..."):
            time.sleep(2) # 실제 AI가 분석하는 것처럼 2초 대기 애니메이션
            
            # (교수님 시연을 위한 가짜 AI 판독 로직)
            # 여기서는 시연의 극적 효과를 위해 무조건 '정답' 시나리오를 보여줍니다.
            
            st.markdown("""
                <div class="result-box success-box">
                    <h3 style="margin-bottom: 5px;">✅ 판독 완료: 일치율 98%</h3>
                    <p>정확합니다! <b>발전기(Alternator)</b>를 올바르게 탈거하셨습니다.</p>
                    <p style="font-size: 14px; color: #047857;">[AI 코멘트] V벨트 풀리의 마모 상태도 양호해 보입니다. 다음 조립 단계를 진행해 주세요.</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.write("---")
            st.subheader("🌟 데이터 선순환 기여하기")
            st.write("훌륭하게 탈거된 이 부품 사진을 후배들의 기초 가이드 교재로 등록하시겠습니까?")
            
            # DB 기부 버튼
            st.markdown('<div class="share-btn">', unsafe_allow_html=True)
            if st.button("🚀 내 사진을 실습 DB에 공유하기"):
                st.balloons() # 성공 축하 풍선 애니메이션
                st.success("🎉 학교 실습 데이터베이스에 성공적으로 저장되었습니다! 후배들에게 큰 도움이 될 것입니다.")
            st.markdown('</div>', unsafe_allow_html=True)