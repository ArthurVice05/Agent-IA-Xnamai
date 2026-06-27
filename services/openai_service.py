import os

from dotenv import load_dotenv
from openai import OpenAI

from services.vendas.contexto import ContextoVenda
from services.vendas.prompt import montar_entrada_ia, montar_instrucoes

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-5")


def resposta_saudacao(nome_cliente: str = "") -> str:
    if nome_cliente:
        return (
            f"Oi, {nome_cliente}! Tudo bem? Sou da Xnamai 😊 "
            "Me conta: você tá procurando algo específico ou quer dar uma olhada no que temos?"
        )
    return (
        "Oi! Tudo bem? Sou da Xnamai 😊 "
        "Me conta: você tá procurando algo específico ou quer dar uma olhada no que temos?"
    )


def resposta_sem_foto(produto: dict) -> str:
    nome = produto.get("nome", "produto")
    preco = produto.get("preco", "")
    if preco not in (None, ""):
        return (
            f"Ainda não tenho foto do {nome} aqui. "
            f"O preço é R$ {preco}. Quer saber mais alguma coisa sobre ele?"
        )
    return f"Ainda não tenho foto do {nome} aqui. Quer que eu te passe os detalhes?"


def resposta_com_foto(produto: dict) -> str:
    nome = produto.get("nome", "produto")
    preco = produto.get("preco", "")
    if preco not in (None, ""):
        return f"Segue a foto do {nome} — R$ {preco} 👇"
    return f"Segue a foto do {nome} 👇"


def resposta_ja_informado(produto: dict) -> str:
    nome = produto.get("nome", "produto")
    preco = produto.get("preco", "")
    return f"Como te passei, o {nome} está R$ {preco}. Quer que eu separe pra você?"


def perguntar_ia(
    mensagem: str,
    catalogo: str,
    historico_texto: str = "",
    nome_cliente: str = "",
    ultima_resposta_ia: str = "",
    foto_automatica: bool = False,
    contexto_venda: ContextoVenda | None = None,
) -> str:
    ctx = contexto_venda or ContextoVenda(catalogo=catalogo)
    if catalogo and not ctx.catalogo:
        ctx.catalogo = catalogo

    instrucoes = montar_instrucoes(ctx.briefing)
    entrada = montar_entrada_ia(
        nome_cliente=nome_cliente,
        mensagem=mensagem,
        historico_texto=historico_texto,
        ultima_resposta_ia=ultima_resposta_ia,
        catalogo=ctx.catalogo or catalogo,
        contexto_venda=ctx,
        foto_automatica=foto_automatica,
    )

    resposta = client.responses.create(
        model=MODEL,
        instructions=instrucoes,
        input=entrada,
    )

    return resposta.output_text
