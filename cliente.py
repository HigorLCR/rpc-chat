import xmlrpc.client
import time
import sys


if __name__ == "__main__":

    if len(sys.argv) < 2:  # aqui fazes a verificacao sobre quantos args queres receber, o nome do programa conta como 1
        print('Digite o endereço do Servidor.')
        print(sys.argv)
        sys.exit()
    server_address = sys.argv[1]

    # Descobrir a porta do servidor de calculadora usando o binder
    binder = xmlrpc.client.ServerProxy(f'http://{server_address}:5000')
    chat_server_port = binder.discover_service('chat')

    if chat_server_port is None:
        print("Serviço de calculadora não encontrado.")
        exit(1)
    else:
        print("Achado")

    # Cria um cliente que se conecta ao servidor de calculadora na porta descoberta
    chat_server = xmlrpc.client.ServerProxy(f'http://{server_address}:{chat_server_port}')


    #fluxo inicial do cliente
    usuario_registrado = False
    usuario = ''

    while (not usuario_registrado):
        usuario = input("Registre-se com um nome de usuário:")
        usuario_registrado = chat_server.registra_usuario(usuario)
        
        if not usuario_registrado:
            print("Por favor, insira outro nome de usuário")

    
    sair = False
    #lobby
    while(not sair):
        funcao = 0
        try:
            funcao = int(input("1 - Listar salas\n2 - Entrar em sala\n3 - Criar sala\n4 - sair\nDigite a opção desejada: "))
        except:
            funcao = 0

        emSala = False
        nome_sala = ""

        match(funcao):
            case 1:
                print("Salas existentes:\n")
                salas = chat_server.listar_salas()
                for sala in salas:
                    print(f" - {sala}")
                print("\n")
            case 2:
                nome_sala = input("Digite o nome da sala desejada: ")
                status = chat_server.entrar_sala(usuario, nome_sala)

                print(status)
                if status == "Conectado":
                    emSala = True

                    usuarios = chat_server.listar_usuarios(nome_sala)
                    broadcast = chat_server.receber_broadcast_inicial(nome_sala)
                    print("Usuários conectados:\n")
                    for user in usuarios:
                        print(f" - {user}")

                    for msg in broadcast:
                        print(f"{msg}\n")
                else:
                    print(status)
            case 3:
                nome_sala = input("Digite o nome da nova sala: ")
                status_criacao_sala = chat_server.criar_sala(nome_sala)

                print(status_criacao_sala)
            case 4:
                sair = True
                print("Saindo...")
            case _:
                print("Por favor, insira uma opção válida")

        #dentro de uma sala
        bufferMsg = []
        while(emSala):
            while True:
                bufferMsg = bufferMsg + chat_server.receber_mensagem(usuario, nome_sala)
                time.sleep(60) 

            msg = input("Digite uma mensagem: ")
            chat_server.enviar_mensagem(usuario, nome_sala, msg, recipiente=None)
