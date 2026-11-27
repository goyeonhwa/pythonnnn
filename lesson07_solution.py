import streamlit as st
st.title("신청 미리보기")
with st.form("order_form"):
    email = st.text_input("이메일")
    raw = st.number_input("참가인원", value =1)
    submitted = st.form_submit_button("신청")
if submitted:
    st.session_state.pop("result", None)
    if "@" not in email:
        raise ValueError("정확한 이메일을 입력해주세요.")
    quantity = int(raw)
    if not 1 <= quantity <= 10:
        raise ValueError("1~10의 참가인원을 입력하세요.")
    else:
        st.write(f"{email} | {raw}명")