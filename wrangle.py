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
    df.path = df.path.dropna()
    df.program_id = df.program_id.replace({1: 'full_stack_java_php'})

    df.program_id = df.program_id.replace({2: 'full_stack_java_java'})


    df.program_id = df.program_id.replace({3: 'datascience'})
    df.program_id = df.program_id.replace({4: 'front_end_web_dev'})
    return df 


def question_one(df):
    

    program_1 = df[df.program_id == 'full_stack_java_php']
    program_2 = df[df.program_id == 'full_stack_java_java']
    program_3 = df[df.program_id == 'datascience']
    program_4 = df[df.program_id == 'front_end_web_dev']

    the_list = [program_1, program_2, program_3, program_4]

    
    list_of_most_viewed_full_stack_java_php = []
    list_of_most_viewed_full_stack_java_java = []
    list_of_most_viewed_datascience = []
    list_of_most_viewed_front_end_web_dev = []


    for j in the_list:
        for i in list(set(j.cohort_id)):
            
            answer = j.groupby(by=["cohort_id", 'path']).count()
            answer = answer.reset_index()

            
            if j.program_id.unique()[0] == 'full_stack_java_php':
                answer = answer[answer.path.str.len() > 1]
                answer = answer[answer.path.str.contains('/')]
                answer = answer[answer.path.str.contains('.json') == False]
                answer = answer[answer.path != 'content/php_ii/command-line']
                answer = answer[answer.path != 'content/php_i']
                answer = answer[answer.path != 'html-css/elements']

                the_df = answer[['path', 'cohort_id', 'user_id']][answer.cohort_id == i].sort_values(by ='user_id').tail(1)
                if len(the_df.path.unique()) == 1:

                    list_of_most_viewed_full_stack_java_php.append(the_df.path.iloc[0])

            if j.program_id.unique()[0] == 'full_stack_java_java':
                answer = answer[answer.path.str.len() > 1]
                answer = answer[answer.path.str.contains('/')]
                answer = answer[answer.path.str.contains('.json') == False]
                answer = answer[answer.path != 'content/php_ii/command-line']
                answer = answer[answer.path != 'content/php_i']
                answer = answer[answer.path != 'html-css/elements']

                the_df = answer[['path', 'cohort_id', 'user_id']][answer.cohort_id == i].sort_values(by ='user_id').tail(1)
                if len(the_df.path.unique()) == 1:

                    list_of_most_viewed_full_stack_java_java.append(the_df.path.iloc[0])


            if j.program_id.unique()[0] == 'datascience':
                answer = answer[answer.path.str.len() > 1]
                answer = answer[answer.path.str.contains('/')]
                answer = answer[answer.path.str.contains('.json') == False]
                answer = answer[answer.path != 'content/php_ii/command-line']
                answer = answer[answer.path != 'content/php_i']
                answer = answer[answer.path != 'html-css/elements']

                the_df = answer[['path', 'cohort_id', 'user_id']][answer.cohort_id == i].sort_values(by ='user_id').tail(1)
                if len(the_df.path.unique()) == 1:

                    list_of_most_viewed_datascience.append(the_df.path.iloc[0])

            if j.program_id.unique()[0] == 'front_end_web_dev':
                answer = answer[answer.path.str.len() > 1]
                answer = answer[answer.path.str.contains('/')]
                answer = answer[answer.path.str.contains('.json') == False]
                answer = answer[answer.path != 'content/php_ii/command-line']
                answer = answer[answer.path != 'content/php_i']
                answer = answer[answer.path != 'html-css/elements']

                the_df = answer[['path', 'cohort_id', 'user_id']][answer.cohort_id == i].sort_values(by ='user_id').tail(1)
                if len(the_df.path.unique()) == 1:

                    list_of_most_viewed_front_end_web_dev.append(the_df.path.iloc[0])
                    
                    
    the_dict = {}
    program_names = ['full_stack_java_php','full_stack_java_java','datascience','front_end_web_dev']
    the_dict_of_answers = {}
    list_to_be_added = []
    top_df= pd.DataFrame()
    for iteration, list_of_most_viewed in enumerate([list_of_most_viewed_full_stack_java_php,
                                list_of_most_viewed_full_stack_java_java,
                                list_of_most_viewed_datascience,
                                list_of_most_viewed_front_end_web_dev
                                ]):
        for i in list_of_most_viewed:
            if i in the_dict:
                the_dict[i] += 1
            else:
                the_dict[i] = 1

        for key, values in the_dict.items():
            if the_dict[key] == max(the_dict.values()):
                list_to_be_added.append(key)

        the_dict_of_answers[program_names[iteration]] = list_to_be_added
        
        list_to_be_added = []

        the_dict = {}
    for key, values in the_dict_of_answers.items():
        the_df = pd.DataFrame({'program': str(key), "page":str(values)},  index=[0])
        
        top_df = pd.concat([top_df, the_df])

    return top_df



