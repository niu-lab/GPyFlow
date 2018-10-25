#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='GPyFlow',
    version="0.1",
    license='MIT',
    author='ZhangYu',
    author_email='polozy314@gmail.com',
    description='A simple workflow/pipeline framework for command line.',
    packages=['GPyFlow'],
    include_package_data=True,
    zip_safe=False,
    platforms='linux',
    python_requires='>=3.5',
    entry_points={
        'console_scripts': [
            'pyflow = GPyFlow.pyflow:main',
        ],
    }
)
