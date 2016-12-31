.. QR2Auth documentation master file, created by
   sphinx-quickstart on Thu Feb  5 12:54:26 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===================================
Django authentication using QR2Auth
===================================
This is a Django authentication module and backend that implements QR2Auth authentication.

QR2Auth is a challenge response protocol based on symmetric keys and one-time passwords.
The challenge is transmitted as a QR code, which enables the user to scan it with a mobile device's camera.
The App on the mobile device then computes the response in the form of a one-time password,
which has to be submitted to the application by the user in order to complete the authentication.


Contents
========

.. toctree::
   :maxdepth: 2

   QR2Auth
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
