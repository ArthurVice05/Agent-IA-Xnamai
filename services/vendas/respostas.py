def resposta_fora_catalogo(
    nome_cliente: str = "",
    termos: list | None = None,
    amostra: list | None = None,
) -> str:
    """
    Resposta fixa quando o cliente pede algo que a loja não vende.
    Evita a IA simular estoque (cor/tamanho) ou prometer reposição.
    """
    nome = nome_cliente or "Cliente"
    termos_produto = [t for t in (termos or []) if t not in {
        "vermelha", "vermelho", "azul", "preto", "branco", "rosa", "verde", "amarelo",
        "linda", "lindo", "bonita", "bonito", "fica", "ficou", "show", "perfeito",
    }]
    pedido = " ".join(termos_produto) if termos_produto else (" ".join(termos) if termos else "isso")

    if amostra:
        exemplos = [p.get("nome", "") for p in amostra[:3] if p.get("nome")]
        if len(exemplos) == 1:
            linha_cat = f"Aqui trabalhamos com {exemplos[0]}, por exemplo."
        elif exemplos:
            linha_cat = (
                f"Aqui trabalhamos com {exemplos[0]} e {exemplos[1]}, entre outros."
            )
        else:
            linha_cat = ""
    else:
        linha_cat = ""

    partes = [
        f"{nome}, a gente não trabalha com {pedido} — não faz parte do nosso catálogo."
    ]
    if linha_cat:
        partes.append(linha_cat)
    partes.append("Quer que eu te mostre o que temos disponível?")

    return " ".join(partes)
