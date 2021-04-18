from setuptools import setup, find_packages

NAME = 'mesh-sequence-player'

required_packages = find_packages()
required_packages.append(NAME)

setup(
    app="%s.py" % NAME,
    name=NAME,
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/cansik/mesh-sequence-player',
    license='MIT License',
    author='Florian Bruggisser',
    author_email='github@broox.ch',
    description='A simple mesh sequence player based on open3d.',
    install_requires=['wheel', 'open3d~=0.12.0'],
)
