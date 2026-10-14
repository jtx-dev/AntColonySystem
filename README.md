# Proyecto 2: PFSP

La implementación de AG, AM y ACS para PFSP está en
[`ejercicio_proyecto`](ejercicio_proyecto/README.md). Los comandos de esa entrega
se ejecutan desde dicha carpeta.

## Ejemplo previo: Ant Colony System para Berlin52

Implementación simple y reproducible de Ant Colony System (ACS) para el
Problema del Vendedor Viajero. La instancia incluida usa las 52 ciudades de
Berlin52 y distancias `EUC_2D` redondeadas según TSPLIB.

## Requisitos

- Python 3.10 o superior.
- NumPy, pandas y matplotlib.

Instalación:

```bash
pip install numpy pandas matplotlib
```

## Ejecución

Los argumentos son: instancia, hormigas, iteraciones, evaporación (`alpha`),
peso heurístico (`beta`), `q0`, semilla y archivo CSV de salida.

```bash
python acs.py datos/instancia.txt 50 200 0.1 2.0 0.9 12345 resultados/resultados.csv
```

El programa muestra el mejor recorrido, su costo y el tiempo empleado. El CSV
registra la mejor solución de cada iteración y la mejor acumulada, junto con la
instancia, semilla y parámetros utilizados.

## Pruebas

```bash
python tests.py
```

Las pruebas verifican la lectura de Berlin52, las distancias, la validez de los
recorridos, las actualizaciones de feromonas y la reproducibilidad.

## Gráfico de convergencia

```bash
python graficar.py resultados/resultados.csv graficos/grafico1.pdf
```

El segundo argumento es opcional; por defecto se utiliza
`graficos/grafico1.pdf`.
