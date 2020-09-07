from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='autoscraper',

    version='1.0.0',

    description='Smart Automatic Scraper in Python',
    long_description_content_type="text/markdown",
    long_description=long_description,

    url='https://github.com/alirezamika/autoscraper',

    author='Alireza Mika',
    author_email='alirezamika@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],

    keywords='scraping - scraper',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    python_requires='>=3.6',
    install_requires=['requests', 'bs4', 'lxml'],

)
