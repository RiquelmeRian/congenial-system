from datetime import date
from pessoa import Paciente, Profissional, CadastroPessoas
from clinica import Clinica, CadastroClinicas
from tipos_atendimento import TipoAtendimento, CadastroTiposAtendimento
from atendimento import Atendimento, CadastroAtendimentos
from procedimento import Procedimento, CadastroProcedimentos
from pagamento import (
    PagamentoDinheiro, PagamentoPix, PagamentoCartao, CadastroPagamentos
)
from controllers import (
    PessoasController, ClinicasController, AtendimentosController,
    ProcedimentosController, PagamentosController,
)
from relatorios import (
    clinicas_com_mais_atendimentos,
    atendimentos_mais_caros_e_baratos,
    procedimentos_mais_realizados,
    procedimentos_mais_caros_e_baratos,
)
from views import exibir_lista, mensagem


def ler_texto(prompt):
    while True:
        valor = input(prompt).strip()
        if valor:
            return valor
        print("O campo não pode ficar vazio.")


def ler_int(prompt, minimo=None):
    while True:
        try:
            valor = int(input(prompt).strip())
            if minimo is not None and valor < minimo:
                print(f"Informe um número maior ou igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Informe um número inteiro válido.")


def ler_float(prompt, minimo=0):
    while True:
        try:
            valor = float(input(prompt).strip().replace(",", "."))
            if valor < minimo:
                print(f"Informe um valor maior ou igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Informe um valor numérico válido.")


def escolher(lista, titulo):
    if not lista:
        print(f"Não há {titulo} cadastrados.")
        return None
    exibir_lista(titulo, lista)
    while True:
        indice = ler_int("Número do registro (0 para cancelar): ", 0)
        if indice == 0:
            return None
        if indice <= len(lista):
            return lista[indice - 1]
        print("Número fora da lista.")


def menu_pessoas(controller):
    while True:
        print("\n--- PESSOAS ---\n1. Cadastrar paciente\n2. Cadastrar profissional\n3. Listar pessoas\n4. Excluir pessoa\n0. Voltar")
        op = input("Opção: ").strip()
        try:
            if op == "1":
                obj = Paciente(ler_texto("Nome: "), ler_texto("Celular: "), ler_texto("CPF: "), ler_int("Idade: ", 0))
                controller.incluir(obj)
                mensagem("Paciente cadastrado.")
            elif op == "2":
                obj = Profissional(ler_texto("Nome: "), ler_texto("Celular: "), ler_texto("CPF: "), ler_texto("Especialidade: "), ler_texto("Registro profissional: "))
                controller.incluir(obj)
                mensagem("Profissional cadastrado.")
            elif op == "3":
                exibir_lista("Pessoas", controller.listar())
            elif op == "4":
                cpf = ler_texto("CPF da pessoa a excluir: ")
                controller.excluir(cpf)
                mensagem("Pessoa excluída.")
            elif op == "0": return
            else: print("Opção inválida.")
        except (ValueError, TypeError, LookupError) as erro:
            print(f"Não foi possível concluir a operação: {erro}")


def menu_clinicas(controller):
    while True:
        print("\n--- CLÍNICAS ---\n1. Cadastrar clínica\n2. Listar clínicas\n3. Excluir clínica\n0. Voltar")
        op = input("Opção: ").strip()
        try:
            if op == "1":
                nome = ler_texto("Nome: ")
                cidade = ler_texto("Cidade: ")
                descricao = ler_texto("Descrição: ")
                abertura = ler_texto("Abertura (HH:MM): ") or "08:00"
                fechamento = ler_texto("Fechamento (HH:MM): ") or "18:00"
                controller.incluir(Clinica(nome, cidade, descricao, abertura, fechamento))
                mensagem("Clínica cadastrada.")
            elif op == "2": exibir_lista("Clínicas", controller.listar())
            elif op == "3": controller.excluir(ler_texto("Nome da clínica: ")); mensagem("Clínica excluída.")
            elif op == "0": return
            else: print("Opção inválida.")
        except (ValueError, TypeError, LookupError) as erro: print(f"Não foi possível concluir a operação: {erro}")


