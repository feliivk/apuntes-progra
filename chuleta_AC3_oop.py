# chuleta_AC3_oop.py - exportación de chuleta_AC3_oop.ipynb (mismas celdas, en orden)

# %% [markdown]
# # Chuleta AC3 — OOP avanzado (herencia · multiherencia · ABC · properties · decoradores)
## **Cómo usar esta chuleta:** `Ctrl+F` con la palabra del enunciado (`abstracta`, `property`, `hereda de`, `**kwargs`,
# `diagrama`, `tests`, `__add__`, `Error`). Cada sección tiene: cuándo se usa → código copiable que corre → errores típicos.
# Al final hay tres **problemas tipo resueltos completos** (secciones 8, 9 y 10: genes 2026-1, vehículos 2023-2025, sistema desde cero), una tabla **error → arreglo** (11) y el checklist (12).
## ## Flujo de la AC (2 horas)
## 1. **Leer el enunciado completo** sin escribir. Anotar: carpeta de entrega (`Actividades/AC3`), archivos *No modificar* y *Modificar/Entregar*, y qué se imprime o testea.
# 2. **Subir los archivos base de inmediato** (add, commit, push).
# 3. **Leer los archivos "No modificar"** (`bases.py`, `main.py`, `tests_publicos/`): ahí están los nombres EXACTOS de clases, métodos, argumentos (`**kwargs`) y lo que retornan.
# 4. Resolver **en el orden del enunciado**. Después de cada parte: correr `main.py`/tests → push.
# 5. Si algo no sale en 15 min: dejar `pass`/`return None` para que **no se caiga** (código que se cae al correr los tests = 0 puntos) y seguir con lo siguiente.
## ```bash
# cd ~/Trabajo/feliivk-iic2233-2026-2 && git pull
# mkdir -p Actividades/AC3 && cp -r /ruta/de/la/base/* Actividades/AC3/
# git add . && git commit -m "Base AC3" && git push
# cd Actividades/AC3                                       # SIEMPRE parado en la carpeta de la AC
# python3 main.py
# python3 -m unittest discover tests_publicos -v -b        # todos los tests (si la AC trae tests)
# python3 -m unittest -v -b tests_publicos.tests_parte_1   # solo los de la parte 1
# python3 -m unittest -v -b tests_publicos.tests_parte_1.VerificarAdd.test_dominante_dominante   # uno solo
# ```
## **Leer un test que falla:** `FAIL: test_x (...)` y más abajo `AssertionError: 'Blanco' != 'Negro'` → unittest muestra `primero != segundo`
# en el orden del `assertEqual(a, b)` del test (en los del curso casi siempre `a` = lo que entregó **mi código**, `b` = lo **esperado**;
# confirmar mirando la línea del test que sale en el traceback). `ERROR:` (en vez de `FAIL:`) = mi código lanzó una excepción: leer la última línea del traceback.
# **Ojo con la versión de Python:** los mensajes de error cambian un poco entre 3.10/3.11 (probable en la ISO Lubuntu) y 3.12+ (Arch); la tabla 11 muestra ambas formas.

# %% [markdown]
# ## ¿Se parece la AC3 de hoy a las AC3 de otros semestres? (revisado en los Syllabus 2023-2 → 2026-1)
## | Semestre | AC3 fue… | ¿Mismo tema que hoy? | La AC de OOP avanzado de ese semestre fue… |
# |---|---|---|---|
# | 2026-1 | **OOP avanzado** — genes de perro (`__add__`, `isinstance`, `Dominante`+`Mutable`, ABC, `REGISTRO`) | **SÍ**, exactamente | la misma AC3 → resuelta en la sección 8 |
# | 2025-2 | Iterables e iteradores (lista ligada, DCCruzVerde) | no | no hubo AC; se evaluó en la Experiencia 1 (DCCPalooza: properties acotadas, override de property con `super().animo`) |
# | 2025-1 | Excepciones (DCConductor) | no | **AC2: vehículos** (`Auto`/`Bicicleta` + mixin `MotorElectrico`) |
# | 2024-2 | Programación funcional (DCC Max) | no | **AC2: vehículos** (versión más completa, con tests) |
# | 2024-1 | Iterables y generadores (DCC Max) | no | **AC1: vehículos** |
# | 2023-2 | Threading (DCCarrera) | no | **AC1: vehículos** |
## **Conclusión:** el número "AC3" no importa (cambia el orden de los contenidos cada semestre); lo que se repite es que **la AC de la semana de OOP avanzado**
# siempre pide lo mismo: clase base (a veces ABC) con `__init__(..., *args, **kwargs)`, cadena de hijas con `super().__init__(*args, **kwargs)`,
# **una multiherencia** (diamante o mixin) donde la base debe correr **una sola vez**, **properties** (una con setter que acota + una calculada de solo lectura),
# **override** de un método (extender con `super()` o llamar `Padre.metodo(self, ...)`), **variable de clase** contador y **strings exactos**.
# El enunciado de **vehículos** se usó 4 veces seguidas → está resuelto completo en la sección 9. El de **genes** (2026-1) en la sección 8.

# %% [markdown]
# ## 0. Diccionario: lo que dice el enunciado → lo que escribo
## | Si el enunciado dice… | Escribo… | Sección |
# |---|---|---|
# | "X hereda de Y" / "X **es un** Y" | `class X(Y):` y en `__init__`: `super().__init__(...)` | 1 |
# | "pide los mismos argumentos que Y y además `z`" | `def __init__(self, z, **kwargs): super().__init__(**kwargs); self.z = z` | 3 |
# | "hereda de A **y** B" / "solo **una** llamada a `super`" | `class X(A, B):` + todos los `__init__` con `**kwargs` + instanciar por keyword | 3 |
# | "clase abstracta" / "no se instancia" / "obliga a implementar" | `class X(ABC):` + `@abstractmethod` | 4 |
# | "método abstracto: debe ser implementado en las subclases" | en cada hija: `def metodo(self): ...` (mismo nombre, mismos argumentos) | 4 |
# | "property" / "al leer o asignar el atributo se valida…" | `@property` (getter) + `@x.setter`; adentro **siempre** `self._x` | 5 |
# | "solo lectura" / "no se puede modificar" / "atributo calculado" | `@property` sin setter | 5 |
# | "sobreescribir" / "redefinir el método" | método con el mismo nombre en la hija | 1 |
# | "extender" / "además de lo que hace el padre" | `super().metodo(...)` dentro del método redefinido | 1 |
# | "al usar el operador `+`" / "comparar con `==`" / "ordenar objetos" | `__add__`, `__eq__`, `__lt__` | 2 |
# | "al hacer `print` del objeto" / "representación" | `__str__` (y `__repr__` para verlo dentro de listas) | 2 |
# | "método de clase" / "constructor alternativo" / "registrar subclases" | `@classmethod def m(cls, ...)` | 6 |
# | "método estático" / "no depende de la instancia" | `@staticmethod def m(...)` (sin `self`) | 6 |
# | "contador de instancias" / "compartido por todas las instancias" / "constante" | variable de clase; `Clase.total += 1` | 6 |
# | "determinar si es de tipo…" / "según el tipo de gen" | `isinstance(obj, Clase)` | 1, 8 |
# | "decorador que…" | función que recibe `func` y retorna un `wrapper` | 6 |
# | "diagrama de clases" | flecha hueca = hereda; rombo = "tiene" (atributo con objeto/lista) | 7 |
# | "con probabilidad p" | `from random import random` → `if random() <= p:` | 10 |
# | "identificador único" / "id autoincremental" / "el primero es 0, el segundo 1…" | variable de clase + en `__init__`: `self.id = Clase.contador; Clase.contador += 1` | 6, 9 |
# | "lanza `ValueError`" / "levanta una excepción si…" | `if cond: raise ValueError("mensaje")` (en el setter o en el método) | 5 |
# | "mixin" / "agrega la capacidad de… a una clase" | clase chica con `__init__(self, **kwargs): super().__init__(**kwargs)`; va como segundo padre | 3, 8 |
# | "X es una lista/diccionario con métodos extra" / "hereda de `list`" | `class X(list):` y en los métodos usar `self` como la lista (`for e in self`, `self.append(...)`) | 1 |

