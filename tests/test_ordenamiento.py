"""Pruebas de los algoritmos de ordenamiento.

Ejecucion: python -m unittest discover -s tests
"""
import random
import unittest

from src.ordenamiento import ALGORITMOS, bucket_sort, radix_sort


def referencia(pares):
    # sorted es estable: los empates quedan en orden de entrada.
    return sorted(pares, key=lambda p: -p[1])


class TestOrdenamiento(unittest.TestCase):
    def verificar(self, pares):
        for nombre, alg in ALGORITMOS.items():
            with self.subTest(algoritmo=nombre):
                self.assertEqual(alg(pares), referencia(pares))

    def test_vacio(self):
        self.verificar([])

    def test_un_elemento(self):
        self.verificar([("ai", 5)])

    def test_todos_iguales_conserva_orden(self):
        self.verificar([(f"t{i}", 3) for i in range(50)])

    def test_ya_ordenado_y_al_reves(self):
        pares = [(f"t{i}", i) for i in range(100)]
        self.verificar(pares)
        self.verificar(pares[::-1])

    def test_incluye_ceros(self):
        self.verificar([("a", 0), ("b", 7), ("c", 0), ("d", 10)])

    def test_aleatorio_estable(self):
        rnd = random.Random(2026)
        for _ in range(200):
            n = rnd.randint(1, 300)
            k = rnd.choice([1, 9, 10, 99, 100, 1000, 12345])
            self.verificar([(f"t{i}", rnd.randint(0, k)) for i in range(n)])

    def test_distribucion_tipo_zipf(self):
        # Como en texto real: pocos terminos muy frecuentes, muchos con frecuencia 1.
        rnd = random.Random(7)
        self.verificar([(f"t{i}", max(1, int(500 / (1 + rnd.paretovariate(1.2))))) for i in range(2000)])

    def test_radix_otras_bases(self):
        pares = [(f"t{i}", (i * 7919) % 5000) for i in range(500)]
        for base in (2, 16, 256):
            self.assertEqual(radix_sort(pares, base=base), referencia(pares))

    def test_bucket_pocas_cubetas(self):
        pares = [(f"t{i}", (i * 31) % 97) for i in range(400)]
        for m in (1, 5, 1000):
            self.assertEqual(bucket_sort(pares, num_cubetas=m), referencia(pares))

    def test_no_modifica_entrada(self):
        pares = [("a", 2), ("b", 9), ("c", 1)]
        copia = list(pares)
        for alg in ALGORITMOS.values():
            alg(pares)
            self.assertEqual(pares, copia)

    def test_claves_negativas(self):
        for alg in (ALGORITMOS["Counting Sort"], ALGORITMOS["Radix Sort"]):
            with self.assertRaises(ValueError):
                alg([("a", -1)])


if __name__ == "__main__":
    unittest.main()
