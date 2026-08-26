import os
import collections


def cargar_inventario(path: str) -> dict:
    # Inventario: dict nombre -> {"precio": int, "cantidad": int}
    # Acceso O(1) por nombre de producto.
    inventario = {}
    with open(path, "r") as productos_file:
        for producto_line in productos_file.readlines():
            valores = producto_line.strip().split(",")
            nombre = valores[0]
            precio = int(valores[1])
            cantidad = int(valores[2])
            inventario[nombre] = {"precio": precio, "cantidad": cantidad}
    return inventario


def agregar_al_carro(inventario: dict, carros: dict, rut: str,
                     nombre_producto: str) -> None:
    if nombre_producto not in inventario:
        print(f"[{rut}] El producto {nombre_producto} no existe")
    elif inventario[nombre_producto]["cantidad"] <= 0:
        print(f"[{rut}] No quedan unidades de {nombre_producto}")
    else:
        inventario[nombre_producto]["cantidad"] -= 1  # queda reservado
        carros[rut].append(nombre_producto)          # push al stack
        print(f"[{rut}] {nombre_producto} agregado al carro")


def sacar_del_carro(inventario: dict, carros: dict, rut: str) -> None:
    if len(carros[rut]) == 0:
        print(f"[{rut}] No quedan productos en el carro para sacar")
    else:
        nombre_producto = carros[rut].pop()          # pop: el ultimo agregado
        inventario[nombre_producto]["cantidad"] += 1
        print(f"[{rut}] {nombre_producto} devuelto al inventario")


def cerrar_sesion(inventario: dict, carros: dict, rut: str) -> None:
    if len(carros[rut]) == 0:
        print(f"[{rut}] Error: el carro esta vacio, no hay sesion que cerrar")
    else:
        liberados = []
        while len(carros[rut]) > 0:
            nombre_producto = carros[rut].pop()
            inventario[nombre_producto]["cantidad"] += 1
            liberados.append(nombre_producto)
        print(f"[{rut}] Sesión cerrada. Productos liberados {liberados}")


def pagar(inventario: dict, carros: dict, rut: str) -> None:
    if len(carros[rut]) == 0:
        print(f"[{rut}] No hay nada que pagar")
    else:
        total = 0
        while len(carros[rut]) > 0:
            nombre_producto = carros[rut].pop()
            total += inventario[nombre_producto]["precio"]
        # Las unidades ya fueron descontadas al agregar: no se devuelven.
        print(f"[{rut}] Pagado carro. Total de compra: {total}")


if __name__ == "__main__":
    carpeta = input("Ingrese nombre de carpeta: ")
    productos_path = os.path.join(carpeta, "productos.txt")
    acciones_path = os.path.join(carpeta, "acciones.txt")

    # Aqui se leen los productos
    inventario = cargar_inventario(productos_path)

    # Carros: dict rut -> stack (lista usada con append/pop).
    # defaultdict crea un carro vacio la primera vez que aparece un RUT.
    carros = collections.defaultdict(list)

    # Aqui se leen las acciones
    with open(acciones_path, "r") as acciones_file:
        for accion_line in acciones_file.readlines():
            valores = accion_line.strip().split(",")
            accion = valores[0]
            rut = valores[1]
            if accion == "Agregar al carro":
                nombre_producto = valores[2]
                agregar_al_carro(inventario, carros, rut, nombre_producto)
            elif accion == "Sacar del carro":
                sacar_del_carro(inventario, carros, rut)
            elif accion == "Cerrar sesion":
                cerrar_sesion(inventario, carros, rut)
            elif accion == "Pagar":
                pagar(inventario, carros, rut)