# %% [markdown]
# ## 1. Herencia: `class Hija(Padre)`
## La hija recibe **todos** los atributos y métodos del padre. Puede: **agregar** cosas nuevas, **sobreescribir** (mismo nombre → reemplaza)
# o **extender** (mismo nombre + `super().metodo()` adentro → reutiliza y agrega). La pregunta guía es *"¿un Mago **es un** Personaje?"* → herencia.
## | Necesito | Sintaxis |
# |---|---|
# | Heredar | `class Mago(Personaje):` |
# | Extender el `__init__` | `super().__init__(args_del_padre)` **primero**, después `self.propio = ...` |
# | Sobreescribir un método | definirlo de nuevo con el mismo nombre |
# | Extender un método | `super().metodo(args)` dentro del override |
# | ¿Es de esta clase (o hija)? | `isinstance(obj, Personaje)` → `True` también para `Mago` |
# | ¿Es exactamente de esta clase? | `type(obj) is Mago` / `type(obj).__name__ == "Mago"` |
# | ¿Hereda de? | `issubclass(Mago, Personaje)` |
# | ¿Tiene ese atributo/método? | `hasattr(obj, "curar")` |
# | ¿Es de alguna de estas clases? | `isinstance(obj, (Dominante, Codominante))` → la tupla significa "o" |
# | Heredar de un built-in (`list`, `dict`) | `class Equipo(list):` → `self` **es** la lista (`for p in self`, `self.append`, `len(self)`) |

# %% ---------------------------------------------------------
class Personaje:
    def __init__(self, nombre, vida):
        self.nombre = nombre
        self.vida = vida

    def atacar(self, otro):
        print(f"{self.nombre} ataca a {otro.nombre}")
        otro.vida -= 10

    def __str__(self):
        return f"{type(self).__name__} {self.nombre} ({self.vida} de vida)"


class Mago(Personaje):                          # Mago ES UN Personaje
    def __init__(self, nombre, vida, mana):
        super().__init__(nombre, vida)          # 1° lo del padre (crea nombre y vida)
        self.mana = mana                        # 2° lo propio

    def atacar(self, otro):                     # EXTENDER: hace lo del padre y algo más
        super().atacar(otro)
        self.mana -= 5
        print(f"   (a {self.nombre} le queda {self.mana} de maná)")

    def curar(self):                            # método NUEVO: solo lo tiene Mago
        self.vida += 20


class Guerrero(Personaje):                      # no redefine __init__: usa el del padre tal cual
    def atacar(self, otro):                     # SOBREESCRIBIR: reemplaza por completo
        print(f"{self.nombre} golpea fuerte a {otro.nombre}")
        otro.vida -= 25


m = Mago("Merlín", 100, 50)
g = Guerrero("Conan", 150)
m.atacar(g)
g.atacar(m)
print(m, "|", g)
print(isinstance(m, Personaje), isinstance(m, Guerrero), isinstance(g, Mago))   # True False False
print(issubclass(Mago, Personaje), type(m).__name__, hasattr(g, "curar"))       # True Mago False


class Equipo(list):                             # hereda de un built-in: ya tiene append, len, in, [i], for
    def __init__(self, nombre, *args):
        super().__init__(*args)                 # list acepta un iterable inicial
        self.nombre = nombre

    def vivos(self):
        return [p for p in self if p.vida > 0]  # 'self' ES la lista

    def mas_fuerte(self):
        return max(self, key=lambda p: p.vida)


equipo = Equipo("Aventureros", [m, g])
equipo.append(Guerrero("Ares", 0))
print(len(equipo), [p.nombre for p in equipo.vivos()], equipo.mas_fuerte().nombre, isinstance(equipo, list))

# %% [markdown]
# ## 2. Polimorfismo y métodos "mágicos" (`__str__`, `__add__`, `__eq__`, `__lt__`…)
## **Polimorfismo** = la misma llamada (`obj.atacar(x)`) hace algo distinto según la clase del objeto. Con una lista de objetos
# de distintas clases basta con `for p in lista: p.atacar(x)`; **no** hace falta `if isinstance(...)` si todos tienen el método (*duck typing*).
## | Quiero que funcione… | Defino en la clase | Debe retornar |
# |---|---|---|
# | `print(obj)`, `str(obj)`, `f"{obj}"` | `__str__(self)` | `str` |
# | `print(lista_de_objs)`, consola | `__repr__(self)` (si no hay `__str__`, `print` también lo usa) | `str` |
# | `a + b`, `a - b`, `a * 3` | `__add__(self, otro)`, `__sub__`, `__mul__` | un objeto **nuevo** (no modificar `self`) |
# | `a == b` | `__eq__(self, otro)` | `bool` |
# | `a < b`, `sorted(lista)`, `min`, `max` | `__lt__(self, otro)` (y `__gt__` si piden `>`) | `bool` |
# | `len(obj)` | `__len__(self)` | `int` |
# | `x in obj` | `__contains__(self, x)` | `bool` |
# | `obj[i]` | `__getitem__(self, i)` | el elemento |
# | `if obj:` | `__bool__(self)` | `bool` |
## ⚠️ **No existe *overloading***: si en la misma clase escribo `def m(self, a)` y más abajo `def m(self, a, b)`, solo sobrevive el **último** (sin aviso).
# Para variar argumentos: valores por defecto `def m(self, a, b=None)` o `*args`. Cuidado con el copy-paste que deja dos `__init__`.
# ⚠️ Si defino `__eq__`, el objeto deja de ser *hasheable* (no puede ir en `set` ni ser clave de `dict`) salvo que también defina `__hash__`.

# %% ---------------------------------------------------------
class Dinero:
    def __init__(self, monto, moneda="CLP"):
        self.monto = monto
        self.moneda = moneda

    def __str__(self):                       # print(d)  /  f"{d}"
        return f"${self.monto:,} {self.moneda}"

    def __repr__(self):                      # dentro de listas/dicts y en la consola
        return f"Dinero({self.monto})"

    def __add__(self, otro):                 # d1 + d2 -> objeto NUEVO
        return Dinero(self.monto + otro.monto, self.moneda)

    def __sub__(self, otro):
        return Dinero(self.monto - otro.monto, self.moneda)

    def __mul__(self, numero):               # d * 3
        return Dinero(self.monto * numero, self.moneda)

    def __eq__(self, otro):                  # d1 == d2
        return isinstance(otro, Dinero) and self.monto == otro.monto

    def __hash__(self):                      # necesario si defino __eq__ y quiero usar set / clave de dict
        return hash((self.monto, self.moneda))

    def __lt__(self, otro):                  # d1 < d2  -> habilita sorted / min / max
        return self.monto < otro.monto

    def __bool__(self):                      # if d:  -> False cuando el monto es 0
        return self.monto != 0


class Billetera:
    def __init__(self):
        self.billetes = []

    def __len__(self):                       # len(b)
        return len(self.billetes)

    def __contains__(self, dinero):          # dinero in b   (usa __eq__)
        return dinero in self.billetes

    def __getitem__(self, i):                # b[0]
        return self.billetes[i]


a, b = Dinero(1000), Dinero(2500)
print(a + b, "|", b - a, "|", a * 3)                      # $3,500 CLP | $1,500 CLP | $3,000 CLP
print(a == Dinero(1000), a < b, sorted([b, a]), max(a, b))   # True True [Dinero(1000), Dinero(2500)] $2,500 CLP
#                                       (dentro de la lista se usa __repr__; el objeto suelto en print usa __str__)
w = Billetera()
w.billetes += [a, b]
print(len(w), Dinero(2500) in w, w[1], bool(Dinero(0)))    # 2 True $2,500 CLP False
print(len({a, Dinero(1000), b}))                            # 2 (gracias a __eq__ + __hash__)

# Polimorfismo: misma llamada, cada objeto responde a su manera
# (requiere haber corrido la celda de la sección 1: usa Mago, Guerrero y g)
for p in [Mago("Gandalf", 80, 30), Guerrero("Xena", 120)]:
    p.atacar(g)                              # no necesito saber de qué clase es p

# Ordenar objetos SIN __lt__: con key
personajes = [Mago("Gandalf", 80, 30), Guerrero("Xena", 120), g]
print([p.nombre for p in sorted(personajes, key=lambda p: p.vida, reverse=True)])

