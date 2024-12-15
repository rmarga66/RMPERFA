import streamlit as st

# Données des forfaits issues du tableau
FORFAITS = {
    "PERFADOM1": {"description": "Installation 1 - Système actif électrique", "tarif": 297.67, "frequence": "Unique", "type": "Installation"},
    "PERFADOM2": {"description": "Installation 2 - Système actif électrique", "tarif": 137.38, "frequence": "Unique", "type": "Installation"},
    "PERFADOM4": {"description": "Installation 1 - Diffuseur", "tarif": 190.81, "frequence": "Unique", "type": "Installation"},
    "PERFADOM5": {"description": "Installation 2 - Diffuseur", "tarif": 87.77, "frequence": "Unique", "type": "Installation"},
    "PERFADOM6": {"description": "Installation et suivi - Gravité", "tarif": 38.16, "frequence": "Unique", "type": "Installation"},
    "PERFADOM7": {"description": "Suivi hebdo - Système actif", "tarif": 83.95, "frequence": "Hebdomadaire", "type": "Suivi"},
    "PERFADOM8": {"description": "Suivi hebdo - Diffuseur", "tarif": 38.16, "frequence": "Hebdomadaire", "type": "Suivi"},
    "PERFADOM18": {"description": "Consommables Gravité - 1 perf/jour", "tarif": 63.35, "frequence": "Quotidien", "type": "Consommables"},
    "PERFADOM30": {"description": "Consommables Système actif - 1 perf/jour", "tarif": 200.12, "frequence": "Quotidien", "type": "Consommables"},
    "PERFADOM37": {"description": "Consommables Diffuseur - 1 perf/jour", "tarif": 180.10, "frequence": "Quotidien", "type": "Consommables"},
    "NUT_ENT_1": {"description": "Nutrition entérale - Installation", "tarif": 146.53, "frequence": "Unique", "type": "Installation"},
    "NUT_ENT_2": {"description": "Nutrition entérale - Hebdomadaire sans pompe", "tarif": 50.33, "frequence": "Hebdomadaire", "type": "Suivi"},
    "NUT_PAR_1": {"description": "Nutrition parentérale - Installation", "tarif": 325.00, "frequence": "Unique", "type": "Installation"},
    "NUT_PAR_2": {"description": "Nutrition parentérale 6-7j/7 - Consommables", "tarif": 158.33, "frequence": "Hebdomadaire", "type": "Consommables"},
    "IMMUNO_SC": {"description": "Immunothérapie SC - 1 perf/système actif", "tarif": 39.96, "frequence": "Quotidien", "type": "Consommables"},
}

# Interface Streamlit
st.title("💉 Calculatrice PERFADOM, Nutrition et Immunothérapie")
st.write("""
Sélectionnez les forfaits et la durée du traitement pour calculer le coût total en respectant les règles LPPR.
""")

# Sélection des forfaits
installation_selectionnee = st.selectbox(
    "Sélectionnez un forfait d'installation :",
    options=["Aucun"] + [key for key, val in FORFAITS.items() if val["type"] == "Installation"],
    format_func=lambda key: f"{key} - {FORFAITS[key]['description']}" if key != "Aucun" else "Aucun",
)

# Sélection des consommables et suivis
autres_forfaits = st.multiselect(
    "Sélectionnez les forfaits de suivi et consommables :",
    options=[key for key, val in FORFAITS.items() if val["type"] != "Installation"],
    format_func=lambda key: f"{key} - {FORFAITS[key]['description']}",
)

# Entrée : Durée du traitement
duree_traitement = st.number_input("Durée du traitement (en jours) :", min_value=1, step=1, value=7)

# Validation des sélections
erreurs = []
if installation_selectionnee == "Aucun":
    erreurs.append("⚠️ Vous devez sélectionner un forfait d'installation.")

# Affichage des erreurs
if erreurs:
    for erreur in erreurs:
        st.error(erreur)

# Calcul du coût total
if st.button("🧮 Calculer le coût total") and not erreurs:
    total = 0

    # Forfait d'installation
    if installation_selectionnee != "Aucun":
        total += FORFAITS[installation_selectionnee]["tarif"]
        st.write(f"✅ {FORFAITS[installation_selectionnee]['description']} : {FORFAITS[installation_selectionnee]['tarif']} €")

    # Consommables et suivi
    for key in autres_forfaits:
        forfait = FORFAITS[key]
        if forfait["frequence"] == "Quotidien":
            total_forfait = forfait["tarif"] * duree_traitement
        elif forfait["frequence"] == "Hebdomadaire":
            total_forfait = forfait["tarif"] * ((duree_traitement // 7) + (1 if duree_traitement % 7 > 0 else 0))
        else:
            total_forfait = forfait["tarif"]
        total += total_forfait
        st.write(f"✅ {forfait['description']} : {total_forfait:.2f} €")

    # Affichage du total
    st.success(f"💰 Coût total pour le traitement : {total:.2f} €")

# Footer
st.caption("🩺 Calculatrice développée pour respecter les règles LPPR.")
