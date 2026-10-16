from collections import Counter

def clinicas_com_mais_atendimentos(atendimentos):
    contagem = Counter(a.clinica.nome for a in atendimentos)
    return contagem.most_common()

def atendimentos_mais_caros_e_baratos(atendimentos):
    itens = list(atendimentos)
    if not itens: return {"mais_caros": [], "mais_baratos": []}
    maior, menor = max(a.valor for a in itens), min(a.valor for a in itens)
    return {"mais_caros": [a for a in itens if a.valor == maior],
            "mais_baratos": [a for a in itens if a.valor == menor]}

def procedimentos_mais_realizados(procedimentos):
    return Counter(p.descricao for p in procedimentos).most_common()

def procedimentos_mais_caros_e_baratos(procedimentos):
    itens = list(procedimentos)
    if not itens: return {"mais_caros": [], "mais_baratos": []}
    maior, menor = max(p.custo for p in itens), min(p.custo for p in itens)
    return {"mais_caros": [p for p in itens if p.custo == maior],
            "mais_baratos": [p for p in itens if p.custo == menor]}
