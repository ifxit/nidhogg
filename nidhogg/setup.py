#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from setuptools import setup, find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='nidhogg',
    version='3.2',
    description='wrapper interface to Netapp filers',
    long_description=read('README.rst'),
    author='Christian Assing, Roland Wohlfahrt',
    author_email='christian.assing@infineon.com, roland.wohlfahrt-ee@infineon.com',
    url='https://github.com/ifxit/nidhogg',
    packages=find_packages(exclude=['tests']),
    install_requires=open("requirements.txt").readlines(),
    license=read('LICENSE.txt'),
    platforms='any',
    keywords='netapp vserver sevenmode ontapi',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.4',
        'Natural Language :: English',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Archiving',
        'Topic :: System :: Systems Administration'
    ],
)
