#!/usr/bin/env python3
from setuptools import setup

setup(
    name='mersenne-twister-predictor',
    version='0.0.3',
    description='predicts outputs of Mersenne Twister (MT19937), a pseudorandom number generator',
    install_requires=[],
    author='Kimiyuki Onaka',
    author_email='kimiyuki95@gmail.com',
    url='https://github.com/kmyk/mersenne-twister-predictor',
    license='MIT License',
    py_modules=[ 'mt19937predictor' ],
    scripts=[ 'bin/mt19937predict' ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
)
