Description
SANDA_DETECT est une application web intelligente développée avec Flask pour la détection de fraude dans l'assurance automobile. Cette plateforme offre des espaces dédiés pour l'administration, l'analyse IA, les agents assurance et les clients.
 Installation Rapide
Prérequis
•	Python 3.8 ou supérieur
•	pip (gestionnaire de packages Python)
•	Navigateur web moderne
 Installation en 4 étapes
1.	Télécharger les fichiers
bash
# Si vous utilisez Git
git clone https://github.com/votre-username/SANDA_DETECT.git
cd SANDA_DETECT

# Sinon, téléchargez et décompressez les fichiers dans un dossier SANDA_DETECT
2.	Créer un environnement virtuel
bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
3.	Installer les dépendances

pip install flask==2.3.3 werkzeug==2.3.7 jinja2==3.1.2
4.	Vérifier la structure des fichiers

SANDA_DETECT/
├── app.py                 # Application principale
├── requirements.txt       # Dépendances (optionnel)
└── templates/            # Dossier des pages web
    ├── base.html         # Template principal
    ├── home.html         # Page d'accueil
    ├── admin.html        # Espace administration
    ├── analyst.html      # Espace analyste IA
    ├── agent.html        # Espace agent assurance
    ├── client.html       # Espace client
    ├── 404.html          # Page erreur 404
    └── 500.html          # Page erreur 500
Utilisation
Démarrer l'application
python app.py
