# Ejemplo OPC UA: Servidor y Cliente en Python

Este repositorio contiene un **servidor OPC UA** y un **cliente OPC UA** de ejemplo, escritos en Python, para demostrar cómo exponer una variable (`Temperature`) y cómo leer/escribirla desde un cliente.

## Estructura del repositorio

```text
opcua-ejemplo/
├─ src/
│  ├─ servopcua.py
│  └─ clientopcua.py
├─ requirements.txt
├─ .gitignore
└─ LICENSE
```

## Requisitos

- Python 3.8+
- Librería OPC UA para Python: `pip install opcua` (ver `requirements.txt`)

> Nota: En algunos entornos la librería también se conoce como *FreeOPCUA (opcua)*.

## Cómo correr el **servidor**

1. Crear y activar un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar el servidor:
   ```bash
   python src/servopcua.py
   ```
   Deberías ver en consola algo como:
   ```
   Servidor OPC UA corriendo en: opc.tcp://0.0.0.0:4841/serveropcua/
   ```

## Cómo correr el **cliente**

1. Ajusta la IP/endpoint en `src/clientopcua.py` si tu servidor no corre en la misma máquina:
   ```python
   IPSERVIDOR = "10.10.11.137"   # cámbialo por la IP de tu servidor
   ENDPOINT   = f"opc.tcp://{{IPSERVIDOR}}:4841/serveropcua/"
   ```
2. Ejecuta el cliente:
   ```bash
   python src/clientopcua.py
   ```
   El cliente:
   - Se conectará al endpoint.
   - Buscará el índice de *namespace* correspondiente al URI del servidor.
   - Navegará hasta `Sensor1/Temperature`.
   - Leerá el valor actual y luego **escribirá** nuevos valores (como `Double`).

## Explicación rápida del código

### Servidor (`src/servopcua.py`)
- Define el **endpoint** `opc.tcp://0.0.0.0:4841/serveropcua/` para escuchar en todas las interfaces.
- Registra un *namespace* (URI) único para tus nodos.
- Crea el objeto `Sensor1` y la variable `Temperature` inicializada en 25, marcándola como **writable**.
- Inicia el servidor y entra en un bucle donde imprime el valor actual.

Puntos clave:
- `server.register_namespace(URI)` devuelve el **índice de namespace** (`idx`) para etiquetar tus nodos.
- `add_object` y `add_variable` crean nodos bajo el árbol `Objects`.
- `temperature.set_writable()` permite que los clientes escriban el valor.

### Cliente (`src/clientopcua.py`)
- Se conecta al endpoint del servidor.
- Obtiene el **namespace array** para localizar el índice del URI del servidor.
- Desde `Objects`, navega a `Sensor1` y su variable `Temperature`.
- Lee el valor actual y escribe periódicamente nuevos valores como `ua.Variant(Double)` para robustez de tipo.

Puntos clave:
- `client.get_namespace_array()` devuelve un arreglo de URIs; se usa `index(SERVER_URI)` para hallar el `idx` correcto.
- `get_objects_node().get_child([f"{{idx}}:Sensor1"])` y luego `.get_child([f"{{idx}}:Temperature"])` navegan sin incluir `0:Objects` (ya estás allí).
- Si el tipo de dato no coincide, usa `ua.Variant(valor, ua.VariantType.Double)`.

## Solución de problemas

- **BadNoMatch**: la ruta de navegación no coincide. Verifica el `idx` y no incluyas `0:Objects` si ya partiste de `get_objects_node()`.
- **BadTypeMismatch**: al escribir, usa `ua.Variant(..., ua.VariantType.Double)` para asegurar el tipo.
- **Conexión rechazada**: confirma IP, puerto (4841) y firewall. Si el servidor corre en otra máquina, usa su IP real en el cliente.
- **Namespaces**: recuerda que `ns=0` es estándar OPC UA y tus nodos suelen estar en `ns>=2`.

## Publicar en GitHub

Desde la carpeta `opcua-ejemplo/`:
```bash
git init
git add .
git commit -m "Ejemplo OPC UA: servidor y cliente en Python"
git branch -M main
git remote add origin https://github.com/<tu-usuario>/opcua-ejemplo.git
git push -u origin main
```

---

**Licencia:** MIT
