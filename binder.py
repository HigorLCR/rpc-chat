from xmlrpc.server import SimpleXMLRPCServer

# Dicionário para armazenar o serviço e a porta correspondente
procedures_registry = {}


# Função para registrar um serviço no binder
def register_procedure(service_name, port):
    procedures_registry[service_name] = port
    print(f"Serviço {service_name} registrado na porta {port}")
    return True


# Função para descobrir a porta de um serviço
def lookup_procedure(service_name):
    return procedures_registry.get(service_name, None)


# Cria o servidor XML-RPC para o binder
binder_server = SimpleXMLRPCServer(('localhost', 5000))
print("Binder pronto e aguardando registros...")

# Registra as funções
binder_server.register_function(register_procedure, "register_service")
binder_server.register_function(lookup_procedure, "discover_service")

# Mantém o servidor em execução
binder_server.serve_forever()