def question_two(df):
    program_1 = df[df.program_id == 'full_stack_java_php']
    program_2 = df[df.program_id == 'full_stack_java_java']
    program_3 = df[df.program_id == 'datascience']
    program_4 = df[df.program_id == 'front_end_web_dev']

    the_list = [program_1, program_2, program_3, program_4]

    
    top_df_full_stack_java_php = pd.DataFrame()
    top_df_full_stack_java_java = pd.DataFrame()
    top_df_datascience = pd.DataFrame()
    top_df_front_end_web_dev = pd.DataFrame()


    for j in the_list:
        for i in list(set(j.cohort_id)):
            
            answer = j.groupby(by=["cohort_id", 'path']).count()
            answer = answer.reset_index()
            

            
            if j.program_id.unique()[0] == 'full_stack_java_php':
                answer = answer[answer.path.str.len() > 1]
                answer = answer[answer.path.str.contains('/')]
                answer = answer[answer.path.str.contains('.json') == False]
                answer = answer[answer.path != 'content/php_ii/command-line']
                answer = answer[answer.path != 'content/php_i']
                answer = answer[answer.path != 'html-css/elements']
                
                the_df = answer[['path', 'cohort_id', 'user_id']][answer.cohort_id == i].sort_values(by ='user_id', ascending= False)
                
                if the_df.shape[0] > 0:
                    the_df[the_df.path == 'spring/fundamentals/repositories']
                    top_df_full_stack_java_php = pd.concat([top_df_full_stack_java_php, the_df[the_df.path == 'spring/fundamentals/repositories']]).sort_values(by='user_id', ascending= False)


            if j.program_id.unique()[0] == 'full_stack_java_java':
                answer = answer[answer.path.str.len() > 1]
                answer = answer[answer.path.str.contains('/')]
                answer = answer[answer.path.str.contains('.json') == False]
                answer = answer[answer.path != 'content/php_ii/command-line']
                answer = answer[answer.path != 'content/php_i']
                answer = answer[answer.path != 'html-css/elements']
                
                the_df = answer[['path', 'cohort_id', 'user_id']][answer.cohort_id == i].sort_values(by ='user_id', ascending= False)
                
                if the_df.shape[0] > 0:
                    the_df[the_df.path == 'jquery/ajax/weather-map']
                    top_df_full_stack_java_java = pd.concat([top_df_full_stack_java_java, the_df[the_df.path == 'jquery/ajax/weather-map']]).sort_values(by='user_id', ascending= False)


            if j.program_id.unique()[0] == 'datascience':
                answer = answer[answer.path.str.len() > 1]
                answer = answer[answer.path.str.contains('/')]
                answer = answer[answer.path.str.contains('.json') == False]
                answer = answer[answer.path != 'content/php_ii/command-line']
                answer = answer[answer.path != 'content/php_i']
                answer = answer[answer.path != 'html-css/elements']
                
                the_df = answer[['path', 'cohort_id', 'user_id']][answer.cohort_id == i].sort_values(by ='user_id', ascending= False)
                
                if the_df.shape[0] > 0:
                    the_df[the_df.path == 'classification/overview']
                    top_df_datascience = pd.concat([top_df_datascience, the_df[the_df.path == 'classification/overview']]).sort_values(by='user_id', ascending= False)


    top_df_full_stack_java_php['cohort'] = 'Lassen'
    top_df_full_stack_java_php['program'] = 'full_stack_java_php'

    top_df_full_stack_java_java['cohort'] = 'Staff'
    top_df_full_stack_java_java['program'] = 'full_stack_java_java'

    top_df_datascience['cohort'] = 'Darden'
    top_df_datascience['program'] = 'datascience'

    df_1 = top_df_full_stack_java_php
    df_2 = top_df_full_stack_java_java
    df_3 = top_df_datascience

    return pd.concat([df_1.head(1),df_2.head(1),df_3.head(1),])


