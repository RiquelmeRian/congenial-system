class Pessoa:
    def __init__(self, nome, celular, cpf):
        self.nome = nome
        self.celular = celular
        self.cpf = cpf

    def alterar(self, nome, celular, cpf):
        self.nome = nome
        self.celular = celular
        self.cpf = cpf


class Paciente(Pessoa):
    def __init__(self, nome, celular, cpf, idade):
        super().__init__(nome, celular, cpf)
        self.idade = idade

    def alterar(self, nome, celular, cpf, idade):
        super().alterar(nome, celular, cpf)
        self.idade = idade


class Profissional(Pessoa):
    def __init__(self, nome, celular, cpf, especialidade, registro_profissional):
        super().__init__(nome, celular, cpf)
        self.especialidade = especialidade
        self.registro_profissional = registro_profissional

    def alterar(self, nome, celular, cpf, especialidade, registro_profissional):
        super().alterar(nome, celular, cpf)
        self.especialidade = especialidade
        self.registro_profissional = registro_profissional


class CadastroPessoas:
    def __init__(self):
        self.pessoas = []

    def incluir(self, pessoa):
        self.pessoas.append(pessoa)

    def excluir(self, cpf):
        for pessoa in self.pessoas:
            if pessoa.cpf == cpf:
                self.pessoas.remove(pessoa)
                return True
        return False

    def alterar(self, cpf, nome, celular, novo_cpf):
        for pessoa in self.pessoas:
            if pessoa.cpf == cpf:
                pessoa.alterar(nome, celular, novo_cpf)
                return True
        return False

    def listar(self):
        return self.pessoas