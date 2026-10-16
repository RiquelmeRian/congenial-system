class Atendimento:
    def __init__(self, clinica, paciente, profissional, data,
                 horario_inicio, horario_fim, tipo_atendimento, valor):
        self.clinica = clinica
        self.paciente = paciente
        self.profissional = profissional
        self.data = data
        self.horario_inicio = horario_inicio
        self.horario_fim = horario_fim
        self.tipo_atendimento = tipo_atendimento
        self.valor = valor

        clinica.atendimentos.append(self)

    def alterar(self, clinica, paciente, profissional, data,
                horario_inicio, horario_fim, tipo_atendimento, valor):

        if self in self.clinica.atendimentos:
            self.clinica.atendimentos.remove(self)

        self.clinica = clinica
        self.paciente = paciente
        self.profissional = profissional
        self.data = data
        self.horario_inicio = horario_inicio
        self.horario_fim = horario_fim
        self.tipo_atendimento = tipo_atendimento
        self.valor = valor

        clinica.atendimentos.append(self)


class CadastroAtendimentos:
    def __init__(self):
        self.atendimentos = []

    def incluir(self, atendimento):
        self.atendimentos.append(atendimento)

    def excluir(self, atendimento):
        if atendimento in self.atendimentos:
            self.atendimentos.remove(atendimento)

            if atendimento in atendimento.clinica.atendimentos:
                atendimento.clinica.atendimentos.remove(atendimento)

            return True

        return False

    def alterar(self, atendimento, clinica, paciente, profissional, data,
                horario_inicio, horario_fim, tipo_atendimento, valor):

        if atendimento in self.atendimentos:
            atendimento.alterar(
                clinica,
                paciente,
                profissional,
                data,
                horario_inicio,
                horario_fim,
                tipo_atendimento,
                valor
            )
            return True

        return False

    def listar(self):
        return self.atendimentos