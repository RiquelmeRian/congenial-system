class TipoAtendimento:
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao

    def alterar(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao


class CadastroTiposAtendimento:
    def __init__(self):
        self.tipos_atendimento = []

    def incluir(self, tipo_atendimento):
        self.tipos_atendimento.append(tipo_atendimento)

    def excluir(self, nome):
        for tipo_atendimento in self.tipos_atendimento:
            if tipo_atendimento.nome == nome:
                self.tipos_atendimento.remove(tipo_atendimento)
                return True
        return False

    def alterar(self, nome, novo_nome, descricao):
        for tipo_atendimento in self.tipos_atendimento:
            if tipo_atendimento.nome == nome:
                tipo_atendimento.alterar(novo_nome, descricao)
                return True
        return False

    def listar(self):
        return self.tipos_atendimento