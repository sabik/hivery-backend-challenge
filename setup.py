"""Paranuara Challenge - Jiri Baum"""

from os import path
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))

def get_long_description():
    """ Get the long description from the README file """
    with open(path.join(HERE, 'README.md'), encoding='utf-8') as fh:
        return fh.read()

def get_install_requires():
    """ Get requirements from the requirements.txt file """
    with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as fh:
        return [
            requirement for requirement in (
                line.split('#')[0].strip() for line in fh
            ) if requirement
        ]

setup(
    name='paranuara-jbaum',
    version='0.0.20190216',
    description='Paranuara Challenge - Jiri Baum',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',

    author='Jiri Baum',
    author_email='jiri@baum.com.au',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    python_requires='>=3.5',
    install_requires=get_install_requires(),

    # entry_points={
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },
)
