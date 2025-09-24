# ♻️ Poubelle Intelligente

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?logo=tensorflow)
![Keras](https://img.shields.io/badge/Keras-red?logo=keras)
![FastAPI](https://img.shields.io/badge/FastAPI-0.103-green?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-ff4b4b?logo=streamlit)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)

![Kaggle](https://img.shields.io/badge/Dataset-Kaggle-20beff?logo=kaggle)
![GCP](https://img.shields.io/badge/GCP-Cloud_Run-4285F4?logo=googlecloud)


Un projet de classification d’objets recyclables basé sur **MobileNetV2**, déployé avec **FastAPI**, **Streamlit**, **Docker** et **Google Cloud Run**.

---

## 🚀 Objectifs
Faciliter le tri sélectif grâce à un système intelligent capable de :
- Classifier des déchets en **6 catégories** à partir d’images.
- Fournir une prédiction en temps réel via une **API REST** et une **interface utilisateur**.
- Être déployé en local ou dans le cloud pour une utilisation pratique.

---

## 📂 Dataset
Les données proviennent de **Kaggle** et contiennent des images réparties en 6 classes :
- **Cardboard** : cartons, emballages papier épais.  
- **Glass** : bouteilles, bocaux, objets en verre.  
- **Metal** : canettes, boîtes de conserve, objets métalliques.  
- **Paper** : journaux, magazines, feuilles.  
- **Plastic** : bouteilles, sacs, objets en plastique.  
- **Trash** : déchets non recyclables.  

---

## 🧠 Modèle
Le modèle choisi est **MobileNetV2**, pré-entraîné sur **ImageNet**.

### Architecture :
- `GlobalAveragePooling2D()`  
- `Dense(128, activation="relu")`  
- `Dropout(0.5)`  
- `Dense(6, activation="softmax")`  

### Paramètres d’entraînement :
- **Redimensionnement** : `224x224`  
- **Normalisation** : valeurs entre 0 et 1  
- **Augmentation des données** : rotation, zoom, flip  
- **Optimiseur** : Adam  
- **Loss** : Categorical Crossentropy  
- **Métriques** : Accuracy  

📦 Le modèle est sauvegardé au format **`model.h5`**.

---

## 📊 Résultats
- Évaluation sur dataset de validation.  
- Suivi : `val_loss` et `val_accuracy`.  
- Résultats affichés après entraînement pour mesurer la performance.  

---

## 🔌 API FastAPI
Une API REST permet de tester le modèle.

### Endpoints :
- **GET /** → message de bienvenue.  
- **POST /predict** → upload d’une image et retour de la probabilité de recyclabilité.  

### Lancer l’API :
```bash
uvicorn api:app --reload
```

### 🎨 Interface streamlit : 
Une interface simple pour interagir avec le modèle.  

Fonctionnalités :  

- Upload d’une image.
- Visualisation de l’image.
- Prédiction via l’API.
- Affichage du résultat :
  Probabilité > 50% → objet recyclable ✅
  Sinon → objet non recyclable ❌
  

 
Lancer l’interface :

```bash
streamlit run frontend.py
```


### 🐳 Dockerisation
Dockerfile :
```bash
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```
### construire et lancer l'image : 
``` bash
docker build -t fast_api:v0 .
docker run -p 8000:8000 fast_api:v0
```

API accessible sur : http://localhost:8000
Documentation interactive : http://localhost:8000/docs

### ☁️ Déploiement sur Google Cloud Run

- 1) Créer un projet GCP et installer gcloud.
- 2) Authentifier Docker :
``` bash
gcloud auth configure-docker
```
- 3) Taguer et pousser l’image :

``` bash
docker tag fast_api:v0 gcr.io/<nom_du_projet>/fast_api:v0
docker push gcr.io/<nom_du_projet>/fast_api:v0
```
- 4) Déployer sur Cloud Run depuis la console :

-- 1) Région proche.
-- 2) Port 8000.
-- 3) Autorisations adaptées.

Une URL publique sera générée pour accéder à l’API.

### Installation et utilisation :
Cloner le repo :
``` bash
git clone <URL_DU_REPO>
cd poubelle-intelligente
```

Installer les dépendances :
``` bash
pip install -r requirements.txt
```

### Fichiers principaux :
- entrainement_model.ipynb → entraînement MobileNetV2.
- api.py → API FastAPI.
- frontend.py → Interface Streamlit.
- Dockerfile → déploiement Docker.
- requirements.txt → dépendances.

### Références : 
- Dataset Kaggle
- MobileNetV2 - Paper
- FastAPI Documentation
- Streamlit Documentation
- Google Cloud Run

### Auteur ✍️ 
Yacine Tigrine  
Étudiant en Master 2 Ingénierie & Intelligence Artificielle

Université Paris 8


## 📜 Licence

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
