# standard imports
import pandas as pd
import numpy as np


# visualized your data
import matplotlib.pyplot as plt
import seaborn as sns

# my imports
from env import get_db_url
import os


'''
*------------------*
|                  |
|     ACQUIRE      |
|                  |
*------------------*
'''
# ----------------------------------------------------------------------------------
def check_file_exists(fn, query, url):
    """
    This function will:
    - check if file exists in my local directory, if not, pull from sql db
    - read the given `query`
    - return dataframe
    """
    if os.path.isfile(fn):
        print('csv file found and loaded')
        return pd.read_csv(fn, index_col=0)
    else: 
        print('creating df and exporting csv')
        df = pd.read_sql(query, url)
        df.to_csv(fn)
        return df
    
# ----------------------------------------------------------------------------------
def get_logs_data():
    """
    This function will:
        - from the connection made to the `curriculum_logs` DB
            - using the `get_db_url` from my wrangle module.
    """
    # How to import a database from MySQL
    url = get_db_url('curriculum_logs')

    query = """
    SELECT * 
    FROM curriculum_logs.logs as l 
    JOIN curriculum_logs.cohorts as c ON c.id = l.cohort_id;
    """

    filename = 'logs.csv'
    df = check_file_exists(filename, query, url)

    df = pd.read_sql(query, url)
    
    return df

# ----------------------------------------------------------------------------------
'''
*------------------*
|                  |
|     SUMMARY      |
|                  |
*------------------*
'''
# ----------------------------------------------------------------------------------
# a function that show a summary of the dataset
def data_summary(df):
    # Print the shape of the DataFrame
    print(f'data shape: {df.shape}')
    # set all the columns names to a lowercase
    df.columns = df.columns.str.lower()
    # Create a summary DataFrame
    summary = pd.DataFrame(df.dtypes, columns=['data type'])
    # Calculate the number of missing values
    summary['#missing'] = df.isnull().sum().values 
    # Calculate the percentage of missing values
    summary['%missing'] = df.isnull().sum().values / len(df)* 100
    # Calculate the number of unique values
    summary['#unique'] = df.nunique().values
    # Create a descriptive DataFrame
    desc = pd.DataFrame(df.describe(include='all').transpose())
    # Add the minimum, maximum, and first three values to the summary DataFrame
    summary['count'] = desc['count'].values
    summary['mean'] = desc['mean'].values
    summary['std'] = desc['std'].values
    summary['min'] = desc['min'].values
    summary['25%'] = desc['25%'].values
    summary['50%'] = desc['50%'].values
    summary['75%'] = desc['75%'].values
    summary['max'] = desc['max'].values
    summary['first_value'] = df.loc[0].values
    summary['second_value'] = df.loc[1].values
    summary['third_value'] = df.loc[2].values
    
    # Return the summary DataFrame
    return summary

# ----------------------------------------------------------------------------------
'''
*------------------*
|                  |
|     PREPARE      |
|                  |
*------------------*
'''
# ----------------------------------------------------------------------------------
def remove_columns(df, col_to_remove):
    """
    This function will:
    - take in a df and list of columns (you need to create a list of columns that you would like to drop under the name 'cols_to_remove')
    - drop the listed columns
    - return the new df
    """
    df = df.drop(columns=col_to_remove)
    
    return df

# ----------------------------------------------------------------------------------
def handle_missing_values(df, prop_required_columns=0.5, prop_required_rows=0.75):
    """
    This function will:
    - take in: 
        - a dataframe
        - column threshold (defaulted to 0.5)
        - row threshold (defaulted to 0.75)
    - calculates the minimum number of non-missing values required for each column/row to be retained
    - drops columns/rows with a high proportion of missing values.
    - returns the new df
    """
    column_threshold = int(round(prop_required_columns * len(df.index), 0))
    df = df.dropna(axis=1, thresh=column_threshold)
    
    row_threshold = int(round(prop_required_rows * len(df.columns), 0))
    df = df.dropna(axis=0, thresh=row_threshold)
    
    return df