# %% [markdown]
# ## 3. Multiherencia: `class C(A, B)` + `**kwargs` + MRO
## Reglas (si no se cumplen, aparece un `TypeError` en el `__init__`):
## 1. **Todos** los `__init__` de la cadena reciben `**kwargs` y llaman **una sola vez** `super().__init__(**kwargs)`.
#    Si el enunciado o `bases.py` dan la firma con `*args, **kwargs`, copiar esa forma tal cual: `def __init__(self, propio, *args, **kwargs): super().__init__(*args, **kwargs)`.
# 2. Cada clase **saca por nombre** sus parámetros y **manda el resto** hacia arriba.
# 3. Se instancia **por keyword**: `Pato(nombre="D", altura_max=100, ...)`.
# 4. `C.__mro__` (o `C.mro()`) = orden en que Python busca métodos: `C, A, (padres de A), B, (padres de B), object`.
#    Si `A` y `B` tienen el mismo método, **gana el primero de izquierda a derecha**.
# 5. Para usar la versión de una clase específica (saltándose el MRO): `A.metodo(self, ...)`.
# 6. **Diamante** (`A` y `B` heredan de la misma base): con `super()` en toda la cadena la base corre **una** vez. Con llamadas directas
#    `A.m(self); B.m(self)` desde `C(A, B)`: si `A.m` usa `super().m()`, ese `super()` salta a `B.m` (el siguiente en el MRO de `C`) → se ejecuta
#    A, B, Base, B, Base (la base **y B** corren dos veces). Las llamadas explícitas `Padre.m(self)` solo son seguras si los padres **no** llaman `super()` en ese método (como `recorrer` en Vehículos, sección 9).
# 7. Una clase "mixin" (ej. `Mutable`) es una clase pequeña **sin base común** que agrega comportamiento: igual usa `**kwargs` + `super().__init__(**kwargs)` y se pone en la lista de padres (ejemplo `Ruidoso` abajo).
# 8. Orden de los padres: de la **más específica a la más general**. `class X(Gen, Dominante)` (padre antes que su hija) da `TypeError: Cannot create a consistent method resolution order (MRO)`.

# %% ---------------------------------------------------------
class Ser:                                        # base común -> diamante
    def __init__(self, nombre, **kwargs):
        super().__init__(**kwargs)                # llega a object: kwargs debe venir VACÍO
        self.nombre = nombre

    def presentarse(self):
        return f"Soy {self.nombre}"


class Volador(Ser):
    def __init__(self, altura_max, **kwargs):     # saco lo mío, mando el resto
        super().__init__(**kwargs)
        self.altura_max = altura_max

    def moverse(self):
        return f"{self.nombre} vuela hasta {self.altura_max} m"


class Nadador(Ser):
    def __init__(self, profundidad_max, **kwargs):
        super().__init__(**kwargs)
        self.profundidad_max = profundidad_max

    def moverse(self):
        return f"{self.nombre} nada hasta {self.profundidad_max} m"


class Pato(Volador, Nadador):                     # MRO: Pato, Volador, Nadador, Ser, object
    def __init__(self, sonido, **kwargs):
        super().__init__(**kwargs)                # UNA llamada recorre toda la cadena
        self.sonido = sonido

    def moverse(self):                            # combino las dos versiones a mano
        return Volador.moverse(self) + " y " + Nadador.moverse(self)


p = Pato(nombre="Donald", altura_max=100, profundidad_max=3, sonido="cuac")   # SIEMPRE por keyword
print([c.__name__ for c in Pato.__mro__])
print(p.presentarse(), "|", p.moverse())
print(super(Pato, p).moverse())                   # "el siguiente después de Pato en el MRO" -> Volador


class Cisne(Volador, Nadador):                    # sin redefinir moverse: gana Volador (primero de la lista)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


print(Cisne(nombre="Blanco", altura_max=50, profundidad_max=1).moverse())


# --- MIXIN sin base común (estilo Mutable 2026-1): igual, **kwargs y UNA llamada a super ---
class Ruidoso:                                    # no hereda de Ser
    def __init__(self, volumen, **kwargs):
        super().__init__(**kwargs)                # sigue el MRO: llega a la siguiente clase o a object
        self.volumen = volumen

    def gritar(self):
        return f"{self.nombre} grita a {self.volumen} dB"   # usa atributos que pone OTRA clase del MRO


class PatoRuidoso(Pato, Ruidoso):                 # MRO: PatoRuidoso, Pato, Volador, Nadador, Ser, Ruidoso, object
    def __init__(self, **kwargs):
        super().__init__(**kwargs)                # UNA sola llamada


print(PatoRuidoso(nombre="Lucas", altura_max=5, profundidad_max=1, sonido="cuac", volumen=90).gritar())

# %% ---------------------------------------------------------
# --- Qué pasa cuando NO se usa **kwargs (para reconocer el error) ---
class A:
    def __init__(self, x):
        self.x = x

class B:
    def __init__(self, y):
        self.y = y

class C(A, B):
    def __init__(self, x, y):
        super().__init__(x)          # solo corre A.__init__ ; B.__init__ NUNCA se ejecuta
        # arreglo: A y B con **kwargs y super().__init__(**kwargs); acá super().__init__(x=x, y=y)

c = C(1, 2)
print("¿c tiene y?", hasattr(c, "y"))              # False

try:
    Pato("Donald", 100, 3, "cuac")                # posicional en una clase con **kwargs
except TypeError as e:
    print("TypeError:", e)                        # takes 2 positional arguments but 5 were given

try:
    Pato(nombre="D", altura_max=1, profundidad_max=1, sonido="c", color="blanco")
except TypeError as e:
    print("TypeError:", e)                        # object.__init__() takes exactly one argument -> sobró 'color'

# %% [markdown]
# ## 4. Clases abstractas (`ABC` + `@abstractmethod`): "abstracta", "no se puede instanciar", "debe ser implementado por las subclases"
## - `from abc import ABC, abstractmethod`. La clase hereda de `ABC`; cada método obligatorio lleva `@abstractmethod` encima.
# - **No se puede instanciar** la abstracta ni una hija que no implemente **todos** los abstractos → `TypeError: Can't instantiate abstract class ...`.
# - Un método abstracto **puede tener código**: la hija lo reutiliza con `super().metodo()` (igual debe redefinirlo).
# - Los métodos normales de la abstracta se heredan tal cual (ahí va la lógica común: `simular`, `__str__`, etc.).
# - También puede ser abstracta una property: `@property` y debajo `@abstractmethod`.
# - `@abstractmethod` sobre `__init__` (aparece en el apunte, ej. `Figura`): la hija está **obligada** a escribir su propio `__init__` (normalmente `super().__init__(...)` + lo suyo).
# - "hereda de ABC" a secas ≠ "no se puede instanciar": solo poner `@abstractmethod` si el enunciado dice que el método es abstracto / que la clase no se instancia (en 2025-1 los tests instanciaban la base).
## **Esqueleto mínimo (el 90 % de los casos):**
# ```python
# from abc import ABC, abstractmethod
## class Base(ABC):
#     def __init__(self, x, **kwargs):
#         super().__init__(**kwargs)
#         self.x = x
##     @abstractmethod
#     def accion(self):          # "debe ser implementado por las subclases"
#         pass
## class Hija(Base):
#     def accion(self):          # mismo nombre y mismos argumentos
#         return f"{self.x} en acción"
# ```

# %% ---------------------------------------------------------
from abc import ABC, abstractmethod


class Figura(ABC):                                # abstracta: NO se instancia
    def __init__(self, nombre, **kwargs):
        super().__init__(**kwargs)
        self.nombre = nombre

    @abstractmethod
    def area(self):                               # cada hija DEBE definirlo
        pass

    @abstractmethod
    def describir(self):                          # abstracto PERO con código reutilizable
        return f"{self.nombre} de área {self.area():.1f}"

    def es_grande(self):                          # método concreto: se hereda tal cual
        return self.area() > 50

    @property
    @abstractmethod
    def lados(self):                              # property abstracta
        pass


class Cuadrado(Figura):
    def __init__(self, lado, **kwargs):
        super().__init__(nombre="Cuadrado", **kwargs)
        self.lado = lado

    def area(self):
        return self.lado ** 2

    def describir(self):
        return super().describir() + " (todos sus lados iguales)"   # reutiliza el abstracto

    @property
    def lados(self):
        return 4


class Circulo(Figura):
    def __init__(self, radio, **kwargs):
        super().__init__(nombre="Círculo", **kwargs)
        self.radio = radio

    def area(self):
        return 3.1416 * self.radio ** 2

    def describir(self):
        return super().describir()

    @property
    def lados(self):
        return 0


for f in [Cuadrado(lado=3), Circulo(radio=5)]:    # polimorfismo: misma llamada, distinto cálculo
    print(f.describir(), "| grande:", f.es_grande(), "| lados:", f.lados)

try:
    Figura(nombre="x")
except TypeError as e:
    print("TypeError:", e)      # py<=3.11: Can't instantiate abstract class Figura with abstract methods area, describir, lados
                                # py>=3.12: ...Figura without an implementation for abstract methods 'area', 'describir', 'lados'


