# apuntes.py - exportacion de apuntes.ipynb (mismas celdas, en orden)

# %% [markdown]
# # Apuntes IIC2233 — cómo resolver una actividad (AC) completa
# 
# Orden de trabajo en la AC (2 horas):
# 
# 1. **Leer el enunciado completo** sin escribir. Anotar: carpeta de entrega, archivos que se modifican / no se modifican, salida esperada.
# 2. Copiar los archivos base al repo y hacer el **primer push** (abajo los comandos).
# 3. **Leer los archivos "No modificar"** (`bases.py`, `main.py`): ahí dicen cómo se llaman mis métodos, qué reciben y qué retornan.
# 4. Modelar las **clases** (sección 3) → **cargar datos** (secciones 2 y 4) → **simular acciones** (sección 6) → **reporte** (sección 7).
# 5. Después de cada parte: `python3 main.py`, comparar con la salida esperada, `push`.
# 6. Si algo se traba más de 15 min: dejar un `pass`/`return` mínimo para que el programa NO se caiga y seguir.
# 
# ```bash
# cd ~/Trabajo/<usuario>-iic2233-2026-2
# git pull
# mkdir -p Actividades/ACx            # nombre EXACTO de la sección "Entrega"
# cp -r /ruta/base/* Actividades/ACx/
# git add . && git commit -m "Base ACx" && git push
# cd Actividades/ACx && python3 main.py           # siempre parado en la carpeta de la AC
# ```
# 
# Este notebook resuelve una mini-AC (DCCafetería) de principio a fin: cada celda es copiable.
# Ejecuta las celdas **en orden** (la primera crea los datos de ejemplo).

# %% [markdown]
# ## 1. Estructura de un `main.py` y sus módulos
# 
# - `from productos import Producto` importa la clase desde `productos.py` (misma carpeta).
# - Todo lo que está fuera de funciones/clases se ejecuta al importar → lo ejecutable va bajo `if __name__ == "__main__":`.
# - Las rutas son relativas a la carpeta **desde donde corres `python3`**: siempre `os.path.join("data", "x.csv")`.

# %% ---------------------------------------------------------
import os
from abc import ABC, abstractmethod
from collections import deque, defaultdict, namedtuple

CARPETA_DATOS = "data"      # constante arriba del archivo

# --- solo para que este notebook tenga datos de ejemplo (en la AC ya vienen) ---
os.makedirs(CARPETA_DATOS, exist_ok=True)
with open(os.path.join(CARPETA_DATOS, "productos.csv"), "w", encoding="utf-8") as archivo:
    archivo.write("nombre,precio,stock\nCafe,1500,5\nTe,1200,8\nJugo,1800,1\n")
with open(os.path.join(CARPETA_DATOS, "empleados.csv"), "w", encoding="utf-8") as archivo:
    archivo.write("tipo,nombre,sueldo_base,extra\ncajero,Ana,450000,0.05\n"
                  "repartidor,Carla,400000,Norte\npolifuncional,Elena,500000,0.03;Sur\n")
with open(os.path.join(CARPETA_DATOS, "acciones.txt"), "w", encoding="utf-8") as archivo:
    archivo.write("pedido,Camila,local,Cafe:2\npedido,Tomas,delivery,Jugo:2\n"
                  "atender\natender\nreponer,Jugo,3\npedido,Sofia,local,Torta:1\n"
                  "pedido,Diego,delivery,Jugo:2\natender\natender\natender\n"
                  "deshacer\natender\n")
print(os.listdir(CARPETA_DATOS))

# %% [markdown]
# ## 2. Leer archivos
# 
# - CSV **con encabezado**: saltarlo con `archivo.readline()` y luego `for linea in archivo`.
# - Siempre `linea.strip()` (quita el `\n`) antes de `split(",")`; convertir con `int()` / `float()`.
# - Archivo de **acciones**: una acción por línea, sin encabezado, campos variables → mirar `valores[0]`.
# - Campos con separador interno (`Cafe:2;Te:1`): `split(";")` y luego `split(":")`.

