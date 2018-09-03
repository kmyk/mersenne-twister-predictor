import unittest

from mt19937predictor import tempering, untempering
import os
try:
    from shlex import quote as shlex_quote
except ImportError:
    from pipes import quote as shlex_quote  # for Python 2
import shutil
import tempfile

generator_cpp = '''\
#include <iostream>
#include <random>
using namespace std;
int main() {
    random_device seed_gen;
    mt19937 mt(seed_gen());
    for (int i = 0; i < 1000; ++i) {
        cout << mt() << endl;
    }
    return 0;
}
'''

class CPlusPlusTest(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def system(self, cmd):
        returncode = os.system(cmd)
        self.assertEqual(returncode, 0)

    def test_cplusplus(self):
        with open('generator.cpp', 'w') as fh:
            fh.write(generator_cpp)
        self.system('g++ -std=c++11 generator.cpp')
        self.system('./a.out | head -n 1000 > data.txt')
        self.system('head -n 624 data.txt > known.txt')
        self.system('tail -n 376 data.txt > correct.txt')
        self.system(shlex_quote(self.original_dir + '/bin/mt19937predict') + ' known.txt | head -n 376 > predicted.txt')  # this uses an installed script in system
        self.system('diff predicted.txt correct.txt')