class Triangulo(Figura):                          # olvidé 'describir' y 'lados'
    def area(self):
        return 1

try:
    Triangulo(nombre="t")
except TypeError as e:
    print("TypeError:", e)      # ...abstract methods describir, lados  -> me dice exactamente qué falta


class Molde(ABC):
    @abstractmethod
    def __init__(self, nombre):               # __init__ abstracto: la hija DEBE definir el suyo
        self.nombre = nombre


class SinInit(Molde):
    pass


class ConInit(Molde):
    def __init__(self, nombre):
        super().__init__(nombre)              # puede reutilizar el cuerpo del abstracto


try:
    SinInit("a")
except TypeError as e:
    print("TypeError:", e)                    # ...abstract method '__init__'
print(ConInit("b").nombre)                    # b

# %% [markdown]
# ## 5. Properties (`@property` + `@x.setter`): "no puede ser negativa", "acotada entre", "solo lectura", "atributo calculado", "se valida al asignar"
## Un atributo que por fuera se lee/asigna como `obj.x`, pero por detrás pasa por un método: sirve para **validar**, **calcular** o **avisar**.
## | Quiero | Escribo |
# |---|---|
# | Atributo interno | `self._x = valor` (el `_` marca "no tocar desde afuera") |
# | Getter (al **leer** `obj.x`) | `@property` sobre `def x(self): return self._x` |
# | Setter (al **asignar** `obj.x = v`, incluye `obj.x += 1`) | `@x.setter` sobre `def x(self, v): ...` |
# | Solo lectura / calculado | solo el getter (asignar lanza `AttributeError`) |
# | Validar en el `__init__` también | crear `self._x = valor_seguro` y luego `self.x = valor` (pasa por el setter) |
# | Property abstracta | `@property` y debajo `@abstractmethod` (sección 4) |
# | Deleter (al hacer `del obj.x`) | `@x.deleter` sobre `def x(self): del self._x` |
# | Forma sin decoradores | `x = property(_get_x, _set_x, _del_x)` |
## ⚠️ Dentro del getter/setter usar **`self._x`**, nunca `self.x` (eso vuelve a llamar la property → `RecursionError`).
# ⚠️ Si la hija quiere cambiar **solo el setter**: `@Padre.x.setter` sobre `def x(self, v)` (reutiliza el getter del padre, ejemplo `ArtistaPop`).
# Si quiere cambiar el **getter**: redefine `@property def x` (y `@x.setter` si necesita setter), ejemplo `ArtistaRock`.

# %% ---------------------------------------------------------
# PLANTILLA setter: variantes según el enunciado
# ("no puede ser negativa", "queda en 0", "acotada entre 0 y 100", "si es inválido se ignora", "lanza ValueError")
class Plantilla:
    def __init__(self, energia):
        self._energia = 0              # SIEMPRE crear self._x antes de usar self.x
        self.energia = energia         # pasa por el setter

    @property
    def energia(self):
        return self._energia

    @energia.setter
    def energia(self, valor):
        # 1) "no puede ser negativa (queda en 0)":
        self._energia = max(0, valor)
        # 2) "acotada entre 0 y 100":          self._energia = max(0, min(100, valor))
        # 3) "si es inválido se ignora":        if valor < 0: return  →  else: self._energia = valor
        # 4) "se redondea a 1 decimal":         self._energia = round(float(valor), 1)
        # 5) "lanza ValueError si es negativo": if valor < 0: raise ValueError("energía negativa")


p = Plantilla(-5)
print(p.energia)                       # 0
try:
    raise ValueError("energía negativa")   # así se ve la variante 5 desde afuera
except ValueError as e:
    print("ValueError:", e)

# %% ---------------------------------------------------------
class Cuenta:
    def __init__(self, dueno, saldo):
        self.dueno = dueno
        self._saldo = 0                # atributo REAL. Existe antes de pasar por el setter
        self.saldo = saldo             # esta asignación usa el setter -> se valida

    @property                          # GETTER: se ejecuta al LEER cuenta.saldo
    def saldo(self):
        return self._saldo

    @saldo.setter                      # SETTER: se ejecuta al ASIGNAR cuenta.saldo = x
    def saldo(self, valor):
        if valor < 0:
            print(f"Saldo inválido ({valor}); se mantiene en {self._saldo}")
        else:
            self._saldo = valor

    @property                          # SOLO LECTURA (calculado): no tiene setter
    def saldo_usd(self):
        return round(self._saldo / 950, 2)


c = Cuenta("Feli", 10000)
c.saldo += 5000                        # lee con el getter, asigna con el setter
c.saldo = -1                           # rechazado
print(c.saldo, c.saldo_usd)            # 15000 15.79
try:
    c.saldo_usd = 3
except AttributeError as e:
    print("AttributeError:", e)        # py>=3.11: property 'saldo_usd' of 'Cuenta' object has no setter | py3.10: can't set attribute 'saldo_usd'


class Arquero:                         # estilo AY03: setter con tope y mensaje, getter con "estado"
    def __init__(self, apellido, porc_atajadas):
        self.apellido = apellido
        self._porc_atajadas = porc_atajadas
        self.on_fire = False

    @property
    def porc_atajadas(self):
        if self.on_fire:               # el getter puede devolver un valor "modificado"
            return round(self._porc_atajadas + 0.2, 2)
        return self._porc_atajadas

    @porc_atajadas.setter
    def porc_atajadas(self, nuevo):
        nuevo = round(nuevo, 2)        # OJO floats: 0.65 + 0.05 = 0.7000000000000001 (> 0.7). Redondear ANTES de comparar
        if nuevo <= 0.7:
            self._porc_atajadas = nuevo
            print(f"{self.apellido} sube su porcentaje a {self._porc_atajadas}")
        else:
            print(f"{self.apellido} no puede subir más su porcentaje!")


bravo = Arquero("Bravo", 0.65)
bravo.porc_atajadas += 0.05            # 0.70 -> sube
bravo.porc_atajadas += 0.05            # 0.75 -> rechazado
bravo.on_fire = True
print(bravo.porc_atajadas)             # 0.9 (0.7 + 0.2)

# %% ---------------------------------------------------------
# --- Property en el padre, SOBREESCRITA en la hija (estilo Experiencia 1 2025-2, DCCPalooza) ---
class Artista:
    def __init__(self, nombre, afinidad):
        self.nombre = nombre
        self._afinidad = 0
        self.afinidad = afinidad                       # por el setter

    @property
    def afinidad(self):
        return self._afinidad

    @afinidad.setter
    def afinidad(self, valor):
        self._afinidad = max(0, min(100, valor))       # acotada a [0, 100]

    @property
    def animo(self):                                   # calculada
        return self.afinidad / 10


class ArtistaRock(Artista):
    @property                                          # ¡con @property de nuevo! si no, queda como método
    def animo(self):
        valor = super().animo                          # SIN paréntesis: es una property, no un método
        if valor < 5:
            print(f"{self.nombre} peligrando en el concierto. Animo: {valor}")
        return valor


rock = ArtistaRock("Jorge", 130)     # queda en 100
rock.afinidad -= 80                  # 20 -> animo 2.0
print(rock.animo)


class ArtistaPop(Artista):
    @Artista.afinidad.setter         # cambio SOLO el setter; el getter sigue siendo el del padre
    def afinidad(self, valor):
        self._afinidad = max(50, min(100, valor))   # el pop nunca baja de 50


pop = ArtistaPop("Denise", 10)
print(pop.afinidad, pop.animo)       # 50 5.0


class Caja:                          # atributo "privado" con doble guion bajo (name mangling)
    def __init__(self):
        self.__dia = 1               # por fuera se llama _Caja__dia; NO se accede como caja.__dia

    @property
    def dia(self):                   # solo lectura
        return self.__dia

    def nuevo_dia(self):             # se modifica solo desde adentro
        self.__dia += 1


caja = Caja()
caja.nuevo_dia()
print(caja.dia, hasattr(caja, "__dia"), hasattr(caja, "_Caja__dia"))   # 2 False True

