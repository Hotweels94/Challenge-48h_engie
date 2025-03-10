# Challenge-48h_Engie

Challenge 48h made by : Ait Atmane Samir / Amrane Adam / Wouhaibi Mahdi / Gerard Lucas / Amsellem--Bousignac Ryan

## How to launch the project : 

First, you have to clone or download this repository. 
Next you will need to install depedencies : 
``` pip install pandas ```
``` pip install streamlit ```
``` pip install matplotlib ```
``` pip install seaborn ```
After you need to type in your terminal where you clone / download the project : ```python python/main.py```
To have the visualization you need to type : ```streamlit run python\visualize_KPI.py```

## Methodology used for processing tweets

In this project, the tweet data is processed through several key steps to ensure the data is clean and ready for analysis or generating responses. 1-The first step involves converting the created_at column, which contains the tweet timestamps, into UTC datetime format using pandas. This ensures consistency across all timestamps, making it easier to work with the data for time-based analysis.

2-Next, irrelevant columns such as id, screen_name, and name are dropped from the dataset. These columns are not necessary for the analysis and could contain sensitive or unnecessary information that does not contribute to the purpose of the analysis.

3-The third step focuses on cleaning the text data in the full_text column, which contains the actual tweet content. Several transformations are applied here. Emojis and non-ASCII characters are removed to avoid any unwanted symbols that may interfere with text processing. URLs (e.g., http:// or https://) are also removed to focus solely on the content of the tweet. Additionally, the text is converted to lowercase, and multiple spaces are replaced with a single space to standardize the formatting. These cleaning steps are crucial for ensuring that the text is in a consistent format for further analysis.

4-Finally, any duplicate rows are removed from the dataset to ensure that each tweet is unique, preventing potential bias in the analysis or model results. This is done by identifying and removing exact duplicates from the data.

Overall, these steps help ensure that the tweet data is cleaned, consistent, and ready for further processing( sentiment analysis, generating responses).

## The KPIs selected and their meaning

We have several KPIs: 
- Tweets by day, week, and month, to detect the various dates where we record activity
- Tweets by day, week, and month containing keywords that we have defined to understand the problem of the tweet, to detect the problems perceived by users by date.
- The frequency of mentions of Twitter accounts, to make links between Engie accounts and other companies, to see if there are problems with other companies.
- The sentiment of the tweet, to know if the tweets are rather positive or negative.
- The problem category.
- The discomfort score to prioritize the user's discomfort.

