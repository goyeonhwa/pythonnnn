import streamlit as st
st.title("1부터 n까지 합계 구하기")
@st.cache_data(ttl=55)
def sum_squares(limit):
    return sum(range(limit + 1))

limit = st.number_input("숫자", min_value=1, max_value=10, value=1)
with st.spinner("계산 중"):
    result = sum_squares(int(limit))
st.metric("1부터 n까지 합계", result)
sum_squares.clear()