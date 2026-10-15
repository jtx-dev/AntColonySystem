# Proyecto 2: comparación de AG, AM y ACS para PFSP

Implementación y comparación reproducible de un algoritmo genético, un
algoritmo memético y Ant Colony System para minimizar el makespan del
Permutation Flow Shop Scheduling Problem.

## Estructura

- `preproyecto/`: ACS aplicado a Berlin52, con enunciado, código y resultados.
- `ejercicio_proyecto/`: código, datos, pruebas y guía de ejecución.
- `ejercicio_proyecto/resultados/comparacion_algoritmos/`: 27 ejecuciones finales.
- `ejercicio_proyecto/graficos/`: curvas comparativas de convergencia.
- `informe/proyecto2.tex`: fuente del informe científico.
- `informe/proyecto2.pdf`: informe compilado.

## Uso rápido

Preproyecto Berlin52:

```powershell
cd preproyecto
py .\tests.py
py .\acs.py .\datos\instancia.txt 50 1000 0.1 2.0 0.9 42 .\resultados\resultados_ACS.csv
```

Proyecto 2 PFSP:

```powershell
cd ejercicio_proyecto
py .\tests.py
py .\graficar.py .\resultados\comparacion_algoritmos .\graficos
```

Las instrucciones completas están en [`preproyecto/README.md`](preproyecto/README.md)
y [`ejercicio_proyecto/README.md`](ejercicio_proyecto/README.md).
