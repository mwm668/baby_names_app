import streamlit as st
import altair as alt
import numpy as np
import pandas as pd

from babyname_utils import load_data, get_top_names, display_metrics, display_results

pd.options.mode.chained_assignment = None  # default='warn'

st.set_page_config(page_title="Analyse Name", page_icon="📊")
st.sidebar.header("Analyse Name")

# Define dataframe
df = load_data()

# Select gender of name
gender_select = st.sidebar.radio('',['Female','Male'])
gender_select = gender_select.lower()

#########################
# Specfic NAME analysis  #
#########################

# Set default name for use in input box
top_names_m = get_top_names(df=df,names_gender=gender_select,top_x=5)
baby_name = top_names_m['name'].iloc[0]

# Set specific name in input box
st.sidebar.text_input("Enter baby name:", value=baby_name,key="name_input")
baby_name = st.session_state['name_input'].capitalize()

# Check that name is in list
if len(df[df['name']==baby_name]) > 0:
    # create kpi cards
    display_metrics(df,baby_name)
    # display results chart
    display_results(df,baby_name)
    
else:
    st.error('{0} has not placed in the top 100 between 1954 and 2020.'.format(baby_name))
