import streamlit as st

# Liste des forfaits PERFADOM avec leurs descriptions, tarifs et fréquences
FORFAITS = {
    # Forfaits d'installation (uniques)
    "Installation 1": {
        "description": "Installation initiale - Système actif électrique",
        "tarif": 390.00,
        "frequence": "Unique",
        "type": "Installation",
    },
    "Installation 2": {
        "description": "Installation initiale - Système passif/diffuseur",
        "tarif": 250.00,
        "frequence": "Unique",
        "type": "Installation",
    },
    "Installation 3": {
        "description": "Installation initiale - Perfusion par gravité",
        "tarif": 50.00,
        "frequence": "Unique",
        "type": "Installation",
    },
    # Forfaits de suivi (hebdomadaires)
    "Suivi actif électrique": {
        "description": "Suivi hebdomadaire - Système actif électrique",
        "tarif": 110.00,
        "frequence": "Hebdomadaire",
        "type": "Suivi",
    },
    "Suivi diffuseur": {
        "description": "Suivi hebdomadaire - Diffuseur",
        "tarif": 50.00,
        "frequence": "Hebdomadaire",
        "type": "Suivi",
    },
    # Forfaits de consommables
    "Consommables 1/semaine": {
        "description": "Consommables - 1 perfusion/semaine avec système actif ou diffuseur",
        "tarif": 39.00,
        "frequence": "Hebdomadaire",
        "type": "Consommables",
    },
    "Consommables 1/jour actif": {
        "description": "Consommables - 1 perfusion/jour avec système actif ou diffuseur",
        "tarif": 269.00,
        "frequence": "Quotidien",
        "type": "Consommables",
    },
    "Consommables 1/jour gravité": {
        "description": "Consommables - 1 perfusion/jour par gravité",
        "tarif": 83.00,
        "frequence": "Quotidien",
        "type": "Consommables",
    },
}

# Titre de l'application
st.title("Calculatrice PERFADOM - Respect des règles LPPR")

st.write("""
Cette application permet de calculer automatiquement le coût total d'un traitement PERFADOM tout en respectant les règles de la LPPR :
- Un seul forfait d'installation est autorisé par traitement.
- Les forfaits de suivi et de consommables sont calculés en fonction de la durée du traitement.
""")

# Sélection des forfaits
installation_selectionnee = st.selectbox(
    "Sélectionnez un forfait d'installation (obligatoire) :",
    options=["Aucun"] + [key for key in FORFAITS if FORFAITS[key]["type"] == "Installation"],
    format_func=lambda key: f"{key} - {FORFAITS[key]['description']}" if key != "Aucun" else "Aucun",
)

autres_forfaits = st.multiselect(
    "Sélectionnez les forfaits de suivi et de consommables :",
    options=[key for key in FORFAITS if FORFAITS[key]["type"] != "Installation"],
    format_func=lambda key: f"{key} - {FORFAITS[key]['description']}",
)

# Entrée : Durée du traitement
duree_traitement = st.number_input(
    "Entrez la durée du traitement (en jours) :",
    min_value=1,
    step=1,
    value=7,
)

# Validation des sélections
erreurs = []
if installation_selectionnee == "Aucun":
    erreurs.append("Vous devez sélectionner un forfait d'installation.")
if len([f for f in autres_forfaits if FORFAITS[f]["type"] == "Installation"]) > 0:
    erreurs.append("Un seul forfait d'installation est autorisé.")

# Afficher les erreurs
if erreurs:
    for erreur in erreurs:
        st.error(erreur)

# Calcul automatique du coût total
if st.button("Calculer le coût total") and not erreurs:
    total_general = 0

    # Calcul du forfait d'installation
    if installation_selectionnee != "Aucun":
        forfait = FORFAITS[installation_selectionnee]
        st.write(f"- {installation_selectionnee} : {forfait['description']} = {forfait['tarif']} €")
        total_general += forfait["tarif"]

    # Calcul des autres forfaits
    for forfait_key in autres_forfaits:
        forfait = FORFAITS[forfait_key]
        tarif = forfait["tarif"]

        if forfait["frequence"] == "Quotidien":
            total = tarif * duree_traitement
        elif forfait["frequence"] == "Hebdomadaire":
            total = tarif * (duree_traitement // 7 + (1 if duree_traitement % 7 > 0 else 0))
        else:
            total = tarif

        st.write(f"- {forfait_key} : {forfait['description']} = {total:.2f} €")
        total_general += total

    # Affichage du total général
    st.success(f"Coût total pour le traitement : {total_general:.2f} €")

# Footer
st.caption("Application développée pour respecter les règles LPPR.")
