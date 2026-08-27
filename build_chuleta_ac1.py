"""Genera chuleta_AC1_aldeanos.ipynb y chuleta_AC1_aldeanos.py a partir de la lista CELLS.

Uso:  python3 build_chuleta_ac1.py          (crea/actualiza los dos archivos)
      python3 build_chuleta_ac1.py --run    (además ejecuta todas las celdas de código en orden)
"""
import json
import sys
import io
import contextlib

CELLS = []


def md(texto):
    CELLS.append(("markdown", texto.strip("\n")))


def code(texto):
    CELLS.append(("code", texto.strip("\n")))


# =====================================================================
md(r"""
# Chuleta AC1 — aldeanos (parte 1 property/getter/setter · parte 2 manejo · parte 3 personalidades + regalo)

Mini chuleta con **solo** lo que pide la AC1, en el mismo orden de sus partes. `Ctrl+F` con la palabra del enunciado.
Los nombres usados aquí (`Aldeano`, `Isla`, `recibir_regalo`, `amistad`…) son **ejemplos**: los nombres EXACTOS de
clases, métodos, argumentos y strings salen en los archivos base (`bases.py`, `main.py`, tests) — **leerlos ANTES de escribir**.

- Para más OOP (herencia con `**kwargs`, ABC, multiherencia, `__str__`, classmethod, diagramas): `chuleta_AC3_oop.ipynb`.
- Para leer archivos, armar `main.py` y simular acciones: `apuntes.ipynb`.

**Flujo (2 horas):** 1) leer el enunciado completo sin escribir → 2) push de los archivos base al tiro →
3) leer los archivos "No modificar" → 4) resolver parte 1 → 2 → 3, corriendo `python3 main.py` (o los tests)
y haciendo push **después de cada parte** → 5) si algo se traba >15 min: dejar un `pass`/`return` que no se caiga y seguir.
""")

# =====================================================================
md(r"""
## 0. Diccionario: lo que dice el enunciado → lo que escribo

| Si el enunciado dice… | Escribo… | Parte |
|---|---|---|
| "definir la property `amistad`" / "getter y setter" | `self._amistad` en `__init__` + `@property` + `@amistad.setter` | 1 |
| "acotada entre 0 y 100" / "máximo … mínimo …" | en el setter: `self._amistad = max(0, min(100, valor))` | 1 |
| "no puede ser negativa (queda en 0)" | en el setter: `self._amistad = max(0, valor)` | 1 |
| "si es inválido se ignora" / "lanza `ValueError`" | `if` dentro del setter / `raise ValueError("mensaje")` | 1 |
| "solo lectura" / "se calcula a partir de…" | `@property` sin setter | 1 |
| "la isla / el pueblo **tiene** aldeanos" | clase administradora con `self.aldeanos = []` | 2 |
| "agregar si hay capacidad / si no existe ya" | revisar `len(...)` y `buscar_aldeano(...)` ANTES del `append` | 2 |
| "buscar por nombre" | `for a in self.aldeanos:` → `if a.nombre == nombre: return a` → al final `return None` | 2 |
| "se muda / se va de la isla" / "eliminar" | buscar primero → `self.aldeanos.remove(aldeano)` | 2 |
| "el aldeano con mayor amistad" | `max(self.aldeanos, key=lambda a: a.amistad)` | 2 |
| "listado ordenado por amistad" | `sorted(self.aldeanos, key=lambda a: (-a.amistad, a.nombre))` | 2 |
| "los de personalidad X" / "cuántos…" | `[a for a in self.aldeanos if a.personalidad == x]` / `len(...)` | 2 |
| "cargar aldeanos desde un archivo" | `apuntes.ipynb` secciones 2 y 4 (leer_csv → crear objetos) | 2 |
| "cada personalidad reacciona distinto al regalo" | subclases que redefinen `recibir_regalo` → **forma A** | 3 |
| "además de lo que hace un aldeano (normal)" | extender: `super().recibir_regalo(regalo)` + lo extra | 3 |
| "la personalidad es un atributo" (sin subclases) | dict de reglas o `if/elif` dentro del método → **forma B** | 3 |
| "al recibir un regalo sube la amistad" | `self.amistad += regalo.valor` (usa el setter de la parte 1 → se acota solo) | 3 |
| "si el regalo es de su tipo favorito…" | `if regalo.tipo == ...:` (el gusto como variable de clase o dict) | 3 |
| "identificar la personalidad de un objeto" | `isinstance(a, Grunon)` / `type(a).__name__` | 3 |
| "al hacer `print(aldeano)`" | `def __str__(self): return f"..."` (chuleta AC3 sección 2) | — |
| herencia con `**kwargs`, ABC, multiherencia, classmethod | chuleta_AC3_oop (secciones 3, 4 y 6) | — |
""")