def question_three(df):
    program_1 = df[df.program_id == 'full_stack_java_php']
    program_2 = df[df.program_id == 'full_stack_java_java']
    program_3 = df[df.program_id == 'datascience']
    program_4 = df[df.program_id == 'front_end_web_dev']


    the_list = [program_1, program_2, program_3, program_4]


    list_of_least_viewed_full_stack_java_php = []
    list_of_least_viewed_full_stack_java_java = []
    list_of_least_viewed_datascience = []
    list_of_least_viewed_front_end_web_dev = []
    the_dict_of_answers = {}
    list_to_be_added = []

    for j in the_list:
        for i in list(set(j.cohort_id)):
            
            answer = j.groupby(by=["cohort_id", 'path']).count()
            answer = answer.reset_index()
            answer.cohort_id.unique()

            
            if j.program_id.unique()[0] == 'full_stack_java_php':
                answer = answer[answer.path.str.len() > 1]
                answer = answer[answer.path.str.contains('/')]
                answer = answer[answer.path.str.contains('.json') == False]
                answer = answer[answer.path != 'content/php_ii/command-line']
                answer = answer[answer.path != 'content/php_i']
                answer = answer[answer.path != 'html-css/elements']

                the_df = answer[['path', 'cohort_id', 'user_id']][answer.cohort_id == i].sort_values(by ='user_id').head(1)

                if len(the_df.path.unique()) == 1:
                    list_of_least_viewed_full_stack_java_php.append(the_df.path.iloc[0])


            if j.program_id.unique()[0] == 'full_stack_java_java':
                answer = answer[answer.path.str.len() > 1]
                answer = answer[answer.path.str.contains('/')]
                answer = answer[answer.path.str.contains('.json') == False]
                answer = answer[answer.path != 'content/php_ii/command-line']
                answer = answer[answer.path != 'content/php_i']
                answer = answer[answer.path != 'html-css/elements']
                
                the_df = answer[['path', 'cohort_id', 'user_id']][answer.cohort_id == i].sort_values(by ='user_id').head(1)

                if len(the_df.path.unique()) == 1:
                    list_of_least_viewed_full_stack_java_java.append(the_df.path.iloc[0])

            
            if j.program_id.unique()[0] == 'datascience':
                answer = answer[answer.path.str.len() > 1]
                answer = answer[answer.path.str.contains('/')]
                answer = answer[answer.path.str.contains('.json') == False]
                answer = answer[answer.path != 'content/php_ii/command-line']
                answer = answer[answer.path != 'content/php_i']
                answer = answer[answer.path != 'html-css/elements']
                

                the_df = answer[['path', 'cohort_id', 'user_id']][answer.cohort_id == i].sort_values(by ='user_id').head(1)

                if len(the_df.path.unique()) == 1:
                    list_of_least_viewed_datascience.append(the_df.path.iloc[0])


            if j.program_id.unique()[0] == 'front_end_web_dev':
                answer = answer[answer.path.str.len() > 1]
                answer = answer[answer.path.str.contains('/')]
                answer = answer[answer.path.str.contains('.json') == False]
                answer = answer[answer.path != 'content/php_ii/command-line']
                answer = answer[answer.path != 'content/php_i']
                answer = answer[answer.path != 'html-css/elements']
                
                the_df = answer[['path', 'cohort_id', 'user_id']][answer.cohort_id == i].sort_values(by ='user_id').head(1)

                if len(the_df.path.unique()) == 1:
                    list_of_least_viewed_front_end_web_dev.append(the_df.path.iloc[0])
    

    the_dict = {}
    top_df = pd.DataFrame()
    program_names = ['full_stack_java_php','full_stack_java_java','datascience','front_end_web_dev']
    for iteration, list_of_least_viewed in enumerate([list_of_least_viewed_full_stack_java_php,
                                list_of_least_viewed_full_stack_java_java,
                                list_of_least_viewed_datascience,
                                list_of_least_viewed_front_end_web_dev
                                ]):
        for i in list_of_least_viewed:
            if i in the_dict:
                the_dict[i] += 1
            else:
                the_dict[i] = 1




        for key, values in the_dict.items():
            if the_dict[key] == max(the_dict.values()):
                list_to_be_added.append(key)

        the_dict_of_answers[program_names[iteration]] = list_to_be_added
        list_to_be_added = []

        the_dict = {}
    for key, values in the_dict_of_answers.items():
        the_df = pd.DataFrame({'program': str(key), "page":str(values)},  index=[0])
        top_df = pd.concat([top_df, the_df])

    return top_df