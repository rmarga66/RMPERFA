import streamlit as st
import pandas as pd

# Données complètes : Installation, Suivi, Consommables (PERFADOM, NUT ENT, NUT PAR, IMMUNO)
FORFAITS = {
    # Installations
    "SA_I1": {"description": "Installation 1 - Système actif électrique", "tarif": 297.67, "type": "Installation", "cat": "SA"},
    "DIFF_I1": {"description": "Installation 1 - Diffuseur", "tarif": 190.81, "type": "Installation", "cat": "DIFF"},
    "GRAV_I1": {"description": "Installation et suivi - Gravité", "tarif": 38.16, "type": "Installation", "cat": "GRAV"},
    "NUT_ENT_I": {"description": "Installation - Nutrition entérale", "tarif": 146.53, "type": "Installation", "cat": "NUT_ENT"},
    "NUT_PAR_I": {"description": "Installation - Nutrition parentérale", "tarif": 325.00, "type": "Installation", "cat": "NUT_PAR"},

    # Suivi
    "SA_S1": {"description": "Suivi hebdomadaire - Système actif", "tarif": 83.95, "type": "Suivi", "cat": "SA"},
    "DIFF_S1": {"description": "Suivi hebdomadaire - Diffuseur", "tarif": 38.16, "type": "Suivi", "cat": "DIFF"},
    "NUT_ENT_S1": {"description": "Suivi hebdomadaire - Nutrition entérale sans pompe", "tarif": 50.33, "type": "Suivi", "cat": "NUT_ENT"},
    "NUT_ENT_S2": {"description": "Suivi hebdomadaire - Nutrition entérale avec pompe", "tarif": 68.52, "type": "Suivi", "cat": "NUT_ENT"},
    "NUT_PAR_S1": {"description": "Suivi hebdomadaire - Nutrition parentérale", "tarif": 158.33, "type": "Suivi", "cat": "NUT_PAR"},

    # Consommables
    "SA_C1": {"description": "Consommables - 1 perf/jour système actif", "tarif": 200.12, "type": "Consommables", "cat": "SA"},
    "DIFF_C1": {"description": "Consommables - 1 perf/jour diffuseur", "tarif": 180.10, "type": "Consommables", "cat": "DIFF"},
    "IMMUNO_SC_C": {"description": "Immunothérapie SC - 1 perf/semaine", "tarif": 39.96, "type": "Consommables", "cat": "IMMUNO"},
    "IMMUNO_IV_C": {"description": "Immunothérapie IV - 1 perf/jour", "tarif": 39.96, "type": "Consommables", "cat": "IMMUNO"},
    "NUT_PAR_C": {"description": "Consommables - Nutrition parentérale", "tarif": 95.84, "type": "Consommables", "cat": "NUT_PAR"},
}

# Interface utilisateur Streamlit
st.title("💉 Calculatrice LPPR Complète - Filtrée")

# Choix du forfait d'installation
st.header("📌 Choix du forfait d'installation")
installations = {k: v for k, v in FORFAITS.items() if v["type"] == "Installation"}
installation_key = st.selectbox(
    "Sélectionnez un forfait d'installation :", ["Aucun"] + list(installations.keys()),
    format_func=lambda k: f"{installations[k]['description']} ({installations[k]['tarif']} €)" if k != "Aucun" else "Aucun"
)

# Déterminer la catégorie sélectionnée
selected_cat = installations[installation_key]["cat"] if installation_key != "Aucun" else None

# Filtrer les suivis en fonction de la catégorie sélectionnée
st.header("📋 Forfaits de suivi")
if selected_cat:
    suivis = {k: v for k, v in FORFAITS.items() if v["type"] == "Suivi" and v["cat"] == selected_cat}
else:
    suivis = {}

suivi_selectionnes = {}
for key, value in suivis.items():
    qte = st.number_input(f"{value['description']} ({value['tarif']} €)", min_value=0, step=1, key=f"suivi_{key}")
    if qte > 0:
        suivi_selectionnes[key] = qte

# Consommables disponibles sans restriction
st.header("🛠️ Forfaits de consommables")
consommables = {k: v for k, v in FORFAITS.items() if v["type"] == "Consommables"}
conso_selectionnes = {}
for key, value in consommables.items():
    qte = st.number_input(f"{value['description']} ({value['tarif']} €)", min_value=0, step=1, key=f"conso_{key}")
    if qte > 0:
        conso_selectionnes[key] = qte

# Calcul et affichage du récapitulatif
if st.button("🧮 Calculer le coût total"):
    total = 0
    details = []

    # Installation
    if installation_key != "Aucun":
        total += installations[installation_key]["tarif"]
        details.append([installations[installation_key]["description"], 1, installations[installation_key]["tarif"]])

    # Suivis
    for key, qte in suivi_selectionnes.items():
        cout = suivis[key]["tarif"] * qte
        total += cout
        details.append([suivis[key]["description"], qte, cout])

    # Consommables
    for key, qte in conso_selectionnes.items():
        cout = consommables[key]["tarif"] * qte
        total += cout
        details.append([consommables[key]["description"], qte, cout])

    # Affichage du tableau récapitulatif
    df = pd.DataFrame(details, columns=["Description", "Quantité", "Coût total (€)"])
    st.table(df)

    st.success(f"💰 Coût total global : {total:.2f} €")