# =====================================================================
md(r"""
## Parte 1 — definir property: getter + setter

Un atributo que por fuera se usa como `aldeano.amistad` (leer y asignar), pero por detrás pasa por métodos:
el **getter** corre al **leer** y el **setter** al **asignar** (`obj.x = v`; un `+=`/`-=` usa **ambos**: lee y asigna).
Sirve para **validar/acotar** al asignar o para **calcular** al leer.

| Quiero | Escribo |
|---|---|
| Atributo interno (respaldo) | `self._amistad` (con guion bajo; solo se toca DENTRO de la clase) |
| Getter | `@property` sobre `def amistad(self): return self._amistad` |
| Setter | `@amistad.setter` sobre `def amistad(self, valor): ...` (MISMO nombre que el getter) |
| Validar también lo que llega al `__init__` | `self._amistad = 0` y en la línea siguiente `self.amistad = amistad` (pasa por el setter) |
| Solo lectura / calculada | solo el `@property`, sin setter (asignarla lanza `AttributeError`) |
| Forma sin decoradores (a veces en `bases.py`) | `amistad = property(_get_amistad, _set_amistad)` |

⚠️ Dentro del getter/setter SIEMPRE `self._amistad`; poner `self.amistad` ahí vuelve a llamar la property → `RecursionError`.
⚠️ El getter (`@property`) va ANTES que el setter (`@amistad.setter`) y ambos métodos se llaman igual.
⚠️ Si una hija redefine el getter, lleva `@property` de nuevo (si no, queda como método). Más variantes
(property abstracta, deleter, cambiar solo el setter en la hija con `@Padre.x.setter`): chuleta AC3 sección 5.
""")

code(r'''
class Aldeano:
    def __init__(self, nombre, personalidad, amistad):
        self.nombre = nombre                    # atributos normales, sin property
        self.personalidad = personalidad
        self._amistad = 0                       # 1° crear el interno con un valor seguro
        self.amistad = amistad                  # 2° asignar como self.amistad → pasa por el SETTER (valida gratis)

    @property                                   # GETTER: corre al LEER aldeano.amistad
    def amistad(self):
        return self._amistad

    @amistad.setter                             # SETTER: corre al ASIGNAR aldeano.amistad = v (también con += / -=)
    def amistad(self, valor):
        self._amistad = max(0, min(100, valor))     # "acotada entre 0 y 100"
        # otras variantes según el enunciado (dejar UNA):
        #   "no negativa (queda en 0)"    → self._amistad = max(0, valor)
        #   "inválida → se ignora"        → if 0 <= valor <= 100: self._amistad = valor
        #   "inválida → error"            → if valor < 0: raise ValueError("amistad inválida")
        #   "se redondea a 1 decimal"     → self._amistad = round(float(valor), 1)

    @property                                   # SOLO LECTURA (calculada): NO tiene setter
    def corazones(self):
        return self.amistad // 20               # un getter puede usar OTRA property (nombre distinto, sin paréntesis)

    def conversar(self):                        # los métodos también asignan vía la property...
        self.amistad += 5                       # ...así jamás se sale del rango 0-100


rosita = Aldeano("Rosita", "alegre", 130)
print(rosita.amistad)                       # 100 ← el 130 del __init__ pasó por el setter
rosita.amistad -= 250                       # lee con el getter (100) y asigna -150 → el setter deja 0
print(rosita.amistad, rosita.corazones)     # 0 0
rosita.amistad = 90
rosita.conversar()
print(rosita.amistad, rosita.corazones)     # 95 4
try:
    rosita.corazones = 5                    # asignar a una property sin setter
except AttributeError as e:
    print("AttributeError:", e)             # py>=3.11: ... has no setter | py3.10: can't set attribute
''')

