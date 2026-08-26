"""
PLANTILLA DE ACTIVIDAD - esqueleto tipico de una AC del curso.
Copiar lo que sirva; borrar lo que no. Ejecutar: python3 plantilla_ac.py
Estructura habitual: cargar archivos -> objetos -> simular acciones -> reporte.
"""
import os
from abc import ABC, abstractmethod
from collections import deque, defaultdict, namedtuple

CARPETA_DATOS = "data"
Linea = namedtuple("Linea", ["nombre", "cantidad"])


class Entidad(ABC):
    """Clase base abstracta con **kwargs para permitir multiherencia."""

    def __init__(self, nombre, **kwargs):
        super().__init__(**kwargs)
        self.nombre = nombre

    @abstractmethod
    def actuar(self, contexto):
        pass

    def __str__(self):
        return f"{type(self).__name__} {self.nombre}"


class TipoA(Entidad):
    def __init__(self, valor_a, **kwargs):
        super().__init__(**kwargs)
        self.valor_a = valor_a

    def actuar(self, contexto):
        return f"{self} actua con {self.valor_a}"


class TipoB(Entidad):
    def __init__(self, valor_b, **kwargs):
        super().__init__(**kwargs)
        self.valor_b = valor_b

    def actuar(self, contexto):
        return f"{self} actua con {self.valor_b}"


class TipoAB(TipoA, TipoB):
    def __init__(self, extra, **kwargs):
        super().__init__(**kwargs)               # una sola llamada
        self.extra = extra

    def actuar(self, contexto):
        return super().actuar(contexto) + f" + {self.extra}"


class Recurso:
    def __init__(self, nombre, cantidad):
        self.nombre = nombre
        self._cantidad = 0
        self.cantidad = cantidad                 # pasa por el setter

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        if valor < 0:
            print(f"Cantidad invalida para {self.nombre}: {valor}")
        else:
            self._cantidad = valor

    def __repr__(self):
        return f"Recurso({self.nombre!r}, {self._cantidad})"


def cargar_entidades(ruta):
    """CSV con encabezado: tipo,nombre,valor. Retorna dict nombre -> objeto."""
    entidades = {}
    constructores = {
        "A": lambda nombre, valor: TipoA(nombre=nombre, valor_a=int(valor)),
        "B": lambda nombre, valor: TipoB(nombre=nombre, valor_b=int(valor)),
    }
    with open(ruta, "r", encoding="utf-8") as archivo:
        archivo.readline()
        for linea in archivo:
            if not linea.strip():
                continue
            tipo, nombre, valor = linea.strip().split(",")
            entidades[nombre] = constructores[tipo](nombre, valor)
    return entidades


def procesar_acciones(ruta, entidades):
    """Una accion por linea, sin encabezado; campos variables."""
    cola = deque()
    historial = []                                # stack para deshacer
    conteo = defaultdict(int)
    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            valores = linea.strip().split(",")
            if not valores[0]:
                continue
            accion = valores[0]
            if accion == "llegar":
                cola.append(valores[1])
                print(f"[{valores[1]}] en cola. Esperando: {len(cola)}")
            elif accion == "atender":
                if not cola:
                    print("No hay nadie en cola")
                    continue
                nombre = cola.popleft()
                entidad = entidades.get(nombre)
                if entidad is None:
                    print(f"No existe {nombre}")
                    continue
                print(entidad.actuar(None))
                historial.append(nombre)
                conteo[type(entidad).__name__] += 1
            elif accion == "deshacer":
                if historial:
                    print(f"Deshecho: {historial.pop()}")
                else:
                    print("Nada que deshacer")
    return dict(conteo)


if __name__ == "__main__":
    # Demo autocontenida: crea data/ junto a este archivo si no existe.
    base = os.path.dirname(os.path.abspath(__file__))
    carpeta = os.path.join(base, CARPETA_DATOS)
    os.makedirs(carpeta, exist_ok=True)
    ruta_ent = os.path.join(carpeta, "entidades.csv")
    ruta_acc = os.path.join(carpeta, "acciones.txt")
    if not os.path.exists(ruta_ent):
        with open(ruta_ent, "w", encoding="utf-8") as f:
            f.write("tipo,nombre,valor\nA,Ana,10\nB,Ben,20\n")
        with open(ruta_acc, "w", encoding="utf-8") as f:
            f.write("llegar,Ana\nllegar,Ben\natender\natender\natender\n"
                    "deshacer\n")
    entidades = cargar_entidades(ruta_ent)
    entidades["Cami"] = TipoAB(nombre="Cami", valor_a=1, valor_b=2, extra=3)
    print([c.__name__ for c in TipoAB.__mro__])
    for entidad in entidades.values():           # polimorfismo
        print(entidad.actuar(None))
    print(procesar_acciones(ruta_acc, entidades))
    r = Recurso("Cafe", 5)
    r.cantidad -= 10
    print(r)
