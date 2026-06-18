from fastapi import APIRouter
from services.openai_service import perguntar_ia
from services.zapi_service import enviar_mensagem

router = APIRouter()

historico_conversas = {}

@router.post("/webhook")
async def webhook(data: dict):

    try:

        print("WEBHOOK RECEBIDO:")
        print(data)

        # Ignorar apenas newsletters
        if data.get("isNewsletter"):
            return {"status": "newsletter_ignorada"}

        numero = data.get("phone")

        if not numero:
            print("Número não encontrado")
            return {"status": "sem_numero"}

        texto = ""

        if "text" in data:
            texto = data["text"].get("message", "")

        if not texto:
            print("Mensagem sem texto")
            return {"status": "sem_texto"}

        print("Mensagem recebida:", texto)

        if numero not in historico_conversas:
            historico_conversas[numero] = []

        historico_conversas[numero].append(
            f"Cliente: {texto}"
        )

        contexto = "\n".join(
            historico_conversas[numero][-20:]
        )

        print("ANTES DA IA")

        resposta_ia = perguntar_ia(contexto)

        print("DEPOIS DA IA")
        print("Resposta IA:", resposta_ia)

        historico_conversas[numero].append(
            f"IA: {resposta_ia}"
        )

        print("ANTES DE ENVIAR")

        resultado = enviar_mensagem(
            numero,
            resposta_ia
        )

        print("RESULTADO ENVIO:")
        print(resultado)

        return {
            "status": "ok"
        }

    except Exception as e:

        print("ERRO NO WEBHOOK:")
        print(str(e))

        return {
            "status": "erro",
            "erro": str(e)
        }