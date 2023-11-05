import streamlit as st
import altair as alt
import numpy as np
import pandas as pd

from babyname_utils import load_data, get_top_names, top_names_history
from babyname_utils import display_altair_chart_with_label, display_altair_chart_with_highlight, display_plotly_chart

pd.options.mode.chained_assignment = None  # default='warn'

st.set_page_config(page_title="Year | Baby Names NZ", page_icon="👶")
st.sidebar.header("Search Year")

# Define dataframe
# @st.cache_data
df = load_data()

# Select gender of name
gender_select = st.sidebar.radio('Select:',['Female','Male'],label_visibility='collapsed')
gender_select = gender_select.lower()

#########################
# Specfic YEAR analysis  #
#########################

# Set top number
top_x = 5

# Select year
year_select = st.sidebar.slider(
    label="Year",
    min_value=1954,
    max_value=2020
)

# Get top 5 names for gender
top_names_m = get_top_names(df=df,names_gender=gender_select,names_year=year_select,top_x=top_x)
baby_name = top_names_m['name'].iloc[0]

# Header for buttons
st.subheader('Top {0} {1} names for {2}'.format(top_x,gender_select,year_select))

# Create buttons for top names
for name in top_names_m['name']:
    st.button(label=name,key=name)

# Check if button clicked
for name in top_names_m['name']:
    if st.session_state[name]:
        baby_name = name

# display_results(df,baby_name)


st.subheader("Number of {0}s born by year".format(baby_name))

# Get history of top X names and plot
history_df = top_names_history(df,year_select,gender_select)[['year','name','count']]

display_altair_chart_with_highlight(history_df)

display_altair_chart_with_label(history_df)

display_plotly_chart(history_df)