# =====================================================================
md(r"""
## Parte 2 — manejo de aldeanos (la clase que los "tiene")

"La isla **tiene** aldeanos" = composición: una clase administradora guarda `self.aldeanos = []`
(lista de **objetos**) y sus métodos recorren esa lista. El orden de TODO método de manejo:
**buscar → revisar el caso borde → operar → retornar/imprimir EXACTAMENTE lo que pide el enunciado**.

- Casos borde que siempre evalúan: isla **llena**, aldeano **repetido**, buscar/eliminar uno que **no existe**, isla **vacía** (promedio ÷ 0).
- `print` no es `return`: si dice "retorna", retornar (y los strings impresos, idénticos al enunciado).
- Variante con dict (si `bases.py` trae `self.aldeanos = {}`): agregar `self.aldeanos[a.nombre] = a`,
  buscar `self.aldeanos.get(nombre)`, eliminar `self.aldeanos.pop(nombre, None)`, recorrer `self.aldeanos.values()`.
""")

code(r'''
class Isla:
    CAPACIDAD = 10                              # variable de clase: constante compartida

    def __init__(self, nombre):
        self.nombre = nombre
        self.aldeanos = []                      # la isla TIENE aldeanos (lista de objetos Aldeano)

    def buscar_aldeano(self, nombre):           # el método base: casi todos los demás lo usan
        for aldeano in self.aldeanos:
            if aldeano.nombre == nombre:        # comparar ATRIBUTO con string (no el objeto)
                return aldeano
        return None                             # explícito: no está (quien llama revisa el None)

    def agregar_aldeano(self, aldeano):
        if len(self.aldeanos) >= Isla.CAPACIDAD:
            print(f"{self.nombre} está llena: {aldeano.nombre} no puede mudarse")
            return False
        if self.buscar_aldeano(aldeano.nombre) is not None:
            print(f"{aldeano.nombre} ya vive en {self.nombre}")
            return False
        self.aldeanos.append(aldeano)
        return True

    def eliminar_aldeano(self, nombre):         # "se muda / se va de la isla"
        aldeano = self.buscar_aldeano(nombre)
        if aldeano is None:
            print(f"{nombre} no vive en {self.nombre}")
            return None
        self.aldeanos.remove(aldeano)           # buscar PRIMERO, remover DESPUÉS (nunca dentro de un for)
        return aldeano                          # retornar lo que pida el enunciado (objeto / True / nada)

    # --- reportes típicos de "manejo" ---
    def por_personalidad(self, personalidad):
        return [a for a in self.aldeanos if a.personalidad == personalidad]

    def promedio_amistad(self):
        if not self.aldeanos:                   # caso borde: isla vacía (evita división por 0)
            return 0
        return sum(a.amistad for a in self.aldeanos) / len(self.aldeanos)

    def mejor_amigo(self):
        if not self.aldeanos:
            return None
        return max(self.aldeanos, key=lambda a: a.amistad)

    def reporte(self):                          # amistad descendente; nombre desempata
        for aldeano in sorted(self.aldeanos, key=lambda a: (-a.amistad, a.nombre)):
            print(f"- {aldeano.nombre} ({aldeano.personalidad}): {aldeano.amistad}")


isla = Isla("DCCAldea")
isla.agregar_aldeano(Aldeano("Rosita", "alegre", 60))
isla.agregar_aldeano(Aldeano("Apolo", "gruñón", 40))
isla.agregar_aldeano(Aldeano("Rosita", "alegre", 10))       # repetido → aviso, no entra
for numero in range(1, 10):                                  # con Vecino8 se llega a 10; Vecino9 ya no entra
    isla.agregar_aldeano(Aldeano(f"Vecino{numero}", "normal", 30))
print("viven:", len(isla.aldeanos))                          # 10
isla.eliminar_aldeano("Canela")                              # no existe → aviso, retorna None
isla.eliminar_aldeano("Vecino1")
print("mejor amigo:", isla.mejor_amigo().nombre)             # Rosita (60)
print("promedio:", round(isla.promedio_amistad(), 2))
print("normales:", [a.nombre for a in isla.por_personalidad("normal")])
isla.reporte()
''')

