import unicodedata

def normalize_text(text):
    """Normaliser le texte (insensible à la casse et aux accents)."""
    text = text.lower()
    text = unicodedata.normalize('NFD', text)
    text = ''.join([c for c in text if unicodedata.category(c) != 'Mn'])
    return text

# Liste de mots-clés par catégorie avec pondération
keywords_urgent = {
    "panne": 3, "urgence": 3, "scandale": 2, "danger": 3, "intervention immédiate": 3,
    "crise": 2, "alerte": 2, "détresse": 2, "impossible": 2, "coupure": 3, "black-out": 3,
    "dysfonctionnement majeur": 3, "eau chaude": 2, "chauffage": 2, "électricité": 2,
    "catastrophe": 3, "problème grave": 3, "situation critique": 3, "délestage": 2,
    "arrêt total": 3, "urgent": 3, "immédiat": 3, "coupé": 2, "plus rien": 2
}

keywords_important = {
    "erreur": 2, "retard": 2, "problème": 2, "facture": 2, "litige": 2, "remboursement": 2,
    "réclamation": 2, "inexact": 1, "mauvais": 1, "retard d'intervention": 2, "réponse tardive": 2,
    "surfacturation": 2, "maintenance": 1, "mise à jour échouée": 2, "délai": 2,
    "attente": 1, "semaine": 1, "jour": 1, "mois": 1, "réparation": 2, "technicien": 2,
    "intervention": 2, "rendez-vous": 2, "dysfonctionnement": 2, "problème technique": 2,
    "réclamation": 2, "réparation": 2, "technicien": 2, "intervention": 2, "rendez-vous": 2,
    "dysfonctionnement": 2, "problème technique": 2, "réclamation": 2, "réparation": 2,
    "technicien": 2, "intervention": 2, "rendez-vous": 2, "dysfonctionnement": 2,
    "problème technique": 2, "réclamation": 2, "réparation": 2, "technicien": 2,
    "intervention": 2, "rendez-vous": 2, "dysfonctionnement": 2, "problème technique": 2
}

keywords_neutre = {
    "question": 1, "tarif": 1, "contact": 1, "explication": 1, "service client": 1, "relevé": 1,
    "avis": 1, "réception": 1, "information": 1, "demande": 1, "installation": 1, "courrier": 1,
    "compteur": 1, "renseignement": 1, "détail": 1, "suivi": 1, "consommation": 1,
    "abonnement": 1, "contrat": 1, "facturation": 1, "prix": 1, "coût": 1, "devis": 1,
    "estimation": 1, "budget": 1, "plan": 1, "organisation": 1, "précision": 1,
    "détail": 1, "suivi": 1, "consommation": 1, "abonnement": 1, "contrat": 1,
    "facturation": 1, "prix": 1, "coût": 1, "devis": 1, "estimation": 1, "budget": 1,
    "plan": 1, "organisation": 1, "précision": 1
}

keywords_service_client = {
    "injoignable": 2, "pas de réponse": 2, "hotline inutile": 2, "attente interminable": 2,
    "mauvais service": 2, "pas de solution": 2, "service client déplorable": 2, "agence fantôme": 2,
    "technicien": 1, "relance": 1, "contact": 1, "réponse": 1, "disponibilité": 1,
    "joindre": 1, "disponible": 1, "réactif": 1, "support": 1, "assistance": 1,
    "réactivité": 1, "disponibilité": 1, "joindre": 1, "disponible": 1, "réactif": 1,
    "support": 1, "assistance": 1, "réactivité": 1
}

keywords_application = {
    "bug": 2, "erreur connexion": 2, "problème app": 2, "connexion impossible": 2, "lenteur": 1,
    "maintenance": 1, "mise à jour échouée": 2, "plantage": 2, "application en rade": 2,
    "problème de connexion": 2, "5ghz": 1, "serveur": 1, "plantage": 2, "bug": 2,
    "erreur connexion": 2, "problème app": 2, "connexion impossible": 2, "lenteur": 1,
    "maintenance": 1, "mise à jour échouée": 2, "plantage": 2, "application en rade": 2,
    "problème de connexion": 2, "5ghz": 1, "serveur": 1, "plantage": 2, "bug": 2,
    "erreur connexion": 2, "problème app": 2, "connexion impossible": 2, "lenteur": 1,
    "maintenance": 1, "mise à jour échouée": 2, "plantage": 2, "application en rade": 2,
    "problème de connexion": 2, "5ghz": 1, "serveur": 1
}

