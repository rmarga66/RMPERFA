import streamlit as st

# Données complètes des forfaits PERFADOM, Nutrition Entérale, Nutrition Parentérale et Immunothérapie
FORFAITS = {
    # PERFADOM Installation
    "PERFADOM1": {"description": "Installation 1 - Système actif électrique", "tarif": 297.67, "frequence": "Unique", "type": "Installation"},
    "PERFADOM2": {"description": "Installation 2 - Système actif électrique", "tarif": 137.38, "frequence": "Unique", "type": "Installation"},
    "PERFADOM3": {"description": "Installation par ES - Système actif électrique", "tarif": 137.38, "frequence": "Unique", "type": "Installation"},
    "PERFADOM4": {"description": "Installation 1 - Diffuseur", "tarif": 190.81, "frequence": "Unique", "type": "Installation"},
    "PERFADOM5": {"description": "Installation 2 - Diffuseur", "tarif": 87.77, "frequence": "Unique", "type": "Installation"},
    "PERFADOM6": {"description": "Installation et suivi - Gravité", "tarif": 38.16, "frequence": "Unique", "type": "Installation"},

    # PERFADOM Suivi
    "PERFADOM7": {"description": "Suivi hebdo - Système actif", "tarif": 83.95, "frequence": "Hebdomadaire", "type": "Suivi"},
    "PERFADOM8": {"description": "Suivi hebdo - Diffuseur", "tarif": 38.16, "frequence": "Hebdomadaire", "type": "Suivi"},

    # PERFADOM Consommables
    "PERFADOM17": {"description": "Gravité < 15 perf/28 jours", "tarif": 9.00, "frequence": "Hebdomadaire", "type": "Consommables"},
    "PERFADOM18": {"description": "Gravité - 1 perf/jour", "tarif": 63.35, "frequence": "Quotidien", "type": "Consommables"},
    "PERFADOM19": {"description": "Gravité - 2 perf/jour", "tarif": 119.83, "frequence": "Quotidien", "type": "Consommables"},
    "PERFADOM20": {"description": "Gravité - >2 perf/jour", "tarif": 170.20, "frequence": "Quotidien", "type": "Consommables"},
    "PERFADOM30": {"description": "Actif - 1 perf/jour", "tarif": 200.12, "frequence": "Quotidien", "type": "Consommables"},
    "PERFADOM31": {"description": "Actif - 2 perf/jour", "tarif": 379.14, "frequence": "Quotidien", "type": "Consommables"},
    "PERFADOM32": {"description": "Actif - 3 perf/jour", "tarif": 539.39, "frequence": "Quotidien", "type": "Consommables"},
    "PERFADOM33": {"description": "Actif - >3 perf/jour", "tarif": 679.32, "frequence": "Quotidien", "type": "Consommables"},
    "PERFADOM37": {"description": "Diffuseur - 1 perf/jour", "tarif": 180.10, "frequence": "Quotidien", "type": "Consommables"},
    "PERFADOM38": {"description": "Diffuseur - 2 perf/jour", "tarif": 341.22, "frequence": "Quotidien", "type": "Consommables"},
    "PERFADOM39": {"description": "Diffuseur - 3 perf/jour", "tarif": 485.45, "frequence": "Quotidien", "type": "Consommables"},
    "PERFADOM40": {"description": "Diffuseur - >3 perf/jour", "tarif": 611.38, "frequence": "Quotidien", "type": "Consommables"},

    # Nutrition Parentérale
    "NUT_PAR1": {"description": "Installation - Nutrition parentérale", "tarif": 325.00, "frequence": "Unique", "type": "Installation"},
    "NUT_PAR2": {"description": "6-7 j/7 - Consommables et accessoires", "tarif": 158.33, "frequence": "Hebdomadaire", "type": "Consommables"},

    # Nutrition Entérale
    "NUT_ENT1": {"description": "Installation - Nutrition entérale", "tarif": 146.53, "frequence": "Unique", "type": "Installation"},
    "NUT_ENT2": {"description": "Hebdo - Sans pompe ou gravité", "tarif": 50.33, "frequence": "Hebdomadaire", "type": "Suivi"},
    "NUT_ENT3": {"description": "Hebdo - Avec pompe", "tarif": 68.52, "frequence": "Hebdomadaire", "type": "Suivi"},
}

# Interface utilisateur Streamlit
st.title("💉 Calculatrice LPPR - PERFADOM, Nutrition et Immunothérapie")

st.write("Sélectionnez vos forfaits en respectant les règles LPPR : un seul forfait d'installation par traitement.")

# Sélection des forfaits
installation = st.selectbox(
    "Choisissez un forfait d'installation :",
    options=["Aucun"] + [k for k, v in FORFAITS.items() if v["type"] == "Installation"],
    format_func=lambda k: f"{FORFAITS[k]['description']} ({FORFAITS[k]['tarif']} €)" if k != "Aucun" else "Aucun",
)

autres_forfaits = st.multiselect(
    "Ajoutez les forfaits de suivi et consommables :",
    options=[k for k, v in FORFAITS.items() if v["type"] != "Installation"],
    format_func=lambda k: f"{FORFAITS[k]['description']} ({FORFAITS[k]['tarif']} €)",
)

duree = st.number_input("Durée du traitement (en jours) :", min_value=1, step=1, value=7)

# Calcul du coût total
if st.button("🧮 Calculer le coût total"):
    total = 0

    # Forfait d'installation
    if installation != "Aucun":
        total += FORFAITS[installation]["tarif"]
        st.write(f"✅ {FORFAITS[installation]['description']} : {FORFAITS[installation]['tarif']} €")

    # Autres forfaits
    for forfait in autres_forfaits:
        tarif = FORFAITS[forfait]["tarif"]
        if FORFAITS[forfait]["frequence"] == "Quotidien":
            total += tarif * duree
        elif FORFAITS[forfait]["frequence"] == "Hebdomadaire":
            total += tarif * ((duree // 7) + (1 if duree % 7 > 0 else 0))
        else:
            total += tarif
        st.write(f"✅ {FORFAITS[forfait]['description']} : {tarif:.2f} €")

    st.success(f"💰 Coût total : {total:.2f} €")
