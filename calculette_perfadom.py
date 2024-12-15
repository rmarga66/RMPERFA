import streamlit as st

# Données complètes des forfaits PERFADOM, Nutrition Entérale, Nutrition Parentérale et Immunothérapie
FORFAITS = {
    # PERFADOM Installation
    "PERFADOM1": {"description": "Installation 1 - Système actif électrique", "tarif": 297.67, "type": "Installation"},
    "PERFADOM2": {"description": "Installation 2 - Système actif électrique", "tarif": 137.38, "type": "Installation"},
    "PERFADOM4": {"description": "Installation 1 - Diffuseur", "tarif": 190.81, "type": "Installation"},
    "PERFADOM5": {"description": "Installation 2 - Diffuseur", "tarif": 87.77, "type": "Installation"},
    # PERFADOM Suivi
    "PERFADOM7": {"description": "Suivi hebdo - Système actif", "tarif": 83.95, "type": "Suivi"},
    "PERFADOM8": {"description": "Suivi hebdo - Diffuseur", "tarif": 38.16, "type": "Suivi"},
    # Consommables
    "PERFADOM30": {"description": "Consommables Actif - 1 perf/jour", "tarif": 200.12, "type": "Consommables"},
    "PERFADOM31": {"description": "Consommables Actif - 2 perf/jour", "tarif": 379.14, "type": "Consommables"},
    "PERFADOM37": {"description": "Consommables Diffuseur - 1 perf/jour", "tarif": 180.10, "type": "Consommables"},
    "PERFADOM40": {"description": "Consommables Diffuseur - >3 perf/jour", "tarif": 611.38, "type": "Consommables"},
    # Nutrition Parentérale
    "NUT_PAR1": {"description": "Installation - Nutrition parentérale", "tarif": 325.00, "type": "Installation"},
    "NUT_PAR2": {"description": "Consommables Nutrition parentérale - 6-7 j/7", "tarif": 158.33, "type": "Consommables"},
    # Nutrition Entérale
    "NUT_ENT1": {"description": "Installation - Nutrition entérale", "tarif": 146.53, "type": "Installation"},
    "NUT_ENT2": {"description": "Hebdo - Nutrition entérale sans pompe", "tarif": 50.33, "type": "Suivi"},
    "NUT_ENT3": {"description": "Hebdo - Nutrition entérale avec pompe", "tarif": 68.52, "type": "Suivi"},
    # Immunothérapie
    "IMMUNO_SC": {"description": "Immunothérapie SC - 1 perf/système actif", "tarif": 39.96, "type": "Consommables"},
}

# Interface utilisateur Streamlit
st.title("💉 Calculatrice LPPR - PERFADOM, Nutrition et Immunothérapie")

st.write("""
Sélectionnez vos forfaits et précisez les quantités pour calculer le coût total.  
**Règle** : Un seul forfait d'installation est autorisé.
""")

# Sélection du forfait d'installation
installation = st.selectbox(
    "Choisissez un forfait d'installation :",
    options=["Aucun"] + [k for k, v in FORFAITS.items() if v["type"] == "Installation"],
    format_func=lambda k: f"{FORFAITS[k]['description']} ({FORFAITS[k]['tarif']} €)" if k != "Aucun" else "Aucun",
)

# Sélection des autres forfaits avec quantités
st.write("### Ajoutez les forfaits de suivi et de consommables :")
autres_forfaits = {}
for key, value in FORFAITS.items():
    if value["type"] != "Installation":
        quantite = st.number_input(f"Quantité pour {value['description']} ({value['tarif']} €)", min_value=0, step=1, key=key)
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

    # Affichage du total
    st.success(f"💰 Coût total : {total:.2f} €")

# Footer
st.caption("🩺 Calculatrice développée pour respecter les règles LPPR.")
