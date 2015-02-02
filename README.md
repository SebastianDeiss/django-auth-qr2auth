# QRtoAuth #


### What is this repository for? ###

* QRtoAuth: User friendly challenge response authentication with QR codes.
* Version 0.1


### Requirements ###
* Python >= 2.7.5
* Django >= 1.6.1
* PyCrypto >= 2.6.1
* qrcode >= 5.1


### Setup ###
* Downlaod the latest release
* Install it: python setup.py install
* QRtoAuth ships a demo project. You can run that simply by changeing in the demo directory after installation and follow the steps in the next chapter.


### Usage ###
#### Using the demo project ####
cd demo/
python manage.py runserver
Use the default credentials

#### Add QR2Auth to your django project äää#
##### migrate the database #####
python manage.py migrate
##### Run the project #####
python manage.py runserver

#### Default Credentials ####
* Admin: 
** Username: admin Password: qr2auth
* Testuser:
** Username: c3po Password: c3po


### Issues ###
Please reports bugs to https://bitbucket.org/qrtoauthteam/django-auth-qr2auth/issues
