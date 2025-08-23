from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento  # corrigido o nome


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print('Você não tem saldo suficiente.')

        elif valor > 0:
            self._saldo -= valor
            print(f'Saque de R$ {valor:.2f} realizado com sucesso.')
            return True

        else:
            print('Valor inválido.')

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f'Depósito de R$ {valor:.2f} realizado com sucesso.')
            return True
        else:
            print('Valor inválido')
            return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print('Valor acima do limite por saque.')
        elif excedeu_saques:
            print('Limite de saques diários atingido.')
        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\nAgência:\t{self.agencia}
C/C:\t\t{self.numero}
Titular:\t{self.cliente.nome}"""


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor,
                'data': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),  # corrigido %S
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


# ---------------- MENU ---------------- #

def menu():
    menu = """\n
    ================ MENU ================
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNovo usuário
    [5]\tNova conta
    [6]\tListar contas
    [7]\tSair
    => """
    return input(menu).strip()


def mostrar_extrato(conta):
    print("\n===== EXTRATO =====")
    transacoes = conta.historico.transacoes
    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            print(f"{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}")
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("====================")


def main():
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            cpf = input("Informe o CPF do cliente: ")
            cliente = next((u for u in usuarios if u.cpf == cpf), None)

            if not cliente or not cliente.contas:
                print("Cliente não encontrado ou sem conta.")
                continue

            conta = cliente.contas[0]  # simplificação: sempre a 1ª conta
            valor = float(input("Valor do depósito: R$ "))
            cliente.realizar_transacao(conta, Deposito(valor))

        elif opcao == "2":
            cpf = input("Informe o CPF do cliente: ")
            cliente = next((u for u in usuarios if u.cpf == cpf), None)

            if not cliente or not cliente.contas:
                print("Cliente não encontrado ou sem conta.")
                continue

            conta = cliente.contas[0]
            valor = float(input("Valor do saque: R$ "))
            cliente.realizar_transacao(conta, Saque(valor))

        elif opcao == "3":
            cpf = input("Informe o CPF do cliente: ")
            cliente = next((u for u in usuarios if u.cpf == cpf), None)

            if not cliente or not cliente.contas:
                print("Cliente não encontrado ou sem conta.")
                continue

            conta = cliente.contas[0]
            mostrar_extrato(conta)

        elif opcao == "4":
            nome = input("Nome: ")
            nascimento = input("Data de nascimento (dd-mm-aaaa): ")
            cpf = input("CPF: ")
            endereco = input("Endereço: ")

            if any(u.cpf == cpf for u in usuarios):
                print("CPF já cadastrado.")
            else:
                cliente = PessoaFisica(cpf, nome, nascimento, endereco)
                usuarios.append(cliente)
                print("Usuário cadastrado com sucesso!")

        elif opcao == "5":
            cpf = input("Informe o CPF do cliente: ")
            cliente = next((u for u in usuarios if u.cpf == cpf), None)

            if not cliente:
                print("Cliente não encontrado.")
                continue

            numero_conta = len(contas) + 1
            conta = ContaCorrente.nova_conta(cliente, numero_conta)
            cliente.adicionar_conta(conta)
            contas.append(conta)
            print("\n=== Conta criada com sucesso! ===")

        elif opcao == "6":
            for conta in contas:
                print(conta)

        elif opcao == "7":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()