from os.path import join, dirname

from setuptools import setup

packages = ['lib', 'lib.controllers', 'lib.models', 'lib.storage']

setup(
    name='takinata_lib',
    version='0.1',
    author='sad_snitch',
    author_email='0311snitch@gmail.com',
    packages=packages,
    description='library part of Takinata',
    long_description=open(join(dirname(__file__), 'STATUS.md')).read(),
    include_package_data=False)
