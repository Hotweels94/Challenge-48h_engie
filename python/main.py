import os
import pandas as pd
from data_loader import load_data
from text_cleaner import clean_dataframe
from feature_generator import generate_features
from calculateKPI import calculateKPI
from analyze_tweets import analyze

def main():
    file_path = "./filtered_tweets_engie.csv"
    result_path = "./result_csv/cleaned_data.csv"

    # Vérifier si le fichier résultat existe déjà
    if os.path.exists(result_path):
        print(f"Le fichier {result_path} existe déjà. Chargement du fichier existant...")
        df = pd.read_csv(result_path, sep=';', encoding='utf-8')
    else:
        print(f"Le fichier {result_path} n'existe pas. Création d'un nouveau fichier...")
        df = load_data(file_path)
        df = clean_dataframe(df)
        df = generate_features(df)

        # Sauvegarder le DataFrame nettoyé avant d'analyser
        df.to_csv(result_path, sep=';', index=False)

    # Analyser les tweets
    analyze()

    # Calculer les KPI après l'analyse
    calculateKPI()

if __name__ == "__main__":
    main()
