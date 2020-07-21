from structure.products import *
from structure.people import *

print('-=' * 20)
print(f'{" RUANZIN LANCHES ":=^40}')
print('-=' * 20)
print()
print('''QUAL OPÇÃO DESEJA:
[ 1 ] Cadastro de Produtos
[ 2 ] Cadastro de Clientes
[ 3 ] Pedidos
[ 4 ] Sair''')

while True:
    opcao = int(input('Qual é a opção? '))
    if opcao == 1:
        print('Abrindo janela...')
        run = Product(window=Tk())
        mainloop()
    if opcao == 2:
        print('Abrindo janela...')
        run = Client(window=Tk())
        mainloop()

    if opcao == 3:
        pass

    if opcao == 4:
        break
