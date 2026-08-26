# Material de apoyo para llevar en el pendrive (carpeta `Trabajo`)

Regla anunciada por el curso: en la evaluación se puede usar **apuntes de la materia** y
**material de estudio personal preparado antes** (notebooks, códigos, ejemplos, ejercicios),
**solo desde el mismo dispositivo Linux** (el pendrive). Nada llega desde otro computador,
teléfono ni nube durante la evaluación, así que todo debe estar copiado hoy en `Trabajo`.

Sugerencia honesta: este material se preparó estudiando con IA (permitido durante el estudio).
Para que sea claramente *tu* material, reescribe la chuleta en tus palabras (aunque sea
copiando a mano las partes que vas a usar) y, si tienes dudas de si cuenta, pregunta en las
Discussions antes de mañana.

## Qué hay aquí
- `chuleta_oop_avanzado.py` / `.ipynb` — herencia, `super()`, multiherencia con `**kwargs`,
  MRO/diamante, ABC, properties, `@classmethod`/`@staticmethod`, decoradores, `__str__`/`__repr__`,
  operadores. Corre con `python3 chuleta_oop_avanzado.py` e imprime cada demo.
- `chuleta_edd_archivos.py` / `.ipynb` — dict/defaultdict/stack/deque/set/namedtuple/`*args`,
  lectura y escritura de CSV, paths y módulos.
- `plantilla_ac.py` — esqueleto típico de una AC (clase abstracta con `**kwargs`, subclases,
  multiherencia, property con validación, carga de CSV, cola de acciones con `deque`, stack para
  deshacer, `defaultdict`). Ejecutable como demo.
- `errores_frecuentes.md` — mensaje de error → causa → arreglo, más el flujo git.
- `ejercicios/` — la AC simulada (enunciado, base y solución) y los dos diagnósticos resueltos.

Los `.py` y `.md` se abren con Lite XL dentro de Lubuntu; los `.ipynb` solo si la ISO trae
Jupyter (si no, usa los `.py`, tienen el mismo contenido).

## Cómo dejarlo en el pendrive (elige una)

**A. Por GitHub (la ISO deja entrar a github.com).** En este computador:
```bash
cd ~/Documents/Repo/progra2026/preparacion_control_1
git init apuntes-progra && cp -r material_apoyo_pendrive/* apuntes-progra/ && cd apuntes-progra
git add . && git commit -m "material de estudio"
# crea un repo PRIVADO vacío en github.com (p. ej. apuntes-progra) y luego:
git remote add origin https://github.com/<tu-usuario>/apuntes-progra.git
git push -u origin main
```
Luego, booteado en Lubuntu: `cd ~/Trabajo && git clone https://github.com/<tu-usuario>/apuntes-progra.git`.
No lo pongas dentro de tu repositorio de entregas del curso: mantén ese repo solo con `Actividades/`.

**B. Con un segundo pendrive.** Copia la carpeta a otro USB, bootea Lubuntu, conecta el segundo
USB y copia la carpeta a `~/Trabajo/`.

**C. Desde este Arch, montando la partición persistente del pendrive.** Conecta el pendrive,
`lsblk -o NAME,SIZE,FSTYPE,LABEL` y monta la partición de datos (la que no es la ISO, normalmente
ext4). La ruta interna de `Trabajo` depende de cómo esté armada la imagen del curso, así que
si no la ves a simple vista, usa A o B.

## Además, dentro de Lubuntu (apuntes oficiales)
```bash
cd ~/Trabajo
git clone https://github.com/IIC2233/contenidos.git
git clone https://github.com/IIC2233/Syllabus.git
```
Las ayudantías con solución están en `Syllabus/Ayudantías/AY02` y `AY03`; los apuntes de la
semana 4 en `contenidos/semana-04-oop_avanzado/`.

## Comprobación final (hoy)
1. Apagar Lubuntu, volver a bootear y confirmar que `~/Trabajo` sigue con todo.
2. `python3 ~/Trabajo/apuntes-progra/chuleta_oop_avanzado.py` corre sin errores.
3. `git -C ~/Trabajo/<tu-usuario>-iic2233-2026-2 pull` funciona sin pedir clave (token guardado).
