#!/usr/bin/env python

from setuptools import setup

setup(
    name='geoview',
    version='0.1.0',
    description='Quickly view geo datasets',
    long_description='',
    author='Rich Wareham',
    author_email='rjw57@cam.ac.uk',
    url='https://github.com/rjw57/geoview',
    packages=[
        'geoview',
    ],
    package_dir={'geoview': 'geoview'},
    include_package_data=True,
    setup_requires=['pip'],
    install_requires=[
        'docopt',
        'GDAL',
        'Flask',
    ],
    license="BSD",
    keywords='GIS',
    entry_points={
        'console_scripts': [
            'geoview = geoview.tool:main',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)