# =====================================================================
md(r"""
## Parte 3 — personalidades del aldeano + recibir regalo

Dos formas; el enunciado (o `bases.py`) dice cuál:

- **Forma A — subclases** (si dice "hereda de", "cada personalidad es una clase", "sobreescribir"):
  `class Alegre(Aldeano):` y redefinir `recibir_regalo`. **Sobreescribir** = reemplazar completo;
  **extender** = `super().recibir_regalo(regalo)` + lo extra. Al recorrer la lista y llamar
  `aldeano.recibir_regalo(regalo)`, cada uno reacciona según su clase → **polimorfismo** (sin `if` por tipo).
- **Forma B — una sola clase**: la personalidad es un atributo string y las reglas van en un dict o `if/elif` dentro del método.

El regalo puede llegar como **clase** con `tipo`/`valor`, como namedtuple o como puros argumentos
(`recibir_regalo(self, nombre, valor)`) → mirar `bases.py`. Regla de oro: dentro de `recibir_regalo`
modificar **`self.amistad`** (la property de la parte 1), nunca `self._amistad` → el tope 0-100 se respeta solo.
""")

code(r'''
class Regalo:
    def __init__(self, nombre, tipo, valor):
        self.nombre = nombre
        self.tipo = tipo                        # "fruta", "mueble", "ropa", "flor"...
        self.valor = valor


# FORMA A — la clase de la parte 1 (compacta) + el método base; la personalidad sale de la subclase
class Aldeano:
    def __init__(self, nombre, amistad):
        self.nombre = nombre
        self.personalidad = type(self).__name__.lower()     # "alegre", "grunon", "perezoso"
        self._amistad = 0
        self.amistad = amistad

    @property
    def amistad(self):
        return self._amistad

    @amistad.setter
    def amistad(self, valor):
        self._amistad = max(0, min(100, valor))

    def recibir_regalo(self, regalo):           # reacción BASE (la del aldeano "normal")
        self.amistad += regalo.valor            # por la property → se acota solo
        print(f"{self.nombre} recibe {regalo.nombre} (+{regalo.valor})")


class Alegre(Aldeano):
    def recibir_regalo(self, regalo):           # EXTENDER: lo del padre + algo más
        super().recibir_regalo(regalo)
        self.amistad += regalo.valor            # a los alegres todo les vale doble
        print(f"  ¡{self.nombre} salta de alegría!")


class Grunon(Aldeano):
    GUSTO = "mueble"                            # variable de clase: el gusto de TODOS los gruñones

    def recibir_regalo(self, regalo):           # SOBREESCRIBIR: reemplaza la reacción completa
        if regalo.tipo == Grunon.GUSTO:
            self.amistad += regalo.valor
            print(f"{self.nombre} acepta {regalo.nombre} de mala gana")
        else:
            self.amistad -= 5
            print(f"{self.nombre} gruñe: no quería {regalo.nombre}")


class Perezoso(Aldeano):
    def recibir_regalo(self, regalo):           # AJUSTAR Y DELEGAR: cambia algo y el padre hace el resto
        if regalo.tipo == "fruta":              # la comida le vale doble a un perezoso
            regalo = Regalo(regalo.nombre, regalo.tipo, regalo.valor * 2)
        super().recibir_regalo(regalo)


vecinos = [Alegre("Rosita", 50), Grunon("Apolo", 50), Perezoso("Coco", 50)]
manzana = Regalo("manzana", "fruta", 10)
for vecino in vecinos:
    vecino.recibir_regalo(manzana)              # POLIMORFISMO: mismo llamado, reacción distinta
print([(v.nombre, v.amistad) for v in vecinos])            # Rosita 70, Apolo 45, Coco 70
print(isinstance(vecinos[1], Grunon), type(vecinos[1]).__name__)   # True Grunon
''')

