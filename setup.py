from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='words_count',
    version='1.0',
    packages=find_packages(),
    install_requires=[
		'nltk ~= 3.4',
    ]
)