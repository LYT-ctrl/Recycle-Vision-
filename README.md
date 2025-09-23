# RecycleVision ♻️

> **Classifieur d’objets pour le tri sélectif** (cardboard, glass, metal, paper, plastic, trash) avec **API FastAPI** et **frontend Streamlit**. Le score de **recyclabilité** est calculé comme $1 - P(\text{trash})$ à partir d’un modèle deep learning (MobileNetV2, softmax 6 classes).

<p align="left">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10+-blue" />
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-0.110+-teal" />
  <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-1.32+-red" />
  <img alt="TensorFlow" src="https://img.shields.io/badge/TensorFlow-2.x-orange" />
  <img alt="Docker" src="https://img.shields.io/badge/Docker-ready-2496ED" />
</p>

---

## ✨ Fonctionnalités

* **6 classes**: `cardboard`, `glass`, `metal`, `paper`, `plastic`, `trash`.
* **Recyclabilité**: $P(\text{recyclable}) = 1 - P(\text{trash})$ + **seuil** configurable (par défaut `0.60`).
* **API REST** (`/predict`) qui retourne **label top‑1**, **probabilités par classe**, **recyclable\_prob** et **recyclable** (booléen).
* **Interface Streamlit**: upload/caméra, affichage des probabilités triées, message clair (recyclable / non recyclable / incertain).
* **Docker Compose** pour lancer **API + Front** en 1 commande.

---

## 🧱 Architecture

```
Client (Streamlit)  ──▶  FastAPI (/predict)  ──▶  Modèle (MobileNetV2 softmax 6)
       ▲                         │                      │
       └──────────── JSON ◀──────┴────── preprocess ────┘
```

Réponse JSON typique :

```json
{
  "label": "glass",
  "confidence": 0.78,
  "probabilities": {
    "cardboard": 0.02, "glass": 0.78, "metal": 0.05,
    "paper": 0.03, "plastic": 0.10, "trash": 0.02
  },
  "recyclable_prob": 0.98,
  "recyclable": true
}
```

---

## 🚀 Démarrage rapide

### 1) Local (dev)

```bash
# 0) Cloner
git clone <URL_DU_REPO>
cd recycle-vision

# 1) (optionnel) venv
python -m venv .venv && source .venv/bin/activate

# 2) Dépendances
pip install -r requirements-api.txt
pip install -r requirements-front.txt

# 3) Lancer l’API
uvicorn api:app --reload --port 8000

# 4) Lancer le front
streamlit run frontend.py
```

> Configure l’URL de l’API côté front via `.streamlit/secrets.toml` :

```toml
API_URL = "http://localhost:8000/predict"
```

### 2) Docker (prod/dev)

`docker-compose.yml` (inclus) :

```yaml
version: "3.8"
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.api
    ports: ["8000:8000"]
    volumes:
      - ./model.h5:/app/model.h5
      - ./class_names.json:/app/class_names.json
  front:
    build:
      context: .
      dockerfile: Dockerfile.front
    environment:
      API_URL: http://api:8000/predict
    ports: ["8501:8501"]
    depends_on: [api]
```

➡️ Démarrer :

```bash
docker compose up --build
```

---

## 📦 API

* **Endpoint**: `POST /predict`
* **Body**: `multipart/form-data` avec champ `file` (jpg/png)
* **Exemple**:

```bash
curl -F "file=@tests/sample.jpg" http://localhost:8000/predict
```

---

## 🧠 Modèle & Entraînement

* **Backbone**: MobileNetV2 (ImageNet), tête `Dense(6, softmax)`.
* **Perte**: `sparse_categorical_crossentropy`.
* **Préproc**: RGB → 224×224 → normalisation `/255`.
* **Export**: `model.h5` + `class_names.json` (ordre des classes **identique** à l’entraînement).

Script d’entraînement (extrait) :

```python
# Sauvegarder les classes (ordre) pour l’API
with open("class_names.json", "w") as f:
    json.dump(train_ds.class_names, f)
```

**Recyclabilité**: `recyclable_prob = 1 - P(trash)` ; seuil par défaut `0.60` (ajuster sur validation).

---

## 🗂️ Structure du repo

```
recycle-vision/
├─ api.py                 # FastAPI (multiclasse + recyclable_prob)
├─ frontend.py            # Streamlit UI
├─ train.py               # script d’entraînement (optionnel/notebook)
├─ model.h5               # (via Git LFS ou Release)
├─ class_names.json
├─ requirements-api.txt
├─ requirements-front.txt
├─ Dockerfile.api
├─ Dockerfile.front
├─ docker-compose.yml
├─ assets/
│  ├─ demo.gif            # démo UI
│  └─ samples/            # images de test
└─ README.md
```

---

## 📊 Model Card (résumé)

* **Classes**: cardboard, glass, metal, paper, plastic, trash
* **Métriques**: *à compléter* (accuracy, F1 macro, matrice de confusion)
* **Seuil recyclabilité**: 0.60 (recommandé; à valider selon dataset)
* **Limites**: objets très sales, flous, ou non présents dans les données peuvent dégrader la confiance; `plastic` dépend des filières locales.

---

## 🧭 Roadmap

* [ ] Top‑3 avec explications (labels + %)
* [ ] Téléversement batch / dossier
* [ ] Sauvegarde des requêtes (audit)
* [ ] Quantization / TFLite (edge)
* [ ] Déploiement cloud (CI/CD + monitoring)

---

## 📄 Licence

MIT (voir `LICENSE`).

---

## 🙌 Crédit

Projet réalisé par **Yacine Tigrine** — Vision par Ordinateur & IA. Contributions bienvenues (issues/PR).
