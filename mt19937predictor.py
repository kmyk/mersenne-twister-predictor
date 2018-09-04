import random
import sys

# compatibility
if sys.version_info[0] == 2:
    def _to_bytes(n, length, byteorder):
        assert byteorder == 'little'
        return ('%x' % n).zfill(length * 2).decode('hex')[: : -1]
    def _from_bytes(s, byteorder):
        assert byteorder == 'little'
        return int(str(s[: : -1]).encode('hex'), 16)
else:
    _to_bytes = lambda n, *args, **kwargs: n.to_bytes(*args, **kwargs)
    _from_bytes = lambda *args, **kwargs: int.from_bytes(*args, **kwargs)

N = 624  #: 624 values (of 32bit) is just enough to reconstruct the internal state
M = 397  #:
MATRIX_A   = 0x9908b0df  #:
UPPER_MASK = 0x80000000  #:
LOWER_MASK = 0x7fffffff  #:

def tempering(y):
    y ^= (y >> 11)
    y ^= (y <<  7) & 0x9d2c5680
    y ^= (y << 15) & 0xefc60000
    y ^= (y >> 18)
    return y

def untempering(y):
    y ^= (y >> 18)
    y ^= (y << 15) & 0xefc60000
    y ^= ((y <<  7) & 0x9d2c5680) ^ ((y << 14) & 0x94284000) ^ ((y << 21) & 0x14200000) ^ ((y << 28) & 0x10000000)
    y ^= (y >> 11) ^ (y >> 22)
    return y

def generate(mt, kk):
    mag01 = [0x0, MATRIX_A]
    y = (mt[kk] & UPPER_MASK) | (mt[(kk + 1) % N] & LOWER_MASK)
    mt[kk] = mt[(kk + M) % N] ^ (y >> 1) ^ mag01[y & 0x1]

def genrand_int32(mt, mti):
    generate(mt, mti)
    y = mt[mti]
    mti = (mti + 1) % N
    return tempering(y), mti


class MT19937Predictor(random.Random):
    '''
    Usage:

    .. doctest::

        >>> import random
        >>> from mt19937predictor import MT19937Predictor
        >>> predictor = MT19937Predictor()
        >>> for _ in range(624):
        ...     x = random.getrandbits(32)
        ...     predictor.setrandbits(x, 32)
        >>> random.getrandbits(32) == predictor.getrandbits(32)
        True
        >>> random.random() == predictor.random()
        True
        >>> a = list(range(100))
        >>> b = list(range(100))
        >>> random.shuffle(a)
        >>> predictor.shuffle(b)
        >>> a == b
        True
    '''

    def __init__(self):
        self._mt = [ 0 ] * N
        self._mti = 0

    def setrand_int32(self, y):
        '''Feceive the target PRNG's outputs and reconstruct the inner state.
        when 624 consecutive DOWRDs is given, the inner state is uniquely determined.
        '''
        assert 0 <= y < 2 ** 32
        self._mt[self._mti] = untempering(y)
        self._mti = (self._mti + 1) % N

    def genrand_int32(self):
        y, self._mti = genrand_int32(self._mt, self._mti)
        return y

    def setrandbits(self, y, bits):
        '''The interface for :py:meth:`random.Random.getrandbits` in Python's Standard Library
        '''
        if not (bits % 32 == 0):
            raise ValueError('number of bits must be a multiple of 32')
        if not (0 <= y < 2 ** bits):
            raise ValueError('invalid state')
        if bits == 32:
            self.setrand_int32(y)
        else:
            while bits > 0:
                self.setrand_int32(y & 0xffffffff)
                y >>= 32
                bits -= 32

    def getrandbits(self, bits):
        '''The interface for :py:meth:`random.Random.getrandbits` in Python's Standard Library
        '''
        if not (bits > 0):
            raise ValueError('number of bits must be greater than zero')
        if bits <= 32:
            return self.genrand_int32() >> (32 - bits)
        else:
            acc = bytearray()
            while bits > 0:
                r = self.genrand_int32()
                if bits < 32:
                    r >>= 32 - bits
                acc += _to_bytes(r, 4, byteorder='little')
                bits -= 32
            return _from_bytes(acc, byteorder='little')

    def random(self):
        '''The interface for :py:meth:`random.Random.random` in Python's Standard Library
        '''
        a = self.genrand_int32() >> 5
        b = self.genrand_int32() >> 6
        return ((a * 67108864.0 + b) * (1.0 / 9007199254740992.0))

    def seed(self, *args):
        '''
        Raises:
            :py:exc:`NotImplementedError`
        '''
        raise NotImplementedError

    def setstate(self, *args):
        '''
        Raises:
            :py:exc:`NotImplementedError`
        '''
        raise NotImplementedError

    def getstate(self, *args):
        '''
        Raises:
            :py:exc:`NotImplementedError`
        '''
        raise NotImplementedError

    def gauss(self, *args):
        '''
        Raises:
            :py:exc:`NotImplementedError`
        '''
        raise NotImplementedError
