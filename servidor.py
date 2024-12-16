from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client


# Funções da calculadora
def soma(a, b):
    return a + b


def subtracao(a, b):
    return a - b


def multiplicacao(a, b):
    return a * b


def divisao(a, b):
    if b == 0:
        return "Erro: Divisão por zero."
    return a / b

if __name__ == '__main__':
    # Configura o servidor
    calc_server_port = 65432
    calc_server = SimpleXMLRPCServer(('localhost', calc_server_port))
    print("Servidor de calculadora pronto e aguardando conexões...")

    # Registra as funções da calculadora
    calc_server.register_function(soma, "soma")
    calc_server.register_function(subtracao, "subtracao")
    calc_server.register_function(multiplicacao, "multiplicacao")
    calc_server.register_function(divisao, "divisao")

    # Registrar o servidor da calculadora no binder
    binder = xmlrpc.client.ServerProxy('http://localhost:65431')
    binder.register_service('calculadora', calc_server_port)

    # Mantém o servidor em execução
    calc_server.serve_forever()