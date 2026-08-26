"""
CHULETA OOP AVANZADO (semana 4) - IIC2233 2026-2
Ejecutar: python3 chuleta_oop_avanzado.py
Cada seccion es una funcion demo_*; abajo se ejecutan todas.
"""
from abc import ABC, abstractmethod


# =====================================================================
# 1. HERENCIA, super() y EXTENDER un metodo
#    - class Hija(Padre)
#    - super().__init__(...)  -> sin self, sin nombrar la clase
#    - override: mismo nombre; extender: override que llama super()
#    - isinstance(obj, Clase) es True tambien para subclases
# =====================================================================
class Jugador:
    def __init__(self, apellido, numero):
        self.apellido = apellido
        self.numero = numero
        self.tiene_balon = False

    def pasar(self, otro):
        print(f"{self.apellido} pasa a {otro.apellido}")
        self.tiene_balon = False
        otro.tiene_balon = True

    def __str__(self):
        return f"{type(self).__name__} {self.apellido} #{self.numero}"


class Arquero(Jugador):
    def __init__(self, apellido, numero, porc_atajadas):
        super().__init__(apellido, numero)      # primero lo del padre
        self.porc_atajadas = porc_atajadas       # despues lo propio

    def pasar(self, otro):                       # override que EXTIENDE
        super().pasar(otro)
        print("(saque largo)")


def demo_herencia():
    print("\n--- 1. herencia ---")
    a = Arquero("Bravo", 1, 0.55)
    j = Jugador("Vidal", 8)
    a.pasar(j)
    print(a)                                   # usa __str__
    print(isinstance(a, Jugador), issubclass(Arquero, Jugador),
          issubclass(Jugador, Arquero), type(a) == Jugador)
    # True True False False


# =====================================================================
# 2. MULTIHERENCIA con **kwargs y UNA sola llamada a super()
#    - TODAS las clases de la cadena reciben **kwargs y llaman super()
#    - se instancia por keyword
#    - Clase.__mro__ muestra el orden de busqueda
#    - llamada puntual saltandose el MRO: Defensa.metodo(self, args)
# =====================================================================
class Defensa(Jugador):
    def __init__(self, porc_barridas, **kwargs):
        super().__init__(**kwargs)
        self.porc_barridas = porc_barridas

    def rol(self):
        return "defiende"


class Delantero(Jugador):
    def __init__(self, porc_tiros, **kwargs):
        super().__init__(**kwargs)
        self.porc_tiros = porc_tiros

    def rol(self):
        return "ataca"


class Lateral(Defensa, Delantero):
    def __init__(self, porc_centros, **kwargs):
        super().__init__(**kwargs)               # UNA sola llamada
        self.porc_centros = porc_centros

    def rol(self):
        # gana Defensa (primera base); para usar ambas, llamadas puntuales
        return f"{Defensa.rol(self)} y {Delantero.rol(self)}"


def demo_multiherencia():
    print("\n--- 2. multiherencia ---")
    v = Lateral(apellido="Valdivia", numero=6, porc_barridas=0.4,
                porc_tiros=0.7, porc_centros=0.75)
    print([c.__name__ for c in Lateral.__mro__])
    # ['Lateral', 'Defensa', 'Delantero', 'Jugador', 'object']
    print(v.rol(), "|", v.porc_barridas, v.porc_tiros, v.porc_centros)
    # Errores tipicos (descomentar para ver):
    # Lateral("Valdivia", 6, 0.4, 0.7, 0.75)
    #   TypeError: Lateral.__init__() takes 2 positional arguments but 6 were given
    # Lateral(apellido="V", numero=6, porc_barridas=0.4, porc_tiros=0.7,
    #         porc_centros=0.75, porc_barida=1)
    #   TypeError: object.__init__() takes exactly one argument (typo llega a object)


# =====================================================================
# 3. MRO y PROBLEMA DEL DIAMANTE
#    - super() llama al SIGUIENTE en el MRO de la instancia (no al padre)
#    - con super() la base se ejecuta 1 vez; con llamadas explicitas, 2
# =====================================================================
class Base:
    def llamar(self):
        print("  Base")


class Izq(Base):
    def llamar(self):
        print("  Izq ini")
        super().llamar()
        print("  Izq fin")


class Der(Base):
    def llamar(self):
        print("  Der ini")
        super().llamar()
        print("  Der fin")


class Diamante(Izq, Der):
    def llamar(self):
        print("  Diamante ini")
        super().llamar()
        print("  Diamante fin")


def demo_diamante():
    print("\n--- 3. diamante ---")
    print([c.__name__ for c in Diamante.__mro__])
    # ['Diamante', 'Izq', 'Der', 'Base', 'object']
    Diamante().llamar()
    # Diamante ini / Izq ini / Der ini / Base / Der fin / Izq fin / Diamante fin
    # MRO inconsistente (descomentar): TypeError Cannot create a consistent MRO
    # class X: pass
    # class Y: pass
    # class A(X, Y): pass
    # class B(Y, X): pass
    # class F(A, B): pass


