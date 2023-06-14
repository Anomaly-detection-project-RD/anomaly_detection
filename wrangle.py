import pandas as pd
import env


def get_data():
    df = pd.read_csv('anonymized-curriculum-access.txt', sep=" ")
    df_2 = pd.read_csv('cohorts.csv')
    df_2 = df_2.drop(columns ='Unnamed: 0')
    df.loc[len(df.index)] = ['2018-01-26', '09:55:03', '/', 1, 8 , '97.105.19.61']
    df.columns = ['date', 'time', 'path', 'user_id', 'cohort_id', 'ip']

    df = df.merge(df_2, left_on='user_id', right_on='id')
    return df 

