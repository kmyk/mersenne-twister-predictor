import unittest

from mt19937predictor import tempering, untempering
import random

class UnitTest(unittest.TestCase):

    def test_untempering(self):
        for _ in range(100):
            y = random.randrange(2 ** 32)
            self.assertEqual(y, untempering(tempering(y)))
