#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from setuptools import setup, find_packages

setup(
    name='nidhogg',
    version='3.0',
    description='NetApp Interface done right',
    long_description=open('../doc/source/index.rst').read(),
    author='Chrtian Assing, Roland Wohlfahrt',
    author_email='christian.assing@infineon.com, roland.wohlfahrt-ee@infineon.com',
    url='https://github.com/ifxit/nidhogg',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=open("requirements.txt").readlines(),
    license="MIT License",
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
