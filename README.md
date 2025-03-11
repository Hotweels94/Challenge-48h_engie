# Challenge-48h_Engie

Challenge 48h by:
- Ait Atmane Samir
- Amrane Adam
- Wouhaibi Mahdi
- Gerard Lucas
- Amsellem-Bousignac Ryan

## How to Launch the Project
To run this project, follow these steps:
1. Clone or download this repository:
    ```bash
    git clone https://github.com/Hotweels94/Challenge-48h_engie.git
    ```
    
2. Navigate to the project directory:
    ```bash
    cd Challenge-48h_engie
    ```
    
3. Install the necessary dependencies:
    ```bash
    pip install pandas
    pip install streamlit
    pip install matplotlib
    pip install seaborn
    ```
    
4. After installation, run the main script:
    ```bash
    python python/main.py
    ```
    
5. For data visualization, run:
    ```bash
    streamlit run python/visualize_KPI.py
    ```

## Methodology Used for Processing Tweets
The tweet data goes through several important steps for cleaning and preparing it for analysis or automatic responses:
1. **Datetime Conversion**: The `created_at` column, which contains tweet timestamps, is converted to UTC datetime format using pandas. This ensures consistency across all timestamps for easier time-based analysis.

2. **Removing Irrelevant Columns**: Columns like `id`, `screen_name`, and `name` are dropped as they are not necessary for the analysis and may contain irrelevant or sensitive data.

3. **Text Cleaning**: The text data from the `full_text` column (the tweet content) is cleaned. This involves:
    - Removing emojis and non-ASCII characters.
    - Eliminating URLs (e.g., `http://` or `https://`) to focus on tweet content.
    - Converting all text to lowercase and replacing multiple spaces with a single space to standardize formatting.

4. **Removing Duplicates**: Any duplicate rows in the dataset are removed to ensure that each tweet is unique, preventing bias in analysis or model results.

These steps ensure that the tweet data is clean, consistent, and ready for further processing (sentiment analysis, response generation, etc.).

## KPIs Selected and Their Meaning
We calculated several KPIs to help us understand tweet patterns and user sentiment:
- **Tweets per day/week/month**: Helps detect activity peaks on specific dates.
- **Tweets containing predefined keywords**: Used to identify issues raised by users.
- **Frequency of mentions of Engie accounts**: Helps assess the relationship between Engie accounts and other companies.
- **Sentiment of the tweet**: Assesses whether the tweets are generally positive or negative.
- **Category of the problem**: Classifies the issue raised by the user (e.g., billing, outages).
- **Discomfort Score**: Measures the level of discomfort expressed by the user to prioritize urgent issues.

## Sentiment Analysis
### Approach Used for Sentiment Analysis
The sentiment analysis is based on Mistral AI, an advanced natural language processing (NLP) model. The approach follows these steps:
1. **Preprocessing**:
    - Loading the CSV file containing the tweets.
    - Verifying and creating necessary columns (sentiment, complaint category, discomfort score).
    - Cleaning the text (removing corrupted rows, ensuring UTF-8 encoding).

2. **Tweet Content Analysis**:
    - Sending each tweet to the Mistral API with a structured prompt to ensure the response is in a usable JSON format.
    - Extracting the returned information: sentiment, category, and discomfort score.
    - Updating the CSV file with new data.

3. **Post-Processing**:
    - Verifying the generated results.
    - Correcting misclassified tweets if necessary.
    - Generating statistics to analyze sentiment and complaint trends.

### AI Agent Creation
The AI agent is designed to analyze tweets based on a predefined framework. The logic for detecting complaint types works as follows:
- **Billing Issues**: Incorrect billing, unjustified charges.
- **Outages & Emergencies**: Gas/electricity outages, technical issues.
- **Customer Service Issues**: Difficulty contacting support.
- **App Problems**: Bugs, login issues.
- **Delays in Intervention**: Late repairs or interventions.
- **Other**: Complaints that do not fit into any specific category.

### Example of the Analysis Prompt:
To interact with Mistral AI, we use a structured prompt to get an analysis in JSON format:
```plaintext
"""
Tu es un expert en analyse des tweets clients d'Engie. Ton objectif est de déterminer : - Le **sentiment du tweet** (Positif, Neutre, Négatif) - La **catégorie de réclamation** (Parmi : "Problèmes de facturation", "Pannes et urgences", "Service client injoignable", "Problèmes avec l’application", "Délai d’intervention", "Autre") - Un **score d'inconfort** entre 0 et 100

STRICT RESPONSE FORMAT:
```json
{
"sentiment": "Positif" | "Neutre" | "Négatif", "categorie": "Problèmes de facturation" | "Pannes et urgences" | "Service client injoignable" | "Problèmes avec l’application" | "Délai d’intervention" | "Autre", "score_inconfort": (Un nombre entier entre 0 et 100)
}
```
**Tweet:** {tweet_text}
"""
```

This prompt ensures that the AI agent responds with structured and consistent JSON data for easy processing.

## Discomfort Score Calculation

The discomfort score is calculated based on specific keywords in the tweet:

```python
keyword_weights = {
    "panne": 90, "urgence": 95, "scandale": 85,
    "retard": 60, "facture": 70, "erreur": 65,
    "service client": 75, "bug": 50, "coupure": 85
}
```
---

