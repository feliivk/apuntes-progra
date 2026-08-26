import os
from producto import Producto


def cargar_productos(ruta: str) -> list:
    productos = []
    with open(ruta, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            nombre, precio, stock = linea.split(',')
            productos.append(Producto(nombre, int(precio), int(stock)))
    return productos


def simular_ventas(productos: list) -> None:
    for producto in productos:
        producto.vender()


if __name__ == '__main__':
    ruta = os.path.join('data', 'menu.txt')
    productos = cargar_productos(ruta)
    print('=== DCCafeteria ===')
    for producto in productos:
        print(producto.descripcion())
    print(f'Productos registrados: {Producto.total_productos}')
    simular_ventas(productos)
    simular_ventas(productos)
