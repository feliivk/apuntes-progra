import os

from empleados import Polifuncional
from tienda import Tienda

# Carpeta con los archivos de datos. Puedes cambiarla a "data_grande"
# para probar con el segundo juego de datos, pero la entrega debe
# funcionar con "data".
CARPETA_DATOS = "data"


if __name__ == "__main__":
    tienda = Tienda("DCComercio")
    print(f"=== {tienda.nombre} ===")
    tienda.cargar_productos(os.path.join(CARPETA_DATOS, "productos.csv"))
    tienda.cargar_empleados(os.path.join(CARPETA_DATOS, "empleados.csv"))
    print(f"Productos cargados: {len(tienda.inventario.productos)}")
    print(f"Empleados cargados: {len(tienda.empleados)}")
    for empleado in tienda.empleados:
        print(f"- {empleado}")
    nombres_mro = [clase.__name__ for clase in Polifuncional.__mro__]
    print(f"MRO de Polifuncional: {nombres_mro}")
    print("=== Jornada ===")
    tienda.procesar_acciones(os.path.join(CARPETA_DATOS, "acciones.txt"))
    tienda.pagar_sueldos()
    tienda.resumen()
