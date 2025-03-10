import pandas as pd
import numpy as np
import decimal
import re

path = "../filtered_tweets_engie.csv"

def load_data(path):
    df = pd.read_csv(path, sep=';')
    print(f"Données chargées avec {df.shape[0]} lignes et {df.shape[1]} colonnes.")
    return df

def clean_data(df):
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce', utc=True)
    
    df = df.drop(columns=['id','screen_name', 'name'], axis=1)
    

    def clean_text(text):
        text = re.sub(r'[^\x00-\x7F]+', '', text)  # Enlève les emojis

        text = re.sub(r"[^a-zA-Z0-9âîïûüÿÀÂÎÏÔÛÙÜŸŒ'’\s]", '', text)
        text = re.sub(r'\bhttps\S*', '', text)

        text = text.lower()
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    # Appliquer le nettoyage sur la colonne 'full_text'
    df['full_text'] = df['full_text'].apply(lambda x: clean_text(str(x)) if pd.notnull(x) else x)
    
    # Suppression des doublons
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"Suppression des doublons : {before - after} lignes supprimées.")
    
    return df

def count_keywords(text, keywords):
    # Compter le nombre de mots-clés dans le texte
    count = sum(kw.lower() in text.lower() for kw in keywords)  # Insensible à la casse
    return count


# Extraction d'informations utiles
def extract_features(df, keywords):

    df['hour_of_publication'] = df['created_at'].dt.hour  # Heure de publication
    df['text_length'] = df['full_text'].astype(str).apply(len)  # Longueur du texte
    df['contains_keywords'] = df['full_text'].apply(lambda x: count_keywords(str(x), keywords))  # Nombre de mots-clés présents
    
    return df   



# Exécution du script
if __name__ == "__main__":
    file_path = path
    keywords = ["délai", "panne", "urgence", "scandale", "facture", "service", "bug", "erreur", "problème", "soucis", "coupure", "technique", "arrêt", "dysfonctionnement", "bugs", "paiement", "attente", "devis", "relance", "résilier"]  
    
    df = load_data(file_path)
    df = clean_data(df)
    df = extract_features(df, keywords)

    print(df.head())

    df.to_csv("cleaned_data1.csv", sep=';', index=False)