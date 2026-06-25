import os

from dotenv import load_dotenv

from services.mercos_service import (
    _extrair_termos,
    buscar_produtos_para_atendimento as buscar_produtos_mercos,
    montar_catalogo_texto,
)
from services.supabase_service import buscar_produtos

load_dotenv(override=True)

LIMITE_CATALOGO = 20


def _fonte_configurada() -> str:
    return os.getenv("PRODUTOS_FONTE", "auto").strip().lower()


def _filtrar_produtos(produtos: list[dict], mensagem: str) -> list[dict]:
    termos = _extrair_termos(mensagem)

    if not termos:
        return produtos[:LIMITE_CATALOGO]

    encontrados = []
    for produto in produtos:
        texto = " ".join(
            str(produto.get(campo, "") or "")
            for campo in ("nome", "codigo", "categoria", "descricao")
        ).lower()

        if any(termo in texto for termo in termos):
            encontrados.append(produto)

    return encontrados[:LIMITE_CATALOGO]


def _buscar_supabase(mensagem: str) -> list[dict]:
    produtos = buscar_produtos()
    return _filtrar_produtos(produtos, mensagem)


def buscar_produtos_para_atendimento(mensagem: str) -> dict:
    fonte = _fonte_configurada()
    erro_mercos = None

    if fonte in ("mercos", "auto"):
        try:
            produtos = buscar_produtos_mercos(mensagem)
            return {
                "produtos": produtos,
                "fonte": "mercos",
                "erro_mercos": None,
            }
        except Exception as e:
            erro_mercos = str(e)
            if fonte == "mercos":
                raise

    produtos = _buscar_supabase(mensagem)
    return {
        "produtos": produtos,
        "fonte": "supabase",
        "erro_mercos": erro_mercos,
    }
