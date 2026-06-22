from fastapi import APIRouter

from services.openai_service import perguntar_ia
from services.ultramsg_service import enviar_mensagem

from services.supabase_service import (
    buscar_cliente,
    criar_cliente,
    salvar_mensagem,
    buscar_historico,
    atualizar_historico_json,
    buscar_produtos
)

router = APIRouter()


@router.post("/webhook")
async def webhook(data: dict):

    try:

        print("WEBHOOK RECEBIDO:")
        print(data)

        # Verifica se veio evento válido
        if "data" not in data:
            return {"status": "evento_ignorado"}

        evento = data["data"]

        numero = evento.get("from")
        mensagem = evento.get("body")

        # Ignora eventos sem mensagem
        if not numero or not mensagem:
            return {"status": "sem_mensagem"}

        print("Número:", numero)
        print("Mensagem:", mensagem)

        # Busca cliente
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

        # Atualiza histórico JSON
        atualizar_historico_json(cliente_id)

        print("Mensagem salva")

        # =========================
        # HISTÓRICO DA CONVERSA
        # =========================

        historico = buscar_historico(cliente_id)

        contexto = ""

        for msg in historico:

            if msg["tipo"] == "cliente":
                contexto += f"Cliente: {msg['mensagem']}\n"
            else:
                contexto += f"Atendente: {msg['mensagem']}\n"

        # =========================
        # PRODUTOS DA XNAMAI
        # =========================

        produtos = buscar_produtos()

        print("PRODUTOS ENCONTRADOS:")
        print(produtos)

        contexto_produtos = """

CATÁLOGO OFICIAL DA XNAMAI

Utilize os produtos abaixo para responder clientes.

Se o cliente perguntar sobre produtos,
preços ou recomendações, utilize este catálogo.

"""

        for produto in produtos:

            contexto_produtos += f"""

Nome: {produto['nome']}
Categoria: {produto['categoria']}
Preço: R$ {produto['preco']}
Estoque: {produto['estoque']}
Descrição: {produto['descricao']}

"""

        contexto += contexto_produtos

        print("CONTEXTO ENVIADO PARA IA:")
        print(contexto)

        # =========================
        # IA
        # =========================

        print("ENVIANDO PARA IA")

        resposta_ia = perguntar_ia(contexto)

        print("RESPOSTA IA:")
        print(resposta_ia)

        # Salva resposta da IA
        salvar_mensagem(
            cliente_id,
            "ia",
            resposta_ia
        )

        # Atualiza histórico JSON novamente
        atualizar_historico_json(cliente_id)

        print("Resposta salva")

        # =========================
        # ENVIA WHATSAPP
        # =========================

        enviar_mensagem(
            numero,
            resposta_ia
        )

        print("Mensagem enviada para WhatsApp")

        return {
            "status": "ok"
        }

    except Exception as e:

        print("ERRO:", str(e))

        return {
            "status": "erro",
            "mensagem": str(e)
        }