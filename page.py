from pathlib import Path
import streamlit as st
import pandas as pd
from common import parse_sales,summarize

st.set_page_config(page_title="재고·물품 대여 관리 페이지", layout="wide")
st.title("📦재고·물품 대여 관리")
st.caption("**대여 등록시 품절 상품 새로고침 주의**")

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
        {"product": "자전거", "price": 11000, "total_stock": 10},
        {"product": "돗자리", "price": 5000, "total_stock": 17},
        {"product": "의자", "price": 7000, "total_stock": 18},
        {"product": "테이블", "price": 10000, "total_stock": 8},
        {"product": "텐트", "price": 45000, "total_stock": 7},
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

    if not available_products:
        st.warning("현재 대여 가능한 남은 재고가 없습니다.")
    else:
        selected_product = st.selectbox("대여할 상품 선택", available_products)
        remain_qty = stock_map[selected_product]["remain"]
        unit_price = stock_map[selected_product]["price"]

        st.caption(f"남은 재고: {remain_qty}개 | 단가: {unit_price:,}원")

        with st.form("rental_create_form", clear_on_submit=True):
            col1, col2 = st.columns([2,1])
            with col1:
                renter_name = st.text_input("대여자 이름", placeholder="예: 홍길동")
            with col2:
                rental_qty = st.number_input("대여 수량", min_value=1,max_value=remain_qty, value=1, step=1,)

            submitted = st.form_submit_button("대여 등록")

            if submitted:
                cleaned_name = renter_name.strip()
                if not cleaned_name:
                    st.error("대여자 이름을 입력해 주세요.")
                else:
                    st.session_state["box_orders"].append({
                        "renter": cleaned_name,
                        "product": selected_product,
                        "quantity": int(rental_qty),
                        "price":unit_price,
                    })
                    st.success(f"{cleaned_name} | '{selected_product}' | {int(rental_qty)}개 대여 등록 완료.")
            st.subheader("현재 대여 내역")

            current_rows = base_rows + st.session_state["box_orders"]
            if current_rows:
                df_rentals = pd.DataFrame(current_rows)
                df_rentals["합계금액"] = df_rentals["quantity"] * df_rentals["price"]
                df_rentals = df_rentals.rename(columns={
                    "renter": "대여자",
                    "product": "대여 상품",
                    "quantity": "수량",
                    "price": "단가",
                })
                st.dataframe(df_rentals, use_container_width=True, hide_index=True)
            else:
                st.info("등록된 대여 내역이 없습니다.")
with tab2:
    st.subheader("📦재고 조회")


with tab3:
    st.subheader("💬도우미 챗봇")
