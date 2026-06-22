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

        # =========================
        # CLIENTE
        # =========================

        cliente = buscar_cliente(numero)

        if not cliente:
            cliente = criar_cliente(numero)

        cliente_id = cliente["id"]

        print("CLIENTE ID:", cliente_id)

        # =========================
        # SALVA MENSAGEM CLIENTE
        # =========================

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

        # ==================================
# PRODUTOS
# ==================================

produtos = buscar_produtos()

print("================================")
print("PRODUTOS VINDOS DO SUPABASE:")
print(produtos)

if produtos:
    print("TOTAL PRODUTOS:", len(produtos))
else:
    print("TOTAL PRODUTOS: 0")

print("================================")

catalogo = ""

for produto in produtos:

    catalogo += (
        f"PRODUTO\n"
        f"Nome: {produto['nome']}\n"
        f"Categoria: {produto['categoria']}\n"
        f"Preço: R$ {produto['preco']}\n"
        f"Estoque: {produto['estoque']}\n"
        f"Descrição: {produto['descricao']}\n\n"
    )

print("================================")
print("CATALOGO MONTADO:")
print(catalogo)
print("================================")

contexto_final = f"""
Você é uma atendente da Xnamai.

IMPORTANTE:

Os produtos abaixo EXISTEM no banco de dados.

Você DEVE utilizar esses produtos ao responder.

Se existir um produto relacionado ao pedido do cliente,
você deve apresentar o produto.

Nunca diga que não encontrou produtos sem verificar a lista.

CATÁLOGO DE PRODUTOS:

{catalogo}

HISTÓRICO:

{historico_texto}

MENSAGEM DO CLIENTE:

{mensagem}

EXEMPLOS:

Se existir:

Nome: Fone Bluetooth HMaston RS60

e o cliente pedir:

"quero um fone"

responda:

"Temos o Fone Bluetooth HMaston RS60 disponível por R$ 89,90."

Se existir:

Nome: Caixa de Som Bluetooth LT800

e o cliente pedir:

"quero uma caixa de som"

responda:

"Temos a Caixa de Som Bluetooth LT800 disponível por R$ 129,90."

Nunca invente produtos.
Nunca invente preços.
Nunca invente estoque.
"""