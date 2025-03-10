import unicodedata

def normalize_text(text):
    """Normaliser le texte (insensible à la casse et aux accents)."""
    text = text.lower()
    text = unicodedata.normalize('NFD', text)
    text = ''.join([c for c in text if unicodedata.category(c) != 'Mn'])
    return text


def generate_features(df):
    df['text_length'] = df['full_text'].apply(len)
    return df
