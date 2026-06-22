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

        # Buscar cliente
        cliente = buscar_cliente(numero)

        if not cliente:
            cliente = criar_cliente(numero)

        cliente_id = cliente["id"]

        print("CLIENTE ID:", cliente_id)

        # Salvar mensagem do cliente
        salvar_mensagem(
            cliente_id,
            "cliente",
            mensagem
        )

        atualizar_historico_json(cliente_id)

        # =========================
        # HISTÓRICO
        # =========================

        historico = buscar_historico(cliente_id)

        historico_texto = ""

        for msg in historico:

            if msg["tipo"] == "cliente":
                historico_texto += f"Cliente: {msg['mensagem']}\n"
            else:
                historico_texto += f"Atendente: {msg['mensagem']}\n"

        # =========================
        # PRODUTOS
        # =========================

        produtos = buscar_produtos()

        print("========== PRODUTOS ==========")
        print(produtos)

        if not produtos:
            print("NENHUM PRODUTO ENCONTRADO")
        else:
            print(f"TOTAL PRODUTOS: {len(produtos)}")

        catalogo = ""

        for produto in produtos:

            catalogo += f"""
Nome: {produto.get('nome', '')}
Categoria: {produto.get('categoria', '')}
Preço: R$ {produto.get('preco', '')}
Estoque: {produto.get('estoque', '')}
Descrição: {produto.get('descricao', '')}

"""

        print("========== CATÁLOGO ==========")
        print(catalogo)

        # =========================
        # CONTEXTO DA IA
        # =========================

        contexto_final = f"""
ATENÇÃO:

Os produtos abaixo existem no banco de dados da Xnamai.

Nunca diga que não encontrou produtos sem verificar o catálogo.

CATÁLOGO:

{catalogo}

HISTÓRICO DA CONVERSA:

{historico_texto}

MENSAGEM ATUAL DO CLIENTE:

{mensagem}

REGRAS:

- Utilize apenas os produtos do catálogo.
- Informe nome, preço, descrição e estoque.
- Nunca invente produtos.
- Nunca invente preços.
- Nunca invente estoque.
"""

        print("========== CONTEXTO ==========")
        print(contexto_final)

        # =========================
        # IA
        # =========================

        resposta_ia = perguntar_ia(contexto_final)

        print("RESPOSTA IA:")
        print(resposta_ia)

        # Salvar resposta da IA
        salvar_mensagem(
            cliente_id,
            "ia",
            resposta_ia
        )

        atualizar_historico_json(cliente_id)

        # =========================
        # WHATSAPP
        # =========================

        enviar_mensagem(
            numero,
            resposta_ia
        )

        print("Mensagem enviada")

        return {
            "status": "ok"
        }

    except Exception as e:

        print("ERRO:", str(e))

        return {
            "status": "erro",
            "mensagem": str(e)
        }