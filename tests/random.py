import unittest

from mt19937predictor import MT19937Predictor
import random

class PythonStdlibTest(unittest.TestCase):

    def test_int32(self):
        inst = random.Random()
        predictor = MT19937Predictor()
        for _ in range(624):
            x = inst.getrandbits(32)
            predictor.setrandbits(x, 32)
        for _ in range(100):
            x = inst.getrandbits(32)
            y = predictor.getrandbits(32)
            self.assertEqual(x, y)

    def test_getrandbits_arbitrary(self):
        inst = random.Random()
        predictor = MT19937Predictor()
        for _ in range(624):
            x = inst.getrandbits(32)
            predictor.setrandbits(x, 32)
        for _ in range(1000):
            k = random.randint(1, 100)
            x = inst.getrandbits(k)
            y = predictor.getrandbits(k)
            self.assertEqual(x, y)

    def test_setrandbits_arbitrary(self):
        inst = random.Random()
        predictor = MT19937Predictor()
        entropy = 624
        while entropy > 0:
            k = random.randint(1, 3)
            x = inst.getrandbits(k * 32)
            predictor.setrandbits(x, k * 32)
            entropy -= k
        for _ in range(1000):
            x = inst.getrandbits(32)
            y = predictor.getrandbits(32)
            self.assertEqual(x, y)

    def test_random(self):
        inst = random.Random()
        predictor = MT19937Predictor()
        for _ in range(624):
            x = inst.getrandbits(32)
            predictor.setrandbits(x, 32)
        for _ in range(100):
            x = inst.random()
            y = predictor.random()
            self.assertEqual(x, y)

    def test_lognormvariate(self):
        inst = random.Random()
        predictor = MT19937Predictor()
        for _ in range(624):
            x = inst.getrandbits(32)
            predictor.setrandbits(x, 32)
        for _ in range(100):
            mu = random.random()
            sigma = random.random()
            x = inst.lognormvariate(mu, sigma)
            y = predictor.lognormvariate(mu, sigma)
            self.assertEqual(x, y)
