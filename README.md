# apuntes-progra — material de estudio personal IIC2233 2026-2

Regla del curso (aviso del 26/08): en la evaluación se puede usar **apuntes de la materia** y
**material de estudio personal preparado antes** (notebooks, códigos, ejemplos, ejercicios),
**solo desde el mismo dispositivo Linux** (el pendrive). Todo debe estar hoy en `~/Trabajo`.

## Qué hay
- **`apuntes.ipynb`** — LA chuleta. Una sola, ordenada como se resuelve una AC:
  0 flujo y comandos git · 1 estructura de `main.py` · 2 leer archivos · 3 clases (property,
  classmethod, ABC, herencia, multiherencia con `**kwargs`) · 4 cargar datos y qué estructura usar ·
  5 mini-demo de dict/defaultdict/stack/deque/set/namedtuple · 6 simular acciones con casos borde ·
  7 reporte (sorted, formatos) · 8 lo que preguntan en el control · 9 error → arreglo ·
  10 checklist antes del push. Resuelve una mini-AC (DCCafetería) de punta a punta; cada celda es
  copiable. Ejecutar las celdas en orden (la primera crea `data/` de ejemplo).
- `apuntes.py` — las mismas celdas en un `.py` (por si la ISO no trae Jupyter): `python3 apuntes.py`.
- `ejercicios/` — AC simulada DCComercio (enunciado, base, solución) y los dos diagnósticos resueltos.

## Dejarlo en el pendrive (booteado en Lubuntu)
```bash
cd ~/Trabajo
git clone https://github.com/feliivk/apuntes-progra.git     # privado: usuario feliivk + token
git clone https://github.com/IIC2233/contenidos.git          # apuntes oficiales
git clone https://github.com/IIC2233/Syllabus.git            # ayudantías AY02/AY03 con solución
```
Si cambias algo hoy en este computador: `git add . && git commit -m "cambios" && git push` desde
esta carpeta, y `git pull` dentro de Lubuntu. No mezclar con el repo de entregas del curso.

Alternativas si GitHub falla dentro de la ISO: copiar la carpeta con un segundo USB a `~/Trabajo/`.

## Comprobación (hoy)
1. Apagar, volver a bootear: `~/Trabajo` sigue con las tres carpetas.
2. Abrir `apuntes.ipynb` (Jupyter) o `python3 ~/Trabajo/apuntes-progra/apuntes.py` corre sin errores.
3. `git pull` en el repo de entregas funciona sin pedir clave.

## Test de mañana
Resolver la AC real usando solo `apuntes.ipynb` + apuntes oficiales. Después anotar qué faltó,
qué sobró y qué costó encontrar, para ajustar la chuleta para la próxima.
