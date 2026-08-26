# Simulacro AC — DCComercio (OOP Avanzado, IIC2233 2026-2)

- `enunciado.md`: enunciado completo con formato de las AC reales (Entrega, Objetivos,
  diagrama de clases, Partes 1-5, Salida esperada, Bonus, Notas, Notas del simulacro).
- `release/`: archivos base que recibirías en la AC (copia esta carpeta a tu repositorio
  y trabaja ahí). Incluye `pruebas_empleados.py` (no entregable) y dos juegos de datos
  (`data/` y `data_grande/`).
- `solucion/`: solución de referencia que produce exactamente la salida esperada;
  `solucion/bonus.py` contiene el bonus resuelto y verificado. No la mires hasta terminar.
- `salida_esperada.txt`: salida exacta de `python3 main.py` con `data/`.
- `salida_esperada_grande.txt`: salida exacta con `CARPETA_DATOS = "data_grande"`.

Uso: `cp -r release ~/mi_repo/Actividades/AC3`, luego parado en esa carpeta
`python3 main.py > mi_salida.txt` y `diff mi_salida.txt <ruta>/salida_esperada.txt`.
