"""
CHULETA EDD + ARCHIVOS + MODULOS (semanas 1-3) - IIC2233 2026-2
Ejecutar: python3 chuleta_edd_archivos.py
"""
import os
from collections import deque, defaultdict, namedtuple


# =====================================================================
# 1. ELEGIR LA ESTRUCTURA
#   buscar por nombre/id ............ dict           d[k], k in d: O(1)
#   contar / agrupar sin KeyError ... defaultdict(int|list|set)
#   "el ultimo que entro" (deshacer)  stack = list    append / pop()
#   "el primero que llego" (turnos) . deque           append / popleft
#   sin duplicados, union/intersec .. set             add / discard / | & - ^
#   registro fijo e inmutable ....... namedtuple
#   llave compuesta / secuencia fija  tuple           (5,) es tupla, (5) no
# =====================================================================
LineaPedido = namedtuple("LineaPedido", ["nombre", "cantidad"])


def demo_edd():
    print("\n--- EDD ---")
    # dict
    precios = {"Cafe": 1500, "Te": 1200}
    print(precios.get("Jugo", 0), "Cafe" in precios)      # 0 True
    for nombre, precio in precios.items():
        print(f"{nombre:8s} ${precio}")
    # defaultdict: crea el valor al primer acceso (ojo: acceder = crear llave)
    conteo = defaultdict(int)
    for letra in "banana":
        conteo[letra] += 1
    grupos = defaultdict(list)
    grupos["bebida"].append("Cafe")
    print(dict(conteo), dict(grupos))
    # stack (LIFO)
    historial = []
    historial.append("a")
    historial.append("b")
    if historial:                                          # nunca pop en vacio
        print("pop ->", historial.pop())                   # b
    # cola (FIFO) y fila rotatoria
    cola = deque()
    cola.append("pedido1")
    cola.append("pedido2")
    print("popleft ->", cola.popleft())                    # pedido1
    turnos = deque(["Ana", "Ben", "Carla"])
    actual = turnos.popleft()
    turnos.append(actual)                                  # rota
    print(turnos)
    # set
    vistos = set()
    vistos.add("Cafe")
    vistos.add("Cafe")
    vistos.discard("Nada")                                 # remove daria KeyError
    print(vistos, {1, 2} | {2, 3}, {1, 2} & {2, 3}, {1, 2} - {2, 3})
    # namedtuple y desempaquetado
    linea = LineaPedido("Cafe", 2)
    nombre, cantidad = linea
    print(linea.nombre, cantidad, linea)
    # *args / **kwargs
    def f(*args, **kwargs):
        return args, kwargs
    print(f(1, 2, x=3))                                    # ((1, 2), {'x': 3})
    primero, *resto = (1, 2, 3)
    print(primero, resto)                                  # 1 [2, 3]  (lista)


# =====================================================================
# 2. ARCHIVOS: leer CSV a objetos, escribir
#   - paths relativos a la carpeta desde donde corres python3
#   - os.path.join("data", "x.csv"); with open(...) as f; strip(); split(",")
#   - "w" vacia el archivo al abrirlo; write no agrega "\n"
# =====================================================================
def cargar_csv(ruta, saltar_encabezado=True):
    filas = []
    with open(ruta, "r", encoding="utf-8") as archivo:
        if saltar_encabezado:
            archivo.readline()
        for linea in archivo:
            linea = linea.strip()
            if not linea:                                  # linea vacia final
                continue
            filas.append(linea.split(","))
    return filas


def guardar_csv(ruta, filas, encabezado):
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(",".join(encabezado) + "\n")
        for fila in filas:
            archivo.write(",".join(str(x) for x in fila) + "\n")


def demo_archivos():
    print("\n--- archivos ---")
    carpeta = os.path.join(os.path.dirname(__file__), "data_demo")
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, "productos.csv")
    guardar_csv(ruta, [("Cafe", 1500, 5), ("Te", 1200, 8)],
                ["nombre", "precio", "stock"])
    for nombre, precio, stock in cargar_csv(ruta):
        print(nombre, int(precio), int(stock))
    print(os.listdir(carpeta), os.path.exists(ruta))
    # Acciones "una por linea" sin encabezado, con campos variables:
    # for valores in cargar_csv(ruta_acciones, saltar_encabezado=False):
    #     accion, rut = valores[0], valores[1]
    #     if accion == "Agregar al carro":
    #         producto = valores[2]


# =====================================================================
# 3. MODULOS y ejecucion
#   from producto import Producto     -> importa la clase
#   import utils; utils.funcion()     -> con prefijo
#   todo el codigo de nivel superior se ejecuta al importar:
#   lo ejecutable va bajo  if __name__ == "__main__":
#   ejecutar: cd carpeta_de_la_AC && python3 main.py
# =====================================================================

if __name__ == "__main__":
    demo_edd()
    demo_archivos()
