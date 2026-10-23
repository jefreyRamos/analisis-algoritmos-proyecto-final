"""Radix Sort LSD (digito menos significativo primero), descendente y estable.

Ordena por la frecuencia procesando un digito en base b por pasada. Cada
pasada es un Counting Sort estable sobre ese digito (k = b), de modo que el
orden logrado en pasadas anteriores se conserva entre claves con el mismo
digito actual.

Complejidad: O(d * (n + b)), con d = numero de digitos de la clave maxima
en base b. Como d y b son constantes respecto a n, el costo es O(n).
"""
from __future__ import annotations

from typing import List, Tuple

Par = Tuple[str, int]


def _pasada_por_digito(pares: List[Par], divisor: int, base: int) -> List[Par]:
    """Counting Sort estable y descendente sobre el digito (f // divisor) % base."""
    conteo = [0] * base
    for _, f in pares:
        conteo[(f // divisor) % base] += 1

    inicio = [0] * base
    acumulado = 0
    for digito in range(base - 1, -1, -1):
        inicio[digito] = acumulado
        acumulado += conteo[digito]

    salida: List[Par] = [None] * len(pares)  # type: ignore[list-item]
    for par in pares:
        digito = (par[1] // divisor) % base
        salida[inicio[digito]] = par
        inicio[digito] += 1
    return salida


def radix_sort(pares: List[Par], base: int = 10) -> List[Par]:
    if not pares:
        return []
    if base < 2:
        raise ValueError("La base debe ser >= 2")

    maximo = 0
    for _, f in pares:
        if f < 0:
            raise ValueError("Radix Sort requiere claves enteras no negativas")
        if f > maximo:
            maximo = f

    resultado = list(pares)
    divisor = 1
    while True:
        resultado = _pasada_por_digito(resultado, divisor, base)
        divisor *= base
        if maximo // divisor == 0:
            break
    return resultado
