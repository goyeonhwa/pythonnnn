import streamlit as st
st.title("온라인 문구점")
left, right = st.columns(2)
with left:
    st.header("노트")
    st.markdown("**학습 기록용** 노트입니다.")
with right:
    st.header("가격")
    st.write("8,000원")
    st.sidebar.write("설명을 읽고 상품을 선택하세요.")