def cadastrar_tipo(tipos):
    try:
        tipo = TipoAtendimento(ler_texto("Nome do tipo: "), ler_texto("Descrição: "))
        if any(t.nome.lower() == tipo.nome.lower() for t in tipos):
            raise ValueError("Já existe um tipo de atendimento com esse nome.")
        tipos.append(tipo)
        print("Tipo de atendimento cadastrado.")
    except (ValueError, TypeError) as erro: print(f"Não foi possível concluir: {erro}")


def menu_atendimentos(controller, clinicas, pessoas, tipos, procedimentos, pagamentos):
    while True:
        print("\n--- ATENDIMENTOS ---\n1. Agendar atendimento\n2. Listar atendimentos\n3. Excluir atendimento\n0. Voltar")
        op = input("Opção: ").strip()
        try:
            if op == "1":
                clinica = escolher(clinicas, "clínicas")
                pacientes = [p for p in pessoas if isinstance(p, Paciente)]
                paciente = escolher(pacientes, "pacientes")
                profissionais = [p for p in pessoas if isinstance(p, Profissional)]
                profissional = escolher(profissionais, "profissionais")
                tipo = escolher(tipos, "tipos de atendimento")
                if not all((clinica, paciente, profissional, tipo)):
                    print("Agendamento cancelado.")
                    continue
                data_txt = ler_texto("Data (AAAA-MM-DD): ")
                data_atendimento = date.fromisoformat(data_txt)
                inicio = ler_texto("Horário inicial (HH:MM): ")
                fim = ler_texto("Horário final (HH:MM): ")
                valor = ler_float("Valor do atendimento: ")
                atendimento = Atendimento(clinica, paciente, profissional, data_atendimento, inicio, fim, tipo, valor)
                controller.incluir(atendimento)
                mensagem("Atendimento agendado.")
            elif op == "2": exibir_lista("Atendimentos", controller.listar())
            elif op == "3":
                atendimento = escolher(controller.listar(), "atendimentos")
                if atendimento:
                    controller.excluir(atendimento)
                    for proc in list(procedimentos.listar()):
                        if proc in atendimento.procedimentos: procedimentos.cadastro.excluir(proc)
                    for pag in list(pagamentos.listar()):
                        if pag.atendimento is atendimento: pagamentos.excluir(pag)
                    mensagem("Atendimento excluído.")
            elif op == "0": return
            else: print("Opção inválida.")
        except (ValueError, TypeError, LookupError, AttributeError) as erro:
            print(f"Não foi possível concluir a operação: {erro}")


def menu_procedimentos(controller, atendimentos, pessoas):
    while True:
        print("\n--- PROCEDIMENTOS ---\n1. Registrar procedimento\n2. Listar procedimentos\n0. Voltar")
        op = input("Opção: ").strip()
        try:
            if op == "1":
                atendimento = escolher(atendimentos, "atendimentos")
                profissionais = [p for p in pessoas if isinstance(p, Profissional)]
                profissional = escolher(profissionais, "profissionais")
                if not atendimento or not profissional: continue
                proc = Procedimento(ler_texto("Descrição: "), ler_float("Custo: "), profissional)
                controller.incluir(proc, atendimento)
                mensagem("Procedimento registrado.")
            elif op == "2": exibir_lista("Procedimentos", controller.listar())
            elif op == "0": return
            else: print("Opção inválida.")
        except (ValueError, TypeError, LookupError) as erro: print(f"Não foi possível concluir: {erro}")


