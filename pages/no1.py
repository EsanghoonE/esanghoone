
import streamlit as st

st.title("나의 꿈을 돌아보기")
st.markdown("""
초등학교, 중학교 시절 나의 꿈은 무엇이었나요? 그리고 왜 그런 꿈을 갖게 되었는지 자유롭게 적어보세요.
""")

with st.form("dream_form"):
	st.subheader("초등학교 때의 꿈")
	dream_elem = st.text_area("초등학교 때 나의 꿈은 무엇이었나요?", height=100)
	reason_elem = st.text_area("왜 그 꿈을 갖게 되었나요?", height=100)

	st.subheader("중학교 때의 꿈")
	dream_middle = st.text_area("중학교 때 나의 꿈은 무엇이었나요?", height=100)
	reason_middle = st.text_area("왜 그 꿈을 갖게 되었나요? (중학교)", height=100)

	submitted = st.form_submit_button("작성 완료")
	if submitted:
		st.success("입력이 저장되었습니다. 나의 꿈을 돌아보는 소중한 시간이 되었길 바랍니다!")
