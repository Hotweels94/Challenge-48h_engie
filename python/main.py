# main.py

import threading
import os
import pandas as pd
from fetch_tweets import fetch_tweets  # Importer la fonction fetch_tweets depuis fetch_tweets.py
from data_loader import load_data
from text_cleaner import clean_dataframe
from feature_generator import generate_features
from calculateKPI import calculateKPI
from analyze_tweets import analyze

def fetch_tweets_in_background():
    # Lancer la récupération des tweets en arrière-plan
    fetch_tweets("ENGIEpartFR")  # Recherche "ENGIEpartFR" par ton mot-clé de recherche

def main():
    file_path = "./filtered_tweets_engie.csv"
    new_data_path = "./filtered_tweets_engie1.csv"
    result_path = "./result_csv/cleaned_data.csv"

    # Lancer la récupération des tweets en parallèle
    tweet_thread = threading.Thread(target=fetch_tweets_in_background)
    tweet_thread.start()

    # Vérifier si le fichier résultat existe déjà
    if os.path.exists(result_path):
        print(f"📂 Chargement du fichier existant : {result_path}")
        df = pd.read_csv(result_path, sep=';', encoding='utf-8')
    else:
        print(f"📂 Création du fichier nettoyé...")

        # Charger les anciennes et nouvelles données
        df_existing = pd.read_csv(file_path, sep=';', encoding='utf-8')
        df_new = pd.read_csv(new_data_path, sep=';', encoding='utf-8')

        # Fusionner les données
        df = pd.concat([df_existing, df_new], ignore_index=True)

        # Nettoyer et traiter les données (ajuste les fonctions selon tes besoins)
        df = clean_dataframe(df)
        df = generate_features(df)
        df.to_csv(result_path, sep=';', index=False)

    # Analyser les tweets
    analyze()

    # Calculer les KPI
    calculateKPI()

    # Attendre que le thread fetch_tweets termine
    tweet_thread.join()

if __name__ == "__main__":
    main()
