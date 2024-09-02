import csv
import os

def sauvegarder_options(fichier_csv, options):
    """
    Sauvegarde les options dans un fichier CSV au format option:valeur.

    :param fichier_csv: Chemin du fichier CSV où les options seront sauvegardées.
    :param options: Dictionnaire contenant les options à sauvegarder.
    """
    with open(fichier_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        for option, valeur in options.items():
            writer.writerow([option, valeur])

def recuperer_options_avec_creation(fichier_csv, options_defaut=None):
    """
    Vérifie si le fichier CSV existe. Si oui, récupère les options.
    Si non, crée le fichier avec des options par défaut.

    :param fichier_csv: Chemin du fichier CSV à lire ou à créer.
    :param options_defaut: Dictionnaire contenant les options par défaut à utiliser si le fichier n'existe pas.
    :return: Dictionnaire contenant les options récupérées ou les options par défaut.
    """
    options = {}

    # Vérifie si le fichier existe
    if os.path.exists(fichier_csv):
        # Lire les options du fichier CSV
        with open(fichier_csv, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:  # Assure-toi que la ligne contient bien deux éléments
                    option, valeur = row
                    options[option] = valeur
    else:
        # Si le fichier n'existe pas, utilise les options par défaut et crée le fichier
        if options_defaut:
            options = options_defaut
            sauvegarder_options(fichier_csv, options_defaut)
    
    return options