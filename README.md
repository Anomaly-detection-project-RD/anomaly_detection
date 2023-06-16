# Project Description
This project involves analyzing user activity data from Codeup web logs to gain insights into user behavior and curriculum usage. The data includes information about the lessons accessed, the cohorts to which users belong, the times of access, and other related details. The analysis will focus on identifying patterns and anomalies in the data that can answer specific questions about user engagement, curriculum relevance, and potential security issues.

# Project Goals
The goal of the project is to provide answers to at least 5 of the 7 questions below before the board meeting on Friday morning:

1. Which lesson consistently attracts the most traffic across cohorts (per program)?
2. Is there a cohort that referred to a lesson significantly more than other cohorts seemed to gloss over?
3. Are there students who, when active, hardly access the curriculum? If so, what information do you have about these students?
4. Is there any suspicious activity, such as users/machines/etc accessing the curriculum who shouldn’t be? Does it appear that any web-scraping is happening? Are there any suspicious IP addresses?
5. At some point in 2019, the ability for students and alumni to access both curriculums (web dev to ds, ds to web dev) should have been shut off. Do you see any evidence of that happening? Did it happen before?
6. What topics are grads continuing to reference after graduation and into their jobs (for each program)?
7. Which lessons are least accessed?
8. Any other important insights that weren't specifically asked for but are worth noting.

In addition to answering these questions, the project also involves creating a summary slide that can be incorporated into an existing presentation to highlight the most important points from the analysis.


# Initial Thoughts
The dataset provides a comprehensive log of user activity on an online learning platform, including details such as date, time, user ID, cohort ID, accessed path, and IP address. This information can be leveraged to track user engagement, identify popular or less accessed lessons, and observe patterns at the cohort or program level. However, the presence of missing values, particularly in the 'path' column, necessitates careful data cleaning and preparation. The dataset also offers opportunities for feature engineering, such as combining 'date' and 'time' for a more granular time series analysis. Furthermore, the data may contain potential anomalies or suspicious activities that warrant further investigation. Overall, the dataset presents a rich resource for deriving insights into user behavior and curriculum usage, albeit requiring thoughtful preprocessing and analysis.



# The Plan

## Acquire
    
- Build organization repository named anomoly_detection and invite members.  
- Acquired the dataset from MySql Server by creating a query that 
joins the curriculum logs and cohorts on cohort_id.  
- Build env.py file to acquire the dataset from MySql server and a .gitignore to avoid sharing personal information.   
- Use python environment of choice (recommend jupyter lab) and created a CSV file.
- Original dataset contained 847,330 rows and 15 columns.
## Prepare

- The following columns were dropped id, slack, deleted_at
- The 'path' column has 1 null value. the null was eventually dropped using drop.na
- The 'unnamed: 0' column has the most unique values (847330), which suggests that it might be an index column.
- The 'user_id' column has 911 unique values, which suggests that there are 911 unique users in the dataset.
- The 'cohort_id' and 'name' columns each have 47 unique values, which suggests that there are 47 unique cohorts in the dataset.
- The 'ip' column has 5200 unique values, which suggests that there are 5200 unique IP addresses in the dataset.
    after preparation dataset contained

## Explore
 
Answer the following questions:

1. Which lesson appears to attract the most traffic consistently across cohorts (per program)?

    Full Stack PHP: content/html-css and content/laravel/intro
    Full Stack JAVA: mysql/tables
    Data Science: 1-fundamentals/modern-data-scientist.jpg, classification/scale_features_or_not.svg, fundamentals/modern-data-scientist.jpg, 6-regression/1-overview, classification/overview
    Front_End Web Dev: content/html-css

    Based on our analysis, we found a need to evaluate file path names further to ensure that they correspond to specific lessons. 

2. Is there a cohort that referred to a lesson significantly more than other cohorts seemed to gloss over?   
        Full Stack PHP: Cohort 14 - spring/fundamentals/repositories
        Full Stack JAVA: Cohort 28 - jquery/ajax/weather-map
        Data Science: Cohort 59 - classification/overview
        Front End Web Dev: only had one cohort   
        On a positive note, we also found that the above lessons within the program categories consistently attract significant attention.

3. Are there students who, when active, hardly access the curriculum? If so, what information do you have about these students?
    13 users visit the curriculum 1 time
    4 users visited the curriculum 2 times
    5 users visit the curriculum 3 times
    4 users visit the curriculum 4 times
    5 users visit the curriculum 5 times
    2 users visited the curriculum 6 times
    1 user visited the curriculum 7 times
    3 users visited the curriculum 8 times
    2 users visit the curriculum 9 times. 


    There is nothing that stands out for each of these students.