# ----------------------------------------------------------------------------------
def data_prep(df, col_to_remove, prop_required_columns=0.5, prop_required_rows=0.75):
    """
    This function will:
    - take in: 
        - a dataframe
        - list of columns
        - column threshold (defaulted to 0.5)
        - row threshold (defaulted to 0.75)
    - removes unwanted columns
    - remove rows and columns that contain a high proportion of missing values
    - returns cleaned df
    """
    df = remove_columns(df, col_to_remove)
    df = handle_missing_values(df, prop_required_columns, prop_required_rows)
    
    # converts int to datetime
    df.date = pd.to_datetime(df.date)
    
    # rename columns
    df.columns
    df = df.rename(columns={'name':'cohort_name'})   
    
    # rename the numbers for names
    df.program_id = df.program_id.replace({1: 'full_stack_java_php', 2: 'full_stack_java_java', 3: 'datascience', 4: 'front_end_web_dev'})
    return df


# ----------------------------------------------------------------------------------
'''
*------------------*
|                  |
|    Question 1    |
|                  |
*------------------*
'''
# ----------------------------------------------------------------------------------
# Define a function to find the most accessed lesson per program
def most_accessed_lesson(df):
    """
    This function takes in a DataFrame and returns a DataFrame with the most accessed lesson per program.
    """
    # Group by 'program_id' and 'path', count the number of occurrences, and reset the index
    most_accessed = df.groupby(['program_id', 'path']).size().reset_index(name='count')

    # Find the most accessed lesson for each program
    most_accessed = most_accessed.loc[most_accessed.groupby('program_id')['count'].idxmax()]

    return most_accessed
# ----------------------------------------------------------------------------------


'''
*------------------*
|                  |
|    Question 2    |
|                  |
*------------------*
'''
# ----------------------------------------------------------------------------------
# Define a function to find the lesson that a cohort referred to significantly more than other cohorts
def most_referred_lesson(df):
    """
    This function takes in a DataFrame and returns a DataFrame with the lesson that a cohort referred to significantly more than other cohorts.
    """
    # Group by 'cohort_id' and 'path', count the number of occurrences, and reset the index
    most_referred = df.groupby(['cohort_id', 'path']).size().reset_index(name='count')

    # Find the most referred lesson for each cohort
    most_referred = most_referred.loc[most_referred.groupby('cohort_id')['count'].idxmax()]

    return most_referred   

# ----------------------------------------------------------------------------------


'''
*------------------*
|                  |
|    Question 3    |
|                  |
*------------------*
'''
# ----------------------------------------------------------------------------------   
# Define a function to find students who, when active, hardly access the curriculum
def less_active_students(df):
    """
    This function takes in a DataFrame and returns a DataFrame with students who, when active, hardly access the curriculum.
    """
    # Group by 'user_id', count the number of occurrences, and reset the index
    user_activity = df.groupby('user_id').size().reset_index(name='count')

    # Find students who accessed the curriculum less than a certain threshold
    # Here, the threshold is set to 10, but it can be adjusted as needed
    less_active = (user_activity[user_activity['count'] < 10]).sort_values(by='count',ascending=True)

    return less_active

# ----------------------------------------------------------------------------------

'''
*------------------*
|                  |
|    Question 4    |
|                  |
*------------------*
'''
# ---------------------------------------------------------------------------------- 
# Define a function to find suspicious activity
def find_suspicious_activity(df):
    """
    This function takes in a DataFrame and returns a DataFrame with suspicious activity, such as users/machines/etc accessing the curriculum who shouldn’t be.
    """
    # Group by 'user_id', count the number of occurrences, and reset the index
    user_activity = df.groupby('user_id').size().reset_index(name='count')

    # Find users who accessed the curriculum more than a certain threshold
    # Here, the threshold is set to 10000, but it can be adjusted as needed
    suspicious_activity = user_activity[user_activity['count'] > 10000]

    return suspicious_activity

# ---------------------------------------------------------------------------------- 
# -----------------------------The start of Anomalies-------------------------------
def one_user_df_prep(df, user):
    """
    Prepares a DataFrame for a specific user by filtering the data, converting the 
    'date' column to datetime, and setting it as the index. The DataFrame is then 
    sorted by the index, and the 'endpoint' column is resampled by day and counted.

    Parameters:
        df (pd.DataFrame): The original DataFrame, which should include a 'user_id' 
                           and a 'date' column.
        user (int or str): The user ID to filter the DataFrame by.

    Returns:
        pages_one_user (pd.Series): A Series where the index is the date and the 
                                    value is the count of 'endpoint' for that day.
    """
    df = df[df.user_id == user].copy()
    df.date = pd.to_datetime(df.date)
    df = df.set_index(df.date)
    df = df.sort_index()
    pages_one_user = df['path'].resample('d').count()
    return pages_one_user

