def exibir_lista(titulo, itens):
    print(f"\n=== {titulo} ===")

    if not itens:
        print("Nenhum registro cadastrado.")
        return

    for i, item in enumerate(itens, 1):
        print(f"{i}. {type(item).__name__}")

        for atributo, valor in vars(item).items():
            if atributo in ("atendimentos", "procedimentos"):
                continue

            if hasattr(valor, "nome"):
                valor = valor.nome

            print(f"   {atributo.replace('_', ' ').capitalize()}: {valor}")


def mensagem(texto): print(texto)
