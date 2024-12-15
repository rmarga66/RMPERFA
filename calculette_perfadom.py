import tkinter as tk
from tkinter import messagebox

# Tarifs PERFADOM (exemple basique)
TARIFS = {
    "PERFADOM 1": 390.00,
    "PERFADOM 4": 250.00,
    "PERFADOM 6": 50.00,
    "PERFADOM 7": 110.00,
    "PERFADOM 8": 50.00,
    "PERFADOM 10": 39.00,
    "PERFADOM 13": 269.00,
    "PERFADOM 18": 83.00,
}

# Fonction de calcul
def calculer_cout():
    try:
        type_perfusion = type_perfusion_var.get()
        duree = int(duree_var.get())
        frequence = frequence_var.get()

        # Récupérer le tarif correspondant
        tarif = TARIFS.get(type_perfusion, 0)
        
        if frequence == "Quotidien":
            total = tarif * duree
        elif frequence == "Hebdomadaire":
            total = tarif * (duree // 7)
        else:
            total = 0

        # Afficher le résultat
        result_label.config(text=f"Coût total : {total:.2f} €")
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer une durée valide.")

# Interface utilisateur
app = tk.Tk()
app.title("Calculatrice PERFADOM")

# Type de perfusion
tk.Label(app, text="Type de perfusion :").grid(row=0, column=0, padx=10, pady=10)
type_perfusion_var = tk.StringVar()
type_perfusion_menu = tk.OptionMenu(app, type_perfusion_var, *TARIFS.keys())
type_perfusion_menu.grid(row=0, column=1, padx=10, pady=10)

# Fréquence
tk.Label(app, text="Fréquence :").grid(row=1, column=0, padx=10, pady=10)
frequence_var = tk.StringVar()
frequence_menu = tk.OptionMenu(app, frequence_var, "Quotidien", "Hebdomadaire")
frequence_menu.grid(row=1, column=1, padx=10, pady=10)

# Durée
tk.Label(app, text="Durée (en jours) :").grid(row=2, column=0, padx=10, pady=10)
duree_var = tk.StringVar()
duree_entry = tk.Entry(app, textvariable=duree_var)
duree_entry.grid(row=2, column=1, padx=10, pady=10)

# Bouton de calcul
calculer_btn = tk.Button(app, text="Calculer", command=calculer_cout)
calculer_btn.grid(row=3, column=0, columnspan=2, pady=20)

# Résultat
result_label = tk.Label(app, text="Coût total : -")
result_label.grid(row=4, column=0, columnspan=2, pady=10)

# Lancer l'application
app.mainloop()
