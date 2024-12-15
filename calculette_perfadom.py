import streamlit as st

# Tarifs et descriptions pour PERFADOM, Nutrition Entérale, Parentérale, et Immunothérapie
FORFAITS = {
    # PERFADOM
    "PERFADOM 1": {
        "description": "Installation initiale - Système actif électrique",
        "tarif": 390.00,
        "frequence": "Unique",
    },
    "PERFADOM 4": {
        "description": "Installation initiale - Diffuseur",
        "tarif": 250.00,
        "frequence": "Unique",
    },
    "PERFADOM 6": {
        "description": "Installation initiale - Perfusion par gravité",
        "tarif": 50.00,
        "frequence": "Unique",
    },
    "PERFADOM 7": {
        "description": "Suivi hebdomadaire - Système actif électrique",
        "tarif": 110.00,
        "frequence": "Hebdomadaire",
    },
    "PERFADOM 8": {
        "description": "Suivi hebdomadaire - Diffuseur",
        "tarif": 50.00,
        "frequence": "Hebdomadaire",
    },
    "PERFADOM 10": {
        "description": "Consommables - 1 perfusion/semaine avec système actif ou diffuseur",
        "tarif": 39.00,
        "frequence": "Hebdomadaire",
    },
    "PERFADOM 13": {
        "description": "Consommables - 1 perfusion/jour avec système actif ou diffuseur",
        "tarif": 269.00,
        "frequence": "Quotidien",
    },
    "PERFADOM 18": {
        "description": "Consommables - 1 perfusion/jour par gravité",
        "tarif": 83.00,
        "frequence": "Quotidien",
    },
    # Nutrition Entérale
    "Nutrition Entérale 1": {
        "description": "Installation initiale - Nutrition entérale",
        "tarif": 150.00,
        "frequence": "Unique",
    },
    "Nutrition Entérale 2": {
        "description": "Suivi hebdomadaire - Nutrition entérale",
        "tarif": 60.00,
        "frequence": "Hebdomadaire",
    },
    # Nutrition Parentérale
    "Nutrition Parentérale 1": {
        "description": "Installation initiale - Nutrition parentérale avec pompe",
        "tarif": 450.00,
        "frequence": "Unique",
    },
    "Nutrition Parentérale 2": {
        "description": "Suivi hebdomadaire - Nutrition parentérale avec pompe",
        "tarif": 200.00,
        "frequence": "Hebdomadaire",
    },
    # Immunothérapie
    "Immunothérapie 1": {
        "description": "Installation initiale - Immunothérapie avec pompe",
        "tarif": 500.00,
        "frequence": "Unique",
    },
    "Immunothérapie 2": {
        "description": "Suivi hebdomadaire - Immunothérapie",
        "tarif": 250.00,
        "frequence": "Hebdomadaire",
    },
}

# Titre de l'application
st.title("Calculatrice PERFADOM, Nutrition et Immunothérapie")

st.write("""
Cette application permet de calculer automatiquement le coût total d'un traitement en fonction du type de forfait (PERFADOM, nutrition entérale, nutrition parentérale ou immunothérapie), de la durée et de la fréquence.
""")

# Sélection du forfait
forfait_selectionne = st.selectbox(
    "Sélectionnez le forfait :",
    options=list(FORFAITS.keys()),
    format_func=lambda key: f"{key} - {FORFAITS[key]['description']}",
)

# Affichage des détails du forfait
forfait_details = FORFAITS[forfait_selectionne]
st.write(f"**Description :** {forfait_details['description']}")
st.write(f"**Tarif :** {forfait_details['tarif']} €")
st.write(f"**Fréquence d'application :** {forfait_details['frequence']}")

# Entrée : Durée du traitement
if forfait_details["frequence"] != "Unique":
    duree = st.number_input(
        "Durée du traitement (en jours) :", 
        min_value=1, 
        step=1
    )
else:
    duree = 1
    st.write("Ce forfait est appliqué une seule fois (installation).")

# Calcul automatique du coût
if st.button("Calculer le coût total"):
    tarif = forfait_details["tarif"]
    frequence = forfait_details["frequence"]

    if frequence == "Quotidien":
        total = tarif * duree
    elif frequence == "Hebdomadaire":
        total = tarif * (duree // 7 + (1 if duree % 7 > 0 else 0))  # On arrondit à la semaine supérieure
    elif frequence == "Unique":
        total = tarif
    else:
        total = 0

    # Affichage du résultat
    st.success(f"Coût total : {total:.2f} €")

# Footer
st.caption("Application créée pour calculer les coûts PERFADOM, Nutrition et Immunothérapie.")
