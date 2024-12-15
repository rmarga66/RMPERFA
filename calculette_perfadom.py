import streamlit as st

# Données des forfaits PERFADOM, nutrition et immunothérapie
FORFAITS = {
    # PERFADOM Installation
    "PERFADOM 1": {"description": "Installation - Système actif électrique", "tarif": 357.20, "frequence": "Unique", "type": "Installation"},
    "PERFADOM 2": {"description": "Installation - Système passif/diffuseur", "tarif": 250.00, "frequence": "Unique", "type": "Installation"},
    "PERFADOM 3": {"description": "Installation - Gravité", "tarif": 50.00, "frequence": "Unique", "type": "Installation"},
    # PERFADOM Suivi
    "PERFADOM 7": {"description": "Suivi - Système actif électrique (hebdo)", "tarif": 100.75, "frequence": "Hebdomadaire", "type": "Suivi"},
    "PERFADOM 8": {"description": "Suivi - Diffuseur (hebdo)", "tarif": 45.79, "frequence": "Hebdomadaire", "type": "Suivi"},
    # PERFADOM Consommables
    "PERFADOM 13": {"description": "Consommables - 1 perfusion/jour (actif ou diffuseur)", "tarif": 246.81, "frequence": "Quotidien", "type": "Consommables"},
    "PERFADOM 14": {"description": "Consommables - 2 perfusions/jour (actif ou diffuseur)", "tarif": 467.59, "frequence": "Quotidien", "type": "Consommables"},
    "PERFADOM 18": {"description": "Consommables - 1 perfusion/jour (gravité)", "tarif": 76.02, "frequence": "Quotidien", "type": "Consommables"},
    # Nutrition Entérale
    "Nutrition Entérale - Installation": {"description": "Installation initiale - Nutrition entérale", "tarif": 150.00, "frequence": "Unique", "type": "Installation"},
    "Nutrition Entérale - Suivi": {"description": "Suivi - Nutrition entérale (hebdo)", "tarif": 60.00, "frequence": "Hebdomadaire", "type": "Suivi"},
    # Nutrition Parentérale
    "Nutrition Parentérale - Installation": {"description": "Installation initiale - Nutrition parentérale", "tarif": 450.00, "frequence": "Unique", "type": "Installation"},
    "Nutrition Parentérale - Suivi": {"description": "Suivi - Nutrition parentérale (hebdo)", "tarif": 200.00, "frequence": "Hebdomadaire", "type": "Suivi"},
    # Immunothérapie
    "Immunothérapie - Installation": {"description": "Installation initiale - Immunothérapie", "tarif": 500.00, "frequence": "Unique", "type": "Installation"},
    "Immunothérapie - Suivi": {"description": "Suivi - Immunothérapie (hebdo)", "tarif": 250.00, "frequence": "Hebdomadaire", "type": "Suivi"},
}

# Titre de l'application
st.title("Calculatrice PERFADOM, Nutrition et Immunothérapie")

st.write("""
Cette application calcule automatiquement le coût total d'un traitement en fonction des forfaits sélectionnés et de la durée, tout en respectant les règles LPPR :
- Un seul forfait d'installation est autorisé.
- Les forfaits de consommables et de suivi sont calculés en fonction de la durée du traitement.
""")

# Sélection du forfait d'installation
installation_selectionnee = st.selectbox(
    "Sélectionnez un forfait d'installation :",
    options=["Aucun"] + [key for key in FORFAITS if FORFAITS[key]["type"] == "Installation"],
    format_func=lambda key: f"{key} - {FORFAITS[key]['description']}" if key != "Aucun" else "Aucun",
)

# Sélection des autres forfaits (suivi et consommables)
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
