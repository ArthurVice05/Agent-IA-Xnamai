import requests

INSTANCE_ID = "3F4CB317B66E2245E7E58645B9B7D1FC"
TOKEN = "4C2EDD29BAA28D8A82485C7B"

def enviar_mensagem(numero, mensagem):

    url = f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{TOKEN}/send-text"

    payload = {
        "phone": numero,
        "message": mensagem
    }

    response = requests.post(
        url,
        json=payload
    )

    print("STATUS ZAPI:", response.status_code)
    print("RESPOSTA ZAPI:", response.text)