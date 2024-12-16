import xmlrpc.client
import sys


# Função para realizar as operações de cálculo
def calcula(calc_server):
    a = int(input("Digite o primeiro número: "))
    b = int(input("Digite o segundo número: "))

    print(f"Soma: {calc_server.soma(a, b)}")
    print(f"Subtração: {calc_server.subtracao(a, b)}")
    print(f"Multiplicação: {calc_server.multiplicacao(a, b)}")
    print(f"Divisão: {calc_server.divisao(a, b)}")


if __name__ == "__main__":

    if len(sys.argv) < 2:  # aqui fazes a verificacao sobre quantos args queres receber, o nome do programa conta como 1
        print('Digite o endereço do Servidor.')
        print(sys.argv)
        sys.exit()
    server_address = sys.argv[1]
    # Descobrir a porta do servidor de calculadora usando o binder
    binder = xmlrpc.client.ServerProxy(f'http://{server_address}:65431')
    calc_server_port = binder.discover_service('calculadora')

    if calc_server_port is None:
        print("Serviço de calculadora não encontrado.")
        exit(1)

    # Cria um cliente que se conecta ao servidor de calculadora na porta descoberta
    calc_server = xmlrpc.client.ServerProxy(f'http://{server_address}:{calc_server_port}')
    calcula(calc_server)