# %% ---------------------------------------------------------
def leer_csv(ruta):
    """Retorna una lista de listas de strings; salta el encabezado y líneas vacías."""
    filas = []
    with open(ruta, "r", encoding="utf-8") as archivo:
        archivo.readline()                       # encabezado
        for linea in archivo:
            linea = linea.strip()
            if not linea:                        # última línea vacía
                continue
            filas.append(linea.split(","))
    return filas


def leer_acciones(ruta):
    """Sin encabezado. Retorna lista de listas; cada acción decide cuántos campos usa."""
    acciones = []
    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            if linea.strip():
                acciones.append(linea.strip().split(","))
    return acciones


print(leer_csv(os.path.join(CARPETA_DATOS, "productos.csv")))
print(leer_acciones(os.path.join(CARPETA_DATOS, "acciones.txt"))[:3])

# escribir ("w" borra el archivo al abrirlo; write NO agrega salto de línea)
with open(os.path.join(CARPETA_DATOS, "reporte.txt"), "w", encoding="utf-8") as archivo:
    archivo.write("nombre,total\n")
    archivo.write(",".join(["Cafe", str(3000)]) + "\n")

# %% [markdown]
# ## 3. Clases: el patrón completo
# 
# Reglas que se repiten en toda AC:
# 
# | Necesito | Escribo |
# |---|---|
# | Atributo que se valida | `@property` (getter) + `@x.setter`; adentro **siempre** `self._x` |
# | Atributo calculado, no asignable | `@property` sin setter |
# | Contador de instancias | variable de clase y `Producto.total += 1` (no `self.total`) |
# | Construir desde una línea del archivo | `@classmethod def desde_linea(cls, linea)` → `return cls(...)` |
# | Clase que no se instancia y obliga a implementar | `class X(ABC)` + `@abstractmethod` |
# | Subclase | `class Hija(Padre)`; en `__init__`: `super().__init__(...)` y luego lo propio |
# | Cambiar un método del padre pero reutilizarlo | `def m(self): ... super().m() ...` |
# | Clase con dos padres | `class C(A, B)`: todos los `__init__` con `**kwargs` y **una** llamada `super().__init__(**kwargs)`; instanciar por keyword |
# | `print(objeto)` legible | `__str__`; `__repr__` se usa en listas |

# %% ---------------------------------------------------------
class Producto:
    total_creados = 0                            # variable de clase (compartida)

    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.precio = precio
        self._stock = 0                          # existe ANTES de pasar por el setter
        self.stock = stock                       # esta asignación usa el setter
        Producto.total_creados += 1

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        if valor < 0:
            print(f"Stock inválido para {self.nombre}: {valor}. Se mantiene en {self._stock}")
        else:
            self._stock = valor

    @property
    def valor_stock(self):                       # solo lectura
        return self.precio * self._stock

    @classmethod
    def desde_linea(cls, valores):               # valores = ["Cafe", "1500", "5"]
        nombre, precio, stock = valores
        return cls(nombre, int(precio), int(stock))

    def __str__(self):
        return f"{self.nombre}: ${self.precio} (stock: {self._stock})"


p = Producto.desde_linea(["Cafe", "1500", "5"])
p.stock -= 1            # getter y setter
p.stock = -3            # rechazado
print(p, "| valor:", p.valor_stock, "| creados:", Producto.total_creados)

# %% ---------------------------------------------------------
Linea = namedtuple("Linea", ["nombre", "cantidad"])     # registro fijo e inmutable


class Pedido:
    def __init__(self, numero, cliente, tipo, lineas):
        self.numero = numero
        self.cliente = cliente
        self.tipo = tipo                         # "local" o "delivery"
        self.lineas = lineas                     # lista de Linea

    def __repr__(self):                          # lo usa print y también las listas
        return f"Pedido #{self.numero} ({self.tipo}, {self.cliente})"


