def registrar_llamada(funcion):
    """
    Decorador: imprime "[LOG] Ejecutando <nombre>" justo antes de
    ejecutar la funcion decorada y retorna lo que ella retorne.
    """
    def envoltura(*args, **kwargs):
        print(f"[LOG] Ejecutando {funcion.__name__}")
        return funcion(*args, **kwargs)
    return envoltura
