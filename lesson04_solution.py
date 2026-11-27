import pandas as pd
import streamlit as st
df = pd.DataFrame({"subject":["a","b","c"],
                   "score": [80,90,100]})
st.dataframe(df, hide_index=True)
st.bar_chart(df.set_index("subject")["score"])
st.metric("평균", f"{df['score'].mean():.1f}")