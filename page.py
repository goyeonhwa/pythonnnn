import streamlit as st

st.set_page_config(page_title="재고·물품 대여 관리 페이지", layout="wide")
st.title("📦재고·물품 대여 관리")
st.markdown("**재고 조회 및 물품 대여 관리 대시보드**")

if "box_orders" not in st.session_state:
    st.session_state["pos_orders"] = []

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요. 궁금한 내용을 물어보세요."}]

with st.sidebar:
    st.subheader("⚙️대여 관리 메뉴")
    uploaded = st.sidebar.file_uploader("대여 관리 CSV 업로드", type=["csv"])
    if st.button ("대여/반납 내역 초기화"):
        st.session_state.pos_orders = []
        st.sidebar.warning("대여/반납 내역이 초기화되었습니다.")