class Empleado(ABC):
    def __init__(self, nombre, sueldo_base, **kwargs):
        super().__init__(**kwargs)               # permite multiherencia más abajo
        self.nombre = nombre
        self.sueldo_base = sueldo_base
        self.atendidos = 0

    @abstractmethod
    def puede_atender(self, pedido):             # cada subclase DEBE implementarlo
        pass

    def atender(self, pedido, inventario):
        """Método común: revisa stock, descuenta y cuenta. Retorna el monto o None."""
        faltante = inventario.faltante(pedido.lineas)
        if faltante is not None:
            print(f"[{self}] {pedido} rechazado: falta {faltante}")
            return None
        monto = inventario.descontar(pedido.lineas)
        self.atendidos += 1
        return monto

    def calcular_sueldo(self):
        return self.sueldo_base

    def __str__(self):
        return f"{type(self).__name__} {self.nombre}"


class Cajero(Empleado):
    def __init__(self, comision, **kwargs):
        super().__init__(**kwargs)
        self.comision = comision
        self.ventas = 0

    def puede_atender(self, pedido):
        return pedido.tipo == "local"

    def atender(self, pedido, inventario):       # extiende el del padre
        monto = super().atender(pedido, inventario)
        if monto is not None:
            self.ventas += monto
            print(f"[{self}] {pedido} cobrado: ${monto}")
        return monto

    def calcular_sueldo(self):
        return super().calcular_sueldo() + round(self.ventas * self.comision)


class Repartidor(Empleado):
    COSTO_DESPACHO = 2500                        # constante de clase

    def __init__(self, zona, **kwargs):
        super().__init__(**kwargs)
        self.zona = zona
        self.despachos = 0

    def puede_atender(self, pedido):
        return pedido.tipo == "delivery"

    def atender(self, pedido, inventario):
        monto = super().atender(pedido, inventario)
        if monto is not None:
            monto += self.COSTO_DESPACHO
            self.despachos += 1
            print(f"[{self}] {pedido} despachado a {self.zona}: ${monto}")
        return monto

    def calcular_sueldo(self):
        return super().calcular_sueldo() + 3000 * self.despachos


class Polifuncional(Cajero, Repartidor):         # MRO: Polifuncional, Cajero, Repartidor, Empleado
    def __init__(self, bono, **kwargs):
        super().__init__(**kwargs)               # UNA sola llamada; recorre toda la cadena
        self.bono = bono

    def puede_atender(self, pedido):
        return True

    def atender(self, pedido, inventario):
        if pedido.tipo == "local":               # llamada puntual, saltándose el MRO
            return Cajero.atender(self, pedido, inventario)
        return Repartidor.atender(self, pedido, inventario)

    def calcular_sueldo(self):                   # super() encadena Cajero -> Repartidor -> Empleado
        return super().calcular_sueldo() + self.bono


print([clase.__name__ for clase in Polifuncional.__mro__])

# %% [markdown]
# ## 4. Cargar datos a objetos y elegir la estructura
# 
# | Necesidad | Estructura | Operaciones |
# |---|---|---|
# | Buscar por nombre / id | `dict` | `d[k]`, `k in d`, `d.get(k)`, `d.items()` |
# | Contar / agrupar sin `KeyError` | `defaultdict(int)` / `defaultdict(list)` | crea el valor al primer acceso |
# | "El último que entró" (deshacer) | stack = `list` | `append`, `pop()` (revisar `if lista:`) |
# | "El primero que llegó" (turnos, cola) | `deque` | `append`, `popleft()`; fila rotatoria: `popleft` + `append` |
# | Sin duplicados / pertenencia rápida | `set` | `add`, `discard`, `in`, `\|` `&` `-` |
# | Registro fijo | `namedtuple` | acceso por punto, desempaquetado |
# 
# Un `dict` de objetos indexado por nombre es casi siempre la respuesta para el inventario; los empleados van en una `deque` si atienden por turnos.

