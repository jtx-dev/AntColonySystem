import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt



parser = argparse.ArgumentParser(description='Grafica la convergencia de una ejecución ACS.')
parser.add_argument('resultados', help='Archivo CSV generado por acs.py.')
parser.add_argument(
    'salida',
    nargs='?',
    default='graficos/grafico1.pdf',
    help='Gráfico PDF de salida.',
)
argumentos = parser.parse_args()

with open(argumentos.resultados, newline='', encoding='utf-8') as archivo:
    filas = list(csv.DictReader(archivo))
if not filas:
    parser.error('El archivo de resultados no contiene datos.')

iteraciones = [int(fila['iteracion']) for fila in filas]
costos = [int(fila['mejor_costo']) for fila in filas]
salida = Path(argumentos.salida)
salida.parent.mkdir(parents=True, exist_ok=True)

plt.figure(figsize=(7, 4))
plt.plot(iteraciones, costos)
plt.xlabel('Iteración')
plt.ylabel('Mejor costo')
plt.title('Convergencia de ACS')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(salida)
print('Gráfico guardado en:', salida)
