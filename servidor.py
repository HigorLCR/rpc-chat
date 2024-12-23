from xmlrpc.server import SimpleXMLRPCServer
from datetime import datetime, timedelta
import xmlrpc.client

usuarios_registrados = ['admin']
salas = []

#utilitarias

def is_primeiro_tempo_depois(time1: str, time2: str) -> bool:
    # Converter as strings de tempo para objetos datetime
    dt1 = datetime.strptime(time1, "%d/%m/%Y %H:%M:%S")
    dt2 = datetime.strptime(time2, "%d/%m/%Y %H:%M:%S")

    # Comparar os tempos
    return dt1 > dt2

# Funções do chat
def registra_usuario(nome):
    if any(usuario == nome for usuario in usuarios_registrados):
        return False
    else:
        usuarios_registrados.append(nome)
        return True
    
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

            if not nome in sala['conexoes']:
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
                    return "Conectado"
                except:
                    return "Erro ao conectar"
            else:
                return "Usuario já conectado"
    return "Sala inexistente"

def enviar_mensagem(nome, nome_sala, mensagem, recipiente=None):
    try:
        if nome not in usuarios_registrados:
            return "Usuário não registrado"

        for sala in salas:
            if sala['nome'] == nome_sala:
                try: 
                    agora = datetime.now()
                    string_tempo = agora.strftime("%d/%m/%Y %H:%M:%S")

                    sala['mensagens'].append({
                        'tipo': 'broadcast' if recipiente == None else 'unicast',
                        'origem': nome,
                        'destino': '' if recipiente == None else recipiente,
                        'conteudo': mensagem,
                        'timestamp': string_tempo,
                    })
                    return f"Mensagem enviada a {'broadcast' if recipiente == None else recipiente}"
                except:
                    return "Erro ao conectar"
        return "Sala inexistente"
    except Exception as e:
        print("ERRO: ", e)

def receber_mensagem(nome, nome_sala):
    try:
        dois_segs_atras = (datetime.now() - timedelta(seconds=2))
        dois_segs_atras = dois_segs_atras.strftime("%d/%m/%Y %H:%M:%S")

        if nome not in usuarios_registrados:
            return "Usuário não registrado"

        for sala in salas:
            if sala['nome'] == nome_sala:
                try:
                    def filtro_msgs(mensagem):
                        return (mensagem['tipo'] == 'broadcast' or mensagem['destino'] == nome) #and is_primeiro_tempo_depois(mensagem['timestamp'], dois_segs_atras)

                    mensagens = map(lambda msg: f"[{msg['timestamp']}] {f"({msg['tipo']}){msg['origem']}" if msg['tipo'] == 'broadcast' else msg['origem']}: {msg['conteudo']}", list(filter(filtro_msgs, sala['mensagens'])))
                    response = list(mensagens)
                    return response
                except:
                    return "Erro ao recuperar mensagens"
        return "Sala inexistente"
    except Exception as e:
        print("OUTRO ERRO: ", e)


def receber_broadcast_inicial(nome_sala):
    for sala in salas:
        if sala['nome'] == nome_sala:
            try:
                def filtro_msgs(mensagem):
                    return mensagem['tipo'] == 'broadcast'
                
                mensagens = map(lambda msg: f"[{msg['timestamp']}] {msg['tipo'] if msg['tipo'] == 'broadcast' else msg['origem']}: {msg['conteudo']}", list(filter(filtro_msgs, sala['mensagens'])))
                response = list(mensagens)
                print("MSGS: ", response)
                return response[-50:]
            except:
                return "Erro ao recuperar mensagens"
    return "Sala inexistente"

def listar_salas():
    nomes_salas = [sala['nome'] for sala in salas]
    return nomes_salas

def listar_usuarios(nome_sala):
    for sala in salas:
        if sala['nome'] == nome_sala:
            try: 
                return sala['conexoes']
            except:
                return "Erro ao retornar usuários conectados"
    return "Sala inexistente"


if __name__ == '__main__':
    # Configura o servidor
    server_port = 5100
    server = SimpleXMLRPCServer(('localhost', server_port))
    print("Servidor de chat pronto e aguardando conexões...")

    # Registra as funções da calculadora
    server.register_function(registra_usuario, "registra_usuario")
    server.register_function(criar_sala, "criar_sala")
    server.register_function(entrar_sala, "entrar_sala")
    server.register_function(listar_salas, "listar_salas")
    server.register_function(listar_usuarios, "listar_usuarios")
    server.register_function(enviar_mensagem, "enviar_mensagem")
    server.register_function(receber_mensagem, "receber_mensagem")
    server.register_function(receber_broadcast_inicial, "receber_broadcast_inicial")

    # Registrar o servidor da calculadora no binder
    binder = xmlrpc.client.ServerProxy('http://localhost:5000')
    binder.register_service('chat', server_port)

    # Mantém o servidor em execução
    server.serve_forever()