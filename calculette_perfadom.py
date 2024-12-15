import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import tempfile
import os

# Chemin vers le logo
LOGO_PATH = "logo.png"

# Intégration complète des forfaits
FORFAITS = {
    # Installations
    "SA_I1": {"description": "Installation 1 - Système actif électrique", "tarif": 297.67, "type": "Installation", "cat": "SA"},
    "SA_I2": {"description": "Installation 2 - Système actif électrique", "tarif": 137.38, "type": "Installation", "cat": "SA"},
    "DIFF_I1": {"description": "Installation 1 - Diffuseur", "tarif": 190.81, "type": "Installation", "cat": "DIFF"},
    "DIFF_I2": {"description": "Installation 2 - Diffuseur", "tarif": 87.77, "type": "Installation", "cat": "DIFF"},
    "GRAV_I1": {"description": "Installation et suivi - Gravité", "tarif": 38.16, "type": "Installation", "cat": "GRAV"},
    "NUT_ENT_I": {"description": "Installation - Nutrition entérale", "tarif": 146.53, "type": "Installation", "cat": "NUT_ENT"},
    "NUT_PAR_I": {"description": "Installation - Nutrition parentérale", "tarif": 325.00, "type": "Installation", "cat": "NUT_PAR"},

    # Suivis
    "SA_S1": {"description": "Suivi hebdomadaire - Système actif", "tarif": 83.95, "type": "Suivi", "cat": "SA"},
    "DIFF_S1": {"description": "Suivi hebdomadaire - Diffuseur", "tarif": 38.16, "type": "Suivi", "cat": "DIFF"},
    "GRAV_S1": {"description": "Suivi hebdomadaire - Gravité", "tarif": 63.35, "type": "Suivi", "cat": "GRAV"},
    "NUT_ENT_S1": {"description": "Suivi hebdomadaire - Nutrition entérale sans pompe", "tarif": 50.33, "type": "Suivi", "cat": "NUT_ENT"},
    "NUT_ENT_S2": {"description": "Suivi hebdomadaire - Nutrition entérale avec pompe", "tarif": 68.52, "type": "Suivi", "cat": "NUT_ENT"},
    "NUT_PAR_S1": {"description": "Suivi hebdomadaire - Nutrition parentérale", "tarif": 158.33, "type": "Suivi", "cat": "NUT_PAR"},

    # Consommables par jour
    "SA_C1_D": {"description": "Consommables par jour - Système actif", "tarif": 200.12, "type": "Consommables", "cat": "SA"},
    "DIFF_C1_D": {"description": "Consommables par jour - Diffuseur", "tarif": 180.10, "type": "Consommables", "cat": "DIFF"},
    "GRAV_C1_D": {"description": "Consommables par jour - Gravité", "tarif": 120.33, "type": "Consommables", "cat": "GRAV"},

    # Consommables par semaine
    "SA_C1_W": {"description": "Consommables par semaine - Système actif", "tarif": 1300.84, "type": "Consommables", "cat": "SA"},
    "DIFF_C1_W": {"description": "Consommables par semaine - Diffuseur", "tarif": 1260.70, "type": "Consommables", "cat": "DIFF"},
    "GRAV_C1_W": {"description": "Consommables par semaine - Gravité", "tarif": 890.70, "type": "Consommables", "cat": "GRAV"},
    "NUT_PAR_C1_W": {"description": "Consommables par semaine - Nutrition parentérale", "tarif": 695.70, "type": "Consommables", "cat": "NUT_PAR"},
}

# Fonction pour générer la facture PDF
def generer_facture_pdf(details, total, nom, prenom, numero_sap):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(temp_file.name, pagesize=A4)
    width, height = A4

    # Ajout du logo
    if os.path.exists(LOGO_PATH):
        logo = ImageReader(LOGO_PATH)
        c.drawImage(logo, 50, height - 100, width=100, height=50)

    # Informations client
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 130, "Facture - Forfaits LPPR")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 160, f"Nom : {nom}")
    c.drawString(50, height - 180, f"Prénom : {prenom}")
    c.drawString(50, height - 200, f"Numéro client SAP : {numero_sap}")

    # Tableau des forfaits
    y = height - 240
    for detail in details:
        c.drawString(50, y, f"{detail[0]} - Quantité : {detail[1]} - Coût : {detail[2]:.2f} €")
        y -= 20

    # Total
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y - 20, f"Total à payer : {total:.2f} €")
    c.save()
    return temp_file.name

# Interface utilisateur Streamlit
st.set_page_config(page_title="Calculatrice LPPR", layout="wide")

# Ajout du logo en haut à gauche
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, width=100)

st.title("💉 Calculatrice LPPR Complète avec Facture")

# Informations client
st.header("📋 Informations du client")
nom = st.text_input("Nom", help="Entrez le nom du client")
prenom = st.text_input("Prénom", help="Entrez le prénom du client")
numero_sap = st.text_input("Numéro client SAP", help="Entrez le numéro SAP du client")

# Forfait d'installation
st.header("📌 Forfaits d'installation")
installation_key = st.selectbox(
    "Sélectionnez un forfait d'installation :", ["Aucun"] + [k for k, v in FORFAITS.items() if v["type"] == "Installation"],
    format_func=lambda k: f"{FORFAITS[k]['description']} ({FORFAITS[k]['tarif']} €)" if k != "Aucun" else "Aucun"
)

selected_cat = FORFAITS[installation_key]["cat"] if installation_key != "Aucun" else None

# Forfaits de suivi
st.header("📋 Forfaits de suivi")
suivi_selectionnes = {}
suivis = {k: v for k, v in FORFAITS.items() if v["type"] == "Suivi" and v["cat"] == selected_cat}
for key, value in suivis.items():
    qte = st.number_input(f"{value['description']} ({value['tarif']} €)", min_value=0, step=1, key=f"suivi_{key}")
    if qte > 0:
        suivi_selectionnes[key] = qte

# Consommables
st.header("🛠️ Consommables")
conso_selectionnes = {}
for key, value in FORFAITS.items():
    if value["type"] == "Consommables":
        qte = st.number_input(f"{value['description']} ({value['tarif']} €)", min_value=0, step=1, key=f"conso_{key}")
        if qte > 0:
            conso_selectionnes[key] = qte

# Calcul et affichage
if st.button("🧮 Calculer et Générer Facture"):
    total = 0
    details = []

    if installation_key != "Aucun":
        tarif = FORFAITS[installation_key]["tarif"]
        total += tarif
        details.append([FORFAITS[installation_key]["description"], 1, tarif])

    for key, qte in {**suivi_selectionnes, **conso_selectionnes}.items():
        tarif = FORFAITS[key]["tarif"] * qte
        total += tarif
        details.append([FORFAITS[key]["description"], qte, tarif])

    df = pd.DataFrame(details, columns=["Description", "Quantité", "Coût total (€)"])
    st.dataframe(df.style.set_properties(**{'background-color': 'turquoise', 'color': 'black'}))

    if not nom or not prenom or not numero_sap:
        st.error("⚠️ Veuillez remplir les informations du client pour générer la facture.")
    else:
        pdf_file = generer_facture_pdf(details, total, nom, prenom, numero_sap)
        with open(pdf_file, "rb") as file:
            st.download_button("💾 Télécharger la facture", file, file_name="facture_lppr.pdf", mime="application/pdf")

        st.success(f"💰 Total à payer : {total:.2f} €", icon="💶")
