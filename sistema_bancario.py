saldo = 0
limite_valor = 500
limite_saques = 3
extrato = ''
saques_realizados = 0

while True:
  print('-' * 5, 'MENU', '-' * 5)
  print('''
  1 - Depósito
  2 - Saque
  3 - Extrato
  4 - Sair''')
  print('-' * 16)

  acao = int(input('O que deseja fazer? => '))

  if acao == 1:
    valor = float(input('Informe o valor do depósito: R$ '))
    if valor > 0:
      saldo += valor
      extrato += f'Depósito: R$ {valor:.2f}\n'
      print(f'Depósito de R$ {valor:.2f} realizado com sucesso.\n')
    else:
      print('Valor inválido.')

  elif acao == 2:
    valor = float(input('Informe o valor do saque: R$ '))
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

  elif acao == 3:
    print('-' * 5, 'EXTRATO', '-' * 5)
    if not extrato:
      print('Não foram realizadas movimentações.')
    else:
      print(extrato, end='')
      print(f'\nSaldo: R$ {saldo:.2f}')
      print('-' * 16)

  elif acao == 4:
    print('Encerrando o sistema. Até mais!')
    break

  else:
    print('Opção inválida. Tente novamente.')