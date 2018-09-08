from setuptools import setup

packages = ['console', 'console.parser_api', 'console.presentations']

setup(
    name='console_api',
    version='0.1',
    author='sad_snitch',
    author_email='0311snitch@gmail.com',
    packages=packages,
    description='console part of Takinata',
    include_package_data=False,
    entry_points={
        'console_scripts':
            ['takinata = console.start:main']
    }
)
