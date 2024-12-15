import streamlit as st
import pandas as pd

# Données des forfaits complets
FORFAITS_INSTALLATION = {
    "PERFADOM1": {"description": "Installation 1 - Système actif électrique", "tarif": 297.67},
    "PERFADOM2": {"description": "Installation 2 - Système actif électrique", "tarif": 137.38},
    "PERFADOM3": {"description": "Installation rempli ES - Système actif électrique", "tarif": 137.38},
    "PERFADOM4": {"description": "Installation 1 - Diffuseur", "tarif": 190.81},
    "PERFADOM5": {"description": "Installation 2 - Diffuseur", "tarif": 87.77},
    "PERFADOM6": {"description": "Installation et suivi - Gravité", "tarif": 38.16},
}

FORFAITS_SUIVI = {
    "PERFADOM7": {"description": "Suivi hebdo - Système actif", "tarif": 83.95},
    "PERFADOM8": {"description": "Suivi hebdo - Diffuseur", "tarif": 38.16},
    "NUT_ENT2": {"description": "Suivi hebdo - Nutrition entérale sans pompe", "tarif": 50.33},
    "NUT_ENT3": {"description": "Suivi hebdo - Nutrition entérale avec pompe", "tarif": 68.52},
}

FORFAITS_CONSO = {
    "PERFADOM17": {"description": "Consommables Gravité < 15 perf/28 jours", "tarif": 9.00},
    "PERFADOM18": {"description": "Consommables Gravité - 1 perf/j", "tarif": 63.35},
    "PERFADOM30": {"description": "Consommables Système actif - 1 perf/j", "tarif": 200.12},
    "PERFADOM31": {"description": "Consommables Système actif - 2 perf/j", "tarif": 379.14},
    "PERFADOM37": {"description": "Consommables Diffuseur - 1 perf/j", "tarif": 180.10},
    "IMMUNO_SC": {"description": "Consommables Immunothérapie SC - 1 perf", "tarif": 39.96},
    "IMMUNO_IV": {"description": "Consommables Immunothérapie IV - 1 perf/j", "tarif": 39.96},
}

# Fonction pour afficher un tableau récapitulatif
def afficher_tableau(forfaits_selectionnes):
    if not forfaits_selectionnes:
        st.warning("Aucun forfait sélectionné.")
        return

    # Créer un tableau récapitulatif
    data = [
        {"Catégorie": cat, "Description": val["description"], "Quantité": qte, "Coût total (€)": val["tarif"] * qte}
        for cat, forfaits in forfaits_selectionnes.items()
        for key, (val, qte) in forfaits.items()
        if qte > 0
    ]
    df = pd.DataFrame(data)
    st.table(df)

    # Calcul du coût total global
    total = sum(item["Coût total (€)"] for item in data)
    st.success(f"💰 **Coût total global : {total:.2f} €**")

# Interface utilisateur Streamlit
st.title("💉 Calculatrice Complète - LPPR")
st.write("Sélectionnez vos forfaits et les quantités associées pour calculer le coût total.")

# Sélection des forfaits par catégories
st.header("📌 Forfaits d'installation")
installation_key = st.selectbox(
    "Choisissez un forfait d'installation :", 
    options=["Aucun"] + list(FORFAITS_INSTALLATION.keys()),
    format_func=lambda k: f"{FORFAITS_INSTALLATION[k]['description']} ({FORFAITS_INSTALLATION[k]['tarif']} €)" if k != "Aucun" else "Aucun",
)

st.header("📋 Forfaits de suivi")
suivi_selectionnes = {}
for key, val in FORFAITS_SUIVI.items():
    qte = st.number_input(f"{val['description']} ({val['tarif']} €)", min_value=0, step=1, key=f"suivi_{key}")
    if qte > 0:
        suivi_selectionnes[key] = (val, qte)

st.header("🛠️ Forfaits de consommables")
conso_selectionnes = {}
for key, val in FORFAITS_CONSO.items():
    qte = st.number_input(f"{val['description']} ({val['tarif']} €)", min_value=0, step=1, key=f"conso_{key}")
    if qte > 0:
        conso_selectionnes[key] = (val, qte)

# Récapitulatif et calcul
if st.button("🧮 Calculer le coût total"):
    forfaits_selectionnes = {}
    if installation_key != "Aucun":
        forfaits_selectionnes["Installation"] = {installation_key: (FORFAITS_INSTALLATION[installation_key], 1)}
    if suivi_selectionnes:
        forfaits_selectionnes["Suivi"] = suivi_selectionnes
    if conso_selectionnes:
        forfaits_selectionnes["Consommables"] = conso_selectionnes

    afficher_tableau(forfaits_selectionnes)
