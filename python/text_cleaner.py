import unicodedata
import re
import pandas as pd

def clean_text(text):
    """Nettoyer et normaliser le texte."""
    text = unicodedata.normalize('NFD', text)
    text = ''.join([char for char in text if unicodedata.category(char) != 'Mn'])
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r"[^a-zA-Z0-9@/’'’\s-]", '', text)
    text = re.sub(r'\\n|\\r|\\t', ' ', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\r', ' ', text)
    text = re.sub(r'\t', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.lower()
    return text

def clean_dataframe(df):
    """Nettoyer le DataFrame."""
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce', utc=True)
    df = df.drop(columns=['id', 'screen_name', 'name'], axis=1)
    df['full_text'] = df['full_text'].apply(lambda x: clean_text(str(x)) if pd.notnull(x) else x)
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"Suppression des doublons : {before - after} lignes supprimées.")
    return df
