import textwrap
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime

from colorama import Fore


@dataclass
class Client:
    address: str
    accounts: list = field(init=False, default_factory=lambda: [])

    @staticmethod
    async def make_transaction(account, transaction):
        transaction.register(account)

    async def add_account(self, account):
        self.accounts.append(account)


@dataclass
class PhysicalPerson(Client):
    name: str
    cpf: str
    birth_date: str
    address: str


@dataclass
class Historic:
    _transactions: list = field(default_factory=lambda: [])

    @property
    def transactions(self):
        return self._transactions

    def add_transaction(self, transaction):
        self._transactions.append(
            {
                'type': transaction.__class__.__name__,
                'value': transaction.value,
                'date': datetime.now().strftime("d%-%m-%Y %H:%M:%S")
            }
        )


@dataclass
class Account:
    _number: int = field(init=False)
    _client: str = field(init=False)
    _historic: Historic()
    _balance: float = field(default=0.0)
    _agency: str = field(default='0001')

    @classmethod
    def new_account(cls, _client, _number):
        return cls(_client, _number)

    @property
    def balance(self):
        return self._balance

    @property
    def number(self):
        return self._number

    @property
    def client(self):
        return self._client

    @property
    def agency(self):
        return self._agency

    @property
    def historic(self):
        return self._historic

    def cash_out(self, value) -> bool:
        balance = self.balance
        exceeded_balance = value > balance

        if exceeded_balance:
            print(f"{Fore.RED}Saldo insuficiente!{Fore.RESET}")

        elif value > 0:
            self._balance -= value
            print(f"{Fore.GREEN}Saque realizado com sucesso!{Fore.RESET}")
            return True

        else:
            print(f"{Fore.RED}Valor inválido! Por favor, digite um valor maior que zero.{Fore.RESET}")

        return False

    def deposit(self, value) -> bool:
        if value > 0:
            self._balance += value
            print(f"\n {Fore.GREEN}Depósito realizado com sucesso!{Fore.RESET}")
            return True
        else:
            print(f"{Fore.RED}Valor inválido! Por favor, digite um valor maior que zero.{Fore.RESET}")
            return False


@dataclass
class CurrentAccount(Account):
    numero: int = field(init=False)
    client: str = field(init=False)
    limit: float = field(default=500.0)
    limit_cash_out: int = field(default=3)

    def cash_out(self, value) -> bool or float:
        num_cash_out = len(
            [transaction for transaction in self.historic if transaction.type == CashOut.__name__]
        )
        exceeded_limit = value >= self.limit_cash_out
        exceeded_cash_out = num_cash_out >= self.limit_cash_out

        if exceeded_limit:
            print(f"{Fore.RED}Limite de saques excedido!{Fore.RESET}")
        elif exceeded_cash_out:
            print(f"{Fore.RED}Limite de saques excedido!{Fore.RESET}")
        else:
            return super().cash_out(value)

        return False

    def __str__(self) -> str:
        return f"""
        {Fore.GREEN}{'*' * 20} Conta {'*' * 20}{Fore.RESET}
        {Fore.YELLOW}\tAgência:{Fore.RESET} {self.agency}
        {Fore.YELLOW}\tConta:{Fore.RESET} {self.number}
        {Fore.YELLOW}\tTitular:{Fore.RESET} {self.client}
        {Fore.GREEN}{'*' * 47}{Fore.RESET}
        """


@dataclass
class Transaction(ABC):
    @property
    @abstractmethod
    def value(self) -> float:
        pass

    @abstractmethod
    def register(self, account) -> None:
        pass


@dataclass
class CashOut(Transaction):
    _valor: float

    @property
    def value(self) -> float:
        return self._valor

    def register(self, account) -> None:
        success_transaction = account.cash_out(self.value)

        if success_transaction:
            account.historic.add_transaction(self)


@dataclass
class Deposit(Transaction):
    _valor: float

    @property
    def value(self) -> float:
        return self._valor

    def register(self, account) -> None:
        success_transaction = account.deposit(self.value)

        if success_transaction:
            account.historic.add_transaction(self)


