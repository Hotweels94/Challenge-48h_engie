import requests
import pandas as pd
import time
import json
import os
from config import MISTRAL_API_KEY, MISTRAL_API_URL

# Paramètres d'optimisation
DEBUG = True
SAVE_INTERVAL = 5  # Nombre de tweets après lesquels on sauvegarde le fichier

def analyze():
    if not MISTRAL_API_KEY:
        print("❌ ERREUR : La clé API Mistral n'est pas définie ! Vérifie `config.py`.")
        exit()

    print("✅ Configuration chargée, démarrage de l'analyse des tweets...")

    # 📂 Charger les tweets
    file_path = "./result_csv/cleaned_data.csv"
    try:
        df = pd.read_csv(file_path, sep=";", encoding="utf-8", on_bad_lines="skip", dtype={"score_inconfort": "Int64"})
        print(f"📊 Nombre de tweets détectés : {len(df)}")
    except Exception as e:
        print(f"❌ ERREUR : Impossible de lire le fichier CSV : {e}")
        exit()

    # 📌 Vérifier et ajouter les colonnes manquantes
    for col in ["sentiment", "categorie_reclamation", "score_inconfort"]:
        if col not in df.columns:
            df[col] = "" if col != "score_inconfort" else 0

    def analyze_tweet(tweet_text):
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }

        prompt = f"""
        Tu es un expert en analyse des tweets clients d'Engie.
        Ton objectif est de déterminer :
        - Le **sentiment du tweet** (Positif, Neutre, Négatif)
        - La **catégorie de réclamation** (Parmi : "Problèmes de facturation", "Pannes et urgences", "Service client injoignable", "Problèmes avec l’application", "Délai d’intervention", "Autre")
        - Un **score d'inconfort** entre 0 et 100

        📌 **FORMAT STRICT DE LA RÉPONSE :**
        ```json
        {{
            "sentiment": "Positif" | "Neutre" | "Négatif",
            "categorie": "Problèmes de facturation" | "Pannes et urgences" | "Service client injoignable" | "Problèmes avec l’application" | "Délai d’intervention" | "Autre",
            "score_inconfort": (Un nombre entier entre 0 et 100)
        }}
        ```

        **Réponds UNIQUEMENT avec ce JSON valide et rien d'autre.**

        ✉️ **Tweet :** {tweet_text}
        """

        payload = {
            "model": "mistral-medium",
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            response = requests.post(MISTRAL_API_URL, json=payload, headers=headers)

            if response.status_code != 200:
                if DEBUG:
                    print(f"❌ ERREUR API : {response.status_code}, {response.text}")
                return "Erreur", "Autre", 50

            response_data = json.loads(response.text)
            choices = response_data.get("choices", [])
            if not choices:
                return "Erreur", "Autre", 50

            model_response = choices[0].get("message", {}).get("content", "").strip()

            if model_response.startswith("```json") and model_response.endswith("```"):
                model_response = model_response[7:-3].strip()

            json_response = json.loads(model_response)
            return json_response.get("sentiment", "Neutre"), json_response.get("categorie", "Autre"), json_response.get("score_inconfort", 50)

        except Exception as e:
            if DEBUG:
                print(f"❌ ERREUR API Mistral : {e}")
            return "Erreur", "Autre", 50

    print("🚀 Début de l'analyse des tweets...")

    results = []
    try:
        for index, row in df.iterrows():
            if (
                pd.isna(row["sentiment"]) or row["sentiment"] == "" or row["sentiment"] == "Erreur" or
                pd.isna(row["categorie_reclamation"]) or row["categorie_reclamation"] == "" or row["categorie_reclamation"] == "Autre" or
                pd.isna(row["score_inconfort"]) or row["score_inconfort"] == 0 or row["score_inconfort"] == 50
            ):
                if DEBUG:
                    print(f"📨 Analyse du tweet {index + 1}/{len(df)} : {row['full_text'][:50]}...")

                sentiment, category, discomfort_score = analyze_tweet(row["full_text"])
                results.append((index, sentiment, category, discomfort_score))

                # Sauvegarde intermédiaire tous les N tweets
                if len(results) >= SAVE_INTERVAL:
                    for idx, sent, cat, score in results:
                        df.at[idx, "sentiment"] = sent
                        df.at[idx, "categorie_reclamation"] = cat
                        df.at[idx, "score_inconfort"] = score
                    df.to_csv(file_path, sep=";", index=False)
                    results = []  # Réinitialiser les résultats
                    print("💾 Sauvegarde intermédiaire effectuée.")

                time.sleep(4)  # Pause pour éviter surcharge API

        # Dernière sauvegarde après la boucle
        if results:
            for idx, sent, cat, score in results:
                df.at[idx, "sentiment"] = sent
                df.at[idx, "categorie_reclamation"] = cat
                df.at[idx, "score_inconfort"] = score
            df.to_csv(file_path, sep=";", index=False)
            print("💾 Sauvegarde finale effectuée.")

        print("✅ Analyse terminée, résultats enregistrés dans le fichier CSV.")

    except Exception as e:
        print(f"❌ ERREUR INATTENDUE : {e}")

