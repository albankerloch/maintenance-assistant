Dans Google Cloud Cloud shell :

- Créer les fichiers :
    - requirements.txt
    - streamlit_app.py

- Lancer les commandes suivantes :
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

streamlit run app.py \
  --browser.serverAddress=localhost \
  --server.enableCORS=false \
  --server.enableXsrfProtection=false \
  --server.port 8080

Tester avec : localhost:8080
