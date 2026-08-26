"""
Bonus resuelto del simulacro DCComercio. Ejecutar con: python3 bonus.py
(parado en la carpeta solucion/). No es parte de la entrega. Todas las
respuestas fueron verificadas ejecutando este archivo con Python 3.14.

Respuestas conceptuales:

1. Lectura del MRO.
   - Con class Polifuncional(Repartidor, Cajero) main.py imprime
     MRO de Polifuncional: ['Polifuncional', 'Repartidor', 'Cajero',
     'Empleado', 'ABC', 'object'].
   - El sueldo de Elena NO cambia: sigue siendo $508081, porque la
     cadena de super().calcular_sueldo() suma los mismos tres extras
     (comision, bono por despachos y bono fijo), solo que en otro orden.
   - Si Polifuncional redefine puede_atender pero NO atender, el MRO
     resuelve atender en Cajero: el pedido #4 (delivery, Matias) se
     imprime como "[Polifuncional Elena] Pedido #4 (delivery, Matias)
     cobrado: $11100" (7500 + 3600, sin COSTO_DESPACHO) y no suma
     despachos. Lo mismo pasa con el #10 (cobrado: $5700). Como ventas
     sube a 19500 (comision int(19500 * 0.03) = 585) pero despachos queda
     en 0, el sueldo baja a $505585.

2. __repr__ vs __str__.
   - print(pedido) y f"{pedido}" llaman a str(pedido). Pedido no define
     __str__, asi que se usa object.__str__, que por defecto llama a
     __repr__. Por eso ambos muestran "Pedido #1 (local, Camila)".
   - Al imprimir una lista, Python usa __repr__ de cada elemento (no
     __str__). Como Producto solo define __str__, se veria algo como
     [<productos.Producto object at 0x7f...>].

3. Property de solo lectura y argumentos posicionales.
   - producto.valor_stock = 1 lanza
     AttributeError: property 'valor_stock' of 'Producto' object has no setter
   - Cajero("Ana", 450000, 0.05) lanza
     TypeError: Cajero.__init__() takes 2 positional arguments but 4 were given
     (solo self y comision son posicionales; nombre y sueldo_base viajan
     por **kwargs y por eso deben ir por nombre).
   - Extra: Cajero(nombre="Ana", sueldo_base=1, comision=0.1, zona="X")
     lanza TypeError: object.__init__() takes exactly one argument (the
     instance to initialize): el keyword sobrante llega hasta object.

4. faltante con un pedido que mezcla producto inexistente y sin stock:
   retorna el primero EN EL ORDEN DEL PEDIDO (ver abajo: Sushi y luego
   Torta, segun como se escriban las lineas).
"""
import io
import contextlib
import os

import tienda as modulo_tienda
from bases import LineaPedido, Pedido
from empleados import Cajero, Repartidor, Polifuncional
from productos import Producto, Inventario
from tienda import Tienda


class PolifuncionalInvertida(Repartidor, Cajero):

    def __init__(self, bono: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.bono = bono

    def puede_atender(self, pedido: Pedido) -> bool:
        return (Cajero.puede_atender(self, pedido)
                or Repartidor.puede_atender(self, pedido))

    def atender(self, pedido: Pedido, inventario) -> bool:
        if pedido.tipo == "local":
            return Cajero.atender(self, pedido, inventario)
        return Repartidor.atender(self, pedido, inventario)

    def calcular_sueldo(self) -> int:
        return super().calcular_sueldo() + self.bono


class PolifuncionalSinAtender(Cajero, Repartidor):

    def __init__(self, bono: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.bono = bono

    def puede_atender(self, pedido: Pedido) -> bool:
        return (Cajero.puede_atender(self, pedido)
                or Repartidor.puede_atender(self, pedido))

    def calcular_sueldo(self) -> int:
        return super().calcular_sueldo() + self.bono


def simular_con(clase_polifuncional) -> str:
    """Corre la jornada con data/ usando otra clase para 'polifuncional'."""
    modulo_tienda.Polifuncional = clase_polifuncional
    salida = io.StringIO()
    with contextlib.redirect_stdout(salida):
        tienda = Tienda("DCComercio")
        tienda.cargar_productos(os.path.join("data", "productos.csv"))
        tienda.cargar_empleados(os.path.join("data", "empleados.csv"))
        tienda.procesar_acciones(os.path.join("data", "acciones.txt"))
        tienda.pagar_sueldos()
    modulo_tienda.Polifuncional = Polifuncional
    return salida.getvalue()


if __name__ == "__main__":
    print("1) MRO invertido:",
          [clase.__name__ for clase in PolifuncionalInvertida.__mro__])
    lineas = simular_con(PolifuncionalInvertida).splitlines()
    print("   Sueldo:", [x for x in lineas if x.startswith("Polif")][-1])

    print("2) Sin redefinir atender:")
    lineas = simular_con(PolifuncionalSinAtender).splitlines()
    for linea in lineas:
        if "Elena" in linea and "en cola" not in linea:
            print("  ", linea)

    print("3) Pedido.__str__ is object.__str__:",
          Pedido.__str__ is object.__str__)
    print("   lista de Producto:", [Producto("Cafe", 1500, "bebidas", 5)])

    producto = Producto("Cafe", 1500, "bebidas", 5)
    try:
        producto.valor_stock = 1
    except AttributeError as error:
        print("4) AttributeError:", error)
    try:
        Cajero("Ana", 450000, 0.05)
    except TypeError as error:
        print("5) TypeError:", error)
    try:
        Cajero(nombre="Ana", sueldo_base=1, comision=0.1, zona="X")
    except TypeError as error:
        print("6) TypeError:", error)

    inventario = Inventario()
    inventario.agregar(Producto("Torta", 12000, "pasteleria", 0))
    print("7) faltante:",
          inventario.faltante([LineaPedido("Sushi", 1),
                               LineaPedido("Torta", 1)]),
          inventario.faltante([LineaPedido("Torta", 1),
                               LineaPedido("Sushi", 1)]))
