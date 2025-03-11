import tweepy
import pandas as pd
import time
import os
import re
from config import TWITTER_BEARER_TOKEN  # Importer la clé Bearer depuis config.py

TIME_LIMIT_TWITTER_API = 15 * 60  # 15 minutes

# Fonction pour initialiser l'API Twitter avec la clé Bearer
def initialize_api():
    client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)
    return client

# Fonction pour nettoyer le texte des tweets
def clean_tweet_text(text):
    # Nettoyer le texte des retours à la ligne et autres caractères indésirables
    text = text.replace("\n", " ").replace("\r", " ")  # Remplacer les retours à la ligne par un espace
    text = re.sub(r'\s+', ' ', text)  # Remplacer plusieurs espaces par un seul
    text = text.strip()  # Enlever les espaces de début et fin
    return text

# Fonction pour récupérer les tweets avec gestion de réessais
def fetch_tweets(query, max_results=100, retries=3):
    client = initialize_api()

    attempt = 0
    while attempt < retries:
        try:
            response = client.search_recent_tweets(query=query, max_results=max_results, tweet_fields=["created_at", "text", "author_id"])

            # Extraire les données des tweets
            tweets_data = []
            for tweet in response.data:
                # Nettoyer le texte du tweet
                clean_text = clean_tweet_text(tweet.text)

                # Récupérer les informations de l'utilisateur (nom complet) via author_id
                user = client.get_user(id=tweet.author_id)
                user_name = user.data.name  # Récupérer le nom de l'utilisateur

                tweets_data.append({
                    "id": tweet.id,
                    "screen_name": tweet.author_id,
                    "name": user_name,
                    "created_at": tweet.created_at,
                    "full_text": clean_text
                })

            df_new = pd.DataFrame(tweets_data)

            # Vérifier si le fichier existant existe
            file_path = './filtered_tweets_engie1.csv'
            if os.path.exists(file_path):
                df_existing = pd.read_csv(file_path, sep=';', encoding='utf-8')
                # Fusionner les anciennes données avec les nouvelles
                df = pd.concat([df_existing, df_new], ignore_index=True)
            else:
                # Si le fichier n'existe pas, on crée un nouveau DataFrame
                df = df_new

            # Sauvegarder la fusion des tweets dans filtered_tweets_engie.csv
            df.to_csv(file_path, sep=';', index=False)
            print(f"Successfully fetched and saved {len(df_new)} tweets.")

            # Ajouter un délai de 15 minutes entre les requêtes
            print("Délai de 15 minutes avant la prochaine requête.")
            time.sleep(TIME_LIMIT_TWITTER_API)  # Limite Twitter de 15 minutes entre les requêtes

            return  # Sortir de la fonction si la récupération est réussie

        except tweepy.errors.TooManyRequests as e:
            print(f"Erreur 429: Trop de requêtes. Tentative {attempt + 1} sur {retries}...")
            attempt += 1
            if attempt < retries:
                print("Nouvelle tentative dans 15 minutes...")
                time.sleep(TIME_LIMIT_TWITTER_API)  # Attendre 15 minutes avant la prochaine tentative
            else:
                print("Limite d'essais atteinte, arrêt de la récupération.")
                break
