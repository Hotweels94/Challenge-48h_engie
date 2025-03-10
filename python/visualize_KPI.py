import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Fonction pour charger les fichiers CSV
def load_csv(filename):
    return pd.read_csv(f'./result_csv/{filename}.csv', sep=';')

# Fonction pour filtrer les faibles valeurs par jour
def filter_low_values_day(df, threshold=3):
    return df[df['Nombre de mentions'] > threshold] if 'Nombre de mentions' in df.columns else df[df.iloc[:, 1] > threshold]

# Fonction pour filtrer les faibles valeurs par semaine
def filter_low_values_week(df, threshold=15):
    return df[df['Nombre de mentions'] > threshold] if 'Nombre de mentions' in df.columns else df[df.iloc[:, 1] > threshold]

# Fonction pour créer un graphique en pie
def plot_pie(df, title):
    # Regroupe les faibles valeurs dans la catégorie "Autres"
    df['Compte'] = df['Compte'].apply(lambda x: x if df['Nombre de mentions'][df['Compte'] == x].sum() > 5 else 'Autres')
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

# Fonction pour créer des barres verticales avec toutes les valeurs
def plot_full_bar(df, title):
    fig, ax = plt.subplots(figsize=(12,6))
    ax.bar(df.iloc[:, 0], df.iloc[:, 1], color='lightgreen')
    ax.set_xlabel(title)
    ax.set_ylabel('Nombre de tweets')
    ax.set_xticklabels(df.iloc[:, 0], rotation=90)
    st.pyplot(fig)
    st.write(f'Graphique complet pour {title}')

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

# 1. Graphique mentions_count (Pie chart avec catégorie 'Autres')
st.subheader("Mentions des comptes Engie")
plot_pie(mentions_count_df, 'Mentions des comptes Engie')

# 2. Graphique tweets_per_day (Barres verticales, avec seuil pour exclure les faibles valeurs)
st.subheader("Tweets par jour")
tweets_per_day_filtered = filter_low_values_day(tweets_per_day_df)
plot_bar(tweets_per_day_filtered, 'Tweets par jour')

# 3. Graphique tweets_per_week (Barres verticales, avec seuil pour exclure les faibles valeurs)
st.subheader("Tweets par semaine")
tweets_per_week_filtered = filter_low_values_week(tweets_per_week_df)
plot_bar(tweets_per_week_filtered, 'Tweets par semaine')

# 4. Graphique tweets_per_month (Barres verticales avec toutes les valeurs)
st.subheader("Tweets par mois")
plot_full_bar(tweets_per_month_df, 'Tweets par mois')

# 5. Graphique tweets_per_day_keywords (Barres verticales)
st.subheader("Tweets avec mots-clés par jour")
plot_full_bar(tweets_per_day_keywords_df, 'Tweets avec mots-clés par jour')

# 6. Graphique tweets_per_week_keywords (Barres verticales)
st.subheader("Tweets avec mots-clés par semaine")
plot_full_bar(tweets_per_week_keywords_df, 'Tweets avec mots-clés par semaine')

# 7. Graphique tweets_per_month_keywords (Barres verticales)
st.subheader("Tweets avec mots-clés par mois")
plot_full_bar(tweets_per_month_keywords_df, 'Tweets avec mots-clés par mois')