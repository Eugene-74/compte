import csv
import os
from tkinter import Tk, Label, Entry, Button, Text, END, StringVar, OptionMenu, ttk 
from datetime import datetime
import shutil
from pathlib import Path
from tkinter import messagebox

# Chemin du fichier CSV
CSV_FILE = "save/expenses.csv"
CSV_FILE_BUDGET = 'save/budget_mensuel.csv'

if not os.path.exists(CSV_FILE_BUDGET):
        with open(CSV_FILE_BUDGET, 'w', newline='') as csvfile:
            print('creating')

def mois_en_nombre(mois):
    mois_dict = {
        "janvier": "01",
        "février": "02",
        "mars": "03",
        "avril": "04",
        "mai": "05",
        "juin": "06",
        "juillet": "07",
        "août": "08",
        "septembre": "09",
        "octobre": "10",
        "novembre": "11",
        "décembre": "12"
    }
    
    mois = mois.lower()
    if mois in mois_dict:
        return mois_dict[mois]
    else:
        return None

# Liste des catégories
categories = ["Nourriture", "Vie quotidienne", "Santé", "Loisir", "Vêtement", "Transport", "Coiffeur", "Épargne"]
# budget = [212,30,20,30,30,84,12,0]

# Liste des mois et des catégories
lMois = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']

categoriess = ['Mois','Nourriture', 'Vie quotidienne', 'Santé', 'Loisir', 'Vêtement', 'Transport', 'Coiffeur', 'Épargne', 'Total']

months = ["Tous", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
years = ["Tous", "2022", "2023", "2024"]  # Mettre à jour avec les années disponibles dans votre CSV

directory_path = Path('save')

if not directory_path.exists():
    directory_path.mkdir(parents=True, exist_ok=False)

def get_month_index(mois):
    return lMois.index(mois)

def trier_colonne(tv, col, type_donnees):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    
    if type_donnees == 'date':
        l.sort(key=lambda t: datetime.strptime(t[0], '%d/%m/%Y'))
    elif type_donnees == 'prix':
        l.sort(key=lambda t: float(t[0]),reverse = True)
    elif type_donnees == 'mois':
        l.sort(key=lambda t: get_month_index(t[1]))
        # TODO trier dans l'ordre des mois
    else:
        l.sort(key=lambda t: t[0])
    
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)
    
    tv.heading(col, command=lambda: trier_colonne(tv, col, type_donnees))




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
    updateBudget()
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
                if ("Tous" == selected_year) or ((selected_year == date.split('/')[2] and date.split('/')[1] == selected_month)or  (selected_month == "Tous"and selected_year == date.split('/')[2])) :
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
        selected_year = year_var.get()

        totals = get_budget_for_month_year(mois_en_nombre(mois),selected_year)

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
                        
                        # print(category)
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
# root.attributes('-fullscreen', True)
root.update_idletasks()
root.state('zoomed')
max_width = root.winfo_screenwidth()
max_height = root.winfo_screenheight()
# root.geometry(str(max_width)+'x'+str(max_height))
# print(f"Largeur: {width}, Hauteur: {height}")


# Variables pour les champs d'entrée
name_var = StringVar()
date_var = StringVar()
price_var = StringVar()
category_var = StringVar()
category_var.set(categories[0])

depenseFrame = ttk.Frame(root, padding="10")
depenseFrame.grid(row=0, column=0)


# Widgets pour les champs d'entrée
Label(depenseFrame, text="Ajouter une dépense").grid(row=0, column=0,columnspan=2)


Label(depenseFrame, text="Nom").grid(row=1, column=0)
Entry(depenseFrame, textvariable=name_var).grid(row=1, column=1)

Label(depenseFrame, text="Date (JJ/MM/AAAA)").grid(row=2, column=0)
Entry(depenseFrame, textvariable=date_var).grid(row=2, column=1)

Label(depenseFrame, text="Prix").grid(row=3, column=0)
Entry(depenseFrame, textvariable=price_var).grid(row=3, column=1)

Label(depenseFrame, text="Catégorie").grid(row=4, column=0)
OptionMenu(depenseFrame, category_var, *categories).grid(row=4, column=1)

Label(depenseFrame, text="Description").grid(row=5, column=0)
description_text = Text(depenseFrame, height=1, width=15)
description_text.grid(row=5, column=1)

# Bouton pour ajouter une dépense
submit_button = ttk.Button(depenseFrame,text="Ajouter", command=add_expense)
submit_button.grid(row=6, column=0,columnspan=2)
# Button(root, text="Ajouter", command=add_expense).grid(row=6, column=0,columnspan=2)

