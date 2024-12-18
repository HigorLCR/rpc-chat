from xmlrpc.server import SimpleXMLRPCServer
from datetime import datetime
import xmlrpc.client

usuarios_registrados = ['admin']
salas = []

# Funções do chat
def registra_usuario(nome):
    if any(usuario == nome for usuario in usuarios_registrados):
        return "nome já existente. Por favor, insira outro nome de usuário"
    else:
        usuarios_registrados.append(nome)
        return "nome de usuário registrado!"
    
def criar_sala(nome_sala):
    if any(sala['nome'] == nome_sala for sala in salas):
        return "nome de sala já existente. Por favor, insira outro."
    else:
        salas.append({
            'nome': nome_sala,
            'conexoes': [],
            'mensagens': [],
        })
        return "nome de sala registrado!"
    
def entrar_sala(nome, nome_sala):
    if nome not in usuarios_registrados:
        return "Usuário não registrado"
    
    for sala in salas:
        if sala['nome'] == nome_sala:
            try: 
                agora = datetime.now()
                string_tempo = agora.strftime("%d/%m/%Y %H:%M:%S")

                sala['conexoes'].append(nome)
                sala['mensagens'].append({
                    'tipo': 'broadcast',
                    'origem': nome,
                    'destino': '',
                    'conteudo': f'{nome} entrou na sala',
                    'timestamp': string_tempo,
                })
                print("USERS: ", usuarios_registrados)
                print("SALA: ", salas)
                return "Conectado"
            except:
                return "Erro ao conectar"
    return "Sala inexistente"

def listar_salas():
    nomes_salas = [sala['nome'] for sala in salas]
    return f'Salas: {nomes_salas}'

def listar_usuarios(nome_sala):
    for sala in salas:
        if sala['nome'] == nome_sala:
            try: 
                return f"Usuários: {sala['conexoes']}"
            except:
                return "Erro ao retornar usuários conectados"
    return "Sala inexistente"


if __name__ == '__main__':
    # Configura o servidor
    server_port = 5100
    server = SimpleXMLRPCServer(('localhost', server_port))
    print("Servidor de calculadora pronto e aguardando conexões...")

    # Registra as funções da calculadora
    server.register_function(registra_usuario, "registra_usuario")
    server.register_function(criar_sala, "criar_sala")
    server.register_function(entrar_sala, "entrar_sala")
    server.register_function(listar_salas, "listar_salas")
    server.register_function(listar_usuarios, "listar_usuarios")

    # Registrar o servidor da calculadora no binder
    binder = xmlrpc.client.ServerProxy('http://localhost:5000')
    binder.register_service('chat', server_port)

    # Mantém o servidor em execução
    server.serve_forever()