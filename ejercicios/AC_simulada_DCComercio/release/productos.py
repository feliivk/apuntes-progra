class Producto:

    def __init__(self, nombre: str, precio: int, categoria: str,
                 stock: int) -> None:
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        # TODO Parte 1: crea el atributo "privado" _stock (parte en 0) ANTES
        # de la linea siguiente, porque el setter lo lee para armar el
        # mensaje "Se mantiene en <stock actual>".
        self.stock = stock  # debe pasar por el setter de la property

    # TODO Parte 1: metodo de clase desde_linea(cls, linea) que reciba una
    # linea del csv ya sin salto de linea ("Cafe,1500,bebidas,5"), la
    # separe por coma y retorne un Producto (precio y stock como int).

    # TODO Parte 1: property stock (getter) y su setter con validacion.
    # Si el valor es negativo, imprime
    # "Stock inválido para <nombre>: <valor>. Se mantiene en <stock actual>"
    # y NO cambies el atributo. Si es valido, guardalo.

    # TODO Parte 1: property de SOLO LECTURA valor_stock que retorne
    # precio * stock (sin setter).

    # TODO Parte 1: __str__ con el formato
    # "<nombre> ($<precio>) - stock: <stock>"


class Inventario:

    def __init__(self) -> None:
        # TODO Parte 1: crea ambos atributos con la estructura que indica
        # el diagrama y justifica en un comentario de una linea por que
        # es la adecuada.
        # self.productos -> nombre del producto -> Producto. Debe permitir
        #                   buscar un Producto por su nombre de forma
        #                   eficiente (sin recorrer todo).
        # self.agotados  -> nombres (sin repetir) de los productos cuyo
        #                   stock es 0.
        pass

    def agregar(self, producto: Producto) -> None:
        """
        Guarda el producto en self.productos usando su nombre como llave.
        Si su stock es 0, tambien lo registra en self.agotados.
        """
        # TODO Parte 1
        pass

    def faltante(self, lineas: list) -> str | None:
        """
        Recibe una lista de LineaPedido. Retorna el nombre del PRIMER
        producto (en el orden de la lista) que no existe en el inventario
        o que no tiene stock suficiente. Si todo esta disponible retorna
        None.
        """
        # TODO Parte 1
        pass

    def descontar(self, lineas: list) -> int:
        """
        Descuenta del stock la cantidad pedida en cada LineaPedido y
        retorna el total a pagar (suma de precio * cantidad). Si un
        producto queda en 0, lo agrega a self.agotados.
        Puedes asumir que faltante(lineas) ya retorno None.
        """
        # TODO Parte 1
        pass

    def reponer(self, nombre: str, cantidad: int) -> None:
        """
        Si el producto no existe imprime "No existe el producto <nombre>".
        Si existe, suma cantidad a su stock (la validacion la hace la
        property), lo saca de self.agotados si quedo con stock mayor a 0
        e imprime "Reposición de <nombre>: ahora tiene <stock> unidades".
        """
        # TODO Parte 1
        pass
