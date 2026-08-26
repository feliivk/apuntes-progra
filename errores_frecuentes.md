# Errores frecuentes → causa → arreglo (verificados en Python 3.12)

| Mensaje | Causa | Arreglo |
|---|---|---|
| `AttributeError: 'X' object has no attribute 'a'` | La subclase no llamó a `super().__init__()`, o nombre mal escrito | Llamar `super().__init__(...)` antes de usar atributos heredados |
| `TypeError: Can't instantiate abstract class X without an implementation for abstract method 'm'` | Instanciar clase con abstractos sin implementar (o subclase que olvidó uno / typo en el nombre) | Implementar todos los abstractos con el nombre exacto |
| `RecursionError: maximum recursion depth exceeded` | Getter/setter usa `self.x` en vez de `self._x` | Atributo interno con nombre distinto a la property |
| `AttributeError: property 'x' of 'C' object has no setter` | Asignar a property de solo lectura (a veces desde `__init__`) | Agregar `@x.setter` o asignar a `self._x` |
| `TypeError: 'NoneType' object is not callable` | Decorador sin `return wrapper` | Retornar la función interna sin paréntesis |
| `TypeError: C.__init__() takes 2 positional arguments but 4 were given` | Posicionales a una clase con `**kwargs`, o `super().__init__(self, …)` | Instanciar por keyword; `super()` no recibe `self` |
| `TypeError: object.__init__() takes exactly one argument` | Sobró un keyword al final de la cadena `super().__init__(**kwargs)` (typo o clase que no lo consume) | Revisar nombres de parámetros en toda la jerarquía |
| `AttributeError: 'super' object has no attribute 'm'` | `super().m()` donde el siguiente del MRO es `object` | Solo la subclase encadena; o `Base.m(self)` explícito |
| `TypeError: Cannot create a consistent method resolution order (MRO)` | Bases en órdenes contradictorios | Mismo orden de bases en toda la jerarquía |
| `TypeError: __str__ returned non-string` | `__str__` hace `print` o retorna no-str | `return f"..."` |
| `TypeError: 'int' object is not callable` | Llamar una property con paréntesis `obj.x()` | Sin paréntesis |
| `TypeError: f() missing 1 required positional argument` | Dos `def f` con distinta firma: solo sobrevive la última (no hay overloading) | Un solo `def`, valores por defecto o `*args` |
| `FileNotFoundError: [Errno 2] No such file or directory: 'data/x.csv'` | `python3` ejecutado desde otra carpeta | `cd` a la carpeta de la AC; `os.path.join("data", "x.csv")` |
| `ModuleNotFoundError` / `ImportError: cannot import name` | Ejecutar desde otra carpeta o renombrar una clase que otro archivo importa | No cambiar nombres de lo que importan `main.py`/tests |
| `KeyError: 'x'` | `dict[llave]` inexistente; `set.remove` inexistente | `in` / `get` / `defaultdict`; `discard` |
| `IndexError: pop from empty list` / `pop from an empty deque` | `pop()`/`popleft()` sobre vacío | `if not cola:` antes |
| `ValueError: invalid literal for int() with base 10: '5\n'` | Falta `strip()` al leer la línea | `linea.strip().split(",")` |
| `ValueError: too many values to unpack` | Desempaquetar con cantidad distinta de variables (línea con más comas, encabezado no saltado) | Saltar encabezado; revisar el separador |
| `TypeError: unhashable type: 'list'` | Lista como llave de dict o elemento de set | Usar tupla |
| `AttributeError: can't set attribute` (namedtuple) | Asignar campo de namedtuple | `_replace` devuelve copia; o usar clase |
| `RuntimeError: dictionary changed size during iteration` | Borrar/agregar llaves mientras se itera el dict | Iterar sobre `list(d)` o acumular y aplicar después |

## Recordatorios de git (los 5 comandos del curso)
`git clone` → `git pull` → `git add .` → `git commit -m "msg"` → `git push`.
`commit` guarda solo lo que estaba en staging; `push` sube commits, no el staging.
Siempre `cd Actividades/ACx && python3 main.py`. Verificar en github.com antes de las 17:10.
