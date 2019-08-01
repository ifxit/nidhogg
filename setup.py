#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from setuptools import setup


def read(fname):
    """Utility function to read the README file.

    Used for the long_description.  It's nice, because now 1) we have a top level
    README file and 2) it's easier to type in the README file than to put a raw
    string in below ...
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="nidhogg",
    version="3.8.0",
    description="wrapper interface to Netapp filers",
    long_description=read("README.rst"),
    author="Christian Assing, Roland Wohlfahrt",
    author_email="christian.assing@infineon.com, roland.wohlfahrt@infineon.com",
    url="https://github.com/ifxit/nidhogg",
    packages=["nidhogg"],
    install_requires=open("requirements.txt").readlines(),
    license="MIT License, Copyright (c) 2018 Infineon Technologies AG",
    platforms="any",
    keywords=["netapp", "vserver", "sevenmode", "ontapi"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Natural Language :: English",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Archiving",
        "Topic :: System :: Systems Administration",
    ],
)
