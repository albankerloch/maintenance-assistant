Dans Google Cloud Cloud shell :

- Créer les fichiers :
    - requirements.txt
    - streamlit_app.py
    - app.yaml

- Tester avec la commande :
    - streamlit run streamlit_app.py \
    --browser.serverAddress=localhost \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --server.port 8080

- Lancer les commandes suivantes :
    - gcloud app deploy

Tester avec l'URL dans : gcloud app browse

Pour utiliser Cloud Run : https://www.cloudskillsboost.google/course_templates/978/labs/488167

Bonus : activer l'authification pour certains compte google 