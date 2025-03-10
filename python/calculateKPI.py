import pandas as pd


def calculateKPI():
    # Charger les données
    def load_data(path):
        df = pd.read_csv(path, sep=';', parse_dates=['created_at'])
        return df

    # Calcul des KPI
    def compute_kpis(df):
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        # Supprimer le fuseau horaire avant la conversion
        df['created_at'] = df['created_at'].dt.tz_localize(None)
        print(df.head(10))
        df['day'] = df['created_at'].dt.date
        df['week'] = df['created_at'].dt.to_period('W').astype(str)
        df['month'] = df['created_at'].dt.to_period('M').astype(str)
        
        # Nombre de tweets par jour, semaine, mois
        tweets_per_day = df.groupby('day').size().reset_index(name='Tweets par jour')
        tweets_per_week = df.groupby('week').size().reset_index(name='Tweets par semaine')
        tweets_per_month = df.groupby('month').size().reset_index(name='Tweets par mois')
        
        # Fréquence des mentions des comptes Engie
        df['mentions'] = df['full_text'].str.findall(r'@\w+')
        mentions_exploded = df.explode('mentions')
        mentions_count = mentions_exploded['mentions'].value_counts().reset_index()
        mentions_count.columns = ['Compte', 'Nombre de mentions']
        
        # Détection des tweets contenant des mots-clés critiques
        keywords = ["délai", "panne", "urgence", "scandale", "facture", "service", "bug", "erreur", "problème", "soucis", "coupure", "technique", "arrêt", "dysfonctionnement", "bugs", "paiement", "attente", "devis", "relance", "résilier"]
        df['contains_critical_keywords'] = df['full_text'].apply(lambda x: any(kw in x.lower() for kw in keywords))
        
        tweets_with_keywords = df[df['contains_critical_keywords']]
        tweets_per_day_keywords = tweets_with_keywords.groupby('day').size().reset_index(name='Mots-clés par jour')
        tweets_per_week_keywords = tweets_with_keywords.groupby('week').size().reset_index(name='Mots-clés par semaine')
        tweets_per_month_keywords = tweets_with_keywords.groupby('month').size().reset_index(name='Mots-clés par mois')
        
        # Fusion des résultats
        results = {
            'tweets_per_day': tweets_per_day,
            'tweets_per_week': tweets_per_week,
            'tweets_per_month': tweets_per_month,
            'mentions_count': mentions_count,
            'tweets_per_day_keywords': tweets_per_day_keywords,
            'tweets_per_week_keywords': tweets_per_week_keywords,
            'tweets_per_month_keywords': tweets_per_month_keywords,
        }
        
        return results

    # Sauvegarde des résultats
    def save_results(results):
        for key, df in results.items():
            df.to_csv(f'./result_csv/{key}.csv', index=False, sep=';')

    # Exécution du script
    path = "./result_csv/cleaned_data.csv"
    df = load_data(path)
    results = compute_kpis(df)
    save_results(results)

if __name__ == "__main__":
    calculateKPI()