# %% ---------------------------------------------------------
class Inventario:
    def __init__(self):
        self.productos = {}                      # nombre -> Producto (búsqueda O(1))
        self.agotados = set()                    # nombres sin stock, sin duplicados

    def agregar(self, producto):
        self.productos[producto.nombre] = producto

    def faltante(self, lineas):
        """Primer producto inexistente o sin stock suficiente; None si todo está."""
        for linea in lineas:
            if linea.nombre not in self.productos:
                return linea.nombre
            if self.productos[linea.nombre].stock < linea.cantidad:
                return linea.nombre
        return None

    def descontar(self, lineas):
        total = 0
        for linea in lineas:
            producto = self.productos[linea.nombre]
            producto.stock -= linea.cantidad     # pasa por el setter
            total += producto.precio * linea.cantidad
            if producto.stock == 0:
                self.agotados.add(producto.nombre)
        return total

    def reponer(self, nombre, cantidad):
        if nombre not in self.productos:
            print(f"No existe el producto {nombre}")
            return
        self.productos[nombre].stock += cantidad
        self.agotados.discard(nombre)            # discard no falla si no está
        print(f"Reposición de {nombre}: ahora tiene {self.productos[nombre].stock} unidades")


def cargar_inventario(ruta):
    inventario = Inventario()
    for valores in leer_csv(ruta):
        inventario.agregar(Producto.desde_linea(valores))
    return inventario


def cargar_empleados(ruta):
    """Un constructor por tipo; instanciar SIEMPRE por keyword cuando hay **kwargs."""
    empleados = deque()
    for tipo, nombre, sueldo, extra in leer_csv(ruta):
        if tipo == "cajero":
            empleado = Cajero(nombre=nombre, sueldo_base=int(sueldo), comision=float(extra))
        elif tipo == "repartidor":
            empleado = Repartidor(nombre=nombre, sueldo_base=int(sueldo), zona=extra)
        elif tipo == "polifuncional":
            comision, zona = extra.split(";")
            empleado = Polifuncional(nombre=nombre, sueldo_base=int(sueldo),
                                     comision=float(comision), zona=zona, bono=20000)
        else:
            print(f"Tipo desconocido: {tipo}")
            continue
        empleados.append(empleado)
    return empleados


inventario = cargar_inventario(os.path.join(CARPETA_DATOS, "productos.csv"))
empleados = cargar_empleados(os.path.join(CARPETA_DATOS, "empleados.csv"))
for producto in inventario.productos.values():
    print(producto)
print([str(e) for e in empleados])

# %% [markdown]
# ## 5. Mini-demo de cada estructura (para copiar)

# %% ---------------------------------------------------------
conteo = defaultdict(int)                        # contar
for letra in "banana":
    conteo[letra] += 1
por_tipo = defaultdict(list)                     # agrupar
por_tipo["bebida"].append("Cafe")
print(dict(conteo), dict(por_tipo))

historial = []                                   # stack
historial.append("a"); historial.append("b")
if historial:
    print("deshacer:", historial.pop())          # b

fila = deque(["Ana", "Ben", "Carla"])            # cola / fila rotatoria
turno = fila.popleft()
fila.append(turno)
print(fila)

vistos = {"Cafe"}                                # set ({} vacío es dict: usar set())
vistos.add("Te"); vistos.discard("Nada")
print(vistos, {1, 2} | {2, 3}, {1, 2} & {2, 3}, {1, 2} - {2, 3})

nombre, cantidad = Linea("Cafe", 2)              # namedtuple: desempaquetar
primero, *resto = [1, 2, 3]                      # resto es lista
print(nombre, cantidad, primero, resto)

