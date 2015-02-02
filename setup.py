#
# Copyright (C) 2014-2015 Sebastian Deiss, all rights reserved.
#
# This file is a part of QRtoAuth.
#
# QRtoAuth is free software; you can redistribute it and/or modify it under the
# terms of the MIT licensee. For further information see LICENSE.txt in the
# parent folder.


import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-auth-qrtoauth',
    version='0.1',
    packages=['qrtoauth'],
    include_package_data=True,
    license='MIT',
    description='QRtoAuth is an user friendly challenge respnse\
                authentication with QR codes',
    long_description=README,
    url='https://bitbucket.org/qrtoauthteam/',
    author='Sebastian Deiss',
    author_email='sdeiss@haw-landshut.de',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
