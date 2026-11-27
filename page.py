from pathlib import Path
import streamlit as st
import pandas as pd
from common import parse_sales,summarize

st.set_page_config(page_title="재고·물품 대여 관리 페이지", layout="wide")
st.title("📦재고·물품 대여 관리")
st.caption("재고 조회 및 물품 대여 관리 대시보드")

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

base_rows = []
if uploaded:
    try:
        base_rows = parse_sales(uploaded.getvalue())
        st.sidebar.success(f"CSV에서 {len(base_rows)}행을 불러왔습니다.")
    except ValueError as exc:
        st.sidebar.error(str(exc))

else:
    sample_path = Path(__file__).resolve().parent / "data" / "sales.csv"
    if sample_path.exists():
        base_rows = parse_sales(sample_path.read_bytes())
    else:
        base_rows = [{"대여 상품": "book", "quantity": 2, "price": 12000}, {"product": "pen", "quantity": 5, "price": 1500}]
all_rows = base_rows + st.session_state.pos_orders

tab1, tab2, tab3, tab4 = st.tabs(["📥대여", "📤반납", "📦재고 조회", "🤖도우미 챗봇"])
