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

        if "data" not in data:
            return {"status": "evento_ignorado"}

        evento = data["data"]

        numero = evento.get("from")
        mensagem = evento.get("body")

        if not numero or not mensagem:
            return {"status": "sem_mensagem"}

        print("Número:", numero)
        print("Mensagem:", mensagem)

        cliente = buscar_cliente(numero)

        if not cliente:
            cliente = criar_cliente(numero)

        cliente_id = cliente["id"]

        print("CLIENTE ID:", cliente_id)

        salvar_mensagem(
            cliente_id,
            "cliente",
            mensagem
        )

        atualizar_historico_json(cliente_id)

        historico = buscar_historico(cliente_id)

        historico_texto = ""

        for msg in historico:

            if msg["tipo"] == "cliente":
                historico_texto += f"Cliente: {msg['mensagem']}\n"
            else:
                historico_texto += f"IA: {msg['mensagem']}\n"

        produtos = buscar_produtos()

        print("================================")
        print("PRODUTOS VINDOS DO SUPABASE:")
        print(produtos)
        print("================================")

        catalogo = ""

        for produto in produtos:

            catalogo += (
                f"Nome: {produto['nome']}\n"
                f"Categoria: {produto.get('categoria', '')}\n"
                f"Preço: R$ {produto['preco']}\n"
                f"Estoque: {produto['estoque']}\n"
                f"Descrição: {produto['descricao']}\n\n"
            )

        print("================================")
        print("CATALOGO MONTADO:")
        print(catalogo)
        print("================================")

        contexto = f"""
HISTÓRICO DA CONVERSA:

{historico_texto}

MENSAGEM ATUAL DO CLIENTE:

{mensagem}

PRODUTOS DISPONÍVEIS:

{catalogo}
"""

        print("ENVIANDO PARA IA")

        resposta_ia = perguntar_ia(contexto)

        print("RESPOSTA IA:")
        print(resposta_ia)

        salvar_mensagem(
            cliente_id,
            "ia",
            resposta_ia
        )

        atualizar_historico_json(cliente_id)

        enviar_mensagem(
            numero,
            resposta_ia
        )

        print("MENSAGEM ENVIADA")

        return {
            "status": "ok"
        }

    except Exception as e:

        print("ERRO:")
        print(str(e))

        return {
            "status": "erro",
            "mensagem": str(e)
        }