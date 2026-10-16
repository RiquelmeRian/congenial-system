from datetime import date, datetime
from abc import ABC, abstractmethod

def _data(valor):
    if isinstance(valor, datetime): return valor.date()
    if isinstance(valor, date): return valor
    try: return datetime.strptime(valor, "%Y-%m-%d").date()
    except (TypeError, ValueError) as exc: raise ValueError("Data deve estar no formato AAAA-MM-DD.") from exc

class Pagamento(ABC):
    def __init__(self, data, atendimento, valor_pago):
        self.data, self.atendimento = _data(data), atendimento
        if atendimento is None: raise ValueError("Atendimento obrigatório.")
        if self.data > _data(atendimento.data): raise ValueError("Pagamento deve ser realizado até a data do atendimento.")
        try: valor_pago = float(valor_pago)
        except (TypeError, ValueError) as exc: raise ValueError("Valor pago inválido.") from exc
        if valor_pago <= 0: raise ValueError("O valor pago deve ser maior que zero.")
        if valor_pago > atendimento.valor_restante: raise ValueError("Pagamento excede o valor restante.")
        self.paciente, self.valor_pago = atendimento.paciente, valor_pago
    @abstractmethod
    def modalidade(self): pass

class PagamentoDinheiro(Pagamento):
    def modalidade(self): return "Dinheiro"

class PagamentoPix(Pagamento):
    def __init__(self, data, atendimento, valor_pago, cpf_pagador):
        if not cpf_pagador: raise ValueError("CPF do pagador é obrigatório para PIX.")
        self.cpf_pagador = cpf_pagador
        super().__init__(data, atendimento, valor_pago)
    def modalidade(self): return "PIX"

class PagamentoCartao(Pagamento):
    def __init__(self, data, atendimento, valor_pago, numero_cartao, bandeira):
        if not numero_cartao or not bandeira: raise ValueError("Número do cartão e bandeira são obrigatórios.")
        self.numero_cartao, self.bandeira = numero_cartao, bandeira
        super().__init__(data, atendimento, valor_pago)
    def modalidade(self): return "Cartão de crédito"

class CadastroPagamentos:
    def __init__(self): self.pagamentos = []
    def incluir(self, pagamento):
        if not isinstance(pagamento, Pagamento): raise TypeError("Pagamento inválido.")
        if pagamento in self.pagamentos: raise ValueError("Pagamento já cadastrado.")
        pagamento.atendimento.pagamentos.append(pagamento)
        self.pagamentos.append(pagamento)
    def excluir(self, pagamento):
        if pagamento not in self.pagamentos: return False
        self.pagamentos.remove(pagamento)
        if pagamento in pagamento.atendimento.pagamentos: pagamento.atendimento.pagamentos.remove(pagamento)
        return True
    def alterar(self, pagamento, data, valor_pago):
        if pagamento not in self.pagamentos: return False
        atendimento = pagamento.atendimento
        d = _data(data)
        if d > _data(atendimento.data): raise ValueError("Pagamento deve ser realizado até a data do atendimento.")
        v = float(valor_pago)
        outros = sum(p.valor_pago for p in atendimento.pagamentos if p is not pagamento)
        if v <= 0 or v + outros > atendimento.valor + atendimento.total_procedimentos: raise ValueError("Valor pago inválido ou acima do saldo.")
        pagamento.data, pagamento.valor_pago = d, v
        return True
    def listar(self): return list(self.pagamentos)
