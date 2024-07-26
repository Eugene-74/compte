from cx_Freeze import setup, Executable

# Nom de votre script Python
script_name = "compte.py"

# Configuration de l'exécutable
setup(
    name = "compte",
    version = "1.0",
    description = "Description de votre programme",
    executables = [Executable(script_name)]
)