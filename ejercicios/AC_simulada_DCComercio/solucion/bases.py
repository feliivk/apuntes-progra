"""
Clases base de DCComercio.

NO MODIFICAR ESTE ARCHIVO. Lee el codigo con atencion: las clases que
debes completar heredan de Empleado y usan Pedido y LineaPedido.
"""
from abc import ABC, abstractmethod
from collections import namedtuple

# Costo fijo que se le cobra al cliente por cada despacho a domicilio.
COSTO_DESPACHO = 2500
# Bono que recibe un repartidor por cada pedido despachado.
BONO_DESPACHO = 1500

# Una linea de un pedido: nombre del producto y cantidad solicitada.
LineaPedido = namedtuple("LineaPedido", ["nombre", "cantidad"])


class Pedido:

    def __init__(self, id_pedido: int, cliente: str, tipo: str,
                 zona: str, lineas: list) -> None:
        self.id_pedido = id_pedido
        self.cliente = cliente
        self.tipo = tipo      # "local" o "delivery"
        self.zona = zona      # "-" cuando el pedido es local
        self.lineas = lineas  # list[LineaPedido]

    def __repr__(self) -> str:
        return f"Pedido #{self.id_pedido} ({self.tipo}, {self.cliente})"


class Empleado(ABC):

    def __init__(self, nombre: str, sueldo_base: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.nombre = nombre
        self.sueldo_base = sueldo_base
        self.pedidos_atendidos = 0

    @abstractmethod
    def puede_atender(self, pedido: Pedido) -> bool:
        pass

    @abstractmethod
    def atender(self, pedido: Pedido, inventario) -> bool:
        pass

    def revisar_stock(self, pedido: Pedido, inventario) -> bool:
        """
        Retorna True si el inventario tiene todo lo que pide el pedido.
        Si falta algo, imprime el rechazo y retorna False.
        """
        faltante = inventario.faltante(pedido.lineas)
        if faltante is None:
            return True
        print(f"[{self}] {pedido} rechazado: falta {faltante}")
        return False

    def calcular_sueldo(self) -> int:
        return self.sueldo_base

    def __str__(self) -> str:
        return f"{type(self).__name__} {self.nombre}"
