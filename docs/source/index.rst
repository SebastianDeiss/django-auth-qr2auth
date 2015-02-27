.. QR2Auth documentation master file, created by
   sphinx-quickstart on Thu Feb  5 12:54:26 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===================================
Django authentication using QR2Auth
===================================
This is a Django authentication module and backend that implements QR2Auth authentication.
QR2Auth is a user friendly challenge response authentication with QR codes. It requires an
app for your mobile device that scans the QR code and then processes the challenge from the
QR code. The app then returns a unique one-time password which you have to enter at the website
you want to authenticate against.


Contents
========

.. toctree::
   :maxdepth: 2

   install
   settings
   core
   backend
   util
   qr2auth_ref


Requirements
============
* Python >= 2.7.5      (https://www.python.org/)
* Django >= 1.6.1      (https://www.djangoproject.com/download/)
* PyCrypto >= 2.6.1    (https://pypi.python.org/pypi/pycrypto)
* qrcode >= 5.1        (https://pypi.python.org/pypi/qrcode)



License
=======
.. include:: ../../LICENSE.txt
   :literal:
