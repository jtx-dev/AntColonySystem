# Checklist del proyecto: ACS y comparación para PFSP

Avanzaremos por fases, manteniendo funciones simples y la estructura actual.

**Estado actual:** preproyecto de ACS para Berlin52 completado (fases 1 a 6).
El próximo objetivo es la fase 7: adaptar ACS al PFSP del Proyecto 2.

## Fase 1 — Ordenar el avance actual

- [x] Hacer que `leer_datos` reciba la ruta de la instancia.
- [x] Hacer que `calcular_distancias` devuelva la matriz.
- [x] Mover la ejecución principal de `operadores.py` a `acs.py`.
- [x] Corregir los comentarios para distinguir coordenadas y distancias.
- [x] Comprobar la lectura de las 52 ciudades y la matriz resultante.

## Fase 2 — Representar y evaluar recorridos TSP

- [x] Representar un recorrido como una lista de ciudades.
- [x] Calcular su distancia total, incluyendo el regreso al inicio.
- [x] Verificar que cada ciudad aparezca exactamente una vez.
- [x] Comprobar el cálculo con un ejemplo pequeño conocido.
- [x] Confirmar la convención de distancias de Berlin52.

Berlin52 utiliza la convención `EUC_2D` de TSPLIB: cada distancia euclidiana se redondea al entero más cercano. TSPLIB advierte que evaluar estas distancias como números decimales define un problema diferente. Fuentes: [TSPLIB](https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/) y [TSPLIB FAQ](https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/TSPFAQ.html).

## Fase 3 — Preparar ACS

- [x] Definir los parámetros: hormigas, iteraciones, `q0`, peso heurístico y actualización de feromonas.
- [x] Controlar la aleatoriedad mediante una semilla.
- [x] Inicializar la matriz de feromonas.
- [x] Calcular la información heurística a partir de las distancias.
- [x] Excluir la ciudad actual y las visitadas de las opciones de movimiento.

## Fase 4 — Construir una solución con una hormiga

- [x] Elegir la ciudad inicial.
- [x] Mantener la lista de ciudades pendientes.
- [x] Implementar la elección por explotación.
- [x] Implementar la elección probabilística por exploración.
- [x] Aplicar la actualización local de feromonas.
- [x] Completar y evaluar el recorrido, incluido su cierre.

## Fase 5 — Completar y validar ACS para TSP

- [x] Ejecutar todas las hormigas de cada iteración.
- [x] Registrar la mejor solución de la iteración y la mejor global.
- [x] Aplicar la actualización global con la mejor hormiga elegida.
- [x] Repetir el proceso durante las iteraciones indicadas.
- [x] Registrar la evolución del mejor costo.
- [x] Verificar recorridos válidos y resultados reproducibles con la misma semilla.
- [x] Evaluar el desempeño sobre Berlin52.

## Fase 6 — Ejecución y resultados básicos

- [x] Recibir instancia, semilla y parámetros desde la consola.
- [x] Mostrar mensajes claros ante argumentos o archivos inválidos.
- [x] Mostrar el mejor recorrido, su costo y el tiempo empleado.
- [x] Guardar los resultados y la convergencia en CSV.
- [x] Implementar un gráfico sencillo en `graficar.py`.
- [x] Documentar cómo ejecutar el programa en el README.
- [x] Excluir archivos generados como `__pycache__`.

## Fase 7 — Adaptar ACS a PFSP

- [ ] Incorporar la lectura de instancias Taillard.
- [ ] Representar una solución como una permutación de trabajos.
- [ ] Implementar el cálculo común del makespan.
- [ ] Verificarlo con un ejemplo pequeño calculado manualmente.
- [ ] Adaptar las feromonas a transiciones entre trabajos.
- [ ] Elegir e implementar una heurística sencilla para PFSP.
- [ ] Adaptar la construcción y evaluación de soluciones, sin regreso al trabajo inicial.
- [ ] Adaptar las actualizaciones de feromonas al objetivo de minimizar el makespan.
- [ ] Verificar soluciones válidas y reproducibilidad.

## Fase 8 — Integrar AG y AM

- [ ] Revisar el código previo de AG y AM, si está disponible.
- [ ] Compartir la lectura de instancias y el evaluador de makespan.
- [ ] Completar AG con selección, cruce para permutaciones, mutación y elitismo.
- [ ] Completar AM con búsqueda local y definir su frecuencia o intensidad.
- [ ] Mantener ejecutables separados: `ag.py`, `am.py` y `acs.py`.
- [ ] Respetar los argumentos por consola indicados en el enunciado.
- [ ] Verificar permutaciones válidas y reproducibilidad en los tres algoritmos.

## Fase 9 — Comparación experimental

- [ ] Seleccionar instancias de tamaños 20×5, 50×10 y 100×10.
- [ ] Registrar el mejor valor conocido de cada instancia y su fuente.
- [ ] Definir semillas, repeticiones y condiciones comparables.
- [ ] Registrar los parámetros utilizados en cada ejecución.
- [ ] Ejecutar AG, AM y ACS sobre las mismas instancias.
- [ ] Calcular makespan, RPD y tiempo de CPU.
- [ ] Preparar tablas comparativas y gráficos de convergencia.
- [ ] Analizar calidad de soluciones, variabilidad y escalabilidad.

## Fase 10 — Informe y entrega

- [ ] Preparar el artículo con la plantilla IEEE Transactions.
- [ ] Redactar introducción, metodología y configuración experimental.
- [ ] Incorporar resultados y analizar exploración y explotación.
- [ ] Redactar conclusiones, trabajo futuro y resumen.
- [ ] Añadir referencias en formato IEEE.
- [ ] Revisar la extensión sugerida de 2000–3000 palabras.
- [ ] Completar el README con instrucciones y dependencias.
- [ ] Comprobar los comandos de ejecución y los archivos de entrega.
- [ ] Revisar el cumplimiento del enunciado y la pauta de evaluación.
