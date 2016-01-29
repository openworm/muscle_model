from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = "OpenWormMuscleModel",

    version = "1.0.dev0",

    description = "This is a NeuroML2 implementation of the C elegans muscle cell model" ,
    long_description=long_description,

    url="https://github.com/openworm/muscle_model" ,

    author = "OpenWorm authors and contributors" ,
    author_email = "stephen.larson@gmail.com" ,

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering' ,

        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='Biological Simulations' ,

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    dependency_links = [
        'git+https://github.com/LEMS/pylems.git@master#egg=pylems' ,
        'git+https://github.com/NeuralEnsemble/libNeuroML.git@development#egg=libNeuroML',
        'git+https://github.com/OpenSourceBrain/OSB_API.git@master#egg=PyOSB',
        'git+https://github.com/purcell/airspeed.git@master#egg=airspeed',
        'git+https://github.com/NeuroML/pyNeuroML.git#egg=pyNeuroML'
    ],

    install_requires=[
        'lxml',
        'pylems',
        'libNeuroML',
        'PyOSB',
        'airspeed',
        'pyNeuroML'
    ],
)