current_date_time = datetime.now()




# Menu déroulant pour sélectionner le mois et l'année
# Label(root, text="Filtrer par mois et année:").grid(row=7, column=0)

dateFrame = ttk.Frame(root, padding="10")
dateFrame.grid(row=1, column=0)

month_var = StringVar()
month_menu = OptionMenu(dateFrame, month_var, *months)
month_menu.grid(row=0, column=0)

if(current_date_time.month<10):
    month_var.set( "0" + str(current_date_time.month))
else :
    month_var.set(current_date_time.month)
    


# Vous pouvez personnaliser les années selon celles présentes dans votre CSV
year_var = StringVar()
year_menu = OptionMenu(dateFrame, year_var, *years)
year_menu.grid(row=0, column=1)
year_var.set(current_date_time.year)

submit_button = ttk.Button(dateFrame, text="Mettre à jour", command=load_expenses)
submit_button.grid(row=0, column=2)

# Button(dateFrame, text="Mettre à jour", command=load_expenses).grid(row=0, column=2  )

expensesFrame = ttk.Frame(root, padding="10")
expensesFrame.grid(row=0, column=1)

# Tableau pour afficher les dépenses
expenses_table = ttk.Treeview(expensesFrame, columns=("Nom", "Date", "Prix", "Catégorie", "Description"), show="headings")
expenses_table.heading("Nom", text="Nom", command=lambda: trier_colonne(expenses_table, 'Nom', 'texte'))
expenses_table.heading("Date", text="Date", command=lambda: trier_colonne(expenses_table, 'Date', 'date'))
expenses_table.heading("Prix", text="Prix", command=lambda: trier_colonne(expenses_table, 'Prix', 'prix') )
expenses_table.heading("Catégorie", text="Catégorie", command=lambda: trier_colonne(expenses_table, 'Catégorie', 'texte'))
expenses_table.heading("Description", text="Description", command=lambda: trier_colonne(expenses_table, 'Description', 'texte'))
expenses_table.grid(row=0, column=0)

expenses_table.column('Nom', width=200)
expenses_table.column('Date', width=100)
expenses_table.column('Prix', width=100)
expenses_table.column('Catégorie', width=100)
expenses_table.column('Description', width=500)

expenses_table.tag_configure('red', background='light sky blue')
expenses_table.tag_configure('green', background='lightgreen')

# Bouton pour supprimer une dépense sélectionnée
# Button(root, text="Supprimer Dépense", command=delete_expense).grid(row=9, column=1)
submit_button = ttk.Button(expensesFrame, text="Supprimer dépense", command=delete_expense)
submit_button.grid(row=1, column=0)

# Zone de texte pour afficher les totaux
# expenses_list = Text(root, height=15, width=60)
# expenses_list.grid(row=9, column=0, columnspan=3)

# Bouton pour charger les dépenses






# TOTAL SOMME






# Créer le cadre principal
# mainframe = ttk.Frame(root, padding="10")
# mainframe.grid(row=30, column=0, columnspan=4)

# Créer le tableau avec Treeview
table = ttk.Treeview(root, columns=categoriess, show='headings')
table.grid(row=2, column=1)
table["height"] = 12

table.tag_configure('red', background='salmon')
table.tag_configure('green', background='lightgreen')

# Définir les en-têtes de colonnes
for categorie in categoriess:
    if (categorie == "Mois"):
        table.heading(categorie, text=categorie, command=lambda: trier_colonne(table, categorie, 'mois'))
    else :
        table.heading(categorie, text=categorie, command=lambda: trier_colonne(table, categorie, 'prix'))
    

# Ajuster la largeur des colonnes
for categorie in categoriess:
    table.column(categorie, width=100)

# Ajouter les lignes pour chaque mois
for i, mois in enumerate(lMois):
    table.insert('', 'end', iid=mois, values=(mois, *["" for _ in categoriess[:-1]], "0.00"))


# Configurer la mise en forme de la grille
for i in range(len(mois) + 2):
    root.rowconfigure(i, weight=1)
for j in range(len(categoriess)):
    root.columnconfigure(j, weight=1)


