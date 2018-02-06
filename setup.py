
from distutils.core import setup

try:
    with open('README.md') as f:
        long_description = f.read()
except IOError:
    long_description = ''

setup(
    name='gproxy',
    version=open('VERSION').read(),
    description='requests Session based proxy in Python.',
    author='Gaurav Singh',
    author_email='gauravsingh042@gmail.com',
    url='https://github.com/gccode1/gproxy',
    packages=['gproxy'],
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
    license='GNU LGPL v2.1',
    long_description=long_description,
    requires=['requests', "bs4"],
)
