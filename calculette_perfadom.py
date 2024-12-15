import streamlit as st

# Tarifs et descriptions pour tous les forfaits
FORFAITS = {
    # Forfaits d'installation
    "Installation 1": {
        "description": "Installation initiale - Système actif électrique",
        "tarif": 390.00,
        "frequence": "Unique",
    },
    "Installation 2": {
        "description": "Installation initiale - Système passif/diffuseur",
        "tarif": 250.00,
        "frequence": "Unique",
    },
    "Installation 3": {
        "description": "Installation initiale - Perfusion par gravité",
        "tarif": 50.00,
        "frequence": "Unique",
    },
    # Forfaits de suivi
    "Suivi actif électrique": {
        "description": "Suivi hebdomadaire - Système actif électrique",
        "tarif": 110.00,
        "frequence": "Hebdomadaire",
    },
    "Suivi diffuseur": {
        "description": "Suivi hebdomadaire - Diffuseur",
        "tarif": 50.00,
        "frequence": "Hebdomadaire",
    },
    # Forfaits de consommables
    "Consommables 1/semaine": {
        "description": "Consommables - 1 perfusion/semaine avec système actif ou diffuseur",
        "tarif": 39.00,
        "frequence": "Hebdomadaire",
    },
    "Consommables 1/jour actif": {
        "description": "Consommables - 1 perfusion/jour avec système actif ou diffuseur",
        "tarif": 269.00,
        "frequence": "Quotidien",
    },
    "Consommables 1/jour gravité": {
        "description": "Consommables - 1 perfusion/jour par gravité",
        "tarif": 83.00,
        "frequence": "Quotidien",
    },
    # Nutrition Entérale
    "Nutrition Entérale - Installation": {
        "description": "Installation initiale - Nutrition entérale",
        "tarif": 150.00,
        "frequence": "Unique",
    },
    "Nutrition Entérale - Suivi": {
        "description": "Suivi hebdomadaire - Nutrition entérale",
        "tarif": 60.00,
        "frequence": "Hebdomadaire",
    },
    # Nutrition Parentérale
    "Nutrition Parentérale - Installation": {
        "description": "Installation initiale - Nutrition parentérale avec pompe",
        "tarif": 450.00,
        "frequence": "Unique",
    },
    "Nutrition Parentérale - Suivi": {
        "description": "Suivi hebdomadaire - Nutrition parentérale avec pompe",
        "tarif": 200.00,
        "frequence": "Hebdomadaire",
    },
    # Immunothérapie
    "Immunothérapie - Installation": {
        "description": "Installation initiale - Immunothérapie avec pompe",
        "tarif": 500.00,
        "frequence": "Unique",
    },
    "Immunothérapie - Suivi": {
        "description": "Suivi hebdomadaire - Immunothérapie",
        "tarif": 250.00,
        "frequence": "Hebdomadaire",
    },
}

# Titre de l'application
st.title("Calculatrice complète : PERFADOM, Nutrition et Immunothérapie")

st.write("""
Cette application permet de calculer automatiquement le coût total d'un traitement en combinant plusieurs forfaits (installation, consommables, suivi). Vous pouvez sélectionner plusieurs forfaits pour un traitement complexe.
""")

# Sélection des forfaits
forfaits_selectionnes = st.multiselect(
    "Sélectionnez les forfaits pour votre traitement :",
    options=list(FORFAITS.keys()),
    format_func=lambda key: f"{key} - {FORFAITS[key]['description']}",
)

# Affichage des forfaits sélectionnés
if forfaits_selectionnes:
    st.write("### Détails des forfaits sélectionnés")
    total_general = 0
    forfaits_calculables = []
    for forfait in forfaits_selectionnes:
        details = FORFAITS[forfait]
        st.write(f"- **{forfait}** : {details['description']} | Tarif : {details['tarif']} € | Fréquence : {details['frequence']}")
        forfaits_calculables.append(details)
else:
    st.write("Veuillez sélectionner au moins un forfait pour continuer.")

# Entrée : Durée du traitement pour forfaits hebdomadaires et quotidiens
duree_traitement = 0
if any(f['frequence'] in ["Hebdomadaire", "Quotidien"] for f in forfaits_calculables):
    duree_traitement = st.number_input(
        "Entrez la durée du traitement (en jours) pour les forfaits hebdomadaires et quotidiens :",
        min_value=1,
        step=1,
    )

# Calcul du coût total
if st.button("Calculer le coût total"):
    total_general = 0
    for forfait in forfaits_calculables:
        tarif = forfait['tarif']
        frequence = forfait['frequence']

        if frequence == "Quotidien":
            total = tarif * duree_traitement
        elif frequence == "Hebdomadaire":
            total = tarif * (duree_traitement // 7 + (1 if duree_traitement % 7 > 0 else 0))
        elif frequence == "Unique":
            total = tarif
        else:
            total = 0

        total_general += total

    st.success(f"Coût total pour tous les forfaits sélectionnés : {total_general:.2f} €")

# Footer
st.caption("Application créée pour calculer les coûts PERFADOM, Nutrition et Immunothérapie.")
