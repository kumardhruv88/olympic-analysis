import streamlit as st
import pandas as pd
from click import style
from streamlit import sidebar
import plotly.express as px
import  matplotlib.pyplot as plt
import  seaborn as sns
import plotly.figure_factory as ff
import scipy as sp
import numpy as np
from data_loader import get_athlete_df

import helper
import process
from helper import medal_tally
df=pd.read_csv('https://drive.google.com/file/d/1K5KawxtSc3XsyCLAGZhRg21EE7BgFQ5h/view?usp=drive_link')
region_df=pd.read_csv('noc_regions.csv')

df=process.preprocess(df,region_df)
st.sidebar.title('olympic analysis')
st.sidebar.image('https://logos-world.net/wp-content/uploads/2021/09/Olympics-Emblem.png')
user_menu=st.sidebar.radio(
    'select an option',
    ('medal count','overall analysis','country wise analysis','athlete analysis')
)
athlete_df=get_athlete_df(df)

if user_menu=='medal count':
    st.sidebar.header('medal count')
    years,country=helper.country_year(df)
    selected_year=st.sidebar.selectbox('select year',years)
    selected_country=st.sidebar.selectbox('select country',country)
    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year=='overall' and selected_country=='overall':
        st.title('Overall Medal Tally')
    if selected_year!='overall' and selected_country=='overall':
        st.title('medal tally in'+ str(selected_year) +'olympic')
    if selected_year=='overall' and selected_country!='overall':
        st.title(selected_country+'overall perfomance')
    if selected_year!='overall' and selected_country!='overall':
        st.title(selected_country+' perfomance in '+ str(selected_year) + 'olympic')
    st.table(medal_tally)


if user_menu=="overall analysis":
    editions=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    sports= df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]

    st.title('overall statistics')

    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(editions)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)

    nation=helper.time(df,'region')
    fig = px.line(nation, x='Edition', y='region')
    st.title('countries over the years')
    st.plotly_chart(fig)

    event_over_time = helper.time(df, 'Event')
    fig = px.line(event_over_time, x='Edition', y='Event')
    st.title('events over the years')
    st.plotly_chart(fig)

    athletes = helper.time(df, 'Name')
    fig = px.line(athletes, x='Edition', y='Name')
    st.title('athletes over the years')
    st.plotly_chart(fig)

    st.title('no of sports played ')
    fig,ax=plt.subplots(figsize=(25,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),annot=True)
    st.pyplot(fig)


    st.title('successful athletes')
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'overall')
    selected_sport=st.selectbox('select sport',sport_list)
    y=helper.most(df,selected_sport)
    st.table(y)


if user_menu=="country wise analysis":
    st.sidebar.title('country wise analysis')
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country=st.sidebar.selectbox('select a country',country_list)
    country_df=helper.year_medal_count(df,selected_country)
    fig=px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + "medal over the years")
    st.plotly_chart(fig)

    st.title(selected_country + "perfomance in following sport")
    pt=helper.event_heatmap(df,selected_country)
    fig,ax=plt.subplots(figsize=(25,20))
    ax=sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("top 15 athletes-" + selected_country)
    top_10=helper.success(df,selected_country)
    st.table(top_10)


if user_menu=='athlete analysis':
    athlete_df=df.dropna(subset=['Name','region'])
    x1=athlete_df['Age'].dropna()
    x2=athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3=athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4=athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()
    fig=ff.create_distplot([x1,x2,x3,x4],['overall age','gold medallist','silver medallist','bronze medallist'],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=800,height=600)
    st.title('distribution of Age')

    st.plotly_chart(fig)
    x=[]
    name=[]
    famous_sport=['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sport:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x,name, show_hist=False,
                             show_rug=False)
    fig.update_layout(autosize=False, width=800, height=600)
    st.title('distribution of Age wrt to sport(only gold medals)')
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'overall')
    selected_sport=st.selectbox('select a sport',sport_list)
    temp_df=helper.weight(df,selected_sport)

    fig,ax=plt.subplots(figsize=(30,20))
    ax=sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.title('height vs weight')
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
