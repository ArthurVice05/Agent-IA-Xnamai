import requests

INSTANCE_ID = "instance181898"
TOKEN = "xe2moxi8yqfd51zs"

def enviar_mensagem(numero, mensagem):

    try:

        print("================================")
        print("ENVIANDO WHATSAPP")
        print("NUMERO:", numero)
        print("MENSAGEM:", mensagem)
        print("================================")

        url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"

        payload = {
            "token": TOKEN,
            "to": numero,
            "body": mensagem
        }

        response = requests.post(
            url,
            data=payload,
            timeout=30
        )

        print("STATUS:", response.status_code)
        print("RESPOSTA:", response.text)

        return response.text

    except Exception as e:

        print("ERRO ULTRAMSG:", str(e))

        return None