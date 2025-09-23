# Poubelle Intelligente ♻️

**Classifieur d’objets pour le tri sélectif** (cardboard, glass, metal, paper, plastic, trash) avec **API FastAPI** et **interface Streamlit**.  
Le score de **recyclabilité** utilisé est la **probabilité que l’objet soit recyclable**, et la décision est **binaire** :  
**recyclable si probabilité ≥ 50%**, sinon **non recyclable**.

---

## 📚 Données (Kaggle)

Les données d’entraînement proviennent d’un **dataset public Kaggle** et sont réparties en **6 classes** :

- **Cardboard** : carton et emballages en papier épais  
- **Glass** : bouteilles, bocaux et objets en verre  
- **Metal** : canettes, boîtes de conserve, objets métalliques  
- **Paper** : journaux, magazines, feuilles, emballages papier  
- **Plastic** : bouteilles, sacs, contenants plastiques  
- **Trash** : déchets non recyclables / mélanges / non catégorisés

> Les données ont été téléchargées depuis un dataset existant sur Internet.

---

## 🧠 Modèle (MobileNetV2)

Développé avec **TensorFlow/Keras**, pour classifier des images en **6 catégories**.  
L’entraînement est réalisé dans `entrainement_model.ipynb`.

- **Backbone** : `MobileNetV2` **pré-entraîné ImageNet**, `include_top=False`  
- **Couches additionnelles** :  
  - `GlobalAveragePooling2D()`  
  - `Dense(128, activation="relu")`  
  - `Dropout(0.5)`  
  - `Dense(6, activation="softmax")`  
- **Prétraitement** : redimensionnement **224×224**, **normalisation [0,1]**  
- **Augmentation** : rotation, zoom, flip (améliore la généralisation)  
- **Stratégie** : gel initial des couches du backbone  
- **Optimiseur** : **Adam** (LR ajusté)  
- **Perte** : **Categorical Crossentropy**  
- **Métriques** : **Accuracy**  
- **Export** : modèle sauvegardé en **`.h5`** → `model.h5` (réutilisable pour le déploiement)

### Évaluation
- Calcul de **val_loss** et **val_accuracy** sur un jeu de validation  
- Affichage des métriques après entraînement

---

## 🔌 API FastAPI

L’API reçoit une image et renvoie une **estimation de la recyclabilité**.

**Endpoints**
- `GET /` → message de bienvenue / ping
- `POST /predict` → reçoit une image (`multipart/form-data`, champ `file`) et retourne la **probabilité de recyclabilité**

**Pipeline côté API**
1. Lecture de l’image uploadée  
2. Prétraitement : **resize 224×224**, conversion en **numpy**, **ajout dimension batch**  
3. **Prédiction** via le modèle entraîné  
4. **Retour** d’un JSON avec la **probabilité de recyclabilité** et la **décision binaire (≥ 50%)**

**Réponse (exemple)**
```json
{
  "recyclable_prob": 0.87,
  "recyclable": true
}
```
## 🖥️ Interface Streamlit

- Upload d’image par l’utilisateur  
- Affichage de l’image uploadée  
- Envoi de la requête à l’API et **prédiction en temps réel**  
- Message clair :
  - **≥ 50%** → *Objet recyclable*  
  - **< 50%** → *Objet non recyclable*

---

## ▶️ Lancer en local (API + Front)

### 1) Installer les dépendances
```bash
pip install -r requirements.txt
```


🖥️ Interface Streamlit
Upload d’image par l’utilisateur
Affichage de l’image uploadée
Envoi de la requête à l’API et prédiction en temps réel
Message clair :
≥ 50% → Objet recyclable
< 50% → Objet non recyclable
▶️ Lancer en local (API + Front)
1) Installer les dépendances
pip install -r requirements.txt
Exemple de requirements.txt :
fastapi==0.103.1
uvicorn
python-multipart
tensorflow
pillow
streamlit
2) Démarrer l’API
uvicorn api:app --reload --port 8000
3) Lancer l’interface Streamlit
streamlit run frontend.py
4) Tester
Ouvrir l’URL locale fournie par Streamlit
Charger une image d’objet
Obtenir la classification en temps réel
🐳 Dockerisation (API)
Créez un fichier Dockerfile (sans extension) :
# Utilisation d'une image Python allégée
FROM python:3.10-slim

# Répertoire de travail
WORKDIR /app

# Dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code
COPY . .

# Exposition du port API
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
Construction de l’image
docker build -t fast_api:v0 .
Lancement du conteneur
docker run -p 8000:8000 fast_api:v0
API : http://localhost:8000
Doc Swagger : http://localhost:8000/docs
☁️ Déploiement sur GCP (GCR + Cloud Run)
1) Préparer gcloud
gcloud init
# -> login, choisir/projeter un projet, créer une config (ex. fastapi)

gcloud auth configure-docker
# -> autorise Docker à pousser vers Container Registry (gcr.io)
2) Tagger puis pousser l’image vers GCR
# Remplace <PROJECT_ID> par l'ID de ton projet GCP
docker tag fast_api:v0 gcr.io/<PROJECT_ID>/fast_api:v0
docker push gcr.io/<PROJECT_ID>/fast_api:v0
Dans la console GCP, vérifie que Google Container Registry est activé et que l’image apparaît bien.
3) Déployer sur Cloud Run
Depuis la console :
Ouvrir Cloud Run
Créer un service → choisir l’image gcr.io/<PROJECT_ID>/fast_api:v0
Options :
Région : la plus proche de tes utilisateurs
Port : 8000
Accès : Allow unauthenticated invocations (public)
Créer → récupère l’URL publique
Ou en CLI :
gcloud run deploy poubelle-intelligente-api \
  --image gcr.io/<PROJECT_ID>/fast_api:v0 \
  --platform managed \
  --allow-unauthenticated \
  --port 8000
🧱 Architecture (vue d’ensemble)
Utilisateur (Streamlit UI)
        │ upload image
        ▼
     FastAPI  ── preprocess ──► MobileNetV2 (6 classes)
        │                          │
        └────── JSON ◄─────────────┘
                {
                  "recyclable_prob": p,
                  "recyclable": p >= 0.5
                }
📦 Exemple d’appel API
curl -X POST "http://localhost:8000/predict" \
  -F "file=@tests/sample.jpg"
Réponse attendue :
{
  "recyclable_prob": 0.72,
  "recyclable": true
}
📄 Licence
Ce projet est distribué sous licence MIT (voir LICENSE).
