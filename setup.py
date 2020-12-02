#!/usr/bin/env python
# coding: utf-8
import os
import sys
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version():
    VERSIONFILE = 'carotte/__init__.py'
    initfile_lines = open(VERSIONFILE, 'rt').readlines()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(VSRE, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError('Unable to find version string in %s.' % (VERSIONFILE,))

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='carotte',
    version=get_version(),
    description='Carotte is a very lightweight Celery on zmq',
    long_description=open('README.rst').read(),
    license=open("LICENSE").read(),
    author="toxinu",
    author_email="toxinu@gmail.com",
    url='https://github.com/toxinu/carotte',
    keywords="python zmq pyzmq celery task async",
    packages=['carotte', 'carotte.results', 'carotte.results.backends'],
    scripts=['scripts/carotte'],
    install_requires=['pyzmq', 'docopt'],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3']
)
