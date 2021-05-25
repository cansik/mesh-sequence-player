from setuptools import setup, find_packages

NAME = 'mesh_sequence_player'

required_packages = find_packages()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name=NAME,
    version='1.6.0',
    packages=required_packages,
    entry_points={
        'console_scripts': [
          'mesh-sequence-player = mesh_sequence_player.__main__:main',
        ],
      },
    url='https://github.com/cansik/mesh-sequence-player',
    license='MIT License',
    author='Florian Bruggisser',
    author_email='github@broox.ch',
    description='A simple mesh sequence player based on open3d.',
    install_requires=required,
)
