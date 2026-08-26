"""
Pruebas de las Partes 1 a 3 SIN necesitar la Parte 4.
Ejecutar con: python3 pruebas_empleados.py (parado en la carpeta de la
actividad). No es parte de la entrega: puedes borrarlo o modificarlo.
La salida esperada esta en el enunciado (Parte 3).
"""
from bases import LineaPedido, Pedido
from empleados import Cajero, Repartidor, Polifuncional
from productos import Producto, Inventario


if __name__ == "__main__":
    inventario = Inventario()
    inventario.agregar(Producto("Cafe", 1500, "bebidas", 5))
    inventario.agregar(Producto("Croissant", 1300, "pasteleria", 1))

    ana = Cajero(nombre="Ana", sueldo_base=450000, comision=0.05)
    pedido_1 = Pedido(1, "Camila", "local", "-", [LineaPedido("Cafe", 2)])
    pedido_2 = Pedido(2, "Tomas", "delivery", "Norte",
                      [LineaPedido("Cafe", 1)])
    pedido_3 = Pedido(3, "Sofia", "local", "-",
                      [LineaPedido("Cafe", 1), LineaPedido("Croissant", 2)])
    pedido_4 = Pedido(4, "Matias", "delivery", "Oriente",
                      [LineaPedido("Cafe", 1)])
    print(ana.puede_atender(pedido_1), ana.puede_atender(pedido_2))
    print(ana.atender(pedido_1, inventario))
    print(ana.atender(pedido_3, inventario))
    print(ana.calcular_sueldo(), ana.pedidos_atendidos)

    carla = Repartidor(nombre="Carla", sueldo_base=400000, zona="Norte")
    print(carla.puede_atender(pedido_1), carla.puede_atender(pedido_2))
    print(carla.atender(pedido_2, inventario))
    print(carla.calcular_sueldo(), carla.pedidos_atendidos)
    print(inventario.productos["Cafe"])

    elena = Polifuncional(nombre="Elena", sueldo_base=480000, comision=0.03,
                          zona="Oriente", bono=25000)
    print([clase.__name__ for clase in Polifuncional.__mro__])
    print(elena.puede_atender(pedido_1), elena.puede_atender(pedido_2),
          elena.puede_atender(pedido_4))
    elena.ventas = 2700
    elena.despachos = 2
    print(elena.calcular_sueldo())
