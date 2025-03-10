import requests
import pandas as pd
import time
import json
import os
from config import MISTRAL_API_KEY, MISTRAL_API_URL

def analyze():
    # 📌 Vérifier si la clé API est bien chargée
    if not MISTRAL_API_KEY:
        print("❌ ERREUR : La clé API Mistral n'est pas définie ! Vérifie `config.py`.")
        exit()

    print(f"🔍 Clé API chargée : {MISTRAL_API_KEY[:10]}... (masquée)")
    print("✅ Configuration chargée, démarrage de l'analyse des tweets...")

    # 📌 Charger les tweets depuis le fichier CSV
    file_path = "./result_csv/cleaned_data.csv"
    print(f"📂 Chargement du fichier : {file_path}")

    try:
        df = pd.read_csv(file_path, sep=";", encoding="utf-8", on_bad_lines="skip")
        print(f"📊 Nombre de tweets détectés : {len(df)}")
        print(f"📝 Colonnes détectées : {list(df.columns)}")
    except Exception as e:
        print(f"❌ ERREUR : Impossible de lire le fichier CSV : {e}")
        exit()

    # 📌 Vérifier que la colonne "full_text" existe
    if "full_text" not in df.columns:
        print("❌ Erreur : La colonne 'full_text' n'existe pas dans le fichier CSV.")
        print(f"Colonnes disponibles : {df.columns}")
        exit()

    # 📌 Ajouter ou réinitialiser les colonnes si elles n'existent pas
    if "sentiment" not in df.columns:
        df["sentiment"] = ""
    if "categorie_reclamation" not in df.columns:
        df["categorie_reclamation"] = ""
    if "score_inconfort" not in df.columns:
        df["score_inconfort"] = 0

    # 📌 Forcer l'analyse en vidant les colonnes (pour éviter de sauter des tweets)
    df["sentiment"] = ""
    df["categorie_reclamation"] = ""
    df["score_inconfort"] = 0
    df.to_csv(file_path, sep=";", index=False)
    print("✅ Colonnes `sentiment`, `categorie_reclamation` et `score_inconfort` réinitialisées.")

    # 📌 Fonction pour analyser un tweet avec Mistral
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
            # Envoi de la requête API à Mistral
            response = requests.post(MISTRAL_API_URL, json=payload, headers=headers)
            print(f"🔍 Statut de la réponse : {response.status_code}")
            
            if response.status_code != 200:
                print(f"❌ ERREUR : Requête échouée. Code : {response.status_code}, Message : {response.text}")
                return "Erreur", "Autre", 50

            response_text = response.text.strip()

            # Affichage propre du JSON
            print("\n🔍 Réponse brute Mistral :")
            print(json.dumps(json.loads(response_text), indent=4, ensure_ascii=False))  # Beautify JSON

            # Vérification du JSON retourné
            response_data = json.loads(response_text)
            choices = response_data.get("choices", [])

            if not choices:
                print("❌ Mistral n'a retourné aucune réponse !")
                return "Erreur", "Autre", 50

            # Extraire et vérifier la réponse
            model_response = choices[0].get("message", {}).get("content", "").strip()
            a = model_response.split("{")
            b = a[1].split("}")
            model_response = "{" + b[0] + "}"

            if not model_response.startswith("{"):
                print(f"❌ Réponse non formatée en JSON : {model_response}")
                return "Erreur", "Autre", 50

            json_response = json.loads(model_response)
            sentiment = json_response.get("sentiment", "Neutre").strip()
            category = json_response.get("categorie", "Autre").strip()
            discomfort_score = json_response.get("score_inconfort", 50)

            return sentiment, category, discomfort_score

        except Exception as e:
            print(f"❌ ERREUR API Mistral : {e}")
            return "Erreur", "Autre", 50

    # 📌 Boucle pour analyser chaque tweet
    print("🚀 Début de l'analyse des tweets...")

    for index, row in df.iterrows():
        print(f"📨 Analyse du tweet {index + 1}/{len(df)} : {row['full_text'][:50]}...")

        sentiment, category, discomfort_score = analyze_tweet(row["full_text"])

        # 📌 Mise à jour du DataFrame
        df.at[index, "sentiment"] = sentiment
        df.at[index, "categorie_reclamation"] = category
        df.at[index, "score_inconfort"] = discomfort_score

        # 📌 Sauvegarde intermédiaire après chaque tweet
        df.to_csv(file_path, sep=";", index=False)

        # 📌 Pause pour éviter la surcharge de l'API
        time.sleep(2)

    print("✅ Analyse terminée, résultats enregistrés dans le fichier CSV.")
