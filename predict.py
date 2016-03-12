#!/usr/bin/env python3

N = 624
M = 397
MATRIX_A   = 0x9908b0df
UPPER_MASK = 0x80000000
LOWER_MASK = 0x7fffffff

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

if __name__ == '__main__':
    import sys
    import struct

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='?', default='-')
    parser.add_argument('-f', '--format', default='=I')
    args = parser.parse_args()

    if args.path == '-':
        argf = sys.stdin
    else:
        argf = open(args.path)
    get = lambda: struct.unpack(args.format, argf.buffer.read(4))[0]
    put = lambda y: sys.stdout.buffer.write(struct.pack(args.format, y))

    mt = [untempering(get()) for i in range(N)]
    while True:
        for mti in range(N):
            generate(mt, mti)
            put(tempering(mt[mti]))
