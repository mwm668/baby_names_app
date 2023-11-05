import streamlit as st


from babyname_utils import load_data, top_names_history
from babyname_utils import display_altair_chart_with_highlight

st.set_page_config(
    page_title="Home | Baby Names NZ",
    page_icon="👶"
)

st.write("# Welcome to Baby Names NZ! 👶")


df = load_data()
latest_year = df['year'].max()
last_x_years = 20
df = df[df['year']>latest_year-last_x_years]

st.subheader('Female')
female_df = top_names_history(df,latest_year,'female')[['year','name','count']]
display_altair_chart_with_highlight(female_df)

st.subheader('Male')
male_df = top_names_history(df,latest_year,'male')[['year','name','count']]
display_altair_chart_with_highlight(male_df)

