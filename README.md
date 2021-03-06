# QR2Auth #


### What is QR2Auth? ###
QR2Auth is a user friendly challenge response authentication protocol that uses QR codes.


### Requirements ###
* Python >= 2.7.5      (https://www.python.org/)
* Django >= 1.6.1      (https://www.djangoproject.com/download/)
* PyCrypto >= 2.6.1    (https://pypi.python.org/pypi/pycrypto)
* qrcode >= 5.1        (https://pypi.python.org/pypi/qrcode)


### Setup ###
#### Installation ####
* Downlaod the latest release
* Install it: python setup.py install
* QRtoAuth ships a demo project. You can run that simply by changeing in the demo directory even without installation and follow the steps in the next chapter.

#### Unit Tests ####
* The unit tests verify that the core components of OR2Auth are working
* Run python manage.py test django\_auth\_qr2auth


### Usage ###
* python manage.py runserver
* Use the default credentials
    * Username: admin Password: qr2auth (superuser)
    * Username: c3po Password: c3po     (testuser)


### QR2Auth Android Application ###
Of course this Django authentication module makes only sense with a mobile application.
The QR2Auth Android App is available at https://bitbucket.org/qr2auth/qr2auth-android.


### LDAP Support ###
Storing username and QR2Auth shared secret on an LDAP server and syncronising it with the local Django databse is
planed.


### Issues ###
Please reports bugs to https://bitbucket.org/qr2auth/qr2auth-django-auth-qr2auth/issues.
