import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

import numpy as np

from operadores import (
    actualizar_feromona_global,
    calcular_distancia_recorrido,
    calcular_distancias,
    calcular_feromona_inicial,
    calcular_heuristica,
    construir_recorrido,
    inicializar_feromonas,
    leer_datos,
)


@dataclass
class ParametrosACS:
    hormigas: int
    iteraciones: int
    evaporacion: float
    peso_heuristico: float
    q0: float
    semilla: int

    def __post_init__(self):
        if self.hormigas <= 0:
            raise ValueError('La cantidad de hormigas debe ser mayor que cero.')
        if self.iteraciones <= 0:
            raise ValueError('La cantidad de iteraciones debe ser mayor que cero.')
        if not 0 < self.evaporacion <= 1:
            raise ValueError('La evaporación debe estar entre 0 (excluido) y 1.')
        if self.peso_heuristico < 0:
            raise ValueError('El peso heurístico no puede ser negativo.')
        if not 0 <= self.q0 <= 1:
            raise ValueError('q0 debe estar entre 0 y 1.')


def ejecutar_acs(matriz_distancias, parametros):
    generador = np.random.default_rng(parametros.semilla)
    feromona_inicial = calcular_feromona_inicial(matriz_distancias)
    feromonas = inicializar_feromonas(len(matriz_distancias), feromona_inicial)
    heuristica = calcular_heuristica(matriz_distancias)
    mejor_recorrido = None
    mejor_costo = float('inf')
    historial = []
    inicio = perf_counter()

    for iteracion in range(1, parametros.iteraciones + 1):
        mejor_recorrido_iteracion = None
        mejor_costo_iteracion = float('inf')

        for _ in range(parametros.hormigas):
            recorrido = construir_recorrido(
                feromonas,
                heuristica,
                feromona_inicial,
                parametros.evaporacion,
                parametros.peso_heuristico,
                parametros.q0,
                generador,
            )
            costo = calcular_distancia_recorrido(recorrido, matriz_distancias)
            if costo < mejor_costo_iteracion:
                mejor_recorrido_iteracion = recorrido.copy()
                mejor_costo_iteracion = costo

        if mejor_costo_iteracion < mejor_costo:
            mejor_recorrido = mejor_recorrido_iteracion
            mejor_costo = mejor_costo_iteracion

        actualizar_feromona_global(
            feromonas,
            mejor_recorrido,
            mejor_costo,
            parametros.evaporacion,
        )
        historial.append({
            'iteracion': iteracion,
            'mejor_recorrido_iteracion': ' '.join(
                str(ciudad + 1) for ciudad in mejor_recorrido_iteracion
            ),
            'mejor_costo_iteracion': int(mejor_costo_iteracion),
            'mejor_recorrido': ' '.join(str(ciudad + 1) for ciudad in mejor_recorrido),
            'mejor_costo': int(mejor_costo),
            'tiempo_segundos': perf_counter() - inicio,
        })

    return mejor_recorrido, int(mejor_costo), historial


def guardar_resultados(salida, instancia, parametros, historial):
    salida = Path(salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    campos = [
        'instancia',
        'semilla',
        'hormigas',
        'iteraciones',
        'evaporacion',
        'peso_heuristico',
        'q0',
        'iteracion',
        'mejor_recorrido_iteracion',
        'mejor_costo_iteracion',
        'mejor_recorrido',
        'mejor_costo',
        'tiempo_segundos',
    ]

    with salida.open('w', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for registro in historial:
            escritor.writerow({
                'instancia': Path(instancia).name,
                'semilla': parametros.semilla,
                'hormigas': parametros.hormigas,
                'iteraciones': parametros.iteraciones,
                'evaporacion': parametros.evaporacion,
                'peso_heuristico': parametros.peso_heuristico,
                'q0': parametros.q0,
                **registro,
            })


def crear_parser():
    parser = argparse.ArgumentParser(
        description='Resuelve una instancia TSP mediante Ant Colony System.'
    )
    parser.add_argument('instancia', help='Archivo con ciudad, coordenada X y coordenada Y.')
    parser.add_argument('hormigas', type=int)
    parser.add_argument('iteraciones', type=int)
    parser.add_argument('evaporacion', type=float, help='Parámetro alpha de ACS.')
    parser.add_argument('peso_heuristico', type=float, help='Parámetro beta de ACS.')
    parser.add_argument('q0', type=float)
    parser.add_argument('semilla', type=int)
    parser.add_argument('salida', help='Archivo CSV de salida.')
    return parser



parser = crear_parser()
argumentos = parser.parse_args()

try:
    parametros = ParametrosACS(
        argumentos.hormigas,
        argumentos.iteraciones,
        argumentos.evaporacion,
        argumentos.peso_heuristico,
        argumentos.q0,
        argumentos.semilla,
    )
    coordenadas, n = leer_datos(argumentos.instancia)
    matriz_distancias = calcular_distancias(coordenadas, n)
    recorrido, costo, historial = ejecutar_acs(matriz_distancias, parametros)
    guardar_resultados(argumentos.salida, argumentos.instancia, parametros, historial)
except (OSError, ValueError) as error:
    parser.error(str(error))

print('Mejor recorrido:', ' -> '.join(str(ciudad + 1) for ciudad in recorrido))
print('Costo:', costo)
print(f"Tiempo: {historial[-1]['tiempo_segundos']:.3f} segundos")
print('Resultados guardados en:', argumentos.salida)
