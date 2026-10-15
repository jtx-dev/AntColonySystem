import numpy as np
import pandas as pd


def leer_datos(entrada):
    """Lee identificador, coordenada X y coordenada Y de cada ciudad."""
    datos = pd.read_table(entrada, header=None, sep=r'\s+')
    if datos.shape[1] < 3 or datos.empty:
        raise ValueError('La instancia debe contener: ciudad, coordenada X y coordenada Y.')

    coordenadas = datos.iloc[:, 1:3].to_numpy(dtype=float)
    return coordenadas, len(coordenadas)


def calcular_distancias(coordenadas, n):
    """Calcula las distancias EUC_2D redondeadas como indica TSPLIB."""
    matriz_distancias = np.zeros((n, n), dtype=int)
    for i in range(n - 1):
        for j in range(i + 1, n):
            distancia = np.sqrt(np.sum(np.square(coordenadas[i] - coordenadas[j])))
            matriz_distancias[i, j] = int(distancia + 0.5)
            matriz_distancias[j, i] = matriz_distancias[i, j]
    return matriz_distancias


def recorrido_valido(recorrido, n):
    return len(recorrido) == n and set(recorrido) == set(range(n))


def calcular_distancia_recorrido(recorrido, matriz_distancias):
    n = len(matriz_distancias)
    if not recorrido_valido(recorrido, n):
        raise ValueError('El recorrido debe visitar cada ciudad exactamente una vez.')

    return int(sum(
        matriz_distancias[recorrido[i], recorrido[(i + 1) % n]]
        for i in range(n)
    ))


def calcular_heuristica(matriz_distancias):
    heuristica = np.zeros_like(matriz_distancias, dtype=float)
    np.divide(1.0, matriz_distancias, out=heuristica, where=matriz_distancias > 0)
    return heuristica


def recorrido_vecino_mas_cercano(matriz_distancias, inicio=0):
    n = len(matriz_distancias)
    recorrido = [inicio]
    pendientes = set(range(n)) - {inicio}

    while pendientes:
        actual = recorrido[-1]
        siguiente = min(pendientes, key=lambda ciudad: matriz_distancias[actual, ciudad])
        recorrido.append(siguiente)
        pendientes.remove(siguiente)
    return recorrido


def calcular_feromona_inicial(matriz_distancias):
    recorrido = recorrido_vecino_mas_cercano(matriz_distancias)
    costo = calcular_distancia_recorrido(recorrido, matriz_distancias)
    return 1.0 / (len(matriz_distancias) * costo)


def inicializar_feromonas(n, feromona_inicial):
    feromonas = np.full((n, n), feromona_inicial, dtype=float)
    np.fill_diagonal(feromonas, 0.0)
    return feromonas


def calcular_probabilidades(feromonas, heuristica, actual, libres, beta):
    libres = np.asarray(libres, dtype=int)
    pesos = feromonas[actual, libres] * heuristica[actual, libres] ** beta
    total = pesos.sum()
    if total <= 0:
        return np.full(len(libres), 1.0 / len(libres))
    return pesos / total


def elegir_siguiente(libres, probabilidades, q0, generador):
    libres = np.asarray(libres, dtype=int)
    if generador.random() < q0:
        return int(libres[np.argmax(probabilidades)])
    return int(generador.choice(libres, p=probabilidades))


def actualizar_feromona_local(feromonas, origen, destino, evaporacion, feromona_inicial):
    nueva = (
        (1 - evaporacion) * feromonas[origen, destino]
        + evaporacion * feromona_inicial
    )
    feromonas[origen, destino] = nueva
    feromonas[destino, origen] = nueva


def construir_recorrido(
    feromonas,
    heuristica,
    feromona_inicial,
    evaporacion,
    beta,
    q0,
    generador,
):
    n = len(feromonas)
    recorrido = [int(generador.integers(n))]

    while len(recorrido) < n:
        actual = recorrido[-1]
        visitadas = set(recorrido)
        libres = [ciudad for ciudad in range(n) if ciudad not in visitadas]
        probabilidades = calcular_probabilidades(
            feromonas, heuristica, actual, libres, beta
        )
        siguiente = elegir_siguiente(libres, probabilidades, q0, generador)
        actualizar_feromona_local(
            feromonas, actual, siguiente, evaporacion, feromona_inicial
        )
        recorrido.append(siguiente)

    actualizar_feromona_local(
        feromonas, recorrido[-1], recorrido[0], evaporacion, feromona_inicial
    )
    return recorrido


def actualizar_feromona_global(feromonas, recorrido, costo, evaporacion):
    deposito = 1.0 / costo
    for i, origen in enumerate(recorrido):
        destino = recorrido[(i + 1) % len(recorrido)]
        nueva = (1 - evaporacion) * feromonas[origen, destino] + evaporacion * deposito
        feromonas[origen, destino] = nueva
        feromonas[destino, origen] = nueva
