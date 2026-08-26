from collections import deque

from bases import LineaPedido, Pedido
from empleados import Cajero, Repartidor, Polifuncional
from productos import Producto, Inventario
from utils import registrar_llamada


class Tienda:

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.inventario = Inventario()
        # deque: el empleado que atiende se saca de cualquier posicion
        # (remove) y se agrega al final (append); ademas se recorre en
        # orden. Una lista tambien sirve, pero deque deja explicito que
        # es una fila que rota.
        self.empleados = deque()
        # deque: los pedidos entran por el final (append) y salen por el
        # inicio (popleft) en O(1). Con una lista, pop(0) es O(n).
        self.cola_pedidos = deque()
        # list usada como stack: append para guardar y pop para sacar el
        # mas reciente (LIFO), ambos O(1).
        self.rechazados = []

    def cargar_productos(self, ruta: str) -> None:
        with open(ruta, encoding="utf-8") as archivo:
            archivo.readline()  # saltamos el encabezado
            for linea in archivo:
                producto = Producto.desde_linea(linea.strip())
                self.inventario.agregar(producto)

    def cargar_empleados(self, ruta: str) -> None:
        with open(ruta, encoding="utf-8") as archivo:
            archivo.readline()  # saltamos el encabezado
            for linea in archivo:
                valores = linea.strip().split(",")
                tipo, nombre, sueldo, comision, zona, bono = valores
                if tipo == "cajero":
                    empleado = Cajero(nombre=nombre, sueldo_base=int(sueldo),
                                      comision=float(comision))
                elif tipo == "repartidor":
                    empleado = Repartidor(nombre=nombre,
                                          sueldo_base=int(sueldo), zona=zona)
                else:
                    empleado = Polifuncional(nombre=nombre,
                                             sueldo_base=int(sueldo),
                                             comision=float(comision),
                                             zona=zona, bono=int(bono))
                self.empleados.append(empleado)

    def crear_pedido(self, id_pedido: str, cliente: str, tipo: str,
                     zona: str, texto_lineas: str) -> Pedido:
        lineas = []
        for item in texto_lineas.split(";"):
            nombre, cantidad = item.split(":")
            lineas.append(LineaPedido(nombre, int(cantidad)))
        return Pedido(int(id_pedido), cliente, tipo, zona, lineas)

    def encolar_pedido(self, pedido: Pedido) -> None:
        self.cola_pedidos.append(pedido)
        print(f"{pedido} en cola. Pedidos esperando: "
              f"{len(self.cola_pedidos)}")

    def buscar_empleado(self, pedido: Pedido):
        for empleado in self.empleados:
            if empleado.puede_atender(pedido):
                return empleado
        return None

    def atender_siguiente(self) -> None:
        if not self.cola_pedidos:
            print("No hay pedidos en cola")
            return
        pedido = self.cola_pedidos.popleft()
        empleado = self.buscar_empleado(pedido)
        if empleado is None:
            print(f"{pedido} sin empleado disponible")
            self.rechazados.append(pedido)
            return
        exito = empleado.atender(pedido, self.inventario)
        if not exito:
            self.rechazados.append(pedido)
        # El empleado pasa al final de la fila, haya tenido exito o no.
        self.empleados.remove(empleado)
        self.empleados.append(empleado)

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

    @registrar_llamada
    def pagar_sueldos(self) -> None:
        print("=== Sueldos ===")
        for empleado in self.empleados:
            print(f"{empleado}: ${empleado.calcular_sueldo()} "
                  f"({empleado.pedidos_atendidos} pedidos atendidos)")

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
