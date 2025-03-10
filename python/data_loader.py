import pandas as pd

def load_data(path):
    """Charger les données à partir d'un fichier CSV."""
    df = pd.read_csv(path, sep=';')
    print(f"Données chargées avec {df.shape[0]} lignes et {df.shape[1]} colonnes.")
    return df
