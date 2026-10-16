class Clinica:
    def __init__(self, nome, cidade, descricao):
        self.nome = nome
        self.cidade = cidade
        self.descricao = descricao
        self.atendimentos = []

    def alterar(self, nome, cidade, descricao):
        self.nome = nome
        self.cidade = cidade
        self.descricao = descricao


class CadastroClinicas:
    def __init__(self):
        self.clinicas = []

    def incluir(self, clinica):
        self.clinicas.append(clinica)

    def excluir(self, nome):
        for clinica in self.clinicas:
            if clinica.nome == nome:
                self.clinicas.remove(clinica)
                return True
        return False

    def alterar(self, nome, novo_nome, cidade, descricao):
        for clinica in self.clinicas:
            if clinica.nome == nome:
                clinica.alterar(novo_nome, cidade, descricao)
                return True
        return False

    def listar(self):
        return self.clinicas