@dataclass
class SystemBank:
    clients: list = field(default_factory=lambda: [])
    accounts: list = field(default_factory=lambda: [])

    @staticmethod
    def menu():
        menu = f"""\n
        {Fore.GREEN}{'=' * 20} Menu {'=' * 20}{Fore.RESET}
        {Fore.YELLOW}
        [1]\tDepositar
        [2]\tSacar
        [3]\tExtrato
        [4]\tNova Conta
        [5]\tListar Contas
        [6]\tNovo Usuário
        [7]\tSair
        {Fore.RESET}
        {Fore.GREEN}{'=' * 46}{Fore.RESET}
        => """
        return input(textwrap.dedent(menu))

    def filter_clients(self, cpf):
        filter_client = [client for client in self.clients if client.cpf == cpf]
        return filter_client[0] if filter_client else None

    @staticmethod
    def request_customer_account(client):
        if not client:
            print(f"{Fore.RED}Usuário não encontrado!{Fore.RESET}")
            return

        return client.accounts[0]

    def get_user(self, with_cpf=False) -> tuple or None or Client:
        cpf = input(f"{Fore.YELLOW}Digite o CPF do usuário: {Fore.RESET}")
        client = self.filter_clients(cpf)

        if not client:
            print(f"{Fore.RED}Usuário não encontrado!{Fore.RESET}")
            return None, cpf if with_cpf else None
        else:
            return client, cpf if with_cpf else client

    def deposit(self):
        client = self.get_user()

        value = float(input(f"{Fore.YELLOW}Digite o valor do depósito: {Fore.RESET}"))
        transaction = Deposit(value)
        account = self.request_customer_account(client)

        if not account:
            return
        client.make_transaction(account, transaction)

    def cash_out(self):
        client = self.get_user()

        value = float(input(f"{Fore.YELLOW}Digite o valor do saque: {Fore.RESET}"))
        transaction = CashOut(value)
        account = self.request_customer_account(client)

        if not account:
            return
        client.make_transaction(account, transaction)

    def extract(self):
        client = self.get_user()

        account = self.request_customer_account(client)

        if not account:
            return
        print(f"\n{Fore.GREEN}{'*' * 20} Extrato {'*' * 20}{Fore.RESET}")
        transactions = account.historic.transactions
        extract = ""
        if not transactions:
            extract = "Não há transações para exibir."
        else:
            for transaction in transactions:
                extract += f"\n{Fore.YELLOW}{transaction['type']}:{Fore.RESET}\n\tR$ {transaction['value']:.2f}" \
                           f"\n{Fore.YELLOW}Data:{Fore.RESET}\n\t{transaction['date']}"
        print(extract)
        print(f"\n{Fore.YELLOW}Saldo:{Fore.RESET}\n\tR$ {account.balance:.2f}")
        print(f"{Fore.GREEN}{'*' * 49}{Fore.RESET}")

    def create_client(self):
        client, cpf = self.get_user(with_cpf=True)

        if client:
            print(f'{Fore.RED}Já existe cliente com esse CPF!{Fore.RESET}')
            return

        name = input(f"{Fore.YELLOW}Digite o nome completo: {Fore.RESET}")
        birth_data = str(input(f"{Fore.YELLOW}Digite a data de nascimento (dd/mm/yyyy): {Fore.RESET}"))
        address = input(f"{Fore.YELLOW}Digite o endereço (logradouro, nº - bairro - cidade/sigla_estado): {Fore.RESET}")

        client = PhysicalPerson(name, cpf, birth_data, address)

        self.clients.append(client)

        print(f"\n{Fore.GREEN}=== Cliente criado com sucesso! ==={Fore.RESET}")

    def create_account(self, account_number):
        client = self.get_user()

        if not client:
            return

        account = CurrentAccount.new_account(client, account_number)
        self.accounts.append(account)
        client.accounts.append(account)

        print(f"\n{Fore.GREEN}=== Conta criada com sucesso! ==={Fore.RESET}")

    def list_accounts(self):
        print(f"\n{Fore.GREEN}{'*' * 20} Contas {'*' * 20}{Fore.RESET}")
        for account in self.accounts:
            print(f"\n{Fore.YELLOW}Número da conta:{Fore.RESET}\n\t{account.number}")
            print(f"{Fore.YELLOW}Saldo:{Fore.RESET}\n\tR$ {account.balance:.2f}")
            print(f"{Fore.YELLOW}Limite de saque:{Fore.RESET}\n\tR$ {account.limit_cash_out:.2f}")
            print(f"{Fore.YELLOW}Número de saques:{Fore.RESET}\n\t{account.num_cash_out}")
            print(f"{Fore.YELLOW}Data de criação:{Fore.RESET}\n\t{account.creation_date}")
            print(f"{Fore.YELLOW}Data de atualização:{Fore.RESET}\n\t{account.update_date}")
            print(f"{Fore.YELLOW}Status:{Fore.RESET}\n\t{account.status}")
            print(f"{Fore.GREEN}{'*' * 100}{Fore.RESET}")


@dataclass
class Setup(SystemBank):
    def main(self):
        while True:
            option = int(self.menu())

            if option == 1:
                self.deposit()

            elif option == 2:
                self.cash_out()

            elif option == 3:
                self.extract()

            elif option == 4:
                account_number = len(self.accounts) + 1
                self.create_account(account_number)

            elif option == 5:
                self.list_accounts()

            elif option == 6:
                self.create_client()

            elif option == 7:
                print(f"{Fore.GREEN}Saindo...{Fore.RESET}\n")
                break

            else:
                print(f"{Fore.RED}Opção inválida! Por favor, selecione uma opção válida.{Fore.RESET}")


if __name__ == '__main__':
    start = Setup()
    start.main()