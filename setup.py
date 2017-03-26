#!/usr/bin/env python

from setuptools import setup, find_packages
import sys

if sys.version >= '3':
    raise Exception('Unfortunately, this package only runs in python 2.')

setup(name='change_tense',
      version='1.0',
      description='Change the tense of text',
      author='Ben Dichter',
      author_email='ben.dichter@gmail.com',
      url='',
      packages=find_packages(exclude='test'),
      install_requires=['spacy', 'pattern','flask']
     )
