# data_loader.py

def get_athlete_df(df):
    athlete_df = df.dropna(subset=['Name', 'region'])
    return athlete_df
