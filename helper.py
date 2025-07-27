import  numpy as np

from data_loader import  get_athlete_df


def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    medal_tally['total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']
    medal_tally['Gold']=medal_tally['Gold'].astype(int)
    medal_tally['Silver'] = medal_tally['Silver'].astype(int)
    medal_tally['Bronze'] = medal_tally['Bronze'].astype(int)
    medal_tally['total'] = medal_tally['total'].astype(int)
    return medal_tally

def country_year(df):
    years=df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'overall')
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'overall')
    return years, country

def fetch_medal_tally(df,year,country):
    medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag=0
    if year=='overall' and country=='overall':
        temp_df=medal_df
    if year=='overall' and country!='overall':
        flag=1
        temp_df=medal_df[medal_df['region']==country]
    if year!='overall' and country=='overall':
        temp_df=medal_df[medal_df['Year']==int(year)]

    if year!='overall' and country!='overall':
        temp_df=medal_df[(medal_df['Year']==int(year)) & (medal_df['region']==country)]
    if flag==1:
        x=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

    x['total']=x['Gold']+x['Silver']+x['Bronze']
    x['Gold'] = x['Gold'].astype(int)
    x['Silver'] = x['Silver'].astype(int)
    x['Bronze'] =x['Bronze'].astype(int)
    x['total'] =x['total'].astype(int)
    return  x


def time(df,col):
    nation = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nation.rename(columns={'Year': 'Edition', 'count': col}, inplace=True)
    return nation

def most(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    athlete_medal_count = temp_df['Name'].value_counts().reset_index()
    athlete_medal_count.columns = ['Name', 'Medal count']

    merged_df = athlete_medal_count.merge(df, on='Name', how='left')

    merged_df = merged_df[['Name', 'Medal count', 'Sport', 'region']].drop_duplicates('Name')

    return merged_df.head(15)


def year_medal_count(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df=new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df



def event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt=new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt


def success(df,country):
    temp_df = df.dropna(subset=['Medal'])
    if country!= 'overall':
        temp_df = temp_df[temp_df['region'] == country]

    athlete_medal_count = temp_df['Name'].value_counts().reset_index()
    athlete_medal_count.columns = ['Name', 'Medal count']

    merged_df = athlete_medal_count.merge(df, on='Name', how='left')

    merged_df = merged_df[['Name', 'Medal count', 'Sport', 'region']].drop_duplicates('Name')

    return merged_df.head(15)



def weight(df,sport):
    athlete_df=df.drop_duplicates(subset=['Name','region'])
    athlete_df['Medal'].fillna('no medal',inplace=True)
    temp_df = athlete_df[athlete_df['Sport'] == sport]
    return temp_df

def men_vs_women(df):
    athlete_df=df.drop_duplicates(subset=['Name','region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