# =====================================================================
# 4. CLASES ABSTRACTAS: ABC + @abstractmethod
#    - el TypeError es al INSTANCIAR, no al definir
#    - subclase sin implementar TODOS los abstractos sigue siendo abstracta
#    - un abstracto puede tener cuerpo y reutilizarse con super()
# =====================================================================
class Figura(ABC):
    def __init__(self, nombre):
        self.nombre = nombre

    @abstractmethod
    def area(self):
        pass

    def describir(self):                         # normal: se hereda
        return f"{self.nombre}: {self.area()}"


class Cuadrado(Figura):
    def __init__(self, lado):
        super().__init__("Cuadrado")
        self.lado = lado

    def area(self):
        return self.lado ** 2


class Circulo(Figura):
    def __init__(self, radio):
        super().__init__("Circulo")
        self.radio = radio

    def area(self):
        return round(3.14159 * self.radio ** 2, 2)


def demo_abstractas():
    print("\n--- 4. abstractas ---")
    for figura in [Cuadrado(3), Circulo(2)]:     # polimorfismo
        print(figura.describir())
    try:
        Figura("x")
    except TypeError as error:
        print("TypeError:", error)
    # Can't instantiate abstract class Figura without an implementation
    # for abstract method 'area'


# =====================================================================
# 5. PROPERTIES: @property (getter) + @x.setter; solo lectura sin setter
#    - dentro del getter/setter usar self._x (self.x -> RecursionError)
#    - self.x = valor en __init__ TAMBIEN pasa por el setter
#    - forma funcional: x = property(fget, fset)
# =====================================================================
class Producto:
    total_creados = 0                            # variable de clase

    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.precio = precio
        self._stock = 0                          # existe antes del setter
        self.stock = stock                       # pasa por el setter
        Producto.total_creados += 1              # NO self.total_creados

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        if valor < 0:
            print(f"Stock invalido para {self.nombre}: {valor}. "
                  f"Se mantiene en {self._stock}")
        else:
            self._stock = valor

    @property
    def valor_stock(self):                       # solo lectura
        return self.precio * self._stock

    @classmethod
    def desde_linea(cls, linea):                 # fabrica desde CSV
        nombre, precio, stock = linea.strip().split(",")
        return cls(nombre, int(precio), int(stock))

    @staticmethod
    def sin_iva(precio):                         # ni self ni cls
        return round(precio / 1.19)

    def __repr__(self):
        return f"Producto({self.nombre!r}, {self.precio}, {self._stock})"


def demo_properties():
    print("\n--- 5. properties ---")
    p = Producto.desde_linea("Cafe,1500,5\n")
    p.stock -= 1                                 # getter y luego setter
    p.stock = -3                                 # rechazado por el setter
    print(p, p.valor_stock, Producto.sin_iva(1500), Producto.total_creados)
    try:
        p.valor_stock = 1
    except AttributeError as error:
        print("AttributeError:", error)
    # property 'valor_stock' of 'Producto' object has no setter


# =====================================================================
# 6. DECORADORES
#    - funcion que recibe una funcion y RETORNA otra (wrapper)
#    - @deco  ==  f = deco(f)
#    - wrapper con *args, **kwargs y return func(...)
#    - olvidar "return wrapper" -> f queda None -> 'NoneType' not callable
# =====================================================================
def registrar_llamada(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] Ejecutando {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


@registrar_llamada
def pagar(monto, iva=0.19):
    return round(monto * (1 + iva))


def demo_decoradores():
    print("\n--- 6. decoradores ---")
    print(pagar(1000))
    print(pagar(1000, iva=0))
    saludo = pagar                               # sin parentesis: referencia
    print(saludo.__name__)                       # 'wrapper'


# =====================================================================
# 7. __str__ vs __repr__, OPERADORES, duck typing
#    - print usa __str__; si no existe, __repr__; las listas usan __repr__
#    - __add__ retorna un objeto NUEVO; __eq__ define ==; __lt__ define <
#    - no existe function overloading: la ultima def gana
# =====================================================================
class Fraccion:
    def __init__(self, num, den):
        self.num, self.den = num, den

    def __repr__(self):
        return f"Fraccion({self.num}, {self.den})"

    def __str__(self):
        return f"{self.num}/{self.den}"

    def __add__(self, otra):
        return Fraccion(self.num * otra.den + otra.num * self.den,
                        self.den * otra.den)

    def __eq__(self, otra):
        return self.num * otra.den == otra.num * self.den

    def __lt__(self, otra):
        return self.num * otra.den < otra.num * self.den


def demo_operadores():
    print("\n--- 7. str/repr/operadores ---")
    f = Fraccion(1, 2)
    print(f)                                     # 1/2
    print([f, Fraccion(1, 3)])                   # [Fraccion(1, 2), Fraccion(1, 3)]
    print(f + Fraccion(1, 3), f == Fraccion(2, 4), Fraccion(1, 3) < f)

    class Pato:
        def hablar(self):
            return "Quack"

    class Robot:
        def hablar(self):
            return "Beep"

    for cosa in [Pato(), Robot()]:               # duck typing
        print(cosa.hablar())


if __name__ == "__main__":
    demo_herencia()
    demo_multiherencia()
    demo_diamante()
    demo_abstractas()
    demo_properties()
    demo_decoradores()
    demo_operadores()
