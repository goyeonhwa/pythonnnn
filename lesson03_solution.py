import streamlit as st
price = st.number_input("단가", min_value=1, value=1000)
quantity = st.number_input("수량", min_value=1, value=5)
st.metric("총액", f"{price * quantity:,}원")