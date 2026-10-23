"""Requerimiento 3 - Busqueda exacta de patrones en los abstracts.

Plan de modulos (cada uno expone buscar(texto, patron) -> lista de posiciones,
sin usar find(), index() ni expresiones regulares):
    kmp.py          Knuth-Morris-Pratt (tabla de prefijo-sufijo)
    boyer_moore.py  regla del caracter malo y del sufijo bueno
    rabin_karp.py   rolling hash con aritmetica modular

Las pruebas deben comparar contra una busqueda ingenua de referencia.
"""
