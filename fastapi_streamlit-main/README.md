Projet de Classification d'objets Recyclables

Objectif du Projet

Ce projet a pour but de développer un système intelligent de classification des déchets basé sur l'intelligence artificielle. Il utilise un modèle de deep learning pour déterminer si un objet est recyclable ou non à partir d'images. L'objectif est de faciliter le tri sélectif et d'améliorer la gestion des déchets grâce à une API FastAPI et une interface utilisateur Streamlit.

Grandes Étapes du Projet

1️⃣ Acquisition des Données

Les données proviennent de Kaggle et contiennent des images classées en six catégories distinctes :

Cardboard : Carton et emballages en papier épais.

Glass : Bouteilles, bocaux et autres objets en verre.

Metal : Canettes, boîtes de conserve et objets métalliques.

Paper : Journaux, magazines, feuilles et emballages en papier.

Plastic : Bouteilles, sacs et objets en plastique.

Trash : Déchets non recyclables.

2️⃣ Prétraitement des Données

Redimensionnement des images à 224x224 pixels.

Normalisation des pixels (valeurs entre 0 et 1).

Augmentation des données (rotation, zoom, flip) pour améliorer la robustesse du modèle.

3️⃣ Entraînement du Modèle

Utilisation de MobileNetV2, un réseau de neurones convolutionnel pré-entraîné sur ImageNet.

Ajout de couches personnalisées :

GlobalAveragePooling2D() pour la réduction des dimensions.

Dense(128, activation="relu") pour améliorer la classification.

Dropout(0.5) pour éviter le surapprentissage.

Dense(2, activation="softmax") pour classer les objets en recyclable ou non recyclable.

Entraînement sur un jeu d'entraînement avec validation.

Évaluation : Calcul de la perte (val_loss) et de la précision (val_accuracy) sur le jeu de validation.

Sauvegarde du modèle sous format .h5 (model.h5).

4️⃣ Développement de l'API avec FastAPI

Création d'une API REST avec FastAPI permettant de :

Envoyer une image et obtenir une prédiction sur sa recyclabilité.

Fournir une probabilité associée à la classification.

Endpoints de l'API :

GET / : Message de bienvenue.

POST /predict : Prend une image en entrée et retourne la classification (recyclable ou non).

5️⃣ Développement de l'Interface Utilisateur avec Streamlit

Interface simple et intuitive permettant aux utilisateurs d'uploader une image.

Affichage de l’image uploadée.

Envoi de la requête à l’API pour classification.

Affichage du résultat avec indication de recyclabilité.

6️⃣ Dockerisation et Déploiement

Dockerisation de l'application avec Docker.

Fichier Dockerfile permettant de :

Installer les dépendances (requirements.txt).

Exposer le service via uvicorn sur le port 8000.

Déploiement sur Google Cloud Platform (GCP) :

Hébergement de l’image Docker sur Google Container Registry.

Déploiement avec Google Cloud Run pour une mise en production accessible via une URL publique.

📌 Téléchargement des fichiers du projet

Pour télécharger l'ensemble du projet, y compris la vidéo contenue dans l'archive ZIP :

Cloner le dépôt GitHub :

git clone https://github.com/LYT-ctrl/projet.git
cd projet

Télécharger tous les fichiers :

Aller sur GitHub

Cliquer dessus et sélectionner Download.

📌 Utilisation du Projet

Installation des dépendances :

pip install -r requirements.txt

Démarrage de l'API :

uvicorn api:app --reload

Lancement de l'interface utilisateur Streamlit :

streamlit run frontend.py

Utilisation de Docker :

docker build -t fast_api:v0 .
docker run -p 8000:8000 fast_api:v0

Déploiement sur Google Cloud :

gcloud auth configure-docker
docker tag fast_api:v0 gcr.io/<nom_du_projet>/fast_api:v0
docker push gcr.io/<nom_du_projet>/fast_api:v0

🚀 Conclusion

Ce projet allie intelligence artificielle, développement web et cloud computing pour fournir une solution efficace de classification des objets recyclables. Grâce à FastAPI et Streamlit, l'application permet une interaction fluide et accessible avec le modèle d'IA, tandis que Docker et GCP assurent une mise en production rapide et scalable.
