"""Counting Sort (ordenamiento por conteo), descendente y estable.

Entrada: lista de pares (termino, frecuencia) con frecuencia entera >= 0.
Salida: nueva lista ordenada de mayor a menor frecuencia. Los empates
conservan el orden de entrada (estabilidad).

Complejidad: O(n + k) en tiempo y O(n + k) en espacio, con
n = numero de terminos y k = frecuencia maxima.
"""
from __future__ import annotations

from typing import List, Tuple

Par = Tuple[str, int]


def counting_sort(pares: List[Par]) -> List[Par]:
    n = len(pares)
    if n == 0:
        return []

    # 1. Rango de claves: O(n)
    k = 0
    for _, f in pares:
        if f < 0:
            raise ValueError("Counting Sort requiere claves enteras no negativas")
        if f > k:
            k = f

    # 2. Histograma de frecuencias: O(n)
    conteo = [0] * (k + 1)
    for _, f in pares:
        conteo[f] += 1

    # 3. Posicion inicial de cada clave en la salida (suma acumulada
    #    recorriendo de la clave mayor a la menor, por ser descendente): O(k)
    inicio = [0] * (k + 1)
    acumulado = 0
    for clave in range(k, -1, -1):
        inicio[clave] = acumulado
        acumulado += conteo[clave]

    # 4. Ubicacion directa de cada elemento. Se recorre la entrada de
    #    izquierda a derecha, por eso los empates mantienen su orden: O(n)
    salida: List[Par] = [None] * n  # type: ignore[list-item]
    for par in pares:
        f = par[1]
        salida[inicio[f]] = par
        inicio[f] += 1

    return salida
