from bases import Empleado, Pedido, COSTO_DESPACHO, BONO_DESPACHO


class Cajero(Empleado):

    def __init__(self, comision: float, **kwargs) -> None:
        super().__init__(**kwargs)
        self.comision = comision
        self.ventas = 0

    def puede_atender(self, pedido: Pedido) -> bool:
        return pedido.tipo == "local"

    def atender(self, pedido: Pedido, inventario) -> bool:
        if not self.revisar_stock(pedido, inventario):
            return False
        total = inventario.descontar(pedido.lineas)
        self.ventas += total
        self.pedidos_atendidos += 1
        print(f"[{self}] {pedido} cobrado: ${total}")
        return True

    def calcular_sueldo(self) -> int:
        return super().calcular_sueldo() + int(self.ventas * self.comision)


class Repartidor(Empleado):

    def __init__(self, zona: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.zona = zona
        self.despachos = 0

    def puede_atender(self, pedido: Pedido) -> bool:
        return pedido.tipo == "delivery" and pedido.zona == self.zona

    def atender(self, pedido: Pedido, inventario) -> bool:
        if not self.revisar_stock(pedido, inventario):
            return False
        total = inventario.descontar(pedido.lineas) + COSTO_DESPACHO
        self.despachos += 1
        self.pedidos_atendidos += 1
        print(f"[{self}] {pedido} despachado a {pedido.zona}: ${total}")
        return True

    def calcular_sueldo(self) -> int:
        return super().calcular_sueldo() + BONO_DESPACHO * self.despachos


class Polifuncional(Cajero, Repartidor):
    # MRO: Polifuncional -> Cajero -> Repartidor -> Empleado -> ABC -> object
    # Por eso super().calcular_sueldo() pasa por Cajero, luego Repartidor
    # y finalmente Empleado, sumando cada extra una sola vez.

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
