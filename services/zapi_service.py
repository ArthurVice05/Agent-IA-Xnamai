import requests

INSTANCE_ID = "SEU_INSTANCE_ID"
TOKEN = "SEU_TOKEN"

def enviar_mensagem(numero, mensagem):

    url = f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{TOKEN}/send-text"

    payload = {
        "phone": str(numero),
        "message": str(mensagem)
    }

    try:

        response = requests.post(
            url,
            json=payload,
            timeout=30
        )

        print("STATUS ZAPI:", response.status_code)
        print("RESPOSTA ZAPI:", response.text)

        return response.text

    except Exception as e:

        print("ERRO ZAPI:", str(e))
        return None