import threading
import os
import pandas as pd
import time
import tweepy
from fetch_tweets import fetch_tweets
from data_loader import load_data
from text_cleaner import clean_dataframe
from feature_generator import generate_features
from calculateKPI import calculateKPI
from analyze_tweets import analyze

def wait_and_retry():
    print("Erreur 429: Trop de requêtes. Attente de 15 minutes...")
    time.sleep(15 * 60)  # Attendre 15 minutes
    print("Reprise après 15 minutes.")
    fetch_tweets("ENGIEpartFR")  # Relancer la récupération des tweets

def fetch_tweets_in_background():
    fetch_tweets("ENGIEpartFR")

def analyze_in_background():
    # Lancer l'analyse des tweets en arrière-plan
    try:
        analyze()  # Fonction d'analyse des tweets
    except tweepy.errors.TooManyRequests as e:
        wait_and_retry()  # Attendre et relancer en cas de limite d'API

# Fonction pour mettre à jour le fichier cleaned_data.csv avec de nouvelles données
def update_cleaned_data():
    file_path = "./filtered_tweets_engie1.csv"
    result_path = "./result_csv/cleaned_data.csv"

    # Charger les nouvelles données
    if os.path.exists(file_path):
        try:
            new_data = pd.read_csv(file_path, sep=';', encoding='utf-8')
            print(f"📥 Nouvelles données récupérées de {file_path}.")
        except pd.errors.EmptyDataError:
            print(f"⚠️ Le fichier {file_path} est vide ou mal formé.")
            return
        except Exception as e:
            print(f"❌ Erreur lors de la lecture du fichier {file_path} : {e}")
            return
    else:
        print("Le fichier de tweets n'existe pas.")
        return

    # Charger les anciennes données si elles existent
    if os.path.exists(result_path):
        df_cleaned = pd.read_csv(result_path, sep=';', encoding='utf-8')
        print(f"📂 Chargement des anciennes données de {result_path}.")
    else:
        print(f"Le fichier {result_path} n'existe pas, il va être créé.")
        df_cleaned = pd.DataFrame()

    # Nettoyer les nouvelles données
    new_data_cleaned = clean_dataframe(new_data)

    # Vérification avant concaténation
    print(f"Anciennes données : {df_cleaned.shape[0]} lignes.")
    print(f"Nouvelles données nettoyées : {new_data_cleaned.shape[0]} lignes.")

    # Ajouter les nouvelles données nettoyées au DataFrame existant
    df_combined = pd.concat([df_cleaned, new_data_cleaned], ignore_index=True)

    # Supprimer les doublons en utilisant la colonne 'id'
    df_combined = df_combined.drop_duplicates(subset=['id'])

    # Vérification après suppression des doublons
    print(f"Nombre de lignes après suppression des doublons : {df_combined.shape[0]}.")

    # Sauvegarder les données nettoyées dans le fichier CSV
    df_combined.to_csv(result_path, sep=';', index=False)
    print(f"✅ Les nouvelles données ont été ajoutées au fichier {result_path}")


def main():
    result_path = "./result_csv/cleaned_data.csv"
    file_path = "./filtered_tweets_engie1.csv"

    # Vérifier si le fichier de résultats existe déjà
    if os.path.exists(result_path):
        print(f"📂 Chargement du fichier existant : {result_path}")
        df = pd.read_csv(result_path, sep=';', encoding='utf-8')
    else:
        print(f"📂 Création du fichier nettoyé...")
        # Charger les données à partir de filtered_tweets_engie1.csv
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, sep=';', encoding='utf-8')
        else:
            # Si le fichier n'existe pas, on crée un DataFrame vide
            df = pd.DataFrame()

        # Nettoyer et traiter les données (ajustez les fonctions selon vos besoins)
        df = clean_dataframe(df)
        df = generate_features(df)
        df.to_csv(result_path, sep=';', index=False)

    # Lancer la récupération des tweets en parallèle
    tweet_thread = threading.Thread(target=fetch_tweets, args=("(@ENGIEpartFR OR @ENGIEpartSAV) -is:retweet lang:fr",))
    tweet_thread.start()

    # Lancer l'analyse des tweets en parallèle
    analysis_thread = threading.Thread(target=analyze_in_background)
    analysis_thread.start()

    # Mettre à jour le fichier cleaned_data.csv avec de nouvelles données (ajouter les tweets récents)
    update_cleaned_data()

    # Calculer les KPI
    calculateKPI()

    # Attendre que le thread fetch_tweets termine
    tweet_thread.join()

    # Attendre que le thread analyse termine
    analysis_thread.join()

if __name__ == "__main__":
    main()