code(r'''
# FORMA B — sin subclases: la personalidad es un string y las reglas viven en el método (o en dicts)
MULTIPLICADOR = {"alegre": 2, "normal": 1, "perezoso": 1, "gruñón": 1}
TIPO_FAVORITO = {"perezoso": "fruta", "gruñón": "mueble"}


class AldeanoSimple:
    def __init__(self, nombre, personalidad, amistad):
        self.nombre = nombre
        self.personalidad = personalidad
        self._amistad = 0
        self.amistad = amistad

    @property
    def amistad(self):
        return self._amistad

    @amistad.setter
    def amistad(self, valor):
        self._amistad = max(0, min(100, valor))

    def recibir_regalo(self, regalo):
        puntos = regalo.valor * MULTIPLICADOR.get(self.personalidad, 1)
        if TIPO_FAVORITO.get(self.personalidad) == regalo.tipo:
            puntos += 5                                     # "+5 si es de su tipo favorito"
        elif self.personalidad == "gruñón":
            puntos = -5                                     # el gruñón rechaza lo que no le gusta
        self.amistad += puntos
        print(f"{self.nombre} ({self.personalidad}): {puntos:+d} de amistad")


fauna = AldeanoSimple("Fauna", "normal", 50)
apolo = AldeanoSimple("Apolo", "gruñón", 50)
sofa = Regalo("sofá", "mueble", 10)
fauna.recibir_regalo(sofa)                  # +10 → 60
apolo.recibir_regalo(sofa)                  # +15 (10 x 1 + 5 por favorito) → 65
apolo.recibir_regalo(Regalo("polera", "ropa", 10))          # -5 → 60
print(fauna.amistad, apolo.amistad)
''')

code(r'''
# --- Las tres partes juntas: mini simulación estilo main.py ---
isla = Isla("DCCAldea")                                     # la Isla de la parte 2 acepta aldeanos
for vecino in [Alegre("Rosita", 45), Grunon("Apolo", 45), Perezoso("Coco", 45)]:
    isla.agregar_aldeano(vecino)                            # ...de cualquier subclase (forma A)

acciones = [("regalar", "Rosita", Regalo("rosa", "flor", 10)),
            ("regalar", "Apolo", Regalo("sofá", "mueble", 10)),
            ("regalar", "Canela", Regalo("rosa", "flor", 10)),   # no vive aquí → caso borde
            ("mudar", "Coco", None)]

for accion, nombre, regalo in acciones:
    if accion == "regalar":
        aldeano = isla.buscar_aldeano(nombre)
        if aldeano is None:                                 # SIEMPRE revisar el None antes de usar
            print(f"{nombre} no vive en {isla.nombre}")
            continue
        aldeano.recibir_regalo(regalo)
    elif accion == "mudar":
        isla.eliminar_aldeano(nombre)

isla.reporte()                                              # Rosita 65, Apolo 55 (Coco ya se fue)
print("Mejor amigo:", isla.mejor_amigo().nombre)
''')

