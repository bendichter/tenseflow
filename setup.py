#!/usr/bin/env python
from setuptools import setup, find_packages
from setuptools.command.install import install
import sys
import os


class CustomInstall(install):

    def run(self):
        install.run(self)
        os.system("sudo python -m spacy download en")

if sys.version >= '3':
    raise Exception('Unfortunately, this package only runs in python 2.')

setup(name='tenseflow',
      version='0.1',
      description='Change the tense of text',
      author='Ben Dichter',
      author_email='ben.dichter@gmail.com',
      url='',
      packages=find_packages(exclude='test'),
      install_requires=['spacy', 'pattern', 'flask'],
      cmdclass={'install': CustomInstall})
