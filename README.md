# 🛰️ Ejemplo OPC UA — Servidor y Cliente en Python

Este proyecto demuestra cómo **crear un servidor OPC UA** y un **cliente OPC UA** con Python utilizando la librería [FreeOPCUA](https://github.com/FreeOpcUa/python-opcua).  
Aprenderás a **exponer variables desde un servidor** (por ejemplo, `Temperature`) y a **leer o escribir valores** desde un cliente remoto.

---

## 🧱 Estructura del proyecto

```bash
opcua-ejemplo/
├── src/
│   ├── servopcua.py      # Servidor OPC UA
│   └── clientopcua.py    # Cliente OPC UA
├── requirements.txt       # Dependencias
├── .gitignore             # Ignora archivos de entorno/IDE
└── LICENSE                # Licencia MIT
```

---

## ⚙️ Requisitos previos

- 🐍 **Python 3.8+**
- 📦 Instalar librerías necesarias:

```bash
pip install -r requirements.txt
```

---

## 🚀 Cómo ejecutar el **servidor**

1. **Crea y activa un entorno virtual (opcional pero recomendado):**

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

2. **Ejecuta el servidor:**

   ```bash
   python src/servopcua.py
   ```

   Verás algo como:

   ```
   Servidor OPC UA corriendo en opc.tcp://0.0.0.0:4841/serveropcua/
   ```

   👉 Este servidor crea un objeto `Sensor1` con la variable `Temperature`, que se puede leer y modificar desde un cliente.

---

## 🔗 Cómo ejecutar el **cliente**

1. Ajusta la IP de conexión en `src/clientopcua.py` si el servidor está en otra máquina:

   ```python
   IPSERVIDOR = "192.168.1.100"  # IP de tu servidor
   ENDPOINT   = f"opc.tcp://{IPSERVIDOR}:4841/serveropcua/"
   ```

2. Ejecuta el cliente:

   ```bash
   python src/clientopcua.py
   ```

   🧭 El cliente:
   - Se conecta al endpoint del servidor.
   - Busca el *namespace* correspondiente.
   - Accede al objeto `Sensor1` y su variable `Temperature`.
   - Lee y **escribe** nuevos valores cada cierto tiempo.

---

## 🧠 Explicación técnica

### 🖥️ Servidor (`src/servopcua.py`)

- Configura el endpoint `opc.tcp://0.0.0.0:4841/serveropcua/`
- Registra un *namespace* personalizado:
  ```python
  uri = "http://examples.freeopcua.github.io"
  idx = server.register_namespace(uri)
  ```
- Crea:
  - Un objeto `Sensor1`
  - Una variable `Temperature = 25` (marcada como *writable*)

🔁 Luego entra en un bucle donde imprime el valor de temperatura cada 5 segundos.

---

### 💻 Cliente (`src/clientopcua.py`)

- Se conecta al endpoint del servidor.
- Usa `get_namespace_array()` para identificar el índice del namespace (`idx`).
- Navega hasta `Sensor1 → Temperature`.
- Escribe valores con tipo `ua.Variant(Double)` para evitar errores de tipo.

Ejemplo de escritura segura:
```python
temperature.set_value(ua.Variant(30.5, ua.VariantType.Double))
```

---

## 🧩 ¿Qué son los *namespaces*?

Los *namespaces* sirven para **diferenciar nodos** creados por distintos fabricantes o módulos.  
Cada nodo se identifica como `ns=X; s=Nombre`, donde `X` es el índice del namespace.

| Namespace | Descripción |
|------------|--------------|
| `ns=0` | Estándar OPC UA |
| `ns=1` | Servidor interno |
| `ns>=2` | Nodos definidos por el usuario o fabricante |

👉 En este ejemplo, tus nodos (`Sensor1`, `Temperature`) están en el namespace con URI `http://examples.freeopcua.github.io` (generalmente `ns=2`).

---

## 🧰 Solución de problemas

| Error | Causa probable | Solución |
|-------|----------------|-----------|
| **BadNoMatch** | Ruta de nodo incorrecta | Verifica que no incluyas `"0:Objects"` si ya estás en `get_objects_node()` |
| **BadTypeMismatch** | Tipo de valor incompatible | Usa `ua.Variant(valor, ua.VariantType.Double)` |
| **Connection Refused** | IP o puerto incorrecto | Revisa firewall y que el servidor esté activo |
| **Namespace incorrecto** | `idx` diferente entre cliente y servidor | Usa `client.get_namespace_array()` para detectarlo dinámicamente |

---

## 🧾 Licencia

Este proyecto se distribuye bajo la licencia **MIT**.  
Puedes usarlo libremente con fines educativos.


## 🌟 Créditos

Proyecto creado para fines educativos y demostrativos sobre el protocolo **OPC UA** con Python.  
Inspirado en los ejemplos de [FreeOPCUA](https://github.com/FreeOpcUa/python-opcua).
