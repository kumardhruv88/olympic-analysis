import pandas as pd


def preprocess(df,region_df):

    df=df[df['Season']=='Summer']
    df=df.merge(region_df,how='left',on='NOC')
    df.drop_duplicates(inplace=True)
    df=pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
    return df