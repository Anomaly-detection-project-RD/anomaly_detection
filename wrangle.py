import pandas as pd
import env


def acquire_logs(user=env.user, password=env.password, host=env.host):
    '''
    This function gathers curriculum_logs data from the 
    SQL codeup database and returns the information in a 
    pandas dataframe
    '''
    url = f'mysql+pymysql://{env.user}:{env.password}@{env.host}/curriculum_logs'
    query = '''
    select * from cohorts;
    '''
    df = pd.read_sql(query, url)
    df.to_csv('cohorts.csv')


def get_data():
    df = pd.read_csv('anonymized-curriculum-access.txt', sep=" ")
    df_2 = pd.read_csv('cohorts.csv')
    df_2 = df_2.drop(columns ='Unnamed: 0')
    df.loc[len(df.index)] = ['2018-01-26', '09:55:03', '/', 1, 8 , '97.105.19.61']
    df.columns = ['date', 'time', 'path', 'user_id', 'cohort_id', 'ip']

    df = df.merge(df_2, left_on='cohort_id', right_on='id', how='left')


    df = df.drop(columns = 'id')
    df = df.drop(columns = 'deleted_at')
    df = df.drop(columns = 'slack')
    df['date'] = pd.to_datetime( df['date'])
    df['start_date'] = pd.to_datetime( df['start_date'])
    df['end_date'] = pd.to_datetime( df['end_date'])
    df['created_at'] = pd.to_datetime( df['created_at'])
    df['updated_at'] = pd.to_datetime( df['updated_at'])
    return df 

