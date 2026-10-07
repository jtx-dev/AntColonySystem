from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from operadores import calcular_distancia_recorrido, calcular_distancias, leer_datos


@dataclass
class ParametrosACS:
    hormigas: int = 10
    iteraciones: int = 100
    q0: float = 0.9
    peso_heuristico: float = 2.0
    evaporacion_local: float = 0.1
    evaporacion_global: float = 0.1
    feromona_inicial: float = 1.0
    semilla: int | None = 42

    def __post_init__(self):
        if self.hormigas <= 0:
            raise ValueError('La cantidad de hormigas debe ser mayor que cero.')
        if self.iteraciones <= 0:
            raise ValueError('La cantidad de iteraciones debe ser mayor que cero.')
        if not 0 <= self.q0 <= 1:
            raise ValueError('q0 debe estar entre 0 y 1.')
        if self.peso_heuristico < 0:
            raise ValueError('El peso heurístico no puede ser negativo.')
        if not 0 <= self.evaporacion_local <= 1:
            raise ValueError('La evaporación local debe estar entre 0 y 1.')
        if not 0 <= self.evaporacion_global <= 1:
            raise ValueError('La evaporación global debe estar entre 0 y 1.')
        if self.feromona_inicial <= 0:
            raise ValueError('La feromona inicial debe ser mayor que cero.')


def crear_generador(semilla):
    return np.random.default_rng(semilla)


def inicializar_feromonas(n, feromona_inicial):
    feromonas = np.full((n, n), feromona_inicial, dtype=float)
    np.fill_diagonal(feromonas, 0.0)
    return feromonas


def calcular_heuristica(matriz_distancias):
    heuristica = np.zeros_like(matriz_distancias, dtype=float)
    np.divide(
        1.0,
        matriz_distancias,
        out=heuristica,
        where=matriz_distancias > 0,
    )
    return heuristica


def ciudades_disponibles(ciudad_actual, visitadas, n):
    visitadas = set(visitadas)
    return [
        ciudad
        for ciudad in range(n)
        if ciudad != ciudad_actual and ciudad not in visitadas
    ]


def preparar_acs(matriz_distancias, parametros):
    n = len(matriz_distancias)
    generador = crear_generador(parametros.semilla)
    feromonas = inicializar_feromonas(n, parametros.feromona_inicial)
    heuristica = calcular_heuristica(matriz_distancias)
    return generador, feromonas, heuristica


def main():
    parametros = ParametrosACS()
    entrada = Path(__file__).parent / 'datos' / 'instancia.txt'
    coordenadas, n = leer_datos(entrada)
    matriz_distancias = calcular_distancias(coordenadas, n)
    _, feromonas, heuristica = preparar_acs(matriz_distancias, parametros)

    print(f'Ciudades leídas: {n}')
    print(f'Tamaño de la matriz: {matriz_distancias.shape}')
    print(f'Hormigas: {parametros.hormigas}')
    print(f'Iteraciones: {parametros.iteraciones}')
    print(f'Semilla: {parametros.semilla}')
    print(f'Tamaño de la matriz de feromonas: {feromonas.shape}')

print(f'Ciudades leídas: {n}')
print(f'Tamaño de la matriz: {matriz_distancias.shape}')

cantidad_mostrada = min(10, n)
ciudades = range(1, cantidad_mostrada + 1)
vista_previa = pd.DataFrame(
    matriz_distancias[:cantidad_mostrada, :cantidad_mostrada],
    index=ciudades,
    columns=ciudades,
)
vista_previa.index.name = 'Ciudad'

    vista_heuristica = pd.DataFrame(
        heuristica[:cantidad_mostrada, :cantidad_mostrada],
        index=ciudades,
        columns=ciudades,
    )
    vista_heuristica.index.name = 'Ciudad'

    print(f'\nHeurística de las primeras {cantidad_mostrada} ciudades:')
    print(vista_heuristica.to_string())

    recorrido = list(range(n))
    distancia = calcular_distancia_recorrido(recorrido, matriz_distancias)
    print(f'\nDistancia del recorrido 1 -> 2 -> ... -> {n} -> 1: {distancia}')

    ejemplo_visitadas = {0, 1, 2}
    disponibles = ciudades_disponibles(2, ejemplo_visitadas, n)
    print(f'Ciudades disponibles desde ciudad 3 con 1, 2 y 3 visitadas: {disponibles}')


