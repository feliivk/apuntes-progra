from collections import deque

from bases import LineaPedido, Pedido
from empleados import Cajero, Repartidor, Polifuncional
from productos import Producto, Inventario
from utils import registrar_llamada


class Tienda:

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.inventario = Inventario()
        # TODO Parte 4: crea los tres atributos con la estructura que
        # indica el diagrama y justifica cada una en un comentario de una
        # linea (que operacion necesita ser eficiente).
        # self.empleados    -> fila de empleados. El primero que puede
        #                      atender un pedido lo hace y luego pasa al
        #                      FINAL de la fila.
        # self.cola_pedidos -> los pedidos se atienden en el orden en que
        #                      llegaron (el primero en llegar es el primero
        #                      en salir).
        # self.rechazados   -> pedidos rechazados; al final de la jornada
        #                      se revisan del mas reciente al mas antiguo.

    def cargar_productos(self, ruta: str) -> None:
        with open(ruta, encoding="utf-8") as archivo:
            archivo.readline()  # saltamos el encabezado
            for linea in archivo:
                producto = Producto.desde_linea(linea.strip())
                self.inventario.agregar(producto)

    def cargar_empleados(self, ruta: str) -> None:
        """
        Lee el csv de empleados (tiene encabezado). Segun la columna tipo
        crea un Cajero, un Repartidor o un Polifuncional, instanciando
        con argumentos por palabra clave (keywords) y convirtiendo
        sueldo_base y bono a int y comision a float, y lo agrega al final
        de self.empleados. Fijate en cargar_productos como ejemplo.
        """
        # TODO Parte 4
        pass

    def crear_pedido(self, id_pedido: str, cliente: str, tipo: str,
                     zona: str, texto_lineas: str) -> Pedido:
        # Ya implementado: "Cafe:2;Croissant:1" -> lista de LineaPedido.
        lineas = []
        for item in texto_lineas.split(";"):
            nombre, cantidad = item.split(":")
            lineas.append(LineaPedido(nombre, int(cantidad)))
        return Pedido(int(id_pedido), cliente, tipo, zona, lineas)

    def encolar_pedido(self, pedido: Pedido) -> None:
        """
        Agrega el pedido al final de la cola e imprime
        "<pedido> en cola. Pedidos esperando: <largo de la cola>".
        """
        # TODO Parte 4
        pass

    def buscar_empleado(self, pedido: Pedido):
        for empleado in self.empleados:
            if empleado.puede_atender(pedido):
                return empleado
        return None

    def atender_siguiente(self) -> None:
        """
        Si la cola esta vacia imprime "No hay pedidos en cola".
        Si no, saca el primer pedido de la cola y busca un empleado con
        buscar_empleado:
          - si no hay empleado, imprime "<pedido> sin empleado disponible"
            y guarda el pedido en self.rechazados (nadie cambia de lugar
            en la fila);
          - si hay, llama a empleado.atender(pedido, self.inventario). Si
            retorna False guarda el pedido en self.rechazados. En ambos
            casos el empleado pasa al final de la fila.
        """
        # TODO Parte 4
        pass

    def procesar_acciones(self, ruta: str) -> None:
        with open(ruta, encoding="utf-8") as archivo:
            for linea in archivo:
                valores = linea.strip().split(",")
                accion = valores[0]
                if accion == "pedido":
                    pedido = self.crear_pedido(*valores[1:])
                    self.encolar_pedido(pedido)
                elif accion == "atender":
                    self.atender_siguiente()
                elif accion == "reponer":
                    self.inventario.reponer(valores[1], int(valores[2]))

    @registrar_llamada  # Parte 5: el decorador esta en utils.py
    def pagar_sueldos(self) -> None:
        """
        Imprime "=== Sueldos ===" y luego, por cada empleado en el orden
        actual de la fila, una linea con el formato
        "<empleado>: $<sueldo> (<n> pedidos atendidos)".
        """
        # TODO Parte 4
        pass

    def resumen(self) -> None:
        print("=== Inventario final ===")
        valor_total = 0
        for producto in self.inventario.productos.values():
            print(producto)
            valor_total += producto.valor_stock
        print(f"Valor del inventario: ${valor_total}")
        agotados = ", ".join(sorted(self.inventario.agotados))
        print(f"Agotados: {agotados}")
        categorias = {self.inventario.productos[nombre].categoria
                      for nombre in self.inventario.agotados}
        print(f"Categorías con quiebre de stock: "
              f"{', '.join(sorted(categorias))}")
        print("=== Pedidos rechazados (del más reciente al más antiguo) ===")
        while self.rechazados:
            print(self.rechazados.pop())
