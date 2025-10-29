from opcua import Server
from datetime import datetime
import time

URI = "http://examples.opcua.github.io"
ENDPOINT = "opc.tcp://0.0.0.0:4841/serveropcua/"

server = Server()
server.set_endpoint(ENDPOINT)
server.set_server_name("Serv_OPC")


idx = server.register_namespace(URI)

objects = server.get_objects_node()

device = objects.add_object(idx, "Sensor1")
temperature = device.add_variable(idx, "Temperature", 25)
temperature.set_writable()

server.start()
print("Servidor OPC UA corriendo en: "+ ENDPOINT)

try:
    while True:
        new_temp = temperature.get_value()
        #temperature.set_value(new_temp)
        print(f"{datetime.now()}: temperatura = {new_temp}")
        time.sleep(1)
except KeyboardInterrupt:
    print("Deteniendo servidor...")
    server.stop()