# ----------------------------------------------------------------------------------
def compute_pct_b(pages_one_user, span, k, user):
    """
    Computes the Exponential Moving Average (EMA), upper band, lower band, and 
    percentage bandwidth (%b) for a given user's page visits over a specified span 
    of time. The EMA, upper band, and lower band are calculated using a specified 
    number of standard deviations.

    Parameters:
        pages_one_user (pd.Series): A Series where the index is the date and the 
                                    value is the count of 'endpoint' for that day.
        span (int): The span of the window for the EMA calculation, representing 
                    the number of time periods (e.g., 7 for a week, 30 for a month).
        k (int): The number of standard deviations to use when calculating the 
                 upper and lower bands.
        user (int or str): The user ID to be added to the resulting DataFrame.

    Returns:
        my_df (pd.DataFrame): A DataFrame containing the original page visit data, 
                              the EMA (midband), the upper and lower bands (ub and lb), 
                              the %b value (pct_b), and the user ID.
    """
    midband = pages_one_user.ewm(span=span).mean()
    stdev = pages_one_user.ewm(span=span).std()
    ub = midband + stdev*k
    lb = midband - stdev*k
    
    my_df = pd.concat([pages_one_user, midband, ub, lb], axis=1)
    my_df.columns = ['pages_one_user', 'midband', 'ub', 'lb']
    
    my_df['pct_b'] = (my_df['pages_one_user'] - my_df['lb'])/(my_df['ub'] - my_df['lb'])
    my_df['user_id'] = user
    return my_df

# ----------------------------------------------------------------------------------
def plot_bands(my_df, user):
    """
    Plots the number of pages visited by a user, the Exponential Moving Average (EMA or midband), 
    and the upper and lower bands over time. 

    Parameters:
        my_df (pd.DataFrame): A DataFrame containing the original page visit data, 
                              the EMA (midband), the upper and lower bounds (ub and lb), 
                              the %b value (pct_b), and the user ID.
        user (int or str): The user ID to be used in the plot's label.

    Returns:
        None. Displays a plot with the number of pages, EMA/midband, upper band, and lower band 
        over time for the specified user.
    """
    fig, ax = plt.subplots(figsize=(12,8))
    ax.plot(my_df.index, my_df.pages_one_user, label='Number of Pages, User: '+str(user))
    ax.plot(my_df.index, my_df.midband, label = 'EMA/midband')
    ax.plot(my_df.index, my_df.ub, label = 'Upper Band')
    ax.plot(my_df.index, my_df.lb, label = 'Lower Band')
    ax.legend(loc='best')
    ax.set_ylabel('Number of Pages')
    plt.show()

# ----------------------------------------------------------------------------------
def find_anomalies(df, user, span, k, plot=False):
    """
    Finds anomalies in the number of pages visited by a user over a specified span 
    of time. An anomaly is defined as a value that is above the upper band, which 
    is calculated using the Exponential Moving Average (EMA or midband) and a 
    specified number of standard deviations.

    Parameters:
        df (pd.DataFrame): The original DataFrame, which should include a 'user_id' 
                           and a 'date' column.
        user (int or str): The user ID to filter the DataFrame by.
        span (int): The span of the window for the EMA calculation, representing 
                    the number of time periods (e.g., 7 for a week, 30 for a month).
        k (int): The number of standard deviations to use when calculating the 
                      upper and lower bounds.
        plot (bool, optional): Whether to display a plot of the number of pages, 
                               EMA/midband, upper band, and lower band over time 
                               for the specified user. Defaults to False.

    Returns:
        my_df (pd.DataFrame): A DataFrame containing the original page visit data, 
                              the EMA (midband), the upper and lower bounds (ub and lb), 
                              the %b value (pct_b), and the user ID. Only rows where 
                              pct_b > 1 (indicating an anomaly) are included. If no 
                              anomalies are found, the DataFrame will be empty.
    """

    pages_one_user = one_user_df_prep(df, user)
    
    my_df = compute_pct_b(pages_one_user, span, k, user)
    
    if plot:
        plot_bands(my_df, user)
    
    return my_df[my_df.pct_b>1]

