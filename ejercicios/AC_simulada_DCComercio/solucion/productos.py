class Producto:

    def __init__(self, nombre: str, precio: int, categoria: str,
                 stock: int) -> None:
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        # _stock debe existir ANTES de la primera asignacion a self.stock:
        # el setter lo lee para armar el mensaje "Se mantiene en ...".
        self._stock = 0
        self.stock = stock  # pasa por el setter, que valida el valor

    @classmethod
    def desde_linea(cls, linea: str):
        nombre, precio, categoria, stock = linea.split(",")
        return cls(nombre, int(precio), categoria, int(stock))

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int) -> None:
        if valor < 0:
            print(f"Stock inválido para {self.nombre}: {valor}. "
                  f"Se mantiene en {self._stock}")
        else:
            self._stock = valor

    @property
    def valor_stock(self) -> int:
        # Solo lectura: no tiene setter, asignarla lanza AttributeError.
        return self.precio * self.stock

    def __str__(self) -> str:
        return f"{self.nombre} (${self.precio}) - stock: {self.stock}"


class Inventario:

    def __init__(self) -> None:
        # dict nombre -> Producto: faltante, descontar y reponer buscan
        # por nombre; con un dict la busqueda es O(1) y no hay que
        # recorrer todos los productos.
        self.productos = {}
        # set de nombres: no admite repetidos (un producto puede agotarse
        # y reponerse varias veces) y sacar/agregar es O(1).
        self.agotados = set()

    def agregar(self, producto: Producto) -> None:
        self.productos[producto.nombre] = producto
        if producto.stock == 0:
            self.agotados.add(producto.nombre)

    def faltante(self, lineas: list) -> str | None:
        for linea in lineas:
            if linea.nombre not in self.productos:
                return linea.nombre
            if self.productos[linea.nombre].stock < linea.cantidad:
                return linea.nombre
        return None

    def descontar(self, lineas: list) -> int:
        total = 0
        for linea in lineas:
            producto = self.productos[linea.nombre]
            producto.stock -= linea.cantidad
            total += producto.precio * linea.cantidad
            if producto.stock == 0:
                self.agotados.add(producto.nombre)
        return total

    def reponer(self, nombre: str, cantidad: int) -> None:
        if nombre not in self.productos:
            print(f"No existe el producto {nombre}")
            return
        producto = self.productos[nombre]
        producto.stock += cantidad
        if producto.stock > 0:
            self.agotados.discard(nombre)
        print(f"Reposición de {nombre}: ahora tiene {producto.stock} unidades")