# %% [markdown]
# ## 6. Decoradores, `@classmethod`, `@staticmethod`, variables de clase: "contador", "identificador único autoincremental", "verifica antes de ejecutar"
## - **Decorador** = función que recibe una función y retorna otra que la "envuelve". `@deco` sobre `def f` equivale a `f = deco(f)`.
#   El `wrapper` recibe `*args, **kwargs` (así sirve para métodos: `self` viaja en `args`) y **debe retornar** lo que retornó la original.
# - Decorador **con parámetros** (`@repetir(3)`): una capa más (función que retorna el decorador).
# - `@classmethod`: recibe `cls`. Para **constructores alternativos** (`desde_linea`), **registrar** subclases, tocar variables de clase.
# - `@staticmethod`: no recibe `self` ni `cls`; función utilitaria guardada dentro de la clase. Se llama `Clase.f()`.
# - **Variable de clase** (definida bajo `class`, fuera de `__init__`): compartida por todas las instancias. Se modifica con `Clase.x += 1`
#   (con `self.x += 1` se crea una copia de instancia y el contador global no cambia).
# - ⚠️ Nunca poner una **lista/dict como variable de clase** para datos por instancia: todas las instancias compartirían la misma lista. Crearla en `__init__`.

# %% ---------------------------------------------------------
from functools import wraps


def registrar_llamada(func):                 # decorador simple: recibe la función y retorna otra
    @wraps(func)                             # conserva nombre y docstring de la original (opcional)
    def wrapper(*args, **kwargs):            # acepta cualquier argumento (incluido self)
        print(f"-> llamando {func.__name__}{args[1:]}")
        resultado = func(*args, **kwargs)    # ejecuta la original
        print(f"<- {func.__name__} retornó {resultado}")
        return resultado                     # ¡no olvidar el return!
    return wrapper


def repetir(veces):                          # decorador CON parámetros: una capa más
    def decorador(func):
        def wrapper(*args, **kwargs):
            resultado = None
            for _ in range(veces):
                resultado = func(*args, **kwargs)
            return resultado
        return wrapper
    return decorador


def requiere_energia(func):                  # decorador que MIRA self antes de ejecutar ("verifica antes", "solo si")
    def wrapper(self, *args, **kwargs):      # el 1er argumento de un método SIEMPRE es self
        if self.velocidad <= 0:
            print(f"{self.nombre} no puede: sin velocidad")
            return None                      # el enunciado dice qué retornar en ese caso
        return func(self, *args, **kwargs)   # ejecuta el método original
    return wrapper


class Robot:
    creados = 0                              # variable de CLASE: compartida por todos
    VELOCIDAD_MAX = 10                       # "constante" de clase

    def __init__(self, nombre, velocidad):
        self.nombre = nombre                 # variable de INSTANCIA
        self.velocidad = min(velocidad, self.VELOCIDAD_MAX)   # leer una de clase con self está OK
        self.id = Robot.creados              # IDENTIFICADOR ÚNICO autoincremental: 0, 1, 2, ...
        Robot.creados += 1                   # escribirla: Robot.creados (NO self.creados)
        self.tareas = []                     # lista por instancia -> va en __init__, no en la clase

    @classmethod                             # recibe la clase (cls), no la instancia
    def desde_linea(cls, linea):             # constructor alternativo: "R2D2,7"
        nombre, velocidad = linea.strip().split(",")
        return cls(nombre, int(velocidad))   # cls -> funciona también para subclases

    @staticmethod                            # sin self ni cls
    def es_valida(velocidad):
        return 0 <= velocidad <= Robot.VELOCIDAD_MAX

    @registrar_llamada
    def avanzar(self, metros):
        return metros / self.velocidad

    @repetir(3)
    def saludar(self):
        print(f"beep, soy {self.nombre}")

    @requiere_energia
    def retroceder(self, metros):
        return -metros / self.velocidad

    def __repr__(self):
        return f"Robot({self.nombre})"


r = Robot.desde_linea("R2D2,7\n")
r2 = Robot("C3PO", 99)
print(Robot.creados, r.id, r2.id, Robot.es_valida(99), r2.velocidad)    # 2 0 1 False 10
print(r.avanzar(21))
r.saludar()
print(r.retroceder(14), Robot("Wall-E", 0).retroceder(5))               # -2.0 | mensaje y None
r.tareas.append("limpiar")
print(r.tareas, r2.tareas)                                # ['limpiar'] []  (listas separadas)

# %% [markdown]
# ## 7. Diagrama de clases → código
## | En el diagrama | Significa | En código |
# |---|---|---|
# | Caja con 3 partes: nombre / atributos / métodos | una clase. `+` público, `-` privado (`_x`), `#` protegido | `class Nombre:` |
# | *Nombre en cursiva* o `«abstract»` / método en cursiva | clase o método abstracto | `ABC` + `@abstractmethod` |
# | Atributo/método <u>subrayado</u> | de clase (no de instancia) | variable de clase / `@classmethod` |
# | `+ metodo(str, int): bool` | recibe un str y un int, retorna bool | `def metodo(self, a, b): return ...` |
# | `+ __init__(str, str, **kwargs)` | inicializador que reenvía kwargs (multiherencia) | `super().__init__(**kwargs)` |
# | Flecha con **triángulo hueco** apuntando al padre | **herencia** ("es un") | `class Hija(Padre)` |
# | Línea con **rombo relleno** en el "todo" | **composición** ("tiene", el todo **crea** las partes y sin él no existen) | `self.partes = [Parte(...)]` creadas adentro |
# | Línea con **rombo vacío** en el "todo" | **agregación** ("tiene", las partes existen afuera y se **pasan**) | `def __init__(self, partes): self.partes = partes` |
# | Línea simple | asociación (usa) | recibe el objeto como argumento en un método |
# | `1`, `0..1` en el extremo | un objeto (o ninguno) | `self.dueno = objeto` (o `None`) |
# | `*`, `1..*`, `0..*` | muchos | `list` / `dict` de objetos |
# | Línea punteada con triángulo hueco | implementa una interfaz | igual que herencia de una ABC |
# | `+ @kilometraje: int (getter y setter)` | **property** (convención del curso; si dice solo `getter` es de solo lectura) | `self._kilometraje` en `__init__` + `@property def kilometraje` (+ `@kilometraje.setter`) |
# | `+ _kilometraje: int` (con guion bajo) | atributo interno que respalda la property | `self._kilometraje = km` |
# | `+ dueño: str or None` | atributo que parte vacío | `self.dueño = None` en `__init__` |
# | la caja de la hija **no** repite lo del padre | lo hereda; solo se escriben los atributos/métodos nuevos o sobreescritos | no re-declarar; `super().__init__(...)` los crea |

# %% ---------------------------------------------------------
class Estudiante:                                       # Estudiante ◁── Ayudante  (herencia)
    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return self.nombre


class Ayudante(Estudiante):
    def __init__(self, nombre, curso_ayudado):
        super().__init__(nombre)
        self.curso_ayudado = curso_ayudado


class Curso:                                            # Curso ◇── * Estudiante  (agregación)
    def __init__(self, sigla, estudiantes):             # recibe objetos que ya existían
        self.sigla = sigla
        self.estudiantes = estudiantes                  # cardinalidad * -> lista
        self.ayudante = None                            # cardinalidad 0..1

    def __repr__(self):
        return f"Curso({self.sigla})"


class Universidad:                                      # Universidad ◆── 1..* Curso  (composición)
    def __init__(self, nombre):
        self.nombre = nombre
        self.cursos = {}                                # sigla -> Curso; los crea la universidad

    def abrir_curso(self, sigla, estudiantes):
        self.cursos[sigla] = Curso(sigla, estudiantes)  # la parte nace dentro del todo
        return self.cursos[sigla]


uc = Universidad("UC")
curso = uc.abrir_curso("IIC2233", [Estudiante("Feli"), Estudiante("Cami")])
curso.ayudante = Ayudante("Josefa", curso)
print(uc.cursos, curso.estudiantes, curso.ayudante)

# %% [markdown]
# ## 8. Problema tipo A — "completa los métodos de estas subclases" (estilo AC3 2026-1)
## **Enunciado resumido (AC3 2026-1, *Genes de perro*):** `bases.py` (No modificar) trae `Gen(ABC)` con `rasgo`, `valor`, un
# `REGISTRO` de subclases (`@classmethod registrar`), `__add__` abstracto y `__repr__`; `Mutable(ABC)` (mixin con `get_probabilidades_mutar`
# abstracto) y `ParDeGenes(gen1, gen2, fenotipo)`. **Parte 1:** completar `__add__` en `Dominante`, `Recesivo` y `Codominante`
# (retornan `ParDeGenes` con el fenotipo según reglas; usar `isinstance`). **Parte 2:** hacer que `OjosCafes` herede de `Dominante` **y**
# `Mutable` e implemente `get_probabilidades_mutar`. Se corrige con `tests_publicos/` (`unittest`).
## Lo que se evalúa: leer una clase base ya hecha, implementar un operador (`__add__`) que **retorna un objeto nuevo**, decidir con
# `isinstance`, multiherencia con `**kwargs` (una sola llamada a `super`) y clases abstractas. Abajo: primero lo que **me dan** (solo leer), luego lo que **escribo**.
# `REGISTRO` guarda **clases**, no objetos: `Gen.REGISTRO["pelo"]["Negro"]` es la clase `PeloNegro`; para crear el gen se llama: `Gen.REGISTRO["pelo"]["Negro"]()`.
# Lo mismo con cualquier dict `tipo -> Clase`: `clases[tipo](**datos)`.
## **`bases.py` — NO se toca, solo leer (qué me da):**

