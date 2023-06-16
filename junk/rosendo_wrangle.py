import pandas as pd
import numpy as np
import os

# visualized your data
import matplotlib.pyplot as plt
import seaborn as sns



'''
*------------------*
|                  |
|     ACQUIRE      |
|                  |
*------------------*
'''
# # ----------------------------------------------------------------------------------
    
# # ----------------------------------------------------------------------------------


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

'''
*------------------*
|                  |
|     PREPARE      |
|                  |
*------------------*
'''
# ----------------------------------------------------------------------------------
def prep_data(df):
    # set all the columns names to a lowercase
    df.columns = df.columns.str.lower()

    # replace all the nulls with a zero
    df = df.replace(np.nan,0)
    
    # change the status label from string to int
    df['status_label'] = df['status_label'].map({'alive': 1, 'failed': 0})
    
    # rename columns
    df.columns
    df = df.rename(columns={'x1':'current_assets', 'x2':'cost_of_goods_sold',
                         'x3':'depreciation_and_amortization','x4':'ebitda',
                         'x5':'inventory','x6':'net_income',
                         'x7':'total_receivables','x8':'market_value',
                         'x9':'net_sales', 'x10':'total_assets',
                         'x11':'total_long_term_debt','x12':'ebit',
                         'x13':'gross_profit','x14':'total_current_liabilities',
                         'x15':'retained_earnings','x16':'total_revenue',
                         'x17':'total_liabilities','x18':'total_operating_expenses'})
    
    # strips the leading and trailing spaces from the column names
    df.columns = df.columns.str.strip()
    
    # Define quartiles
    Q1 = df['total_assets'].quantile(0.25)
    Q3 = df['total_assets'].quantile(0.75)

    # Create a new variable 'total_assets_size'
    df['total_assets_size'] = ['low_assets' if x < Q1 else 'high_assets' if x >= Q3 else 'medium_assets' for x in df['total_assets']]

    return df

# ----------------------------------------------------------------------------------
def nulls_by_col(df):
    """
    This function will:
        - take in a dataframe
        - assign a variable to a Series of total row nulls for ea/column
        - assign a variable to find the percent of rows w/nulls
        - output a df of the two variables.
    """
    num_missing = df.isnull().sum()
    pct_miss = (num_missing / df.shape[0]) * 100
    cols_missing = pd.DataFrame({
                    'num_rows_missing': num_missing,
                    'percent_rows_missing': pct_miss
                    })
    
    return  cols_missing


# ----------------------------------------------------------------------------------
def remove_columns(df, cols_to_remove):
    """
    This function will:
    - take in a df and list of columns (you need to create a list of columns that you would like to drop under the name 'cols_to_remove')
    - drop the listed columns
    - return the new df
    """
    df = df.drop(columns=cols_to_remove)
    
    return df

# ----------------------------------------------------------------------------------
# remove all outliers put each feature one at a time
def outlier(df, feature, m=2):
    '''
    outlier will take in a dataframe's feature:
    - calculate it's 1st & 3rd quartiles,
    - use their difference to calculate the IQR
    - then apply to calculate upper and lower bounds
    - using the `m` multiplier
    '''
    q1 = df[feature].quantile(.25)
    q3 = df[feature].quantile(.75)
    
    iqr = q3 - q1
    
    multiplier = m
    upper_bound = q3 + (multiplier * iqr)
    lower_bound = q1 - (multiplier * iqr)
    
    return upper_bound, lower_bound

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
    pages_one_user = df['endpoint'].resample('d').count()
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
def find_anomalies(df, user, span, k, plot=False):a
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
# -----------------------------End of Anomalies-------------------------------------

# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------
   

# ----------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------   


# ----------------------------------------------------------------------------------