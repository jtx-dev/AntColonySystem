import numpy as np
def leer_datos():
    coordenadas = []

    with open('datos/instancia.txt', 'r') as lector:
        for linea in lector:
            partes = linea.split()
            if len(partes) <= 3 :
                x = coordenadas.append(partes[1])
                y = coordenadas.append(partes[2])
    return (coordenadas)
leer_datos()