# %% [markdown]
# ## 6. Simular las acciones
# 
# - Un `if/elif` por acción, mirando `valores[0]`; los campos extra se leen recién dentro de cada rama.
# - **Mensajes exactos** del enunciado (mayúsculas, `$`, puntos). Cada caso de error tiene su mensaje.
# - Casos borde que siempre prueban: producto inexistente, sin stock, cola vacía, nadie disponible, deshacer sin historial.
# - La cola de pedidos es `deque` (llega → `append`, se atiende → `popleft`); la fila de empleados rota (`popleft` + `append`); lo rechazado va a una lista/stack.

# %% ---------------------------------------------------------
def crear_pedido(numero, cliente, tipo, texto_lineas):
    """'Cafe:2;Te:1' -> [Linea('Cafe', 2), Linea('Te', 1)]"""
    lineas = []
    for parte in texto_lineas.split(";"):
        nombre, cantidad = parte.split(":")
        lineas.append(Linea(nombre, int(cantidad)))
    return Pedido(numero, cliente, tipo, lineas)


def simular(acciones, inventario, empleados):
    cola = deque()                               # pedidos esperando (FIFO)
    atendidos = []                               # stack para "deshacer"
    numero = 0
    for valores in acciones:
        accion = valores[0]
        if accion == "pedido":
            numero += 1
            pedido = crear_pedido(numero, valores[1], valores[2], valores[3])
            cola.append(pedido)
            print(f"{pedido} en cola. Pedidos esperando: {len(cola)}")
        elif accion == "atender":
            if not cola:                         # borde: cola vacía
                print("No hay pedidos en cola")
                continue
            pedido = cola.popleft()
            empleado = empleados.popleft()       # fila rotatoria
            empleados.append(empleado)
            if not empleado.puede_atender(pedido):
                print(f"[{empleado}] no puede atender {pedido}")
                cola.appendleft(pedido)          # vuelve al frente
                continue
            monto = empleado.atender(pedido, inventario)   # polimorfismo
            if monto is not None:
                atendidos.append((pedido, monto))
        elif accion == "reponer":
            inventario.reponer(valores[1], int(valores[2]))
        elif accion == "deshacer":
            if not atendidos:
                print("Nada que deshacer")
                continue
            pedido, monto = atendidos.pop()
            print(f"Deshecho {pedido} por ${monto}")
        else:
            print(f"Acción desconocida: {accion}")
    return atendidos


acciones = leer_acciones(os.path.join(CARPETA_DATOS, "acciones.txt"))
atendidos = simular(acciones, inventario, empleados)

# %% [markdown]
# ## 7. Reporte final
# 
# - Ordenar objetos: `sorted(lista, key=lambda e: e.calcular_sueldo(), reverse=True)`.
# - Formato: `f"{nombre:<12}{monto:>8}"` alinea; `f"${monto:,}"` pone separador de miles; `round(x, 2)`.
# - Total: `sum(monto for pedido, monto in atendidos)`.

# %% ---------------------------------------------------------
print("=== Sueldos ===")
for empleado in sorted(empleados, key=lambda e: e.calcular_sueldo(), reverse=True):
    print(f"{str(empleado):<22} ${empleado.calcular_sueldo():>8}")
print("=== Inventario ===")
for nombre in sorted(inventario.productos):
    print(inventario.productos[nombre])
print("Agotados:", sorted(inventario.agotados))
print("Total vendido:", sum(monto for pedido, monto in atendidos))
print("Valor del inventario:", sum(p.valor_stock for p in inventario.productos.values()))

# %% [markdown]
# ## 8. Lo que preguntan en el control (con salida verificada)
# 
# - `super()` llama al **siguiente en el MRO de la instancia**, no al padre directo. Con `super()` la base del diamante se ejecuta **una** vez; con llamadas explícitas `A.m(self); B.m(self)`, dos.
# - Si dos padres definen el mismo método sin `super()`, gana el **primero de izquierda a derecha**.
# - El `TypeError` de una clase abstracta es al **instanciar**, no al definir la subclase incompleta.
# - Dentro de una property, `self.x` en vez de `self._x` → `RecursionError`.
# - Un decorador que olvida `return wrapper` deja la función en `None`.
# - `print(obj)` usa `__str__`; si no existe, `__repr__`; las listas siempre usan `__repr__`.
# - Python **no** tiene overloading: dos `def f` con distinta firma → sobrevive la última.
# - `self.total += 1` crea una variable de **instancia**; la de clase se cambia con `Clase.total += 1`.

