class Procedimento:
    def __init__(self, descricao, custo, profissional):
        if not descricao or profissional is None: raise ValueError("Descrição e profissional responsável são obrigatórios.")
        try: custo = float(custo)
        except (TypeError, ValueError) as exc: raise ValueError("Custo inválido.") from exc
        if custo < 0: raise ValueError("Custo não pode ser negativo.")
        self.descricao, self.custo, self.profissional = descricao, custo, profissional
        self.atendimento = None

class CadastroProcedimentos:
    def __init__(self): self.procedimentos = []
    def incluir(self, procedimento, atendimento):
        if not isinstance(procedimento, Procedimento): raise TypeError("Procedimento inválido.")
        if atendimento is None: raise ValueError("Atendimento é obrigatório.")
        if procedimento in self.procedimentos: raise ValueError("Procedimento já cadastrado.")
        procedimento.atendimento = atendimento
        atendimento.procedimentos.append(procedimento)
        self.procedimentos.append(procedimento)
    def excluir(self, procedimento):
        if procedimento not in self.procedimentos: return False
        self.procedimentos.remove(procedimento)
        if procedimento.atendimento and procedimento in procedimento.atendimento.procedimentos:
            procedimento.atendimento.procedimentos.remove(procedimento)
        procedimento.atendimento = None
        return True
    def alterar(self, procedimento, descricao, custo, profissional):
        if procedimento not in self.procedimentos: return False
        novo = float(custo)
        if novo < 0 or not descricao or profissional is None: raise ValueError("Dados do procedimento inválidos.")
        procedimento.descricao, procedimento.custo, procedimento.profissional = descricao, novo, profissional
        return True
    def listar(self): return list(self.procedimentos)