# ----------------------------------------------------------------------------------
def find_all_anomalies(df, span, k):
    """
    Finds anomalies for all users in the provided DataFrame over a specified span 
    of time. An anomaly is defined as a value that is above the upper band, which 
    is calculated using the Exponential Moving Average (EMA or midband) and a 
    specified number of standard deviations.

    Parameters:
        df (pd.DataFrame): The original DataFrame, which should include a 'user_id' 
                           and a 'date' column.
        span (int): The span of the window for the EMA calculation, representing 
                    the number of time periods (e.g., 7 for a week, 30 for a month).
        k (int): The number of standard deviations to use when calculating the 
                 upper and lower bounds.

    Returns:
        anomalies (pd.DataFrame): A DataFrame containing the anomalies for all users. 
                                   Each row includes the original page visit data, 
                                   the EMA (midband), the upper and lower bounds (ub and lb), 
                                   the %b value (pct_b), and the user ID. Only rows where 
                                   pct_b > 1 (indicating an anomaly) are included. If no 
                                   anomalies are found for a user, no rows for that user 
                                   will be included in the DataFrame.
    """
    anomalies = pd.DataFrame()

    for u in df.user_id.unique():
        one_user = find_anomalies(df, u, span, k)
        anomalies = pd.concat([anomalies, one_user])

    return anomalies

# ----------------------------------------------------------------------------------
# Define a function to calculate count
def count(df, column):
    return df[column].value_counts()

# ----------------------------------------------------------------------------------
# Define a function to calculate frequency
def frequency(df, column):
    """
    This function takes in a DataFrame and a column.
    Returns a DataFrame with the frequency of each item in the column.
    """
    return df[column].value_counts(normalize=True)*100

# ----------------------------------------------------------------------------------
# Define a function to visualize count
def visualize_count(df, column):
    """
    This function takes in a DataFrame and a column.
    Returns a horizontal bar plot with the frequency of each item in the column.
    """
    df[column].value_counts().sort_values().plot(kind='barh')
# -----------------------------End of Anomalies-------------------------------------


'''
*------------------*
|                  |
|    Question 5    |
|                  |
*------------------*
'''
# ----------------------------------------------------------------------------------
# Define a function to find evidence of students and alumni accessing both curriculums (web dev to ds, ds to web dev)
def find_cross_access(df):
    """
    This function takes in a DataFrame and returns a DataFrame with evidence of students and alumni accessing both curriculums (web dev to ds, ds to web dev).
    """
    # Filter the DataFrame to include only records from 2019 onwards
    df_2019_onwards = df[df['date'] >= '2019-01-01']

    # Group by 'user_id' and 'program_id', count the number of occurrences, and reset the index
    user_program_activity = df_2019_onwards.groupby(['user_id', 'program_id']).size().reset_index(name='count')

    # Find users who accessed more than one program
    cross_access = user_program_activity[user_program_activity['user_id'].duplicated(keep=False)]

    return cross_access

# ---------------------------------------------------------------------------------- 


'''
*------------------*
|                  |
|    Question 6    |
|                  |
*------------------*
'''
# ----------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------


'''
*------------------*
|                  |
|    Question 7    |
|                  |
*------------------*
'''
# ----------------------------------------------------------------------------------
# Define a function to find the least accessed lessons
def find_least_accessed_lessons(df):
    """
    This function takes in a DataFrame and returns a DataFrame with the least accessed lessons.
    """
    # Group by 'path', count the number of occurrences, and reset the index
    lesson_access_counts = df.groupby('path').size().reset_index(name='count')

    # Sort the DataFrame by 'count' in ascending order
    least_accessed_lessons = lesson_access_counts.sort_values('count')

    return least_accessed_lessons

# ----------------------------------------------------------------------------------


'''
*------------------*
|                  |
|    Question 8    |
|                  |
*------------------*
'''
# ----------------------------------------------------------------------------------