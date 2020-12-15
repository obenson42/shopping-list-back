from setuptools import setup, find_packages

requires = [
    'flask',
    'flask-sqlalchemy',
    'psycopg2',
]

setup(
    name='shopping_list',
    version='0.1',
    description='A shopping list back end built with Flask',
    author='Owen Benson',
    author_email='owenbenson1@gmail.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)