import streamlit as st
import altair as alt
import numpy as np
import pandas as pd

from babyname_utils import load_data, get_top_names, display_metrics, display_results

pd.options.mode.chained_assignment = None  # default='warn'

st.set_page_config(page_title="Blog | Baby Names NZ", page_icon="👶")


st.header("Blog Posts")
st.markdown("""---""")

#########################################################

st.subheader("Title Title")
st.caption("31st Oct 2023")
st.text('Here we write the blog.')
df = load_data()
st.dataframe(df.head(5))
st.text('Here we write some more stuff.')
st.markdown("""---""")

#########################################################
