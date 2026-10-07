import numpy as np
import pandas as pd


def leer_datos(entrada):
    # Lee el identificador y las coordenadas de cada ciudad.
    coordenadas = pd.read_table(entrada, header=None, sep=r'\s+')
    coordenadas = coordenadas.drop(columns=0).to_numpy()
    n = coordenadas.shape[0]
    return coordenadas, n


def calcular_distancias(coordenadas, n):
    # Berlin52 usa distancias euclidianas redondeadas al entero más cercano.
    matriz_distancias = np.zeros((n, n), dtype=int)
    for i in range(n - 1):
        for j in range(i + 1, n):
            distancia = np.sqrt(
                np.sum(np.square(coordenadas[i] - coordenadas[j]))
            )
            matriz_distancias[i][j] = int(distancia + 0.5)
            matriz_distancias[j][i] = matriz_distancias[i][j]
    return matriz_distancias


def recorrido_valido(recorrido, n):
    return len(recorrido) == n and set(recorrido) == set(range(n))


def calcular_distancia_recorrido(recorrido, matriz_distancias):
    n = len(matriz_distancias)
    if not recorrido_valido(recorrido, n):
        raise ValueError('El recorrido debe visitar cada ciudad exactamente una vez.')

    distancia_total = 0
    for i in range(n):
        origen = recorrido[i]
        destino = recorrido[(i + 1) % n]
        distancia_total += matriz_distancias[origen][destino]

    return int(distancia_total)

# ------- ACS ------- #
def calcular_probabilidades(tau, visibilidad, actual, libres):
    pesos = tau[actual, libres] * visibilidad[actual, libres]
    return pesos/pesos.sum()

def elegir_siguiente(libres, probabilidades, q0):
    if np.random.rand() < q0:
        return libres[np.argmax(probabilidades)] # explotación
    return np.random.choice(libres, p=probabilidades) # exploración

def construir_recorrido (tau, visibilidad, tau0, rho, q0):
    n = len(tau)
    recorrido = [np.random.randint(n)]
    while len(recorrido) < n:
        actual = recorrido[-1]
        libres = np.setdiff1d(np.arange(n), recorrido) # Ciudades sin visitar
        probabilidades = calcular_probabilidades(tau, visibilidad, actual, libres)
        siguiente = elegir_siguiente(libres, probabilidades, q0)
        # Falta paso de actualizar feromona.
        recorrido.append(siguiente)

        
