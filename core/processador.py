"""
PROCESSADOR DE ESTRUTURA - WebStruct Analyzer
Processa os dados do mapeamento e constrói a árvore
"""


def processar_estrutura(dados_brutos):
    if not dados_brutos:
        return {"arvore": [], "total": 0, "estatisticas": {}}

    return {
        "arvore": construir_arvore(dados_brutos),
        "total": len(dados_brutos),
        "estatisticas": extrair_estatisticas(dados_brutos),
    }


def construir_arvore(elementos):
    if not elementos:
        return []
    raiz = elementos[0] if elementos else None
    return [raiz] if raiz else []


def extrair_estatisticas(elementos):
    tags = {}
    total_com_texto = total_com_classe = total_com_id = 0

    for elem in elementos:
        tag = elem.get("tag", "")
        tags[tag] = tags.get(tag, 0) + 1

        if elem.get("texto"):
            total_com_texto += 1
        if elem.get("classe"):
            total_com_classe += 1
        if elem.get("id"):
            total_com_id += 1

    return {
        "total_elementos": len(elementos),
        "total_com_texto": total_com_texto,
        "total_com_classe": total_com_classe,
        "total_com_id": total_com_id,
        "tags_mais_comuns": dict(
            sorted(tags.items(), key=lambda x: x[1], reverse=True)[:5]
        ),
    }
