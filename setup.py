import os
from setuptools import setup
import dota2api

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="dota2api",
    version=dota2api.__version__,
    author=dota2api.__author__,
    author_email="mail@joshuaduffy.org",
    description=dota2api.__doc__,
    license = dota2api.__licence__,
    keywords = "dota2 dota api dota2api parser",
    long_description=read('README.md'),
    packages=['dota2api', 'dota2api.src'],
    data_files=[('dota2api/ref', ['dota2api/ref/abilities.json',
                                  'dota2api/ref/heroes.json',
                                  'dota2api/ref/items.json',
                                  'dota2api/ref/lobbies.json',
                                  'dota2api/ref/modes.json',
                                  'dota2api/ref/regions.json'])],
    install_requires=['requests'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 2.7"
    ]
)
