"""Paranuara Challenge - Jiri Baum"""

from setuptools import setup, find_packages
from os import path
from glob import glob

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Get requirements from the requirements.txt file
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    install_requires = [
        requirement for requirement in (
            line.split('#')[0].strip() for line in f
        ) if requirement
    ]

setup(
    name='paranuara-jbaum',
    version='0.0.20190216',
    description='Paranuara Challenge - Jiri Baum',
    long_description=long_description,
    long_description_content_type='text/markdown',

    author='Jiri Baum',
    author_email='jiri@baum.com.au',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    python_requires='>=3.5',
    install_requires=install_requires,

    package_data={
        'paranuara-jbaum': glob(path.join(here, 'resources/*.json')),
        'paranuara_jbaum': glob(path.join(here, 'resources/*.json')),
    },

#    entry_points={  # TODO
#        'console_scripts': [
#            'sample=sample:main',
#        ],
#    },
)
