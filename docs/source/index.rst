.. QR2Auth documentation master file, created by
   sphinx-quickstart on Thu Feb  5 12:54:26 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===================================
Django authentication using QR2Auth
===================================
This is a Django authentication module and backend that implements QR2Auth authentication.

QR2Auth is a challenge-response protocol which uses one time passwords and symmetric keys
for authentication. The challenge is transmitted via QR code from the web service to the
user’s PC. It enables the user to scan the QR code with a mobile device’s camera and
receives a one-time password as a response for authentication on a web site.


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
