"""Bucket Sort (ordenamiento por cubetas), descendente y estable.

Reparte los n elementos en m cubetas segun el intervalo de su frecuencia,
ordena cada cubeta con Insertion Sort (estable) y concatena las cubetas de
la de mayor intervalo a la de menor.

Complejidad: O(n + m) en promedio si las claves se distribuyen de forma
aproximadamente uniforme entre las cubetas (cada cubeta recibe O(1)
elementos). En el peor caso, todo cae en una cubeta y el Insertion Sort
interno cuesta O(n^2).
"""
from __future__ import annotations

from typing import List, Optional, Tuple

Par = Tuple[str, int]


def _insertion_sort_desc(cubeta: List[Par]) -> None:
    """Insertion Sort descendente en sitio. Solo desplaza si la clave anterior
    es estrictamente menor, por lo que los empates no se mueven (estable)."""
    for i in range(1, len(cubeta)):
        actual = cubeta[i]
        j = i - 1
        while j >= 0 and cubeta[j][1] < actual[1]:
            cubeta[j + 1] = cubeta[j]
            j -= 1
        cubeta[j + 1] = actual


def bucket_sort(pares: List[Par], num_cubetas: Optional[int] = None) -> List[Par]:
    n = len(pares)
    if n == 0:
        return []

    minimo = maximo = pares[0][1]
    for _, f in pares:
        if f < minimo:
            minimo = f
        if f > maximo:
            maximo = f

    m = num_cubetas if num_cubetas is not None else n
    rango = maximo - minimo + 1

    # 1. Distribucion: la cubeta i cubre las claves en
    #    [minimo + i*rango/m, minimo + (i+1)*rango/m). O(n)
    cubetas: List[List[Par]] = [[] for _ in range(m)]
    for par in pares:
        indice = (par[1] - minimo) * m // rango
        cubetas[indice].append(par)

    # 2. Ordenamiento interno y 3. concatenacion de mayor a menor. O(n + m)
    salida: List[Par] = []
    for i in range(m - 1, -1, -1):
        if cubetas[i]:
            _insertion_sort_desc(cubetas[i])
            salida.extend(cubetas[i])
    return salida