# Fonction pour récupérer les valeurs des entrées et les sauvegarder dans un fichier CSV
def save_budget():
    budgets = {}
    for category, entry in entries.items():
        try:
            budgets[category] = float(entry.get())
        except ValueError:
            messagebox.showerror("Erreur de saisie", f"Veuillez entrer un nombre valide pour le budget de {category}")
            return

    month = month_var.get()
    year = year_var.get()
    if(month == "Tous"):
        for month in lMois :
            with open(CSV_FILE_BUDGET, 'a', newline='') as csvfile:
                fieldnames = ['Mois', 'Année'] + categories
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Écrire l'en-tête seulement si le fichier est vide
                if csvfile.tell() == 0:
                    writer.writeheader()

                row = {'Mois': mois_en_nombre(month), 'Année': year}
                row.update(budgets)
                writer.writerow(row)

        messagebox.showinfo("Succès", "Le budget a été enregistré avec succès pour tous les mois de cette année")
    else :
        if not month.isdigit() or not year.isdigit():
            messagebox.showerror("Erreur de saisie", "Veuillez entrer un mois et une année valides")
            return

        month = int(month)
        year = int(year)

        if month < 1 or month > 12 or year < 1:
            messagebox.showerror("Erreur de saisie", "Veuillez entrer un mois (1-12) et une année valides")
            return

        # Enregistrer dans un fichier CSV
        with open(CSV_FILE_BUDGET, 'a', newline='') as csvfile:
            fieldnames = ['Mois', 'Année'] + categories
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Écrire l'en-tête seulement si le fichier est vide
            if csvfile.tell() == 0:
                writer.writeheader()

            row = {'Mois': month, 'Année': year}
            row.update(budgets)
            writer.writerow(row)

        messagebox.showinfo("Succès", "Le budget a été enregistré avec succès pour le mois "+str(month)+"/"+str(year))



# Création d'un cadre pour organiser les widgets
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=2,rowspan= 7)




# Fonction pour lire le CSV et récupérer le budget pour un mois et une année précise
def get_budget_for_month_year(month,year):
    

    if (month == "Tous" or year == "Tous"):
        return {cat: 0 for cat in categories}

    if not month.isdigit() or not year.isdigit():
        messagebox.showerror("Erreur de saisie", "Veuillez entrer un mois et une année valides")
        return

    month = int(month)
    year = int(year)
    # result = {}*
    result = {cat: 0 for cat in categories}


    if month < 1 or month > 12 or year < 1:
        messagebox.showerror("Erreur de saisie", "Veuillez entrer un mois (1-12) et une année valides")
        return

    try:
        with open(CSV_FILE_BUDGET, mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row['Mois']) == month and int(row['Année']) == year:
                    # result = f"Budget pour {month}/{year}:\n"
                    for category in categories:
                        result[category] = float(row[category])
                        # result += f"{category}: {row[category]}\n"
                    # messagebox.showinfo("Budget trouvé", result)
                    return result
            # messagebox.showinfo("Pas de données", f"Aucun budget trouvé pour {month}/{year}")
            for category in categories:
                result[category] = 0
            return result

    except FileNotFoundError:
        messagebox.showerror("Erreur", "Le fichier "+CSV_FILE_BUDGET+" est introuvable")

entries = {}

budgetFrame = ttk.Frame(root, padding="10")
budgetFrame.grid(row=2, column=0)

def updateBudget():
    # Dictionnaire pour stocker les entrées
    month = month_var.get()
    year = year_var.get()
    budgets = get_budget_for_month_year(month,year)
    # Ajout des labels et des entrées pour chaque catégorie

    

    label = ttk.Label(budgetFrame, text="Saisir le budget")
    label.grid(row=0, column=0,columnspan=2)

    for i, category in enumerate(categories, start=1):
        label = ttk.Label(budgetFrame, text=category)
        label.grid(row=i, column=0, padx=5, pady=5)
        entry = ttk.Entry(budgetFrame, width=10)
        entry.grid(row=i, column=1, padx=5, pady=5)
        # entry.setvar = 12
        entry.insert(0,budgets[category])
        entries[category] = entry
updateBudget()
# Bouton pour valider les budgets

submit_button = ttk.Button(budgetFrame, text="Valider", command=save_budget)
submit_button.grid(row=len(categories) +1, column=0,columnspan=2, pady=10)

# Configuration de la grille pour l'expansion
for i in range(len(categories) + 2):
    frame.grid_rowconfigure(i, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)
frame.grid_columnconfigure(3, weight=1)




# Création d'un cadre pour organiser les widgets
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=5)



# Liste des catégories

# # Bouton pour rechercher le budget
# search_button = ttk.Button(frame, text="Rechercher", command=get_budget_for_month_year)
# search_button.grid(row=1, column=0, columnspan=4, pady=10)

# Configuration de la grille pour l'expansion
frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)
frame.grid_columnconfigure(3, weight=1)

# trier_colonne(expenses_table,1,"date")

# Lancer la boucle principale de l'interface graphique
load_expenses()
root.mainloop()

