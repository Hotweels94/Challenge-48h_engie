import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from nltk.corpus import stopwords
from collections import Counter
import nltk

nltk.download('stopwords')

# Fonction pour charger les fichiers CSV
def load_csv(filename):
    return pd.read_csv(f'./result_csv/{filename}.csv', sep=';')

# Fonction pour filtrer les faibles valeurs par jour
def filter_low_values_day(df, threshold=3):
    return df[df['Nombre de mentions'] > threshold] if 'Nombre de mentions' in df.columns else df[df.iloc[:, 1] > threshold]

# Fonction pour filtrer les faibles valeurs par semaine
def filter_low_values_week(df, threshold=10):
    return df[df['Nombre de mentions'] > threshold] if 'Nombre de mentions' in df.columns else df[df.iloc[:, 1] > threshold]

# Fonction pour créer un graphique en pie
def plot_pie(df, title):
    df['Compte'] = df['Compte'].apply(lambda x: x if df['Nombre de mentions'][df['Compte'] == x].sum() > 10 else 'Autres')
    grouped = df.groupby('Compte')['Nombre de mentions'].sum().reset_index()

    fig, ax = plt.subplots()
    ax.pie(grouped['Nombre de mentions'], labels=grouped['Compte'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)
    st.write(f'Graphique pie pour {title}')

# Fonction pour créer des barres verticales
def plot_bar(df, title):
    fig, ax = plt.subplots()
    ax.bar(df.iloc[:, 0], df.iloc[:, 1], color='skyblue')
    ax.set_xlabel(title)
    ax.set_ylabel('Nombre de tweets')
    ax.set_xticklabels(df.iloc[:, 0], rotation=90)
    st.pyplot(fig)
    st.write(f'Graphique de barres pour {title}')

# Fonction pour créer un pie chart pour les catégories de réclamations
def plot_category_pie(df):
    category_counts = df['categorie_reclamation'].value_counts()
    fig, ax = plt.subplots()
    category_counts = category_counts[~category_counts.index.isin(['Autres', 'Autre'])]
    ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)
    st.write('Répartition des catégories de réclamation')

# Fonction pour créer un diagramme en barres pour le score d'inconfort
def plot_inconfort_bar(df):
    df_filtered = df[~df['categorie_reclamation'].isin(['Autres', 'Autre'])]
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=df_filtered['categorie_reclamation'], y=df_filtered['score_inconfort'], ax=ax, palette='coolwarm')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_ylabel("Score d'inconfort")
    st.pyplot(fig)
    st.write("Scores d'inconfort par catégorie de réclamation")

# Fonction pour créer un pie chart pour les sentiments
def plot_sentiment_pie(df):
    sentiment_counts = df['sentiment'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)
    st.write('Répartition des sentiments')

# Fonction pour créer un nuage de mots
def plot_wordcloud(tweets_data):
    if not tweets_data.empty and 'full_text' in tweets_data.columns:
        # Définition des stopwords
        stop_words = set(stopwords.words('french'))

        custom_stopwords = stop_words.union({
            "engiepartfr", "engiegroup", "engiepartsav",
            "plus", "a", "ca", "c'est", "fait", "faire", "sans", "bonjour", "c’est", "va",
            "meme", "dire", "j'ai", "ete", "avoir", "donc", "peut", "alors", "bien",
            "encore", "voir", "vraiment", "trop", "tout", "juste", "aucun",
            "comme", "car", "non", "seul", "avant", "si", "entre", "cela",
            "cette", "rien", "jamais", "aucune", "doit", "quel", "n'est", "est", "suis",
            "ni", "tous", "déjà", "chaque", "autre"
        })

        # Fusionner tous tweets en une seule chaîne de texte
        text = " ".join(tweet for tweet in tweets_data['full_text'].dropna())

        # Filtrer les mots en supprimant les stopwords
        filtered_words = [word.lower() for word in text.split() if word.lower() not in custom_stopwords]

        # Générer le nuage de mots
        wordcloud = WordCloud(stopwords=custom_stopwords, background_color='white',
                              width=800, height=400).generate(" ".join(filtered_words))

        # Afficher le nuage de mots
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Nuage de Mots des Tweets')
        st.pyplot(plt)

    else:
        st.warning("Aucune donnée de tweet disponible pour générer le nuage de mots.")

# Interface Streamlit
st.title("Visualisation des KPIs")

# Charger les CSV
mentions_count_df = load_csv('mentions_count')
tweets_per_day_df = load_csv('tweets_per_day')
tweets_per_week_df = load_csv('tweets_per_week')
tweets_per_month_df = load_csv('tweets_per_month')
tweets_per_day_keywords_df = load_csv('tweets_per_day_keywords')
tweets_per_week_keywords_df = load_csv('tweets_per_week_keywords')
tweets_per_month_keywords_df = load_csv('tweets_per_month_keywords')
ai_analyze_df = load_csv('cleaned_data')

# Regrouper les catégories "Problèmes avec l'application"
ai_analyze_df['categorie_reclamation'] = ai_analyze_df['categorie_reclamation'].replace(["Problèmes avec l’application", "Problèmes avec l'application"], "Problèmes avec l'application")

# Filtrer les erreurs
ai_analyze_df = ai_analyze_df[ai_analyze_df['sentiment'] != 'Erreur']

# Graphiques existants
st.subheader("Mentions des comptes Engie")
plot_pie(mentions_count_df, 'Mentions des comptes Engie')

st.subheader("Tweets par jour")
tweets_per_day_filtered = filter_low_values_day(tweets_per_day_df)
plot_bar(tweets_per_day_filtered, 'Tweets par jour')

st.subheader("Tweets par semaine")
tweets_per_week_filtered = filter_low_values_week(tweets_per_week_df)
plot_bar(tweets_per_week_filtered, 'Tweets par semaine')

st.subheader("Tweets par mois")
plot_bar(tweets_per_month_df, 'Tweets par mois')

st.subheader("Tweets avec mots-clés par semaine")
tweets_per_week_keywords_filtered = filter_low_values_day(tweets_per_week_keywords_df)
plot_bar(tweets_per_week_keywords_filtered, 'Tweets avec mots-clés par semaine')

st.subheader("Tweets avec mots-clés par mois")
plot_bar(tweets_per_month_keywords_df, 'Tweets avec mots-clés par mois')

# Nouveaux Graphiques pour l'analyse des réclamations
st.subheader("Analyse des réclamations")
plot_category_pie(ai_analyze_df)
plot_inconfort_bar(ai_analyze_df)
plot_sentiment_pie(ai_analyze_df)

st.subheader("Nuage de mots des tweets")
plot_wordcloud(ai_analyze_df)
