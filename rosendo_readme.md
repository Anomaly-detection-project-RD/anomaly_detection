# Project Description
As a data science consultant Team BCR will find the drivers of wine quality for the California Wine Institute. We will find clusters within the data for exploration, understanding and modeling to present to the data science team for winery supply chain marketing. The project will culminate in a presentation to the data science team.

# Project Goals
Discover features/clusters helpful in predicting wine quality

Use features to develop a machine learning model to predict the quality of wine on a scale of 1-10

Other key drivers:

Is alcohol associated with quality?
Is chlorides associated with quality?
Is residual_sugar associated with quality?
Is alcohol associated with density?

# Initial Thoughts
There are some key indicators in the data that may predict the 'quality' of wine and that those indicators will be evident by the conclusion of the project.
The Plan
Acquire: build organization repository named Team BCR and invite members. Pull winequality-red.csv and winequality-white.csv from data.world into repository. Build .gitignore and env.py files.

# Prepare the data using the following columns:

> target: 12 - quality (score between 0 and 10)
- features:
- 1 - fixed acidity
- 2 - volatile acidity
- 3 - citric acid
- 4 - residual sugar
- 5 - chlorides
- 6 - free sulfur dioxide
- 7 - total sulfur dioxide
- 8 - density
- 9 - pH
- 10 - sulphates
- 11 - alcohol

> Explore dataset for predictors of wine 'quality'

> Answer the following questions:

Is alcohol associated with quality?
Is chlorides associated with quality?
Is residual_sugar associated with quality?
Is alcohol associated with density?


# Develop a model

Using the selected data features develop appropriate predictive models
Evaluate the models in action using train and validate splits as well as scaled data
Choose the most accurate model
Consider several clusters to enhance the chosen model
Evaluate the most accurate model using the final test data set
# Draw conclusions

# Data Dictionary
Feature	Definition (measurement)
Fixed Acidity	The fixed amount of tartaric acid. (g/L)
Volatile Acidity	A wine's acetic acid; (High Volatility = High Vinegar-like smell). (g/L)
Citric Acid	The amount of citric acid; (Raises acidity, Lowers shelf-life). (g/L)
Residual Sugar	Leftover sugars after fermentation. (g/L)
Chlorides	Increases sodium levels; (Affects color, clarity, flavor, aroma). (g/L)
Free Sulfur Dioxide	Related to pH. Determines how much SO2 is available. (Increases shelf-life, decreases palatability). (mg/L)
Total Sulfur Dioxide	Summation of free and bound SO2. (Limited to 350ppm: 0-150, low-processed, 150+ highly processed). (mg/L)
Density	Between 1.08 and 1.09. (Insight into fermentation process of yeast growth). (g/L)
pH	2.5: more acidic - 4.5: less acidic (range)
Sulphates	Added to stop fermentation (Preservative) (g/L)
Alcohol	Related to Residual Sugars. By-product of fermentation process (vol%)
Quality	Score assigned between 0 and 10; 0=low, 10=best

# Steps to Reproduce
Clone the repo git@github.com:Team-BCR/project3_wine.git in terminal
Use personal env.py to connect
Run notebook
Use final_report for findings



# Takeaways and Conclusions




# Recommendations
Create wines that optimize the chemical properties as described above
i.e. the higher/lower values that correspond with higher quality scores
This will not guarantee a higher quality wine, but it should increase the probability of creating a higher quality wine

# Citation
P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis. Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems, Elsevier, 47(4):547-553. ISSN: 0167-9236.


1. Which lesson appears to attract the most traffic consistently across cohorts (per program)?
- Skip this question for right now as we don't have enough information to verify. 

2. Is there a cohort that referred to a lesson significantly more than other cohorts seemed to gloss over?
cohort_id groupby are 3,207
1,334 are null values (missing info)

3. Are there students who, when active, hardly access the curriculum? If so, what information do you have about these students?


4. Is there any suspicious activity, such as users/machines/etc accessing the curriculum who shouldn’t be? Does it appear that any web-scraping is happening? Are there any suspicious IP addresses?


5. At some point in 2019, the ability for students and alumni to access both curriculums (web dev to ds, ds to web dev) should have been shut off. Do you see any evidence of that happening? Did it happen before?


6. What topics are grads continuing to reference after graduation and into their jobs (for each program)?


7. Which lessons are least accessed?


8. Anything else I should be aware of?