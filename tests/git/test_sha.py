#!env python3
import unittest

from cicd_sim.git import SHA

class TestGitSHA(unittest.TestCase):

    def test_initial_value(self):
        sha = SHA()
        first = sha.generate_next()
        self.assertEqual(first, "0000001")

    def test_consecutive_values(self):
        sha = SHA()
        _ = sha.generate_next()
        next = sha.generate_next()
        self.assertEqual(next, "0000002")

    def test_get_current(self):
        sha = SHA()
        first = sha.generate_next()
        first2 = sha.get_current()
        self.assertEqual(first, first2)
