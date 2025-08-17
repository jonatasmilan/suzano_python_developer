def menu():
    menu = """\n
    ================ MENU ================
    [1]\tDepósito
    [2]\tSaque
    [3]\tExtrato
    [4]\tNovo usuário
    [5]\tNova conta
    [6]\tListar contas
    [7]\tSair
    => """
    return input(menu).strip()


def deposito(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f'Depósito: R$ {valor:.2f}\n'
        print(f'Depósito de R$ {valor:.2f} realizado com sucesso.\n')
    else:
        print('Valor inválido.')
    return saldo, extrato


def saque(saldo, valor, extrato, limite_valor, saques_realizados, limite_saques):
    if valor > saldo:
        print('Saldo insuficiente.\n')
    elif valor > limite_valor:
        print('Valor acima do limite por saque.')
    elif saques_realizados >= limite_saques:
        print('Limite de saques diários atingido.')
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        saques_realizados += 1
        print(f'Saque de R$ {valor:.2f} realizado com sucesso.')
    else:
        print('Valor inválido.')

    return saldo, extrato, saques_realizados


def mostrar_extrato(saldo, extrato):
    print('-' * 5, 'EXTRATO', '-' * 5)
    if not extrato:
        print('Não foram realizadas movimentações.')
    else:
        print(extrato, end='')
    print(f'\nSaldo: R$ {saldo:.2f}')
    print('-' * 19)


def criar_usuario(usuarios):
    nome = input('Nome: ')
    nascimento = input('Data de nascimento: ')
    cpf = input('CPF: ')
    endereco = input('Endereço: ')

    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print('CPF já cadastrado.')
        return

    usuarios.append({"nome": nome, "nascimento": nascimento, "cpf": cpf, "endereco": endereco})
    print('Usuário cadastrado com sucesso!')


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\nUsuário não encontrado!")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
Agência:\t{conta['agencia']}
C/C:\t\t{conta['numero_conta']}
Titular:\t{conta['usuario']['nome']}"""
        print('-' * 30)
        print(linha)


def main():
    agencia = '0001'
    saldo = 0
    limite_valor = 500
    limite_saques = 3
    extrato = ''
    saques_realizados = 0
    usuarios = []
    contas = []

    while True:
        acao = menu()

        if acao == '1':
            valor = float(input('Informe o valor do depósito: R$ '))
            saldo, extrato = deposito(saldo, valor, extrato)

        elif acao == '2':
            valor = float(input('Informe o valor do saque: R$ '))
            saldo, extrato, saques_realizados = saque(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite_valor=limite_valor,
                saques_realizados=saques_realizados,
                limite_saques=limite_saques,
            )

        elif acao == '3':
            mostrar_extrato(saldo, extrato=extrato)

        elif acao == '4':
            criar_usuario(usuarios)

        elif acao == '5':
            numero_conta = len(contas) + 1
            conta = criar_conta(agencia, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif acao == '6':
            listar_contas(contas)

        elif acao == '7':
            print("Saindo...")
            break

        else:
            print('Operação inválida.')


main()
 
 