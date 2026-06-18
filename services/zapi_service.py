import requests

INSTANCE_ID = "SEU_ID"
TOKEN = "SEU_TOKEN"

def enviar_mensagem(numero, mensagem):

    url = f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{TOKEN}/send-text"

    payload = {
        "phone": numero,
        "message": mensagem
    }

    response = requests.post(url, json=payload)

    print("STATUS ZAPI:", response.status_code)
    print("RESPOSTA ZAPI:", response.text)