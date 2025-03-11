# fetch_tweets.py

import tweepy
import pandas as pd
import time
from config import TWITTER_BEARER_TOKEN  # Importer la clé Bearer depuis config.py

TIME_LIMIT_TWITTER_API = 15 * 60

# Fonction pour initialiser l'API Twitter avec la clé Bearer
def initialize_api():
    client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)
    return client

# Fonction pour récupérer les tweets
def fetch_tweets(query, max_results=100):
    client = initialize_api()

    # Requête pour récupérer les tweets récents
    try:
        response = client.search_recent_tweets(query=query, max_results=max_results, tweet_fields=["created_at", "text", "author_id"])

        # Extraire les données des tweets
        tweets_data = []
        for tweet in response.data:
            tweets_data.append({
                "id": tweet.id,
                "screen_name": tweet.author_id,
                "created_at": tweet.created_at,
                "full_text": tweet.text
            })

        df = pd.DataFrame(tweets_data)

        # Sauvegarder les tweets dans un fichier CSV
        df.to_csv('./filtered_tweets_engie1.csv', sep=';', index=False)
        print(f"Successfully fetched and saved {max_results} tweets.")

        # Ajouter un délai de 15 minutes entre les requêtes
        print("Délai de 15 minutes avant la prochaine requête.")
        time.sleep(TIME_LIMIT_TWITTER_API)  # Limite twitter de 15 minutes entre les requêtes

    except tweepy.errors.TooManyRequests as e:
        print("Erreur 429: Trop de requêtes. Attente de 15 minutes...")
        time.sleep(TIME_LIMIT_TWITTER_API)  # Attendre 15 minutes en cas de trop de requêtes
        fetch_tweets(query, max_results)