# %% ---------------------------------------------------------
from abc import ABC, abstractmethod
import random

# ---------- "bases.py" (No modificar: solo hay que LEERLO y entender qué me da) ----------
class Gen(ABC):
    REGISTRO = {}                                   # rasgo -> {valor -> clase}

    def __init__(self, rasgo, valor, **kwargs):
        super().__init__(**kwargs)                  # permite multiherencia (Dominante + Mutable)
        self.rasgo = rasgo
        self.valor = valor

    @classmethod
    def registrar(cls, subclase):                   # Gen.registrar(PeloNegro)
        instancia = subclase()
        cls.REGISTRO.setdefault(instancia.rasgo, {})[instancia.valor] = subclase

    @abstractmethod
    def __add__(self, other):                       # gen1 + gen2 -> ParDeGenes
        pass

    def __repr__(self):
        return self.valor


class Mutable(ABC):                                 # mixin: agrega "mutar" a cualquier Gen
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.probabilidades_mutar = self.get_probabilidades_mutar()

    def mutar_random(self):
        valores = [valor for valor, _ in self.probabilidades_mutar]
        pesos = [prob for _, prob in self.probabilidades_mutar]
        return random.choices(valores, weights=pesos)[0]

    @abstractmethod
    def get_probabilidades_mutar(self):
        pass


class ParDeGenes:
    def __init__(self, gen1, gen2, fenotipo):
        self.par_de_genes = (gen1, gen2)
        self.rasgo = gen1.rasgo
        self.fenotipo = fenotipo

    def elegir_alelo_aleatorio(self):
        gen = random.choice(self.par_de_genes)
        if isinstance(gen, Mutable):                # solo los mutables pueden mutar
            return Gen.REGISTRO[gen.rasgo][gen.mutar_random()]()
        return gen

    def __repr__(self):
        return self.fenotipo

# %% [markdown]
# **LO QUE ESCRIBO — Parte 1 (`dominancia.py`): `__add__` que retorna un `ParDeGenes`.**
# Patrón: `def __add__(self, other):` → decidir con `isinstance(other, Clase)` / `other.valor` → `return ObjetoNuevo(self, other, resultado)`.

# %% ---------------------------------------------------------
class Dominante(Gen):
    def __add__(self, other):
        return ParDeGenes(self, other, self.valor)  # el dominante siempre se expresa


class Recesivo(Gen):
    def __add__(self, other):
        if isinstance(other, Recesivo) and other.valor == self.valor:
            fenotipo = self.valor                   # solo con otra copia igual
        else:
            fenotipo = other.valor
        return ParDeGenes(self, other, fenotipo)


class Codominante(Gen):
    def __add__(self, other):
        if isinstance(other, Dominante):
            fenotipo = other.valor
        elif other.valor == self.valor:
            fenotipo = self.valor
        else:
            fenotipo = f"Mezcla entre {self.valor} y {other.valor}"
        return ParDeGenes(self, other, fenotipo)


print(Dominante(rasgo="ojos", valor="Rojos") + Recesivo(rasgo="ojos", valor="Verdes"))   # Rojos

# %% [markdown]
# **LO QUE ESCRIBO — Parte 2 (`caracteristicas.py`): multiherencia `class OjosCafes(Dominante, Mutable)` con una sola llamada a `super`.**

# %% ---------------------------------------------------------
class PeloNegro(Dominante):
    def __init__(self):
        super().__init__(rasgo="pelo", valor="Negro")

class PeloBlanco(Recesivo):
    def __init__(self):
        super().__init__(rasgo="pelo", valor="Blanco")

class OjosAzules(Codominante):
    def __init__(self):
        super().__init__(rasgo="ojos", valor="Azules")

class OjosVerdes(Codominante):
    def __init__(self):
        super().__init__(rasgo="ojos", valor="Verdes")

class OjosCafes(Dominante, Mutable):                # multiherencia: dominante Y mutable
    def __init__(self):
        super().__init__(rasgo="ojos", valor="Cafes")   # UNA llamada: Dominante -> Gen -> Mutable

    def get_probabilidades_mutar(self):             # obligatorio por Mutable
        return [("Cafes", 0.7), ("Verdes", 0.1), ("Azules", 0.2)]


for clase in (PeloNegro, PeloBlanco, OjosAzules, OjosVerdes, OjosCafes):
    Gen.registrar(clase)

print(PeloNegro() + PeloBlanco(), "|", PeloBlanco() + PeloBlanco(), "|", OjosVerdes() + OjosAzules())
print([c.__name__ for c in OjosCafes.__mro__])
par = OjosCafes() + OjosCafes()
print(sorted(str(par.elegir_alelo_aleatorio()) for _ in range(8)))     # mayoría Cafes, algunos mutan

# %% [markdown]
# **Probar como lo hacen los tests.** Si la AC trae `tests_publicos/`, se corren desde la terminal (comandos del inicio). Si no trae,
# escribo mis propios `assert` o un test rápido como este (mismo formato que los del curso: `assertEqual`, `assertIsInstance`, `assertTrue`):

# %% ---------------------------------------------------------
import unittest
from unittest.mock import patch


class TestDominancia(unittest.TestCase):
    def test_dominante_recesivo(self):
        par = PeloBlanco() + PeloNegro()
        self.assertIsInstance(par, ParDeGenes)
        self.assertEqual(par.fenotipo, "Negro")

    def test_codominantes_distintos(self):        # assertIn: acepta cualquiera de las opciones
        self.assertIn((OjosVerdes() + OjosAzules()).fenotipo,
                      ["Mezcla entre Verdes y Azules", "Mezcla entre Azules y Verdes"])

    def test_probabilidades(self):                # assertCountEqual: mismos elementos, CUALQUIER orden
        self.assertCountEqual(OjosCafes().get_probabilidades_mutar(),
                              [("Verdes", 0.1), ("Azules", 0.2), ("Cafes", 0.7)])

    def test_mutable(self):
        self.assertTrue(isinstance(OjosCafes(), Mutable))
        self.assertFalse(isinstance(OjosAzules(), Mutable))

    def test_abstracta(self):                     # assertRaises: "no se puede instanciar"
        with self.assertRaises(TypeError):
            Gen(rasgo="x", valor="y")

    def test_mutacion_forzada(self):              # patch: reemplaza el azar por un valor fijo
        with patch("random.choice", return_value=OjosCafes()):        # se parcha DONDE SE USA la función
            with patch("random.choices", return_value=["Verdes"]):
                gen = (OjosCafes() + OjosCafes()).elegir_alelo_aleatorio()
        self.assertEqual(gen.valor, "Verdes")


suite = unittest.TestLoader().loadTestsFromTestCase(TestDominancia)
unittest.TextTestRunner(verbosity=2).run(suite)

# versión mínima sin unittest:
assert (PeloBlanco() + PeloNegro()).fenotipo == "Negro", "falló dominante+recesivo"
print("asserts OK")

# %% [markdown]
# ## 9. Problema tipo B — "Vehículos" (la AC de OOP avanzado de 2023-2, 2024-1, 2024-2 y 2025-1)
## **Enunciado resumido:** `clases.py` viene con las 6 clases vacías (`pass`) y **sin la herencia escrita**; hay que agregarla según el diagrama.
# - `Vehiculo` (abstracta): variable de clase `identificador` (el primero es 0, el segundo 1…). `__init__(self, rendimiento, marca, energia=111.5, *args, **kwargs)`.
#   Property `energia` con setter que **no permite negativos** (queda en 0) y redondea a 1 decimal; property `autonomia = energia * rendimiento` (solo lectura). `recorrer(kilometros)` abstracto.
# - `AutoBencina(Vehiculo)`: agrega `bencina_favorita`. `recorrer`: recorre `min(km, autonomia)`, gasta `km/rendimiento` (1 decimal) y retorna `"Anduve {N}Km y eso consume {Z}L de bencina"`.
# - `AutoElectrico(Vehiculo)`: agrega `vida_util_bateria`; igual pero `"...{Z}W de energia electrica"`.
# - `Camioneta(AutoBencina)`: agrega `capacidad_maleta`. `Telsa(AutoElectrico)`: `recorrer` = el del padre + `" de forma muy inteligente"`.
# - `FaitHibrido(AutoBencina, AutoElectrico)`: **todos** tienen `vida_util_bateria = 5` (no se recibe). `recorrer`: si `km > 10` recorre 10 como bencina y el resto como eléctrico y une ambos textos con un espacio; si no, solo como eléctrico.
# - Los tests revisan: `TypeError` al instanciar `Vehiculo`, `energia`/`autonomia` son `property`, `Vehiculo.__init__` se llama **una sola vez** al crear un `FaitHibrido`, y que `FaitHibrido.recorrer` llame `AutoBencina.recorrer(self, 10.0)` y `AutoElectrico.recorrer(self, 5.0)`.

