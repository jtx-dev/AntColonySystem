# Preproyecto: ACS para Berlin52

Implementación reproducible de Ant Colony System para la instancia Berlin52
del problema del vendedor viajero. Esta etapa sirvió como base para adaptar
ACS al PFSP en el Proyecto 2.

## Contenido

- `enunciado2.pdf`: enunciado del preproyecto.
- `acs.py`: algoritmo y ejecución por consola.
- `operadores.py`: lectura, distancias, feromonas y construcción de recorridos.
- `tests.py`: pruebas de lectura, costo, feromonas y reproducibilidad.
- `datos/instancia.txt`: coordenadas de Berlin52.
- `resultados/resultados_ACS.csv`: historial de la ejecución conservada.
- `graficos/grafico1.pdf`: gráfico de convergencia de esa ejecución.
- `PLAN_PROYECTO.md`: registro del avance desde Berlin52 hasta PFSP.

## Requisitos

```powershell
pip install numpy matplotlib
```

## Ejecución

Desde esta carpeta:

```powershell
py .\tests.py
py .\acs.py .\datos\instancia.txt 50 1000 0.1 2.0 0.9 42 .\resultados\resultados_ACS.csv
py .\graficar.py .\resultados\resultados_ACS.csv .\graficos\grafico1.pdf
```
