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

@st.cache_data(ttl=60)
def get_cached_summary(rows):
    return summarize(rows)

with st.sidebar:
    st.subheader("⚙️대여 관리 메뉴")
    uploaded = st.sidebar.file_uploader("대여 관리 CSV 업로드", type=["csv"])
    if st.button ("대여/반납 내역 초기화"):
        st.session_state.box_orders = []
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
        base_rows = [{"renter": "고연화", "product": "자전거", "quantity": 1, "price": 11000}, {"renter": "정세은", "product": "돗자리", "quantity": 2, "price": 5000}]
all_rows = base_rows + st.session_state.box_orders

tab1, tab2, tab3, tab4 = st.tabs(["📥대여", "📤반납", "📦재고 조회", "💬도우미 챗봇"])
with tab1:
    st.subheader("📥대여")
    products = ["전체"] + sorted({row["product"] for row in all_rows})
    selected = st.selectbox("조회할 상품 선택", products)
    if selected == "전체":
        filtered = all_rows
    else:
        filtered = [r for r in all_rows if r["product"] == selected]
    summary = get_cached_summary(filtered)
    col1, col2, col3 = st.columns(3)
    col1.metric("총매출", f"{summary['revenue']:,}원")
    col2.metric("총 판매 수량", f"{summary['quantity']:,}개")
    col3.metric("거래 건수", f"{len(filtered)}건")
    left, right = st.columns([1.2, 1])
    with left:
        st.subheader("상세 거래 내역")
        if filtered:
            df = pd.DataFrame(filtered)
            df["subtotal"] = df["quantity"] * df["price"]
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("표시할 데이터가 없습니다.")
    
    with right:
        st.subheader("상품별 대여 비중")
        if summary["by_product"]:
            st.bar_chart(summary["by_product"])
