from opcua import Server,ua
from datetime import datetime
import time

URI = "http://examples.opcua.github.io"
ENDPOINT = "opc.tcp://0.0.0.0:4841/serveropcua/"

server = Server()
server.set_endpoint(ENDPOINT)
server.set_server_name("Serv_OPC")

# Configurar políticas de seguridad (incluyendo usuario/contraseña)
server.set_security_policy([
    ua.SecurityPolicyType.NoSecurity,
    ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
    ua.SecurityPolicyType.Basic256Sha256_Sign
])

idx = server.register_namespace(URI)
objects = server.get_objects_node()
device = objects.add_object(idx, "Sensor1")
temperature = device.add_variable(idx, "Temperature",10)
temperature.set_writable()

def user_manager(isession, username, password):
    if username == "admin" and password == "1234":
        return True
    if username == "operator" and password == "abcd":
        return True
    return False

server.user_manager.set_user_manager(user_manager)

#server.set_security_IDs(["Anonymous", "UserName"])

server.start()
print("Servidor OPC UA corriendo en: "+ ENDPOINT)

try:
    while True:
        new_temp = temperature.get_value()
        if new_temp >= 0:
            temperature.set_value(new_temp+1)
            formateado = datetime.now().strftime("%d %b, %H:%M:%S")
            print(f"{formateado}: temp = {new_temp}")
            time.sleep(30)
        time.sleep(15)
except KeyboardInterrupt:
    print("Deteniendo servidor...")
    server.stop()