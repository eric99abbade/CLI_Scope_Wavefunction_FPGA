from setuptools import setup, find_packages

setup(
    name='periclis',
    version='1.0.0',
    description='CLI for controlling scope, waveform generator, and testing FGPAs',
    authors='Eric Sonagli Abbade and Pedro Trindade',
    url='https://gitlab.cnpem.br/emi-firmware/periclis-instrument-control/-/tree/main?ref_type=heads',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cli = init:main'
        ]
    }
)
