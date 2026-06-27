from services.vendas.catalogo import LIMITE_CATALOGO, montar_contexto_catalogo


def eh_saudacao(mensagem: str, historico_texto: str = "") -> bool:
    from services.conversa_service import eh_saudacao_inicial

    return eh_saudacao_inicial(mensagem, historico_texto)


def buscar_produtos_para_atendimento(mensagem: str, historico_texto: str = "") -> dict:
    """Mercos primeiro; Supabase como fallback. Usado em testes e fechamento."""
    ctx = montar_contexto_catalogo(mensagem, historico_texto)
    return {
        "produtos": ctx["produtos"],
        "similares": ctx["similares"],
        "upsell": ctx["upsell"],
        "complementos": ctx["complementos"],
        "fonte": ctx["fonte"],
        "erro_mercos": ctx["erro_mercos"],
        "catalogo": ctx["catalogo"],
    }
