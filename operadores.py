import numpy as np
import pandas as pd


def leer_datos(entrada):
    # Lee el identificador y las coordenadas de cada ciudad.
    coordenadas = pd.read_table(entrada, header=None, sep=r'\s+')
    coordenadas = coordenadas.drop(columns=0).to_numpy()
    n = coordenadas.shape[0]
    return coordenadas, n


def calcular_distancias(coordenadas, n):
    # Calcula la distancia euclidiana entre cada par de ciudades.
    matriz_distancias = np.zeros((n, n), dtype=float)
    for i in range(n - 1):
        for j in range(i + 1, n):
            matriz_distancias[i][j] = np.sqrt(
                np.sum(np.square(coordenadas[i] - coordenadas[j]))
            )
            matriz_distancias[j][i] = matriz_distancias[i][j]
    return matriz_distancias