def menu_pagamentos(controller, atendimentos):
    while True:
        print("\n--- PAGAMENTOS ---\n1. Registrar pagamento\n2. Listar pagamentos\n0. Voltar")
        op = input("Opção: ").strip()
        try:
            if op == "1":
                atendimento = escolher(atendimentos, "atendimentos")
                if not atendimento: continue
                print(f"Saldo restante: R$ {atendimento.valor_restante:.2f}")
                valor = ler_float("Valor pago: ", 0.01)
                print("1. Dinheiro\n2. PIX\n3. Cartão de crédito")
                modalidade = input("Modalidade: ").strip()
                hoje = date.today()
                if modalidade == "1": pagamento = PagamentoDinheiro(hoje, atendimento, valor)
                elif modalidade == "2": pagamento = PagamentoPix(hoje, atendimento, valor, ler_texto("CPF do pagador: "))
                elif modalidade == "3": pagamento = PagamentoCartao(hoje, atendimento, valor, ler_texto("Número do cartão: "), ler_texto("Bandeira: "))
                else:
                    print("Modalidade inválida.")
                    continue
                controller.incluir(pagamento)
                mensagem(f"Pagamento registrado. Saldo restante: R$ {atendimento.valor_restante:.2f}")
            elif op == "2": exibir_lista("Pagamentos", controller.listar())
            elif op == "0": return
            else: print("Opção inválida.")
        except (ValueError, TypeError, LookupError) as erro: print(f"Não foi possível concluir: {erro}")


def menu_relatorios(atendimentos, procedimentos, clinicas):
    while True:
        print("\n--- RELATÓRIOS ---\n1. Clínicas com mais atendimentos\n2. Atendimentos mais caros e mais baratos\n3. Procedimentos mais realizados\n4. Procedimentos mais caros e mais baratos\n0. Voltar")
        op = input("Opção: ").strip()
        try:
            if op == "1": exibir_lista("Clínicas por quantidade de atendimentos", clinicas_com_mais_atendimentos(atendimentos))
            elif op == "2": exibir_lista("Atendimentos mais caros e mais baratos", atendimentos_mais_caros_e_baratos(atendimentos))
            elif op == "3": exibir_lista("Procedimentos mais realizados", procedimentos_mais_realizados(procedimentos))
            elif op == "4": exibir_lista("Procedimentos mais caros e mais baratos", procedimentos_mais_caros_e_baratos(procedimentos))
            elif op == "0": return
            else: print("Opção inválida.")
        except (ValueError, TypeError, LookupError) as erro: print(f"Erro ao gerar relatório: {erro}")


def main():
    cadastro_pessoas = CadastroPessoas()
    cadastro_clinicas = CadastroClinicas()
    cadastro_atendimentos = CadastroAtendimentos()
    cadastro_procedimentos = CadastroProcedimentos()
    cadastro_pagamentos = CadastroPagamentos()
    pessoas = PessoasController(cadastro_pessoas)
    clinicas = ClinicasController(cadastro_clinicas)
    atendimentos = AtendimentosController(cadastro_atendimentos)
    procedimentos = ProcedimentosController(cadastro_procedimentos)
    pagamentos = PagamentosController(cadastro_pagamentos)
    tipos = []

    while True:
        print("\n========== SISTEMA DE GERENCIAMENTO DE CLÍNICAS ==========")
        print("1. Cadastrar pessoas")
        print("2. Cadastrar clínicas")
        print("3. Cadastrar tipo de atendimento")
        print("4. Listar tipos de atendimento")
        print("5. Gerenciar atendimentos")
        print("6. Gerenciar procedimentos")
        print("7. Gerenciar pagamentos")
        print("8. Relatórios")
        print("0. Sair")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1": menu_pessoas(pessoas)
        elif opcao == "2": menu_clinicas(clinicas)
        elif opcao == "3": cadastrar_tipo(tipos)
        elif opcao == "4": exibir_lista("Tipos de atendimento", tipos)
        elif opcao == "5": menu_atendimentos(atendimentos, clinicas.listar(), pessoas.listar(), tipos, procedimentos, pagamentos)
        elif opcao == "6": menu_procedimentos(procedimentos, atendimentos.listar(), pessoas.listar())
        elif opcao == "7": menu_pagamentos(pagamentos, atendimentos.listar())
        elif opcao == "8": menu_relatorios(atendimentos.listar(), procedimentos.listar(), clinicas.listar())
        elif opcao == "0":
            break
        else: print("Opção inválida. Escolha uma opção do menu.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nSistema encerrado pelo usuário.")
