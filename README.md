Installation et Utilisation
# Étape 1 : Prérequis

Installer Python 3.11
Télécharger Google Chrome
Télécharger ChromeDriver (compatible avec votre version de Chrome)

# Créer un environnement virtuel :
bashpython -m venv venv
# Activer l'environnement virtuel :
bash# Windows:
venv\Scripts\activate
# Étape 2 : Installer les dépendances
bashpip install -r requirements.txt
# Étape 3 : Configuration
Copier le fichier de configuration :
bashcp .env.exemple .env
Modifier le fichier .env avec vos informations Discord.
# Étape 4 : Exécution
Si vous voulez collecter de nouvelles données, supprimer le dataset existant puis lancer :
bashpython bot.py  puis analysez avec eda.ipynb 

