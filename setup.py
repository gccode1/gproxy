
from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='gproxy',
    version=open('VERSION').read().strip(),
    description='Session based proxy in Python.',
    author='Gaurav Singh',
    author_email='gauravsingh042@gmail.com',
    url='https://github.com/gccode1/gproxy',
    packages=['gproxy'],
    license='',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='gproxy proxy https http',
    #py_modules=['gproxy'],
    long_description=long_description,
    install_requires=['requests', "bs4"],
)