keywords_facturation = {
    "facture": 2, "surfacturation": 2, "prélèvement": 2, "remboursement": 2, "litige": 2,
    "erreur de facturation": 2, "montant incorrect": 2, "consommation": 1, "contrat": 1,
    "abonnement": 1, "tarif": 1, "prix": 1, "coût": 1, "augmentation": 2, "majoration": 2,
    "erreur": 2, "facturation": 2, "paiement": 2, "régularisation": 2, "réclamation": 2,
    "erreur de facturation": 2, "montant incorrect": 2, "consommation": 1, "contrat": 1,
    "abonnement": 1, "tarif": 1, "prix": 1, "coût": 1, "augmentation": 2, "majoration": 2,
    "erreur": 2, "facturation": 2, "paiement": 2, "régularisation": 2, "réclamation": 2
}

keywords_delai_intervention = {
    "retard": 2, "délai": 2, "intervention": 2, "rendez-vous": 2, "attente": 1, "semaine": 1,
    "jour": 1, "mois": 1, "réparation": 2, "technicien": 2, "planification": 1,
    "disponibilité": 1, "réactif": 1, "support": 1, "assistance": 1, "réactivité": 1,
    "retard": 2, "délai": 2, "intervention": 2, "rendez-vous": 2, "attente": 1, "semaine": 1,
    "jour": 1, "mois": 1, "réparation": 2, "technicien": 2, "planification": 1,
    "disponibilité": 1, "réactif": 1, "support": 1, "assistance": 1, "réactivité": 1
}

def categorize_tweet(text):
    """Catégoriser un tweet en fonction des mots-clés avec priorisation et pondération."""
    normalized_text = normalize_text(text)
    scores = {
        "URGENT": 0,
        "IMPORTANT": 0,
        "NEUTRE": 0,
        "Panne": 0,
        "Service Client Injoignable": 0,
        "Problèmes avec l'Application": 0,
        "Problèmes de Facturation": 0,
        "Délais d'Intervention": 0
    }

    for kw, weight in keywords_urgent.items():
        if kw in normalized_text:
            scores["URGENT"] += weight
            scores["Panne"] += weight

    for kw, weight in keywords_important.items():
        if kw in normalized_text:
            scores["IMPORTANT"] += weight

    for kw, weight in keywords_neutre.items():
        if kw in normalized_text:
            scores["NEUTRE"] += weight

    for kw, weight in keywords_service_client.items():
        if kw in normalized_text:
            scores["IMPORTANT"] += weight
            scores["Service Client Injoignable"] += weight

    for kw, weight in keywords_application.items():
        if kw in normalized_text:
            scores["IMPORTANT"] += weight
            scores["Problèmes avec l'Application"] += weight

    for kw, weight in keywords_facturation.items():
        if kw in normalized_text:
            scores["IMPORTANT"] += weight
            scores["Problèmes de Facturation"] += weight

    for kw, weight in keywords_delai_intervention.items():
        if kw in normalized_text:
            scores["IMPORTANT"] += weight
            scores["Délais d'Intervention"] += weight

    max_score_category = max(scores, key=scores.get)
    if max_score_category in ["URGENT", "Panne"]:
        return "URGENT", "Critique" if scores["Panne"] > 0 else "Panne"
    elif max_score_category == "IMPORTANT":
        sub_category = max(
            {"Service Client Injoignable": scores["Service Client Injoignable"],
             "Problèmes avec l'Application": scores["Problèmes avec l'Application"],
             "Problèmes de Facturation": scores["Problèmes de Facturation"],
             "Délais d'Intervention": scores["Délais d'Intervention"]},
            key=lambda k: scores[k]
        )
        return "IMPORTANT", sub_category
    elif max_score_category == "NEUTRE":
        return "NEUTRE", "Demande d'information"

    return "NEUTRE", "Autre"

def generate_features(df):
    """Générer des colonnes avec les paramètres extraits."""
    df['importance_level'], df['problem_type'] = zip(*df['full_text'].apply(lambda x: categorize_tweet(str(x))))
    df['text_length'] = df['full_text'].apply(len)
    return df
