#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup script"""

from setuptools import setup
import re


with open('dota2api/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(),
                        re.MULTILINE).group(1)

with open('dota2api/__init__.py', 'r') as fd:
    author = re.search(r'^__author__\s*=\s*[\'"]([^\'"]*)[\'"]',
                       fd.read(),
                       re.MULTILINE).group(1)

with open('dota2api/__init__.py', 'r') as fd:
    licence = re.search(r'^__licence__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(),
                        re.MULTILINE).group(1)

setup(
    name="dota2api",
    version=version,
    author=author,
    author_email="mail@joshuaduffy.org",
    url="https://github.com/joshuaduffy/dota2api",
    description="Dota 2 API wrapper and parser in Python",
    license=licence,
    keywords="dota2 dota api dota2api parser",
    packages=['dota2api', 'dota2api.src', 'dota2api.ref'],
    package_data={'dota2api.ref': ['abilities.json',
                                   'heroes.json',
                                   'leaver.json',
                                   'items.json',
                                   'lobbies.json',
                                   'modes.json',
                                   'regions.json']},
    install_requires=['requests'],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ]
)
