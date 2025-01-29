import streamlit as st
from PIL import Image
import requests

# Titre de l'application
st.title("Poubelle Intelligente")

# Téléchargement de l'image
upload = st.file_uploader("Chargez l'image de votre objet", type=['png', 'jpeg', 'jpg'])

# Colonnes pour afficher l'image et les résultats
c1, c2 = st.columns(2)

if upload:
    # Préparer les données pour la requête
    files = {"file": upload.getvalue()}  # Définit 'files' à partir de l'image téléchargée

    try:
        # Envoyer la requête POST à l'API
        req = requests.post("http://127.0.0.1:8000/predict", files=files)
        req.raise_for_status()  # Vérifie si la requête a échoué
        print("Réponse brute de l'API :", req.text)  # Debug : Affiche la réponse brute
        resultat = req.json()  # Convertir en JSON

        # Interpréter correctement les probabilités
        non_recyclable_prob = resultat["predictions"] * 100  # Probabilité NON recyclable
        recyclable_prob = 100 - non_recyclable_prob  # Complément

        # Afficher l'image chargée
        c1.image(Image.open(upload))

        # Afficher le résultat corrigé
        if recyclable_prob > 50:
            c2.success(f"Je suis certain à {recyclable_prob:.2f}% que l'objet est recyclable.")
        else:
            c2.warning(f"Je suis certain à {non_recyclable_prob:.2f}% que l'objet n'est pas recyclable.")

    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de connexion avec l'API : {e}")
    except KeyError:
        st.error("La réponse de l'API ne contient pas les informations attendues.")
    except Exception as e:
        st.error(f"Une erreur inattendue est survenue : {e}")
else:
    st.info(".")
