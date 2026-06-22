import requests

INSTANCE_ID = "3Finstance181898"
TOKEN = "xe2moxi8yqfd51zs"
CLIENT_TOKEN = "F9cd4078a935541489c79fb0fe74d847fS"

def enviar_mensagem(numero, mensagem):

    url = f"https://api.ultramsg.com/instance181898/{INSTANCE_ID}/token/{TOKEN}/send-text"

    headers = {
        "Client-Token": CLIENT_TOKEN,
        "Content-Type": "application/json"
    }

    payload = {
        "phone": numero,
        "message": mensagem
    }

    print("CLIENT TOKEN USADO:", CLIENT_TOKEN)

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=30
    )

    print("STATUS ZAPI:", response.status_code)
    print("RESPOSTA ZAPI:", response.text)

    return response.text