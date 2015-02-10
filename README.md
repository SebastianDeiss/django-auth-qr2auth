# QR2Auth #


### What is this repository for? ###
QR2Auth: User friendly challenge response authentication with QR codes.


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
#### Using the demo project ####
* python manage.py runserver
* Use the default credentials
    * Username: admin Password: qr2auth (superuser)
    * Username: c3po Password: c3po     (testuser)

#### Add QR2Auth to your django project ####
##### migrate the database #####
python manage.py migrate

##### Run your project #####
python manage.py runserver


### QR2Auth Android Application ###
Of course this Django authentication module makes only sense with a mobile application.
The QR2Auth Android App is still in development and a first release will be available soon.


### LDAP Support ###
Storing username and QR2Auth shared secret on an LDAP server and syncronising it with the local Django databse is
planed.


### Issues ###
Please reports bugs to https://bitbucket.org/qrtoauthteam/django-auth-qr2auth/issues
