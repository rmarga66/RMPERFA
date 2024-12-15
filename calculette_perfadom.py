import streamlit as st

# Intégration complète des données du tableau fourni
FORFAITS = {
    "PERFADOM1": {"description": "Perf à dom, instal1, syst actif électrique", "tarif": 297.67, "type": "Installation"},
    "PERFADOM2": {"description": "Perf à dom, instal2, syst actif électrique", "tarif": 137.38, "type": "Installation"},
    "PERFADOM3": {"description": "Perf rempli ES, syst actif électrique", "tarif": 137.38, "type": "Installation"},
    "PERFADOM4": {"description": "Perf à dom, instal1, diffuseur", "tarif": 190.81, "type": "Installation"},
    "PERFADOM5": {"description": "Perf à dom, instal2, diffuseur", "tarif": 87.77, "type": "Installation"},
    "PERFADOM6": {"description": "Perf à dom, instal et suivi gravité", "tarif": 38.16, "type": "Installation"},
    "PERFADOM7": {"description": "Suivi hebdo, système actif", "tarif": 83.95, "type": "Suivi"},
    "PERFADOM8": {"description": "Suivi hebdo, diffuseur", "tarif": 38.16, "type": "Suivi"},
    "PERFADOM17": {"description": "Gravité < 15 perf/28j", "tarif": 9.00, "type": "Consommables"},
    "PERFADOM18": {"description": "Gravité 1 perf/j", "tarif": 63.35, "type": "Consommables"},
    "PERFADOM19": {"description": "Gravité 2 perf/j", "tarif": 119.83, "type": "Consommables"},
    "PERFADOM20": {"description": "Gravité >2 perf/j", "tarif": 170.20, "type": "Consommables"},
    "PERFADOM30": {"description": "Système actif, 1 perf/j", "tarif": 200.12, "type": "Consommables"},
    "PERFADOM31": {"description": "Système actif, 2 perf/j", "tarif": 379.14, "type": "Consommables"},
    "PERFADOM32": {"description": "Système actif, 3 perf/j", "tarif": 539.39, "type": "Consommables"},
    "PERFADOM33": {"description": "Système actif, >3 perf/j", "tarif": 679.32, "type": "Consommables"},
    "NUT_PAR1": {"description": "Installation - Nutrition parentérale", "tarif": 325.00, "type": "Installation"},
    "NUT_PAR2": {"description": "6 ou 7j/7 - Consommables et accessoires", "tarif": 158.33, "type": "Consommables"},
    "NUT_ENT1": {"description": "Installation - Nutrition entérale", "tarif": 146.53, "type": "Installation"},
    "NUT_ENT2": {"description": "Hebdo - Nutrition entérale sans pompe", "tarif": 50.33, "type": "Suivi"},
    "NUT_ENT3": {"description": "Hebdo - Nutrition entérale avec pompe", "tarif": 68.52, "type": "Suivi"},
    "IMMUNO_SC": {"description": "Immunothérapie SC - 1 perf/système actif", "tarif": 39.96, "type": "Consommables"},
    "IMMUNO_IV": {"description": "Immunothérapie IV - 1 perf/j", "tarif": 39.96, "type": "Consommables"},
}

# Interface utilisateur Streamlit
st.title("💉 Calculatrice Complète - LPPR")
st.write("""
Sélectionnez vos forfaits et précisez les **quantités** pour calculer le coût total.  
**Règle :** Un seul forfait d'installation est autorisé.
""")

# Sélection d'un forfait d'installation
installation = st.selectbox(
    "Choisissez un forfait d'installation :",
    options=["Aucun"] + [k for k, v in FORFAITS.items() if v["type"] == "Installation"],
    format_func=lambda k: f"{FORFAITS[k]['description']} ({FORFAITS[k]['tarif']} €)" if k != "Aucun" else "Aucun",
)

# Sélection des autres forfaits avec quantités
st.write("### Ajoutez les forfaits de suivi et consommables avec quantités :")
autres_forfaits = {}
for key, value in FORFAITS.items():
    if value["type"] != "Installation":
        quantite = st.number_input(f"{value['description']} ({value['tarif']} €) :", min_value=0, step=1, key=key)
        if quantite > 0:
            autres_forfaits[key] = quantite

# Calcul du coût total
if st.button("🧮 Calculer le coût total"):
    total = 0

    # Forfait d'installation
    if installation != "Aucun":
        total += FORFAITS[installation]["tarif"]
        st.write(f"✅ {FORFAITS[installation]['description']} : {FORFAITS[installation]['tarif']} €")

    # Autres forfaits avec quantités
    for key, quantite in autres_forfaits.items():
        tarif_total = FORFAITS[key]["tarif"] * quantite
        total += tarif_total
        st.write(f"✅ {FORFAITS[key]['description']} x {quantite} : {tarif_total:.2f} €")

    # Affichage du coût total
    st.success(f"💰 Coût total : {total:.2f} €")

# Footer
st.caption("🩺 Application développée pour inclure toutes les lignes du tableau LPPR.")
