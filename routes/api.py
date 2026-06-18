from fastapi import APIRouter
from services.openai_service import perguntar_ia
from services.zapi_service import enviar_mensagem

router = APIRouter()

historico_conversas = {}

@router.post("/webhook")
async def webhook(data: dict):

    try:

        if data.get("isGroup"):
            return {"status": "grupo_ignorado"}

        mensagem = data["text"]["message"]
        numero = data["phone"]

        print("Mensagem recebida:", mensagem)

        if numero not in historico_conversas:
            historico_conversas[numero] = []

        historico_conversas[numero].append(
            f"Cliente: {mensagem}"
        )

        contexto = "\n".join(
            historico_conversas[numero]
        )

        resposta_ia = perguntar_ia(contexto)

        historico_conversas[numero].append(
            f"IA: {resposta_ia}"
        )

        enviar_mensagem(numero, resposta_ia)

        return {
            "status": "ok"
        }

    except Exception as e:

        print("ERRO:", e)

        return {
            "status": "erro"
        }