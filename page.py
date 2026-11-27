from pathlib import Path
import streamlit as st
import pandas as pd
from common import parse_sales,summarize

st.set_page_config(page_title="재고·물품 대여 관리 페이지", layout="wide")
st.title("📦재고·물품 대여 관리")
st.caption("재고 조회 및 물품 대여 관리 대시보드")

if "box_orders" not in st.session_state:
    st.session_state["box_orders"] = []

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요. 궁금한 내용을 물어보세요."}]

with st.sidebar:
    st.subheader("⚙️대여 관리 메뉴")
    uploaded = st.file_uploader("대여 관리 CSV 업로드", type=["csv"])
    if st.button ("대여/반납 내역 초기화"):
        st.session_state.box_orders = []
        st.warning("대여/반납 내역이 초기화되었습니다.")

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
        
all_rows = base_rows + st.session_state["box_orders"]

# 1. 초기 재고 설정 (실제 보유 수량과 대여 단가)
if "inventory" not in st.session_state:
    st.session_state["inventory"] = [
        {"product": "자전거", "price": 11000, "total_stock": 5},
        {"product": "돗자리", "price": 5000, "total_stock": 8},
        {"product": "캠핑의자", "price": 7000, "total_stock": 4},
    ]

# 2. 현재 대여 중인 수량 집계 및 남은 재고 계산
rented_qty_map = {}
for row in all_rows:
    prod = row["product"]
    rented_qty_map[prod] = rented_qty_map.get(prod, 0) + int(row["quantity"])

stock_map = {}
available_products = []
for item in st.session_state["inventory"]:
    prod = item["product"]
    remain = max(0, int(item["total_stock"]) - rented_qty_map.get(prod, 0))
    stock_map[prod] = {
        "price": int(item["price"]),
        "remain": remain,
    }
    if remain > 0:
        available_products.append(prod)
        
tab1, tab2, tab3= st.tabs(["📥대여", "📦재고 조회", "💬도우미 챗봇"])

with tab1:
    st.subheader("📥대여")

with tab2:
    st.subheader("📦재고 조회")


with tab3:
    st.subheader("💬도우미 챗봇")
