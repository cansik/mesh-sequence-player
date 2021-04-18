from setuptools import setup, find_packages

NAME = 'mesh_sequence_player'

required_packages = find_packages()

setup(
    name=NAME,
    version='1.2.0',
    packages=required_packages,
    url='https://github.com/cansik/mesh-sequence-player',
    license='MIT License',
    author='Florian Bruggisser',
    author_email='github@broox.ch',
    description='A simple mesh sequence player based on open3d.',
    install_requires=['wheel', 'open3d~=0.12.0'],
)
