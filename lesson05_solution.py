import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import streamlit as st
from common import parse_sales
st.write("필수 열: product, quantity, price")
upload = st.file_uploader("UTF-8 CSV", type=["csv"])
if upload is not None:
    try:
        st.dataframe(parse_sales(upload.getvalue()))
    except ValueError as exc:
        st.error(str(exc))