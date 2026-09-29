import numpy as np
import pandas as pd
def leer_datos():

    # Función: leer datos
    # Esta función lee los datos de la instancia.txt
    # almacenandolos en una matriz de distancias

    entrada = 'datos/instancia.txt'
    coordenadas = pd.read_table(entrada , header = None, sep = '\s+', skiprows = 0, skipfooter = 0)
    coordenadas = coordenadas.drop(columns=0).to_numpy()
    n = coordenadas.shape[0]
    return(coordenadas , n)
def calcular_distancias(coordenadas, n):
    matriz_distancias=np.full((n, n), fill_value = -1.0, dtype = float)
    for i in range(n-1):
        for j in range(i+1, n):
            matriz_distancias[i][j] = np.sqrt(np.sum(np.square(coordenadas[i]- coordenadas[j])))
            matriz_distancias[j][i] = matriz_distancias[i][j]
    print(matriz_distancias)
coordenadas, n = leer_datos()
calcular_distancias(coordenadas, n)