Dans Google Cloud, créer une Cloud Run Fonction :
- Mémoire allouée : 512 Mo (au lieu de 256 Mo)
- Choisir l'environnement d'exécution (Python 3.12)
    - main.py : contenu du fichier 
    - requirements.txt : contenu du fichier 
- Déployer

Tester avec :
    - curl -m 70 -X POST https://europe-west1-poc-chatbot-edf.cloudfunctions.net/simple-gemini-function -H "Content-Type: application/json" -d '{"prompt": "Who is Albert Einstein?"}'
    - POSTMAN : compte alban.kerloch@gmail.com => Google Cloud => Cloud Function => simple-gemini-function
