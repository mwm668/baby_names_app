import streamlit as st
import altair as alt
import numpy as np
import pandas as pd

from babyname_utils import load_data, get_top_names, top_names_history

pd.options.mode.chained_assignment = None  # default='warn'

st.set_page_config(page_title="Search Year", page_icon="📅")
st.sidebar.header("📅 Search Year")

# Define dataframe
# @st.cache_data
df = load_data()

# Select gender of name
gender_select = st.sidebar.radio('',['Female','Male'])
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

# Create size column to highlight top name for current year
history_df['size'] = np.where(history_df['name']==baby_name, 2, 1)

# Get min/max for axis
min_year = history_df['year'].min()
max_year = history_df['year'].max()

# COnvert year to datetime
history_df['year'] = pd.to_datetime(history_df['year'], format="%Y")

# Create altair chart object
selection = alt.selection_multi(fields=['name'], bind='legend')
c = alt.Chart(history_df).mark_line(interpolate='basis').encode(
            alt.X('year:T', title='Year', axis=alt.Axis(format="%Y", tickCount='year'), scale=alt.Scale(domain=(min_year-5, max_year))),
            alt.Y('count', title='Count'),
            alt.Color('name', title='Name', scale=alt.Scale(scheme='category10')), 
            alt.Size('size'),
            tooltip=['name','year(year):T','count'],
            opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
        ).add_selection(selection)

# Add vertical line for selected year
# rule = alt.Chart(pd.DataFrame({
#                 'year': [year_select],
#                 'color': ['steelblue']
#             })).mark_rule().encode(
#                 x='year:T',
#                 color=alt.Color('color:N', scale=None)
#             )

# year_text = rule.mark_text(align='center', xOffset = 15, yOffset = 110)\
#             .encode(text='year(year):T')


# Display the chart           
st.altair_chart(c, use_container_width=True)
# st.altair_chart(c + rule + year_text, use_container_width=True)
