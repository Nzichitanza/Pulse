import requests

# 🔹 CONFIGURAZIONE (inserisci i tuoi dati)
ACCESS_TOKEN = "bd41695e105f8839c6fe2e30ced68e21"
INSTAGRAM_ACCOUNT_ID = "9506809812695056"
POST_ID = "18493807954021875"
PAROLA_CHIAVE = "giardino"
MESSAGGIO_DM = "Ciao! Grazie per il commento, guarda questa immagine. 🌿"
IMAGE_URL = "https://tuosito.com/immagine.jpg"  # URL dell'immagine pubblica

# 🔹 1. Legge i commenti del post
def get_comments():
    url = f"https://graph.facebook.com/v18.0/{POST_ID}/comments?access_token={ACCESS_TOKEN}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print("Errore nel recupero commenti:", response.json())
        return []

# 🔹 2. Risponde ai commenti con la parola chiave
def reply_to_comment(comment_id):
    url = f"https://graph.facebook.com/v18.0/{comment_id}/replies"
    payload = {
        "message": "Fatto",
        "access_token": ACCESS_TOKEN
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print(f"✅ Risposto al commento {comment_id}")
    else:
        print("❌ Errore nella risposta:", response.json())

# 🔹 3. Crea un contenuto immagine per il DM
def create_media_attachment():
    url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media"
    payload = {
        "image_url": IMAGE_URL,  # URL pubblico dell'immagine
        "access_token": ACCESS_TOKEN
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        media_id = response.json().get("id")
        print(f"📸 Immagine caricata con ID: {media_id}")
        return media_id
    else:
        print("❌ Errore nel caricamento immagine:", response.json())
        return None

# 🔹 4. Invia un DM con immagine e testo
def send_dm(user_id):
    media_id = create_media_attachment()
    if not media_id:
        return
    
    url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/messages"
    payload = {
        "recipient": f"{{'id':'{user_id}'}}",
        "message": f"{{'text':'{MESSAGGIO_DM}', 'attachment':{{'type':'image', 'payload':{{'id':'{media_id}'}}}}}}}",
        "access_token": ACCESS_TOKEN
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print(f"📩 DM con immagine inviato a {user_id}")
    else:
        print("❌ Errore nell'invio DM:", response.json())

# 🔹 5. Esegue tutto
def main():
    comments = get_comments()
    for comment in comments:
        comment_id = comment["id"]
        user_id = comment["from"]["id"]
        message = comment["text"].lower()

        if PAROLA_CHIAVE in message:
            reply_to_comment(comment_id)
            send_dm(user_id)

if __name__ == "__main__":
    main()