# %% ---------------------------------------------------------
from abc import ABC, abstractmethod


class Vehiculo(ABC):
    identificador = 0                                     # contador de CLASE

    def __init__(self, rendimiento, marca, energia=111.5, *args, **kwargs):
        super().__init__(*args, **kwargs)                 # (opcional aquí: Vehiculo es la raíz)
        self.rendimiento = rendimiento
        self.marca = marca
        self._energia = 0.0
        self.energia = energia                            # pasa por el setter (acota y redondea)
        self.identificador = Vehiculo.identificador       # atributo de INSTANCIA (mismo nombre que el de clase: lo tapa, es normal)
        Vehiculo.identificador += 1                       # incremento SIEMPRE con Clase.x, nunca self.x

    @property
    def autonomia(self):                                  # solo lectura, calculada
        return float(self.energia * self.rendimiento)

    @property
    def energia(self):
        return self._energia

    @energia.setter
    def energia(self, valor):
        self._energia = round(float(max(valor, 0)), 1)    # nunca negativa, 1 decimal

    @abstractmethod
    def recorrer(self, kilometros):
        pass


class AutoBencina(Vehiculo):
    def __init__(self, bencina_favorita, *args, **kwargs):
        super().__init__(*args, **kwargs)                 # lo mío por nombre, el resto sube
        self.bencina_favorita = bencina_favorita

    def recorrer(self, kilometros):
        recorridos = min(kilometros, self.autonomia)
        gasto = round(recorridos / self.rendimiento, 1)
        self.energia -= gasto                             # usa el setter
        return f"Anduve {recorridos}Km y eso consume {gasto}L de bencina"


