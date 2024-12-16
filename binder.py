from xmlrpc.server import SimpleXMLRPCServer

# Dicionário para armazenar o serviço e a porta correspondente
services_registry = {}


# Função para registrar um serviço no binder
def register_service(service_name, port):
    services_registry[service_name] = port
    print(f"Serviço {service_name} registrado na porta {port}")
    return True


# Função para descobrir a porta de um serviço
def discover_service(service_name):
    return services_registry.get(service_name, None)


# Cria o servidor XML-RPC para o binder
binder_server = SimpleXMLRPCServer(('localhost', 65431))
print("Binder pronto e aguardando registros...")

# Registra as funções
binder_server.register_function(register_service, "register_service")
binder_server.register_function(discover_service, "discover_service")

# Mantém o servidor em execução
binder_server.serve_forever()