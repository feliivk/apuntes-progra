class Producto:
    total_productos = 0

    def __init__(self, nombre: str, precio: int, stock: int) -> None:
        self.nombre = nombre
        self.precio = precio
        self._stock = stock
        Producto.total_productos += 1

    def descripcion(self) -> str:
        return f'{self.nombre}: ${self.precio} (stock: {self._stock})'

    def vender(self) -> None:
        if self._stock > 0:
            self._stock -= 1
            print(f'Vendido: {self.nombre}. Stock restante: {self._stock}')
        else:
            print(f'No queda stock de {self.nombre}')
