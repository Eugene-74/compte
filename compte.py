import csv
import os
from tkinter import Tk, Label, Entry, Button, Text, END, StringVar, OptionMenu, ttk 
from datetime import datetime
import shutil
from pathlib import Path

# Chemin du fichier CSV
CSV_FILE = "save/expenses.csv"

# Liste des catégories
categories = ["Nourriture", "Vie quotidienne", "Santé", "Loisir", "Vêtement", "Transport", "Coiffeur", "Épargne"]
# Liste des mois et des catégories
lMois = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
categoriess = ['Mois','Nourriture', 'Vie quotidienne', 'Santé', 'Loisir', 'Vêtement', 'Transport', 'Coiffeur', 'Épargne', 'Total']
months = ["Tous", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
years = ["Tous", "2022", "2023", "2024"]  # Mettre à jour avec les années disponibles dans votre CSV

directory_path = Path('save')

if not directory_path.exists():
    directory_path.mkdir(parents=True, exist_ok=False)

# Fonction pour ajouter une dépense
def add_expense():
    name = name_var.get()
    date = date_var.get()
    price = price_var.get()
    category = category_var.get()
    description = description_text.get("1.0", END).strip()

    
    if name and date and price and category:
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([name, date, price, category, description])
        load_expenses()
    else:
        print("Tous les champs doivent être remplis")

    now = datetime.now()

    date_str = now.strftime('%Y-%m-%d')

    autoSavePath = "save/" + date_str + ".csv"

    

    with open(autoSavePath, 'w') as file:
        file.write("")
    shutil.copy(CSV_FILE, autoSavePath)

# Fonction pour charger et afficher les dépenses
def load_expenses():
    clear_table()

    # Récupérer le mois et l'année sélectionnés
    selected_year = year_var.get()
    selected_month = month_var.get()




    

    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                name, date, price, category, description = row
                price = float(price)
                if ("Tous" == selected_year) or ((selected_year == date.split('/')[2] and date.split('/')[1] == selected_month)or  selected_month == "Tous") :
                    if(price >0):
                        expenses_table.insert("", "end", values=(name, date, f"{price:.2f}", category, description), tags=('red',))
                    else :
                        expenses_table.insert("", "end", values=(name, date, f"{price:.2f}", category, description), tags=('green',))


    update_totals()

# Fonction pour effacer le tableau des dépenses
def clear_table():
    expenses_table.delete(*expenses_table.get_children())

# Fonction pour mettre à jour les totaux par catégorie et total général
def update_totals():

    for mois in lMois :
        totals = {cat: 0 for cat in categories}
        totals["Nourriture"] = 212
        totals["Vie quotidienne"] = 30
        totals["Santé"] = 20
        totals["Loisir"] = 30
        totals["Vêtement"] = 30
        totals["Transport"] = 84
        totals["Coiffeur"] = 12
        totals["Epargne"] = 0

        selected_year = year_var.get()
        # total_general = totals["Nourriture"] +totals["Vie quotidienne"]+ totals["Santé"]+totals["Loisir"]+totals["Vêtement"]+totals["Transport"]+totals["Coiffeur"]+ totals["Epargne"]

        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    name, date, price, category, description = row
                    price = float(price)
                    # TODO SELECTED MONTH
                    # Vérifier si la dépense correspond au mois et à l'année sélectionnés
                    if((lMois[int(date.split('/')[1])-1]) == mois) and (date.split('/')[2] == selected_year):
                        # print("modif")
                        if (category == "Epargne"):
                            totals[category] += price
                        else :
                            totals[category] -= price
                        
        total_general = totals["Nourriture"] +totals["Vie quotidienne"]+ totals["Santé"]+totals["Loisir"]+totals["Vêtement"]+totals["Transport"]+totals["Coiffeur"]
        # + totals["Epargne"]
    


        # total = 0
        for cat in categories:

        # for j, categorie in enumerate(categories):  # Exclure la colonne Total
            value = totals[cat]
            try:
                value = float(value)
            except ValueError:
                value = 0.0
        
                

            table.set(mois,cat,f"{value:.2f}")
        table.set(mois, 'Total', f"{total_general:.2f}")

#  TODO COULEUR PAR CASE
    for item in table.get_children():
        values = table.item(item, 'values')
        # print(values[9])
        if float(values[9]) > 0 :  # Supposons que le nom est dans la première colonne
            current_tags = table.item(item, 'tags')
            # new_tags = tuple(set(current_tags) | {"gree"})
            table.item(item, tags="green")
        else :
            current_tags = table.item(item, 'tags')
            # new_tags = tuple(set(current_tags) | {"gree"})
            table.item(item, tags="red")

# Fonction pour supprimer une dépense sélectionnée
def delete_expense():
    selected_item = expenses_table.selection()
    if selected_item:
        # Récupérer les valeurs de la dépense sélectionnée
        item_values = expenses_table.item(selected_item, "values")
        name = item_values[0]
        date = item_values[1]
        price = item_values[2]
        category = item_values[3]
        description = item_values[4]
        
        # Ouvrir le fichier CSV et supprimer la ligne correspondante
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            rows = list(csv.reader(file))
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for row in rows:
                if row[0] != name or row[1] != date  or row[3] != category or row[4] != description:
                    writer.writerow(row)
        
        # Recharger les dépenses après suppression
        load_expenses()




# Configuration de l'interface graphique
root = Tk()
root.title("Gestion des Comptes")

# Variables pour les champs d'entrée
name_var = StringVar()
date_var = StringVar()
price_var = StringVar()
category_var = StringVar()
category_var.set(categories[0])

# Widgets pour les champs d'entrée
Label(root, text="Nom").grid(row=0, column=0)
Entry(root, textvariable=name_var).grid(row=0, column=1)

Label(root, text="Date (JJ/MM/AAAA)").grid(row=1, column=0)
Entry(root, textvariable=date_var).grid(row=1, column=1)

Label(root, text="Prix").grid(row=2, column=0)
Entry(root, textvariable=price_var).grid(row=2, column=1)

Label(root, text="Catégorie").grid(row=3, column=0)
OptionMenu(root, category_var, *categories).grid(row=3, column=1)

Label(root, text="Description").grid(row=4, column=0)
description_text = Text(root, height=1, width=15)
description_text.grid(row=4, column=1)

# Bouton pour ajouter une dépense
Button(root, text="Ajouter Dépense", command=add_expense).grid(row=5, column=1)

current_date_time = datetime.now()




# Menu déroulant pour sélectionner le mois et l'année
# Label(root, text="Filtrer par mois et année:").grid(row=7, column=0)

month_var = StringVar()
month_menu = OptionMenu(root, month_var, *months)
month_menu.grid(row=6, column=2)

if(current_date_time.month<10):
    month_var.set( "0" + str(current_date_time.month))
else :
    month_var.set(current_date_time.month)
    


# Vous pouvez personnaliser les années selon celles présentes dans votre CSV
year_var = StringVar()
year_menu = OptionMenu(root, year_var, *years)
year_menu.grid(row=6, column=3)
year_var.set(current_date_time.year)

# Tableau pour afficher les dépenses
expenses_table = ttk.Treeview(root, columns=("Nom", "Date", "Prix", "Catégorie", "Description"), show="headings")
expenses_table.heading("Nom", text="Nom")
expenses_table.heading("Date", text="Date")
expenses_table.heading("Prix", text="Prix")
expenses_table.heading("Catégorie", text="Catégorie")
expenses_table.heading("Description", text="Description")
expenses_table.grid(row=7, column=0, columnspan=4)

expenses_table.tag_configure('red', background='light sky blue')
expenses_table.tag_configure('green', background='lightgreen')

# Bouton pour supprimer une dépense sélectionnée
Button(root, text="Supprimer Dépense", command=delete_expense).grid(row=6, column=1)

# Zone de texte pour afficher les totaux
# expenses_list = Text(root, height=15, width=60)
# expenses_list.grid(row=9, column=0, columnspan=3)

# Bouton pour charger les dépenses
Button(root, text="Mettre à jour", command=load_expenses).grid(row=6, column=0)





# TOTAL SOMME






# Créer le cadre principal
mainframe = ttk.Frame(root, padding="10")
mainframe.grid(row=10, column=0, columnspan=4)

# Créer le tableau avec Treeview
table = ttk.Treeview(mainframe, columns=categoriess, show='headings')
table.grid(row=10, column=0, columnspan=4)

table.tag_configure('red', background='salmon')
table.tag_configure('green', background='lightgreen')

# Définir les en-têtes de colonnes
for categorie in categoriess:
    table.heading(categorie, text=categorie)

# Ajuster la largeur des colonnes
for categorie in categoriess:
    table.column(categorie, width=100)

# Ajouter les lignes pour chaque mois
for i, mois in enumerate(lMois):    
    table.insert('', 'end', iid=mois, values=(mois, *["" for _ in categoriess[:-1]], "0.00"))


# Bouton pour mettre à jour les totaux
# update_button = ttk.Button(mainframe, text="Mettre à jour", command=mettre_a_jour_totaux)
# update_button.grid(row=len(mois) + 1, column=0, columnspan=len(categoriess), pady=10)

# Configurer la mise en forme de la grille
for i in range(len(mois) + 2):
    mainframe.rowconfigure(i, weight=1)
for j in range(len(categoriess)):
    mainframe.columnconfigure(j, weight=1)











# Lancer la boucle principale de l'interface graphique
load_expenses()
root.mainloop()

