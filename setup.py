#
# Copyright (C) 2014-2015 Sebastian Deiss, all rights reserved.
#
# This file is a part of QR2Auth.
#
# QR2Auth is free software; you can redistribute it and/or modify it under the
# terms of the MIT licensee. For further information see LICENSE.txt in the
# parent folder.
#


import os
from setuptools import setup
from django_auth_qr2auth import __version__

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-auth-qr2auth',
    version=__version__,
    packages=['django_auth_qr2auth'],
    include_package_data=True,
    license='MIT',
    description='QR2Auth is an user friendly challenge respnse\
                authentication with QR codes',
    long_description=README,
    url='https://bitbucket.org/qr2auth/qr2auth-django-auth-qr2auth',
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
