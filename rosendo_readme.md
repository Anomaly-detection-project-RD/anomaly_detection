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

Acquire
    
    build organization repository named Team BCR and invite members.
    acquired the dataset from MySql Server by creating a query that 
    joins the curriculum logs and cohorts on cohort_id.
    build env.py file to acquire the dataset from MySql server and a .gitignore to avoid sharing personal information
    use python environment of choice (recommend jupyter lab) and created a CSV
    original dataset contained 847,330 rows and 15 columns
Prepare
   
    BEFORE PREPARATION:
    
   
    AFTER PREPARATION:
    The following columns were dropped id, slack, deleted_at
    The 'path' column has 1 null value. the null was eventually dropped using drop.na
    The 'unnamed: 0' column has the most unique values (847330), which suggests that it might be an index column.
    The 'user_id' column has 911 unique values, which suggests that there are 911 unique users in the dataset.
    The 'cohort_id' and 'name' columns each have 47 unique values, which suggests that there are 47 unique cohorts in the dataset.
    The 'ip' column has 5200 unique values, which suggests that there are 5200 unique IP addresses in the dataset.
    after preparation dataset contained 

Explore

    Questions


# Prepare the data using the following columns:

- features:
- 1 - date
- 2 - time
- 3 - path
- 4 - user_id
- 5 - cohort_id
- 6 - ip
- 7 - name
- 8 - slack
- 9 - start_date
- 10 - end_date
- 11 - created_at
- 12 - updated_at
- 13 - deleted_at
- 14 - program_id

> Explore dataset for to answer eight questions, build a one slide with a summary and send an email pertaning information. 

#  Answer the following questions:

1. Which lesson appears to attract the most traffic consistently across cohorts (per program)?
2. Is there a cohort that referred to a lesson significantly more than other cohorts seemed to gloss over?
3. Are there students who, when active, hardly access the curriculum? If so, what information do you have about these students?
4. Is there any suspicious activity, such as users/machines/etc accessing the curriculum who shouldn’t be? Does it appear that any web-scraping is happening? Are there any suspicious IP addresses?
5. At some point in 2019, the ability for students and alumni to access both curriculums (web dev to ds, ds to web dev) should have been shut off. Do you see any evidence of that happening? Did it happen before?
6. What topics are grads continuing to reference after graduation and into their jobs (for each program)?
7. Which lessons are least accessed?
8. Anything else I should be aware of?


# Deliverables

    • a single email from your team sent to `datascience@codeup.com` answering the questions 
    • a single google slide that can be added into a presentation (attach to email)
    • a new github repository with .py files, final_notebook.ipynb, & readme (include link in email)
• 
# Data Dictionary

| Feature    | Definition                                                                                       |
|------------|--------------------------------------------------------------------------------------------------|
| unnamed: 0 | Unique identifier for each row                                                                   |
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
| program_id | A unique identifier for the program that the user is enrolled in. 1 = Full-Stack Web Dev - PHP,  | |            | 2 = Full-Stack Web Dev - Java, 3 = Data Science, and 4 = front-End Web Dev                       |


# Steps to Reproduce
Clone the repo git@github.com:Team-BCR/project3_wine.git in terminal
Use personal env.py to connect
Run notebook
Use final_report for findings


# REPO REPLICATION
In order to get started reproducing this project, you'll need to set up a proper environment.

a. use the query provided in side the final_project.ipynb to obtain the dataset from MySQL. 

b. use personal env.py to connect to MySQL. 

If you downloaded the file you may need to unzip the downloaded file to recover the american_bankruptcy.csv file.
Prep your repo:
• Create a new repository on GitHub to house this project.

• Clone it into your local machine by copying the SSH link from GitHub and running 'git clone <SSH link'> in your terminal.

Create a .gitignore file in your local repository and include any files you don't want to be tracked by Git or shared on the internet. This can include your newly downloaded .csv files. You can create and edit this file by running 'code .gitignore' in your terminal (if you're using Visual Studio Code as your text editor) if you open it from the terminal run 'open .gitignore'.
Create a README.md file to begin noting the steps taken so far. You can create and edit this file by running code README.md in your terminal.
Transfer your 'american_bankruptcy.csv' file into your newly established local repository.
Create a Jupyter Lab environment to continue working in. You can do this by running 'jupyter lab' in your terminal.
In Jupyter Lab, create a new Jupyter Notebook to begin the data pipeline.
Remember to regularly commit and push your changes to GitHub to ensure your work is saved and accessible from the remote repository.


# Takeaways and Conclusions




# Recommendations
Create wines that optimize the chemical properties as described above
i.e. the higher/lower values that correspond with higher quality scores
This will not guarantee a higher quality wine, but it should increase the probability of creating a higher quality wine



