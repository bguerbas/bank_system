import textwrap
from colorama import Fore


def menu() -> str:
    menu = f"""\n
    {Fore.GREEN}{'='*20} Menu {'='*20}{Fore.RESET}
    {Fore.YELLOW}
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova Conta
    [lc]\tListar Contas
    [nu]\tNovo Usuário
    [q]\tSair
    {Fore.RESET}
    {Fore.GREEN}{'='*46}{Fore.RESET}
    => """
    return input(textwrap.dedent(menu))


def create_user(users: list) -> None:
    cpf = input(f"{Fore.YELLOW}Digite o CPF do usuário: {Fore.RESET}")
    user = filter_user(cpf, users)

    if user:
        print(f"{Fore.RED}Usuário já cadastrado!{Fore.RESET}")
        return

    name = input(f"{Fore.YELLOW}Digite o nome completo: {Fore.RESET}")
    born_date = input(f"{Fore.YELLOW}Digite a data de nascimento (dd/mm/yyyy): {Fore.RESET}")
    address = input(f"{Fore.YELLOW}Digite o endereço (logradouro, nro - bairro - cidade/sigla_estado): {Fore.RESET}")

    users.append({
        'cpf': cpf,
        'name': name,
        'born_date': born_date,
        'address': address
    })
    print(f"{Fore.GREEN}Usuário cadastrado com sucesso!{Fore.RESET}")


def create_account(agency: str, account_num: int, users: list) -> dict or None:
    cpf = input(f"{Fore.YELLOW}Digite o CPF do usuário (apenas números): {Fore.RESET}")
    if len(cpf) != 13:
        print(f"{Fore.RED}CPF inválido!{Fore.RESET}")
        return

    user = filter_user(cpf, users)

    if user:
        print(f"{Fore.RED}Conta criada com sucesso!{Fore.RESET}")
        return {
            'agency': agency,
            'account_num': account_num,
            'user': user
        }

    print(f"{Fore.RED}Usuário não encontrado!{Fore.RESET}")


def list_accounts(accounts: list) -> None:
    if not accounts:
        print(f"{Fore.RED}Nenhuma conta cadastrada!{Fore.RESET}")
        return

    for account in accounts:
        line = f"""
        {Fore.GREEN}{'*'*20} Conta {'*'*20}{Fore.RESET}
        {Fore.YELLOW}\tAgência:{Fore.RESET} {account['agency']}
        {Fore.YELLOW}\tConta:{Fore.RESET} {account['account_num']}
        {Fore.YELLOW}\tTitular:{Fore.RESET} {account['user']['name']}
        {Fore.GREEN}{'*'*47}{Fore.RESET}
        """
        print("=" * 94)
        print(textwrap.dedent(line))


def filter_user(cpf: str, users: list) -> str or None:
    filter_users = [user for user in users if user['cpf'] == cpf]
    return filter_users[0] if filter_users else None


def deposit(balance: float, value: float, extract: str, /) -> tuple:
    if value > 0:
        balance += value
        extract += f"Depósito: R$ {value:.2f}\n"
        print(f"\n {Fore.GREEN}Depósito realizado com sucesso!{Fore.RESET}")
    else:
        print(f"{Fore.RED}Valor inválido! Por favor, digite um valor maior que zero.{Fore.RESET}")
    return balance, extract


def cash_out(*, balance: float, value: float, extract: str, limit: float, num_cash_out: int, limit_cash_out: float) -> tuple:
    exceeded_balance = value > balance
    exceeded_limit = value > limit
    exceeded_num_cash_out = num_cash_out >= limit_cash_out

    if exceeded_balance:
        print(f"{Fore.RED}Saldo insuficiente!{Fore.RESET}")
    elif exceeded_limit:
        print(f"{Fore.RED}Limite de saque excedido!{Fore.RESET}")
    elif exceeded_num_cash_out:
        print(f"{Fore.RED}Limite de saques excedido!{Fore.RESET}")
    elif value > 0:
        balance -= value
        extract += f"Saque:\t\tR$ {value:.2f}\n"
        num_cash_out += 1
        print(f"{Fore.GREEN}Saque realizado com sucesso!{Fore.RESET}")
    else:
        print(f"{Fore.RED}Valor inválido! Por favor, digite um valor maior que zero.{Fore.RESET}")

    return balance, extract


def display_extract(balance: float, /, *, extract: str) -> None:
    print(f"\n{Fore.GREEN}{'*' * 20} EXTRATO {'*' * 20}{Fore.RESET}")
    print("Não foram realizadas movimentações.") if balance == 0.0 and extract == "" else extract
    print(f"\n{Fore.YELLOW}Saldo: R$ {balance:.2f}{Fore.RESET}")
    print(f"{Fore.GREEN}{'*' * 49}{Fore.RESET}")


def main() -> None:
    LIMIT_CASH_OUT = 3
    AGENCY = '0001'

    balance: float = 0.0
    limit_cash_out: float = 500.0
    num_cash_out: int = 0
    extract: str = ""
    users: list = []
    accounts: list = []

    while True:
        option = menu()
        if option == 'd':
            value = float(input(f"{Fore.YELLOW}Digite o valor do depósito: {Fore.RESET}"))

            balance, extract = deposit(balance, value, extract)

        elif option == 's':
            value = float(input(f"{Fore.YELLOW}Digite o valor do saque: {Fore.RESET}"))

            balance, extract = cash_out(
                balance=balance, value=value, extract=extract, limit=limit_cash_out,
                num_cash_out=num_cash_out, limit_cash_out=LIMIT_CASH_OUT
            )

        elif option == 'e':
            display_extract(balance, extract=extract)

        elif option == 'nc':
            account_num = len(accounts) + 1
            account = create_account(AGENCY, account_num, users)

            if account:
                accounts.append(account)

        elif option == 'lc':
            list_accounts(accounts)

        elif option == 'nu':
            create_user(users)

        elif option == 'q':
            print(f"{Fore.GREEN}Saindo...{Fore.RESET}\n")
            break

        else:
            print(f"{Fore.RED}Opção inválida! Por favor, selecione uma opção válida.{Fore.RESET}")


if __name__ == '__main__':
    main()

