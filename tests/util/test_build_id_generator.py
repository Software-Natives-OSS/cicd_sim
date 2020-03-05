#!env python3
import unittest
import random

from cicd_sim import BuildIdGenerator

class TestBuildIdGenerator(unittest.TestCase):

    def test_every_id_unique(self):
        id_gen = BuildIdGenerator()
        id_1 = id_gen.generate_id()
        id_2 = id_gen.generate_id()
        self.assertNotEqual(id_1, id_2)
        
    def test_equal_dates_with_explicit_seed(self):
        random.seed(123)
        id_1 = BuildIdGenerator().generate_id()
        random.seed(123)
        id_2 = BuildIdGenerator().generate_id()

        self.assertEqual(id_1, id_2)
        