class AutoElectrico(Vehiculo):
    def __init__(self, vida_util_bateria, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vida_util_bateria = vida_util_bateria

    def recorrer(self, kilometros):
        recorridos = min(kilometros, self.autonomia)
        gasto = round(recorridos / self.rendimiento, 1)
        self.energia -= gasto
        return f"Anduve {recorridos}Km y eso consume {gasto}W de energia electrica"


class Camioneta(AutoBencina):
    def __init__(self, capacidad_maleta, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.capacidad_maleta = capacidad_maleta


class Telsa(AutoElectrico):
    def recorrer(self, kilometros):                       # EXTIENDE el del padre
        return super().recorrer(kilometros) + " de forma muy inteligente"


class FaitHibrido(AutoBencina, AutoElectrico):            # DIAMANTE: ambas suben a Vehiculo
    def __init__(self, *args, **kwargs):
        super().__init__(vida_util_bateria=5, *args, **kwargs)   # inyecto el kwarg que nadie me pasa

    def recorrer(self, kilometros):
        if kilometros > 10.0:
            texto_bencina = AutoBencina.recorrer(self, 10.0)              # llamada EXPLÍCITA a cada padre
            texto_electrico = AutoElectrico.recorrer(self, kilometros - 10.0)
            return texto_bencina + " " + texto_electrico
        return AutoElectrico.recorrer(self, kilometros)


# --- pruebas rápidas (lo que revisan los tests) ---
try:
    Vehiculo(rendimiento=10, marca="x")
except TypeError as e:
    print("OK, no se instancia:", str(e)[:45], "...")

auto = AutoBencina(bencina_favorita=95, rendimiento=10, marca="chev", energia=32.1)   # por keyword
print(auto.identificador, auto.energia, auto.autonomia)     # 0 32.1 321.0
auto.energia = -2200.3
print(auto.energia)                                          # 0.0
print(Camioneta(capacidad_maleta=300, rendimiento=12, marca="ford", bencina_favorita=93).recorrer(1000))
print(Telsa(vida_util_bateria=8, rendimiento=5, marca="telsa", energia=20).recorrer(30))

antes = Vehiculo.identificador
hibrido = FaitHibrido(rendimiento=1, marca="fait", energia=101.2, bencina_favorita=95)
print("Vehiculo.__init__ corrió", Vehiculo.identificador - antes, "vez (debe ser 1); batería:", hibrido.vida_util_bateria)
print(hibrido.recorrer(15.0))
print([c.__name__ for c in FaitHibrido.__mro__])

# %% [markdown]
# ## 10. Problema tipo C — "modela el sistema completo" (jerarquía + ABC + property + polimorfismo + simulación)
## **Enunciado resumido (típico de AC/AY, ej. *Torneo* de la AY03 o *DCCafetería*):** hay una clase base abstracta con atributos comunes
# y un método abstracto; varias subclases con comportamiento propio; una clase que **hereda de dos** de ellas (`**kwargs`); un atributo
# que se **valida** (property con tope); se cargan objetos desde líneas de texto (`tipo,nombre,...`); se **simulan acciones** con
# probabilidad y se imprime un **reporte ordenado**. Abajo: `DCGimnasio`.

# %% ---------------------------------------------------------
from abc import ABC, abstractmethod
from random import random, seed

seed(2233)                                             # solo para que el ejemplo sea reproducible


class Socio(ABC):
    total_socios = 0                                   # contador compartido

    def __init__(self, nombre, energia, **kwargs):
        super().__init__(**kwargs)
        self.nombre = nombre
        self._energia = 0
        self.energia = energia                         # pasa por el setter
        self.sesiones = 0
        Socio.total_socios += 1

    @property
    def energia(self):
        return self._energia

    @energia.setter
    def energia(self, valor):                          # se mantiene entre 0 y 100
        self._energia = max(0, min(100, valor))

    @property
    def cuota(self):                                   # calculado, solo lectura; cada hija define su base
        return self.cuota_base() + 500 * self.sesiones

    @abstractmethod
    def cuota_base(self):
        pass

    @abstractmethod
    def entrenar(self):                                # abstracto con parte común
        self.sesiones += 1
        self.energia -= 30
        print(f"  {self.nombre} entrena (energía: {self.energia})")

    def descansar(self):
        self.energia += 50

    def __lt__(self, otro):                            # para sorted()
        return self.energia < otro.energia

    def __str__(self):
        return f"{type(self).__name__:<12} {self.nombre:<8} energía={self.energia:>3}  cuota=${self.cuota:,}"


class Runner(Socio):
    def __init__(self, km_semana, **kwargs):
        super().__init__(**kwargs)
        self.km_semana = km_semana

    def cuota_base(self):
        return 20000

    def entrenar(self):
        super().entrenar()                             # reutiliza lo común
        self.km_semana += 5


class Levantador(Socio):
    def __init__(self, peso_max, **kwargs):
        super().__init__(**kwargs)
        self.peso_max = peso_max

    def cuota_base(self):
        return 25000

    def entrenar(self):
        super().entrenar()
        if random() <= 0.5:                            # "con probabilidad 50%"
            self.peso_max += 2
            print(f"    {self.nombre} sube a {self.peso_max} kg!")


class Crossfitero(Runner, Levantador):                 # hereda de dos: cuota_base -> gana Runner
    def __init__(self, **kwargs):
        super().__init__(**kwargs)                     # una sola llamada

    def entrenar(self):
        Runner.entrenar(self)   # su super() sigue el MRO → también corre Levantador.entrenar y Socio.entrenar (una vez c/u).
                                # Si NO quiero eso: Socio.entrenar(self) directo y agrego lo mío a mano.

# %% [markdown]
# **Cargar desde texto `tipo,nombre,...` → dict nombre→objeto · simular acciones con casos borde y probabilidad · reporte con `sorted`.**

# %% ---------------------------------------------------------
DATOS = '''tipo,nombre,energia,extra
runner,Ana,80,20
levantador,Beto,60,90
crossfitero,Cami,90,10;70
'''

def cargar_socios(texto):
    socios = {}                                        # nombre -> Socio  (búsqueda directa)
    for linea in texto.strip().splitlines()[1:]:       # [1:] salta el encabezado
        tipo, nombre, energia, extra = linea.strip().split(",")
        if tipo == "runner":
            socio = Runner(nombre=nombre, energia=int(energia), km_semana=int(extra))
        elif tipo == "levantador":
            socio = Levantador(nombre=nombre, energia=int(energia), peso_max=int(extra))
        elif tipo == "crossfitero":
            km, peso = extra.split(";")
            socio = Crossfitero(nombre=nombre, energia=int(energia), km_semana=int(km), peso_max=int(peso))
        else:
            print(f"Tipo desconocido: {tipo}")
            continue
        socios[nombre] = socio
    return socios


def simular(socios, acciones):
    for accion, nombre in acciones:
        if nombre not in socios:                       # caso borde: no existe
            print(f"  No existe el socio {nombre}")
        elif accion == "entrenar" and socios[nombre].energia < 30:
            print(f"  {nombre} está muy cansado")     # caso borde: regla del enunciado
        elif accion == "entrenar":
            socios[nombre].entrenar()
        elif accion == "descansar":
            socios[nombre].descansar()


socios = cargar_socios(DATOS)
simular(socios, [("entrenar", "Ana"), ("entrenar", "Cami"), ("entrenar", "Zoe"), ("descansar", "Beto"), ("entrenar", "Cami")])
print("\nReporte (de menos a más energía):")
for socio in sorted(socios.values()):                  # usa __lt__
    print(" ", socio)
print("Total socios:", Socio.total_socios, "| MRO:", [c.__name__ for c in Crossfitero.__mro__])

# %% [markdown]
# ## 11. Error → causa → arreglo
## | Mensaje (última línea del traceback) | Causa | Arreglo |
# |---|---|---|
# | `NameError: name 'Vehiculo' is not defined` al importar | la hija está definida **antes** que el padre en el archivo | ordenar: padres arriba, hijas abajo |
# | `TypeError: __str__ returned non-string (type NoneType)` | `__str__`/`__repr__` hace `print` en vez de `return` | `return f"..."` |
# | `TypeError: unhashable type: 'X'` (py 3.14: `cannot use 'X' as a set element (unhashable type: 'X')`) al meter objetos en `set`/`dict` | definí `__eq__` sin `__hash__` | agregar `def __hash__(self): return hash(self.id)` |
# | `TypeError: '>=' not supported between instances of 'method' and 'int'` | sobreescribí una property en la hija **sin** volver a poner `@property` | `@property` también en la hija; `super().prop` sin paréntesis |
# | el test dice `TypeError: Can't instantiate...` pero el enunciado instancia la clase base | puse `@abstractmethod` donde no correspondía | "hereda de ABC" a secas ≠ "no se puede instanciar": solo abstracto si lo dicen |
# | `mock.assert_called_once` falla / el identificador salta de 2 en 2 | la base corre dos veces en el diamante (llamé `A.__init__(self)` y `B.__init__(self)`) | `super().__init__(*args, **kwargs)` en toda la cadena, una vez por clase |
# | `TypeError: Can't instantiate abstract class X with abstract methods m` (py ≤3.11) / `...X without an implementation for abstract methods 'm'` (py ≥3.12) | falta implementar `m` en la subclase (o instancié la abstracta) | `def m(self): ...` en la hija con ese nombre exacto |
# | `TypeError: Cannot create a consistent method resolution order (MRO) for bases Gen, Dominante` | puse un padre ANTES que su propia hija en la lista, o dos padres heredan de las mismas bases en distinto orden | ordenar de más específica a más general: `class OjosCafes(Dominante, Mutable)`, nunca `(Gen, Dominante)` |
# | `AttributeError: 'super' object has no attribute 'metodo'` | un padre/mixin llama `super().metodo()` y el siguiente en el MRO es `object` (o no tiene ese método) | combinar versiones llamando cada una explícitamente `A.metodo(self)`; `super()` en cadena solo si todas las clases lo definen |
# | un método "desaparece" o pide argumentos raros | dos `def` con el mismo nombre en la misma clase (copy-paste): Python se queda con el ÚLTIMO sin avisar | borrar el duplicado; para "dos versiones" usar valores por defecto `def m(self, a, b=None)` |
# | `TypeError: X.__init__() got an unexpected keyword argument 'z'` | pasé un keyword que ninguna clase de la cadena recibe (nombre mal escrito) | revisar el nombre del parámetro; las clases intermedias deben tener `**kwargs` |
# | `TypeError: object.__init__() takes exactly one argument` | un kwarg sobró y llegó hasta `object`, o una base sin `**kwargs` recibió kwargs | ver qué argumento sobra; la base debe "consumirlo" |
# | `TypeError: X.__init__() takes 2 positional arguments but 5 were given` | instancié con posicionales una clase con `**kwargs` | instanciar por keyword: `X(a=1, b=2)` |
# | `TypeError: X.__init__() missing 1 required positional argument: 'y'` | faltó un argumento (o `super().__init__()` sin lo que pide el padre) | pasar todo lo que pide cada `__init__` |
# | `AttributeError: 'X' object has no attribute '_y'` | usé la property antes de crear `self._y`, o no llamé `super().__init__` | en `__init__`: primero `super().__init__(...)`, luego `self._y = ...` |
# | `AttributeError: property 'y' of 'X' object has no setter` (py ≥3.11) / `AttributeError: can't set attribute 'y'` (py 3.10) | asigné a una property de solo lectura | agregar `@y.setter` o no asignar |
# | `RecursionError: maximum recursion depth exceeded` | dentro del getter/setter usé `self.y` en vez de `self._y` | usar `self._y` adentro |
# | `TypeError: unsupported operand type(s) for +: 'X' and 'X'` | falta `__add__` | `def __add__(self, otro): return X(...)` |
# | `TypeError: '<' not supported between instances of 'X' and 'X'` | `sorted`/`min`/`max` sobre objetos sin `__lt__` | definir `__lt__` o usar `key=lambda o: o.attr` |
# | el test dice `None != 'Negro'` | el método termina sin `return` (quedó `pass`) | agregar el `return` |
# | se imprime `<__main__.X object at 0x7f...>` | falta `__str__`/`__repr__` | definir `__repr__` (sirve para ambos) |
# | `TypeError: X.m() missing 1 required positional argument: 'self'` | llamé `Clase.m()` sin instancia o falta `@staticmethod` | `obj.m()` o decorar con `@staticmethod` |
# | `NameError: name 'ABC' is not defined` | falta el import | `from abc import ABC, abstractmethod` |
# | `ModuleNotFoundError: No module named 'bases'` | corrí python desde otra carpeta | `cd Actividades/AC3` y ahí `python3 main.py` |
# | `TypeError: 'X' object is not subscriptable` / `not iterable` | quise hacer `obj[i]` / `for x in obj` sin `__getitem__`/`__iter__` | iterar sobre la lista interna: `obj.items` |
# | el contador de clase queda en 1 para todos | `self.total += 1` crea un atributo de instancia | `Clase.total += 1` |
# | todos los objetos comparten la misma lista | lista definida como variable de clase | crearla en `__init__`: `self.lista = []` |
# | el método del padre se ejecuta **dos veces** en multiherencia | llamé `A.m(self)` y `B.m(self)` y ambos suben a la misma base | usar `super().m()` en toda la cadena, o llamar a la base una sola vez |
# | `AssertionError` en un test de texto | string no idéntico (tilde, mayúscula, `!!`, espacio, `$`) | copiar el string del enunciado tal cual |

# %% [markdown]
# ## 12. Checklist antes de cada push
## - [ ] Estoy parado en `Actividades/AC3` y `python3 main.py` (y los tests) corren **sin excepción**, aunque falten partes.
# - [ ] Cada método que "retorna" tiene `return`; los que "imprimen" imprimen el string **exacto** del enunciado.
# - [ ] Nombres de clases / métodos / atributos **exactamente** como el enunciado (mayúsculas, guiones bajos).
# - [ ] Multiherencia: `**kwargs` en todos los `__init__`, un solo `super().__init__(**kwargs)`, instancias por keyword.
# - [ ] Properties: `self._x` adentro del getter/setter; el `__init__` crea `self._x` antes de usar `self.x`.
# - [ ] Abstractas: todas las hijas implementan **todos** los `@abstractmethod`.
# - [ ] No modifiqué archivos "No modificar"; no importé librerías externas.
# - [ ] `git add . && git commit -m "AC3 parte N" && git push` → revisar en github.com que estén en `Actividades/AC3`, rama `main`.
