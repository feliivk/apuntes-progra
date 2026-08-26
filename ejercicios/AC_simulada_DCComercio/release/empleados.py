from bases import Empleado, Pedido, COSTO_DESPACHO, BONO_DESPACHO


class Cajero(Empleado):
    """
    Atiende pedidos de tipo "local". Recibe una comision (float entre 0
    y 1) sobre el total de sus ventas.
    """

    # TODO Parte 2: __init__ que reciba comision y **kwargs, haga UNA
    # llamada a super().__init__(**kwargs) y cree los atributos comision
    # y ventas (ventas parte en 0).

    # TODO Parte 2: puede_atender, atender y calcular_sueldo (este ultimo
    # EXTIENDE el de Empleado con super()).
    pass


class Repartidor(Empleado):
    """
    Atiende pedidos de tipo "delivery" cuya zona coincide con la suya.
    Recibe BONO_DESPACHO por cada pedido despachado.
    """

    # TODO Parte 2: __init__ que reciba zona y **kwargs, haga UNA llamada
    # a super().__init__(**kwargs) y cree los atributos zona y despachos
    # (parte en 0).

    # TODO Parte 2: puede_atender, atender y calcular_sueldo.
    pass


class Polifuncional:
    """
    Atiende pedidos locales como un Cajero y pedidos delivery de su zona
    como un Repartidor. Ademas recibe un bono fijo.
    """

    # TODO Parte 3: completa la herencia de esta clase (debe heredar de
    # Cajero y de Repartidor, en ese orden) y escribe aqui, en un
    # comentario, el MRO que resulta.

    # TODO Parte 3: __init__ que reciba bono y **kwargs con UNA sola
    # llamada a super().__init__(**kwargs), y los metodos puede_atender,
    # atender y calcular_sueldo.
    pass


# Para probar las Partes 2 y 3 sin la Parte 4 ejecuta
# python3 pruebas_empleados.py (o copia aqui abajo, dentro de un
# if __name__ == "__main__":, lo que quieras probar).
