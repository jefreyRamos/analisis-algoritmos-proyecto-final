"""Pruebas de integridad del corpus compartido por todos los requerimientos.

Ejecucion: python -m unittest discover -s tests
"""
import unittest

from src.corpus.extraccion import cargar_corpus, cargar_metadatos
from src.corpus.preprocesamiento import frecuencias_corpus, tokens_documento


class TestCorpus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.corpus = cargar_corpus()

    def test_veinte_articulos_en_orden(self):
        self.assertEqual([d["id"] for d in self.corpus], list(range(1, 21)))

    def test_campos_completos(self):
        for doc in self.corpus:
            with self.subTest(id=doc["id"]):
                self.assertTrue(doc["titulo"])
                self.assertTrue(doc["autores"])
                self.assertIsInstance(doc["anio"], int)
                self.assertTrue(doc["revista"])
                # Un abstract real tiene entre ~100 y ~350 palabras.
                self.assertTrue(100 <= len(doc["abstract"].split()) <= 350)

    def test_metadatos_coinciden_con_json(self):
        metadatos = cargar_metadatos()
        for doc in self.corpus:
            self.assertEqual(doc["autores"], metadatos[doc["id"]]["autores"])

    def test_tokens_documento_suman_frecuencias(self):
        total = sum(len(tokens_documento(d)) for d in self.corpus)
        self.assertEqual(total, sum(f for _, f in frecuencias_corpus(self.corpus)))


if __name__ == "__main__":
    unittest.main()
