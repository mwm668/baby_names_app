import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'


######### Define functions ###########

def load_data():
    data = pd.read_csv('data/nz_baby_names.csv').sort_values(by=['year','rank'])
    return data


def display_results(df,baby_name):
    """
    Take a dataframe and name, generate chart of that name's history
    """
    
    # Get df filtered on that name
    name_df = df[df.name == baby_name]

    # Convert year to datetime, set as index
    name_df['year'] = pd.to_datetime(name_df['year'], format="%Y")
    # name_df.set_index('year',inplace=True)

    # Plot chart
    # st.subheader("Number of {0}'s born by year".format(baby_name))
    # st.bar_chart(name_df[['count']])

    # Plot chart
    # st.subheader("Number of {0}s born by year".format(baby_name))
    # st.line_chart(name_df[['count']])

    # Create altair chart object
    st.subheader("Number of {0}s born by year".format(baby_name))
    highlight = alt.selection_point(on='mouseover', fields=['symbol'], nearest=True)
    base = alt.Chart(name_df).mark_line(interpolate='basis',strokeWidth=3).encode(
                alt.X('year:T', title='Year', axis=alt.Axis(format="%Y", tickCount='year')),
                alt.Y('count', title='Count')
            )
    
    points = base.mark_circle().encode(opacity=alt.value(0))\
        .add_params(highlight).properties(width=600)

    lines = base.mark_line(interpolate='basis').encode(
        size=alt.condition(~highlight, alt.value(1), alt.value(3))
    )

    # Display the chart           
    st.altair_chart(points + lines, use_container_width=True)
    # st.altair_chart(c, use_container_width=True)


def display_multiple_line_charts(df):
    """
    Given df and the name of category column, generate line chart
    """
    st.line_chart(df[['count']])


def top_names_history(df,names_year,names_gender):
    """
    Take dataframe, gender and year, return df of complete history of top X names
    """
    
    # Get top names for given year
    top_names_list = get_top_names(df,names_year=names_year,names_gender=names_gender)['name'].unique()

    # Return df of data for all those top names
    history_df = df[df['name'].isin(top_names_list)]

    return history_df

#
def get_top_names(df,names_year=2020,names_gender='female',top_x=5):
    """
    Takes a dataframe of names with year, gender, rank. 
    Returns filtered dataframe for specified year, gender and top X names
    """    

    # Get the result of filtering df by year, gender, and top x
    top_df = df[(df.year == names_year) & (df.gender == names_gender) &  (df['rank'] <= top_x)][['rank','name','count']]
    # Set the rank as the index
    top_df.set_index('rank',inplace=True)
    # We want to also have rank as column to use
    top_df['rank'] = top_df.index

    return top_df

# Given a year, convert to decade for data grouping
def year_to_decade(year):
    decade = int(str(year)[:3]+'0')
    return decade

# Given a name, return probability of decades
def decade_probability(df,baby_name):
    name_df = df[df['name']==baby_name]
    name_df['decade'] = name_df.apply(lambda x: year_to_decade(x['year']),axis=1)
    decade_df = name_df.groupby(by=name_df['decade'])['count'].sum().reset_index(name='count')
    decade_df['prob'] = decade_df['count'] / decade_df['count'].sum()
    decade_df.sort_values('prob',ascending=False,inplace=True)
    return decade_df

#
def display_metrics(df,baby_name):
    """
    Take df and name and generate 3 metric cards in Streamlit
    """

    # Get copy of df for our name
    name_df2 = df[df.name == baby_name].copy(deep=True)
    # Sort by highest count & return year
    name_df2.sort_values(by='count',ascending=False,inplace=True)
    highest_year = name_df2.iloc[0].year
    highest_year_count = name_df2.iloc[0]['count']
    total_count = name_df2['count'].sum()

    # Get decade metric
    decade_df = decade_probability(df,baby_name)
    top_decade = int(decade_df.iloc[0].decade)
    top_prob = decade_df.iloc[0].prob
    
    # Display metrics side-by-side
    st.subheader('Interesting facts about {}'.format(baby_name))
    col1a, col2a, col3a = st.columns(3)
    col1a.metric("Most Popular Year",str(highest_year))
    col2a.metric("Total {}s".format(baby_name),f'{total_count:,}')
    col3a.metric("Most popular decade",str(top_decade)+"s")
    
    
    col1b, col2b, col3b = st.columns(3)
    col1b.metric("{0}s in {1}".format(baby_name,highest_year),f'{highest_year_count:,}')
    col3b.markdown("**{0:.0%}** of {1}s were born in the **{2}s**".format(top_prob,baby_name,top_decade))