4. Is there any suspicious activity, such as users/machines/etc accessing the curriculum who shouldn’t be? Does it appear that any web-scraping is happening? Are there any suspicious IP addresses?   
    Three users (User 11, 53, 64) stand out with several occurrences greater than 1000 counts. These users are staff members who have been with the company since day one. We found no evidence of web scraping, and the top 5 IP addresses investigated showed no suspicious activity. 

5. At some point in 2019, the ability for students and alumni to access both curriculums (web dev to ds, ds to web dev) should have been shut off. Do you see any evidence of that happening? Did it happen before?    

    Our investigation revealed that only staff members could access both curriculums. Students didn't have access to both curriculums, with the exception of user_id# 143, who has access to both the Data Sciences and Full Stack Java curriculums.

6. What topics are grads continuing to reference after graduation and into their jobs (for each program)?
 - This question was explored due to time constrains. 

7. Which lessons are least accessed?    
    Lastly, we identified lessons that have been least accessed by specific cohorts, which provides an opportunity to reevaluate the content delivery or consider additional measures to increase engagement in these particular lessons.

    Front_End_Web_Dev: content/html-css/gitbook/images/favicon.ico
    Data Science: %20https://github.com/RaulCPena
    Full Stack_JAVA: content/loops.html
    Full Stack_PHP: content/loops.html

8. Anything else I should be aware of?
 - No additional information was found. 


# Deliverables

- a single email from your team sent to `datascience@codeup.com` answering the questions   
- a single google slide that can be added into a presentation (attach to email)    
- a new github repository with .py files, final_notebook.ipynb, & readme (include link in email)   

# Data Dictionary

| Feature    | Definition                                                                                       |
|------------|--------------------------------------------------------------------------------------------------|
| date       | Date when a particular event or record occurred                                                  |
| time       | Time when a particular event or record occurred                                                  |
| path       | Portion of the URL path for the Codeup website                                                   |
| user_id    | Unique identifier for each user                                                                  |
| cohort_id  | Unique identifier for each cohort (group of users)                                               |
| ip         | IP address of the user or the server that generated the record                                   |
| name       | Name of cohort                                                                                   |
| start_date | Start date of a particular event, such as the start of a user's membership or a cohort's program |
| end_date   | End date of a particular event, such as the end of a user's membership or a cohort's program     |
| created_at | The date and time when the record was created                                                    |
| updated_at | The date and time when the record was last updated                                               |
| program_id | A unique identifier for the program that the user is enrolled in. 1 = Full-Stack Web Dev - PHP,  |
|            | 2 = Full-Stack Web Dev - Java, 3 = Data Science, and 4 = front-End Web Dev                       |



# REPO REPLICATION
In order to get started reproducing this project, you'll need to set up a proper environment.

a. use the query provided in side the final_project.ipynb to obtain the dataset from MySQL. 

b. use personal env.py to connect to MySQL. 

Prep your repo:
• Clone it into your local machine by copying the SSH link from GitHub and running 'git clone <SSH link'> in your terminal.

• Create a Jupyter Lab environment to continue working in. You can do this by running 'jupyter lab' in your terminal.


# Conclusions

• We found some information but based on our analysis, we found a need to evaluate file path names further to ensure that they correspond to specific lessons.

• There is suspicious activity, such as users/machines/etc accessing the curriculum who shouldn’t be. 

• We can infer that certain lessons within the Full_stack_php, Full_stack_java, Datascience, and Front_end_web_dev categories are consistently popular or require more attention. 

• Students Hardly Accessing Curriculum: User 11 accessed the curriculum 17,913 times, while users 53 and 64 accessed it 12,329 and 16,322 times, respectively.

• Suspicious Activity: User 11 accessed the curriculum 17,913 times, while users 53 and 64 accessed it 12,329 and 16,322 times, respectively, indicating potential unauthorized access.

• Cross-Program Access: Users 37 and 53 accessed both Full_stack_php, Full_stack_java, indicating engagement across multiple curriculums.

• Least Accessed Lessons: Cohort-specific analysis highlights specific lessons that have been least accessed by certain cohorts.




# Recommendations and Next Steps

Based on the analysis, provide recommendations and next steps.

This could include:

• Monitoring the IP addresses identified as anomalies for potential security threats.
• Investigating the reasons for users accessing the curriculum less than a certain threshold. This could indicate issues with user engagement or potential technical problems.
• If there are frequent errors (like 404 errors), investigate the cause and fix the issues.
• If there are peak times of website access, ensure that the server can handle the load during these times

