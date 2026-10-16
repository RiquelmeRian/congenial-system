class PessoasController:
    def __init__(self, cadastro): self.cadastro = cadastro
    def incluir(self, pessoa): self.cadastro.incluir(pessoa); return pessoa
    def excluir(self, cpf):
        if not self.cadastro.excluir(cpf): raise LookupError("Pessoa não encontrada.")
    def listar(self): return self.cadastro.listar()

class ClinicasController:
    def __init__(self, cadastro): self.cadastro = cadastro
    def incluir(self, clinica): self.cadastro.incluir(clinica); return clinica
    def excluir(self, nome):
        if not self.cadastro.excluir(nome): raise LookupError("Clínica não encontrada.")
    def listar(self): return self.cadastro.listar()

class AtendimentosController:
    def __init__(self, cadastro): self.cadastro = cadastro
    def incluir(self, atendimento): self.cadastro.incluir(atendimento); return atendimento
    def excluir(self, atendimento):
        if not self.cadastro.excluir(atendimento): raise LookupError("Atendimento não encontrado.")
    def listar(self): return self.cadastro.listar()

class ProcedimentosController:
    def __init__(self, cadastro): self.cadastro = cadastro
    def incluir(self, procedimento, atendimento): self.cadastro.incluir(procedimento, atendimento); return procedimento
    def listar(self): return self.cadastro.listar()

class PagamentosController:
    def __init__(self, cadastro): self.cadastro = cadastro
    def incluir(self, pagamento): self.cadastro.incluir(pagamento); return pagamento
    def listar(self): return self.cadastro.listar()