# =====================================================================
md(r"""
## Error → arreglo (los de estas tres partes)

| Sale… | Causa típica | Arreglo |
|---|---|---|
| `RecursionError: maximum recursion depth exceeded` | `self.amistad` DENTRO del getter/setter de `amistad` | adentro siempre `self._amistad` |
| `AttributeError: property 'x' of 'Aldeano' object has no setter` (py ≥3.11) / `can't set attribute` (py 3.10) | asigné a una property de solo lectura | agregar `@x.setter`, o no asignarla |
| `AttributeError: 'Aldeano' object has no attribute '_amistad'` | el getter/setter corrió antes de crear `self._amistad` | en `__init__`: `self._amistad = 0` ANTES de `self.amistad = valor` |
| `TypeError: 'int' object is not callable` | llamé la property con paréntesis: `a.amistad()` | sin paréntesis: `a.amistad` |
| `'<' not supported between instances of 'method' and 'int'` (o compara raro) | faltó `@property` sobre el getter, o al sobreescribirlo en la hija | poner el decorador (también en la hija) |
| `ValueError: list.remove(x): x not in list` | eliminé algo que no estaba, o `remove` dentro del `for` sobre la misma lista | buscar primero, revisar `None`, remover después |
| `AttributeError: 'NoneType' object has no attribute '…'` | `buscar_aldeano` retornó `None` y lo usé igual | `if aldeano is None:` antes de usarlo |
| el repetido igual entra / nunca encuentra | comparé objeto con string: `aldeano == nombre` | comparar atributos: `aldeano.nombre == nombre` |
| la amistad queda >100 o negativa | modifiqué `self._amistad` directo fuera del setter | usar `self.amistad += …` (pasa por el setter) |
| `TypeError: __init__() missing 1 required positional argument` | faltaron argumentos al crear, o la hija no pasó todo en `super().__init__(...)` | revisar orden/cantidad contra `bases.py` |

## Checklist AC1 (antes de cada push)

- [ ] Nombres EXACTOS de clases, métodos y argumentos = los de `bases.py`/`main.py`/tests (mayúsculas, tildes, guiones bajos).
- [ ] Strings impresos idénticos a los del enunciado / salida esperada (espacios y puntuación incluidos).
- [ ] Property: afuera `self.amistad`, adentro del getter/setter `self._amistad`; el `__init__` asigna vía `self.amistad = ...`.
- [ ] Cada método retorna lo que pide el enunciado (objeto / `True`-`False` / `None` / string) — un `print` no reemplaza al `return`.
- [ ] Casos borde probados: valor fuera de rango en la property, isla llena, repetido, buscar/eliminar inexistente, isla vacía.
- [ ] `python3 main.py` corre sin caerse (y los tests si hay: `python3 -m unittest discover tests_publicos -v -b`).
- [ ] `git add . && git commit -m "AC1 parte N" && git push` después de CADA parte; revisar en github.com que llegó.
""")


# =====================================================================
def build_ipynb():
    cells = []
    for tipo, src in CELLS:
        lines = src.splitlines(keepends=True)
        cell = {"cell_type": tipo, "metadata": {}, "source": lines}
        if tipo == "code":
            cell["execution_count"] = None
            cell["outputs"] = []
        cells.append(cell)
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.10"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def build_py():
    out = ["# chuleta_AC1_aldeanos.py - exportación de chuleta_AC1_aldeanos.ipynb (mismas celdas, en orden)\n"]
    for tipo, src in CELLS:
        if tipo == "markdown":
            out.append("\n# %% [markdown]\n")
            out.extend("# " + l if l.strip() else "#" + l for l in src.splitlines(keepends=True))
            out.append("\n")
        else:
            out.append("\n# %% ---------------------------------------------------------\n")
            out.append(src + "\n")
    return "".join(out)


def run_all():
    ns = {}
    for i, (tipo, src) in enumerate(CELLS):
        if tipo != "code":
            continue
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                exec(compile(src, f"celda_{i}", "exec"), ns)
        except Exception as e:  # noqa: BLE001
            print(buf.getvalue())
            print(f"!!! celda {i} falló: {type(e).__name__}: {e}")
            raise
        print(f"=== celda {i} OK ===")
        print(buf.getvalue())


if __name__ == "__main__":
    with open("chuleta_AC1_aldeanos.ipynb", "w", encoding="utf-8") as f:
        json.dump(build_ipynb(), f, ensure_ascii=False, indent=1)
    with open("chuleta_AC1_aldeanos.py", "w", encoding="utf-8") as f:
        f.write(build_py())
    print(f"{len(CELLS)} celdas -> chuleta_AC1_aldeanos.ipynb / chuleta_AC1_aldeanos.py")
    if "--run" in sys.argv:
        run_all()
