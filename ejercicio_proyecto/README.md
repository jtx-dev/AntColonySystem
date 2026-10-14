# AG, AM y ACS para PFSP

AG (`ag.py`) y AM (`am.py`) reutilizan los operadores del Proyecto 1,
adaptados al formato de datos y evaluador comunes de este proyecto.

Adaptación del ACS de Berlin52 (directorio raíz del repositorio) al
*Permutation Flow Shop Scheduling Problem* (PFSP), siguiendo la metodología
del Pre Proyecto 2: separar el **algoritmo general** (`acs.py`) de los
**operadores específicos del problema** (`operadores.py`), probarlos,
experimentar con los parámetros y analizar los resultados.

El objetivo es encontrar la permutación de trabajos que minimiza el makespan
`C_max`, calculado con la recursión

```
C(i, j) = max(C(i-1, j), C(i, j-1)) + p[π_i, j],   C(0, j) = C(i, 0) = 0,   C_max = C(n, m)
```

## Requisitos

- Python 3.10 o superior.
- NumPy y matplotlib (matplotlib solo para `graficar.py`).

```bash
pip install numpy matplotlib
```

## Estructura

```
ejercicio_proyecto/
├── acs.py            # Algoritmo ACS y ejecución por consola (qué hace el algoritmo)
├── ag.py             # Algoritmo genético y ejecución por consola
├── am.py             # Algoritmo memético y ejecución por consola
├── operadores.py     # Datos, evaluación y operadores de los algoritmos
├── tests.py          # Pruebas de los operadores y del algoritmo
├── experimentos.py   # Experimentos variando los parámetros de ACS
├── graficar.py       # Gráficos de convergencia y de experimentos
├── datos/            # Instancias de Taillard
├── resultados/       # CSV de ejecuciones y experimentos
├── graficos/         # Gráficos PDF
└── README.md
```

Todos los comandos se ejecutan desde la carpeta `ejercicio_proyecto`.

## Instancias

| Archivo | Instancia | Tamaño | Semilla de Taillard | Mejor conocido (`C_max`) |
|---|---|---|---|---|
| `datos/tai20_5.txt` | ta001 | 20 × 5 | 873654221 | 1278 |
| `datos/tai50_10.txt` | ta041 | 50 × 10 | 1958948863 | 2991 |
| `datos/tai100_10.txt` | ta071 | 100 × 10 | 1539989115 | 5770 |

Los archivos usan el formato de Taillard: una línea con
`n m semilla cota_superior cota_inferior` y luego `m` filas (una por máquina)
con los `n` tiempos de procesamiento. Los tiempos se obtuvieron con el
generador publicado por Taillard (1993) a partir de las semillas oficiales;
ta001 coincide con la instancia publicada. Los mejores valores conocidos de
permutación provienen de la tabla de Mattfeld y Vaessens. `leer_instancia`
también acepta los archivos originales de Taillard (lee la primera instancia).

## Ejecución

### Algoritmo genético

```bash
python ag.py datos/tai20_5.txt 12345 50 200 0.8 0.1 resultados/res_ag.csv
```

Argumentos, en ese orden: instancia, semilla, tamaño de población,
generaciones, probabilidad de cruce, probabilidad de mutación y salida CSV.
La población debe contener al menos 2 individuos; las generaciones deben ser
positivas y las probabilidades estar entre 0 y 1. `python ag.py --help` muestra
la ayuda completa.

El AG usa torneo de dos individuos, cruce OX, mutación por inserción y un
individuo élite. Se siembra un generador local para que la misma instancia,
semilla y parámetros produzcan la misma secuencia y makespan. Su CSV tiene
una fila por generación: mejor de esa generación, mejor acumulado, RPD y
tiempo de CPU acumulado. El tiempo incluye la búsqueda desde la población
inicial y excluye lectura y escritura de archivos. El mejor acumulado se
inicializa con la población inicial y, por eso, nunca empeora.

Los trabajos se indexan desde 0 dentro del programa y desde 1 en pantalla y
CSV. La matriz común es `tiempos[trabajo, maquina]`. AG y ACS llaman al mismo
`calcular_makespan` de `operadores.py`, al igual que AM.

### Algoritmo memético

```bash
python am.py datos/tai20_5.txt 12345 50 200 0.8 0.1 10 resultados/res_am.csv
```

Los primeros seis argumentos son los mismos del AG. El argumento `10` es la
**frecuencia de búsqueda local**: se aplica en las generaciones 10, 20, 30,
etc., al mejor individuo de la población recién generada. Debe ser un entero
positivo. `python am.py --help` muestra el orden completo.

AM usa la misma selección, cruce, mutación y elitismo del AG. La búsqueda
local mueve un trabajo a otra posición y acepta la primera inserción que
reduce el makespan. Repite desde la solución mejorada hasta que no encuentra
una mejora o evalúa `10 × número de trabajos` vecinos. Este límite evita que
una sola búsqueda local en 100×10 consuma una parte excesiva del experimento.
No incorpora perturbaciones ni reinicios por estancamiento.

El CSV tiene una fila por generación, el campo `frecuencia_bl` y las mismas
métricas que AG. El makespan de la generación se registra después de la
búsqueda local cuando corresponda. La medición de CPU incluye esa búsqueda.

### Ant Colony System

Orden fijo de argumentos, según el enunciado del Proyecto 2: instancia,
semilla, hormigas, iteraciones, evaporación (`alpha`), peso heurístico
(`beta`), `q0` y archivo de salida.

```bash
python acs.py datos/tai20_5.txt 12345 50 200 1.0 2.0 0.9 resultados/res_acs.csv
```

