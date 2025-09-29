
import streamlit as st

import streamlit as st

st.set_page_config(page_title="용산철도고등학교 진학 설문조사", layout="centered")
st.title("🚄 용산철도고등학교 진학 희망 중학생 설문조사")
st.markdown("""
이 설문은 용산철도고등학교 진학을 희망하는 중학생 여러분의 다양한 특성과 생각을 파악하기 위해 만들어졌습니다. 
성적, 흥미, 적성 등 여러 요소를 바탕으로 여러분의 의견을 자유롭게 입력해 주세요.
""")

# 용산철도고등학교 실제 학교 사진 (구글 이미지 검색 활용)
st.image("https://search.pstatic.net/common/?src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20200130_181%2F1580379648887QwQwA_JPEG%2F%25C0%25CF%25BB%25EA%25C3%25BB%25B5%25B5%25B0%25ED%25B5%25BF%25C7%25D1%25B1%25B3_%25281%2529.jpg&type=sc960_832", use_container_width=True, caption="용산철도고등학교 전경(출처: 네이버 지도)")

with st.form("survey_form"):
    st.subheader("기본 정보")
    name = st.text_input("이름(선택)")
    contact = st.text_input("연락처(휴대폰 번호 등, 선택)")
    gender = st.radio("성별", ["남", "여", "응답하지 않음"])
    grade = st.selectbox("학년", ["1학년", "2학년", "3학년"])
    school = st.text_input("학교명(선택)")

    st.subheader("학업 및 진로")
    score = st.slider("최근 학기 주요과목 평균 점수", 0, 100, 70)
    fav_subject = st.text_input("가장 좋아하는 과목")
    aptitude = st.selectbox("본인의 적성에 가장 가깝다고 생각하는 분야", ["이공계", "인문/사회", "예체능", "기타"])
    interest = st.multiselect("관심 있는 분야(복수 선택 가능)", ["철도운전", "철도차량", "전기/전자", "IT/소프트웨어", "기계/설비", "기타"])

    st.subheader("용산철도고등학교 진학 동기 및 기대")
    reason = st.text_area("왜 용산철도고등학교에 진학하고자 하나요? (관심 계열, 진로 목표, 기대하는 점 등)")
    concern = st.text_area("진학에 있어 가장 고민되는 점은 무엇인가요?")

    st.subheader("기타 의견")
    etc = st.text_area("추가로 하고 싶은 말이 있다면 적어주세요.")

    submitted = st.form_submit_button("제출하기")
    if submitted:
        st.success("설문이 성공적으로 제출되었습니다. 감사합니다!")
