from opcua import Client, ua
import time

IPSERVIDOR = "10.10.11.137"
ENDPOINT = "opc.tcp://"+IPSERVIDOR+":4841/serveropcua/"
SERVER_URI = "http://examples.opcua.github.io"

client = Client(ENDPOINT)
try:
    client.connect()
    print("Cliente conectado")
    ns_array = client.get_namespace_array()
    idx = ns_array.index(SERVER_URI) 
    #print("Namespaces:", ns_array)
    #print("Namespace index para SERVER_URI:", idx)
    objects = client.get_objects_node()
    sensor = objects.get_child([f"{idx}:Sensor1"])
    temperature = sensor.get_child([f"{idx}:Temperature"])
    curr = temperature.get_value()
    print(f"\nValor actual de Temperature: {curr}")
    i = 1
    while True:
        new_val = float(curr) + i + 0.5
        temperature.set_value(ua.Variant(new_val, ua.VariantType.Double))
        print(f"Escrito Temperature = {new_val}")
        i+=1
        time.sleep(1)
except Exception as e:
    print("Error:", e)
finally:
    client.disconnect()
    print("Cliente desconectado")