Restricciones: hormigas e iteraciones > 0, `0 < alpha <= 1`, `beta >= 0` y
`0 <= q0 <= 1`. Ante argumentos o archivos inválidos se muestra un mensaje
de error y el uso correcto.

En pantalla se muestran la instancia, la mejor secuencia (trabajos numerados
desde 1), su makespan, el mejor valor conocido, el RPD y el tiempo. El CSV
registra, para cada iteración, la instancia, la semilla, los parámetros, la
mejor secuencia de la iteración y la mejor global con sus makespans, el mejor
valor conocido, el RPD y el tiempo acumulado:

```
RPD(%) = (C_max obtenido - C_max mejor conocido) / C_max mejor conocido × 100
```

La misma semilla, instancia y parámetros entregan siempre la misma secuencia
y el mismo makespan.

## CSV y tiempo de CPU comunes

AG, AM y ACS usan el mismo escritor de `operadores.py`, con las mismas
columnas y una fila por generación o iteración. `algoritmo` identifica el
método; los parámetros que no le corresponden quedan vacíos. Las secuencias
se guardan desde 1 y `rpd` corresponde a `mejor_makespan`, el mejor acumulado.
Los valores se guardan sin redondeo adicional; se redondean al mostrarlos.

`tiempo_segundos` mide CPU acumulada con `process_time()`, desde antes de
inicializar cada algoritmo. Incluye la población inicial de AG/AM, la
heurística y feromonas iniciales de ACS, y la búsqueda local de AM. Excluye
lectura de datos, escritura del CSV e impresión. La última fila contiene el
resultado y tiempo final de la ejecución; las anteriores permiten graficar
la convergencia.

Los CSV de ACS generados antes de este cambio contienen tiempo transcurrido
medido con `perf_counter()`. Es necesario repetir esas ejecuciones para
comparar tiempos de CPU; los resultados antiguos no se convierten automáticamente.
`experimentos.py` conserva su formato de resumen (una fila por ejecución)
y toma el tiempo de CPU de ACS en las nuevas ejecuciones.

## Algoritmo ACS

`acs.py` muestra las etapas del algoritmo; los detalles están en `operadores.py`:

```
inicializar                τ0 = 1 / (n · C_max(SPT)), matriz τ, heurística η
repetir por iteración:
    construir soluciones   cada hormiga arma una permutación + actualización local
    evaluar soluciones     makespan de cada permutación
    actualizar feromonas   depósito de la mejor hormiga de la iteración
    actualizar mejor       se conserva la mejor solución global
```

Decisiones de diseño:

- **Solución:** permutación de trabajos, sin regreso al trabajo inicial.
- **Grafo:** `τ[i, j]` es la deseabilidad de programar `j` inmediatamente
  después de `i`. Es una matriz **dirigida** (no simétrica) y tiene una fila
  extra para un nodo de inicio ficticio, de modo que la colonia también
  aprende qué trabajo conviene programar primero.
- **Heurística:** `η[i, j] = 1 / (1 + ocio)`, donde
  `ocio = Σ_k max(0, p[j, k] - p[i, k+1])` estima el tiempo que la máquina
  `k+1` espera a `j` cuando sigue a `i`. Desde el inicio, el ocio es
  `Σ_{k<m} p[j, k]`. Se probó primero la regla SPT (`η_j = 1 / Σ_k p[j, k]`),
  pero no depende de la transición y su secuencia tiene un RPD de 26 % en
  ta041, similar al de una permutación aleatoria (28 %); con ella ACS quedaba
  alrededor de 14 % en ta041, frente a ~10 % con la heurística de ocio.
- **Regla de transición:** con probabilidad `q0` se elige el trabajo con mayor
  `τ[i, j] · η[i, j]^β` (explotación); si no, se sortea proporcionalmente a
  ese valor (exploración).
- **Actualización local:** `τ[i, j] ← (1 - α) τ[i, j] + α τ0` en cada arista usada.
- **Actualización global:** `τ[i, j] ← (1 - α) τ[i, j] + α / C_max` en las
  aristas de la mejor hormiga de la iteración, lo que mantiene el orden
  *actualizar feromonas → actualizar mejor solución* del enunciado.

## Pruebas

```bash
python tests.py
```

Verifican que:

- las instancias se leen correctamente (tamaños, cotas y tiempos de ta001);
- el makespan coincide con un ejemplo de 3 trabajos × 2 máquinas calculado a mano;
- se rechazan secuencias inválidas y el RPD se calcula bien;
- la heurística, la feromona inicial y las actualizaciones local y global
  siguen sus fórmulas;
- las hormigas generan permutaciones válidas;
- el algoritmo es reproducible y la mejor solución mejora o se mantiene.
- AG conserva permutaciones, élite y padres; su resultado y CSV son coherentes.
- AM aplica búsqueda local en la frecuencia indicada, mantiene la
  reproducibilidad y respeta el límite de evaluaciones de vecinos.

## Experimentos

```bash
python experimentos.py                 # genera resultados/experimentos.csv
python graficar.py resultados/experimentos.csv graficos/experimentos.pdf
```

Configuración base: 20 hormigas, 100 iteraciones, `alpha = 0.1`, `beta = 2.0`,
`q0 = 0.9`. Se varía un parámetro a la vez y cada configuración se ejecuta
con las semillas 1 a 5 en las tres instancias.

## Gráficos

```bash
python graficar.py resultados/res_acs_tai50_10.csv graficos/convergencia_tai50_10.pdf
```

Si se omite el segundo argumento se usa `graficos/<nombre del CSV>.pdf`.
`graficar.py` reconoce si el CSV proviene de `acs.py` (curva de convergencia)
o de `experimentos.py` (sensibilidad a los parámetros y calidad vs. tiempo).
