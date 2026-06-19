from fastapi import APIRouter

from services.openai_service import perguntar_ia
from services.zapi_service import enviar_mensagem

from services.supabase_service import (
    buscar_cliente,
    criar_cliente,
    salvar_mensagem,
    buscar_historico
)

router = APIRouter()


@router.post("/webhook")
async def webhook(data: dict):

    try:

        print("WEBHOOK RECEBIDO:")
        print(data)

        # Ignora grupos
        if data.get("isGroup"):
            return {"status": "grupo_ignorado"}

        # Ignora mensagens enviadas pelo próprio número
        if data.get("fromMe"):
            return {"status": "mensagem_propria"}

        mensagem = data["text"]["message"]
        numero = data["phone"]

        print("Mensagem recebida:", mensagem)

        # Procura cliente
        cliente = buscar_cliente(numero)

        print("CLIENTE ENCONTRADO:", cliente)

        # Cria cliente se não existir
        if not cliente:
            cliente = criar_cliente(numero)

        cliente_id = cliente["id"]

        print("CLIENTE ID:", cliente_id)

        # Salva mensagem do cliente
        salvar_mensagem(
            cliente_id,
            "cliente",
            mensagem
        )

        print("Mensagem salva:", mensagem)

        # Busca histórico completo
        historico = buscar_historico(cliente_id)

        contexto = ""

        for msg in historico:

            if msg["tipo"] == "cliente":
                contexto += f"Cliente: {msg['mensagem']}\n"
            else:
                contexto += f"IA: {msg['mensagem']}\n"

        print("ANTES DA IA")

        resposta_ia = perguntar_ia(contexto)

        print("DEPOIS DA IA")
        print("Resposta IA:", resposta_ia)

        # Salva resposta da IA
        salvar_mensagem(
            cliente_id,
            "ia",
            resposta_ia
        )
        print("Resposta IA salva:", resposta_ia)

        print("ANTES DE ENVIAR")

        enviar_mensagem(
            numero,
            resposta_ia
        )

        return {
            "status": "ok"
        }

    except Exception as e:

        print("ERRO:", str(e))

        return {
            "status": "erro",
            "mensagem": str(e)
        }