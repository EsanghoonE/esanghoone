
import streamlit as st
import pandas as pd
import numpy as np
import time


st.set_page_config(page_title="Streamlit 요소 예시", layout="wide")
st.title("🧩 Streamlit 요소 예시 페이지")
st.markdown("""
이 페이지는 Streamlit에서 자주 사용하는 다양한 요소(위젯, 레이아웃, 차트 등)를 한눈에 볼 수 있도록 예시로 구성되어 있습니다.
""")

st.header("1. 텍스트와 마크다운")
st.text("이것은 일반 텍스트입니다.")
st.markdown("**마크다운** _스타일링_ :star:")
st.code("print('Hello, Streamlit!')", language="python")
st.latex(r"E=mc^2")

st.header("2. 입력 위젯")
name = st.text_input("이름을 입력하세요:")
age = st.number_input("나이", min_value=0, max_value=120, value=25)
agree = st.checkbox("동의합니다")
color = st.radio("좋아하는 색상은?", ("빨강", "파랑", "초록"))
option = st.selectbox("선택하세요", ["옵션1", "옵션2", "옵션3"])
st.slider("슬라이더", 0, 100, 50)
st.date_input("날짜 선택")
st.time_input("시간 선택")
st.file_uploader("파일 업로드")

st.header("3. 버튼과 상호작용")
if st.button("클릭!"):
    st.success("버튼이 눌렸습니다!")

st.header("4. 컬럼과 레이아웃")
col1, col2 = st.columns(2)
with col1:
    st.info("왼쪽 컬럼")
with col2:
    st.warning("오른쪽 컬럼")

with st.expander("더보기 (Expander)"):
    st.write("이곳에 추가 정보를 넣을 수 있습니다.")

st.header("5. 데이터프레임과 표")
df = pd.DataFrame(
    np.random.randn(5, 3),
    columns=["A", "B", "C"]
)
st.dataframe(df)
st.table(df.head(3))

st.header("6. 차트와 시각화")
st.subheader("Line Chart")
st.line_chart(df)
st.subheader("Bar Chart")
st.bar_chart(df)
st.subheader("Area Chart")
st.area_chart(df)

st.header("7. 이미지와 미디어")
st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)
st.audio(np.random.randn(44100), sample_rate=44100)
st.video("https://www.youtube.com/watch?v=R2nr1uZ8ffc")

st.header("8. 상태 표시 및 알림")
st.success("성공 메시지 예시")
st.info("정보 메시지 예시")
st.warning("경고 메시지 예시")
st.error("에러 메시지 예시")
st.exception(Exception("예외 메시지 예시"))

st.header("9. 진행바와 스피너")
with st.spinner("잠시만 기다려주세요..."):
    time.sleep(1)
st.success("완료!")
progress = st.progress(0)
for i in range(1, 101, 10):
    progress.progress(i)
    time.sleep(0.05)

st.header("10. 사이드바")
st.sidebar.title("사이드바 예시")
st.sidebar.write("여기에 다양한 위젯을 넣을 수 있습니다.")
st.sidebar.selectbox("사이드바 선택", ["A", "B", "C"])
