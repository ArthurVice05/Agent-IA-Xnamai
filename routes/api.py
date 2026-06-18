from fastapi import APIRouter
from services.openai_service import perguntar_ia
from services.zapi_service import enviar_mensagem

router = APIRouter()

@router.post("/webhook")
async def webhook(data: dict):

    print("WEBHOOK RECEBIDO:")
    print(data)

    try:

        if data.get("isGroup"):
            return {"status": "grupo_ignorado"}

        mensagem = data["text"]["message"]

        numero = data["phone"]

        print("Mensagem recebida:", mensagem)

        resposta_ia = perguntar_ia(mensagem)

        print("Resposta IA:", resposta_ia)

        enviar_mensagem(numero, resposta_ia)

        return {
            "status": "ok"
        }

    except Exception as e:

        print("ERRO:", e)

        return {
            "status": "erro"
        }