# %% ---------------------------------------------------------
class Base:
    def llamar(self):
        print("  Base")


class Izq(Base):
    def llamar(self):
        print("  Izq ini"); super().llamar(); print("  Izq fin")


class Der(Base):
    def llamar(self):
        print("  Der ini"); super().llamar(); print("  Der fin")


class Diamante(Izq, Der):
    def llamar(self):
        print("  Diamante ini"); super().llamar(); print("  Diamante fin")


print([c.__name__ for c in Diamante.__mro__])    # Diamante, Izq, Der, Base, object
Diamante().llamar()

try:
    Empleado(nombre="x", sueldo_base=1)
except TypeError as error:
    print("TypeError:", error)

def registrar(func):                             # decorador
    def wrapper(*args, **kwargs):
        print(f"[LOG] {func.__name__}")
        return func(*args, **kwargs)
    return wrapper                               # sin esto: 'NoneType' object is not callable

@registrar
def pagar(monto):
    return monto * 2

print(pagar(10))

# %% [markdown]
# ## 9. Error → causa → arreglo
# 
# | Mensaje | Causa | Arreglo |
# |---|---|---|
# | `AttributeError: 'X' object has no attribute 'a'` | falta `super().__init__()` en la subclase / nombre mal escrito | llamar `super().__init__(...)` primero |
# | `TypeError: Can't instantiate abstract class X ...` | subclase sin implementar un abstracto (o typo en el nombre) | implementar todos con el nombre exacto |
# | `RecursionError` | getter/setter usa `self.x` | usar `self._x` |
# | `AttributeError: property 'x' ... has no setter` | asignar a property sin setter | agregar `@x.setter` o asignar `self._x` |
# | `TypeError: 'NoneType' object is not callable` | decorador sin `return wrapper` | retornar la interna |
# | `TypeError: X.__init__() takes 2 positional arguments but 5 were given` | posicionales con `**kwargs`, o `super().__init__(self, …)` | instanciar por keyword; `super()` sin `self` |
# | `TypeError: object.__init__() takes exactly one argument` | sobró un keyword al final de la cadena (typo) | revisar nombres de parámetros |
# | `TypeError: Cannot create a consistent MRO` | bases en órdenes contradictorios | mismo orden en toda la jerarquía |
# | `FileNotFoundError: ... 'data/x.csv'` | corriste `python3` desde otra carpeta | `cd` a la carpeta de la AC |
# | `ValueError: invalid literal for int(): '5\n'` | falta `strip()` | `linea.strip().split(",")` |
# | `ValueError: too many values to unpack` | encabezado no saltado / separador distinto | `readline()` antes; revisar `split` |
# | `KeyError` / `IndexError: pop from empty` | llave inexistente / `pop` en vacío | `in`, `get`, `defaultdict` / `if cola:` |
# | `TypeError: unhashable type: 'list'` | lista como llave o en set | usar tupla |

# %% [markdown]
# ## 10. Antes del último push (17:10)
# 
# - [ ] `python3 main.py` corre **completo** desde la carpeta de la AC y la salida coincide carácter por carácter.
# - [ ] Sin `print` de depuración, sin imports extra, sin tocar archivos "No modificar".
# - [ ] PEP8: `snake_case`, 4 espacios, espacios tras comas y operadores, líneas ≤ 100.
# - [ ] `git add . && git commit -m "Entrega ACx" && git push`, y revisar en github.com carpeta + rama `main`.
# - [ ] Marcar la salida con la TUC.
