#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup script"""

from setuptools import setup
import dota2api

setup(
    name="dota2api",
    version=dota2api.__version__,
    author=dota2api.__author__,
    author_email="mail@joshuaduffy.org",
    description=dota2api.__doc__,
    license=dota2api.__licence__,
    keywords="dota2 dota api dota2api parser",
    packages=['dota2api', 'dota2api.src'],
    data_files=[('Lib/site-packages/dota2api/ref', ['dota2api/ref/abilities.json',
                                                    'dota2api/ref/heroes.json',
                                                    'dota2api/ref/items.json',
                                                    'dota2api/ref/lobbies.json',
                                                    'dota2api/ref/modes.json',
                                                    'dota2api/ref/regions.json'])],
    install_requires=['requests'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python"
    ]
)
