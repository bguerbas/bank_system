

menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
=> """

saldo = 0.0
limite_saque = 1000.0
extrato = 0.0
numero_saques = 0
LIMITE_SAQUES = 3


while True:
    opcao = input(menu)
    if opcao == 'd':
        valor = float(input("Digite o valor do depósito: "))

        if valor > 0:
            saldo += valor
            print(f"Novo saldo: R$ {saldo:.2f}\n")
        else:
            print("Valor inválido! Por favor, digite um valor maior que zero.")
    elif opcao == 's':
        if numero_saques < LIMITE_SAQUES:
            valor = float(input("Digite o valor do saque: "))
            if saldo >= valor > 0 and valor <= limite_saque:
                saldo -= valor
                numero_saques += 1
                extrato = f"Novo saldo: R$ {saldo:.2f}\n"
            else:
                print("Saldo insuficiente ou limite de saque excedido!")
        else:
            print("Limite de saques excedido!")
    elif opcao == 'e':
        print('\n' + '*' * 20 + ' EXTRATO ' + '*' * 20)
        if saldo == 0.0 and extrato == 0.0:
            print('Não foram realizadas movimentações.')
        print(f"\nSaldo: R$ {saldo:.2f}")
        print('*' * 49)
    elif opcao == 'q':
        print("Saindo...")
        break
    else:
        print("Opção inválida! Por favor, selecione uma opção válida.")

