============
Installation
============


Preparations
============
Before using QR2Auth you must set up the default Django authentication system or another authentication system.
In order to do that you can either use the demo project as reference or read the 
documentation at https://docs.djangoproject.com/en/1.7/topics/auth/default/.


Installation
============
* Run ``python setup.py install`` or copy the `django_auth_qr2auth` folder in you project directory.
* Copy the QR2Auth templates from `django_auth_qr2auth/templates/` into your templates directory.
* Edit your `urls.py` and add this line:

.. code-block:: python
   
   url(r'^qrtoauth/', include('django_auth_qr2auth.urls', app_name='QR2Auth')),

                                        
* Edit your `settings.py` and add these lines to it:

.. code-block:: python
   
   INSTALLED_APPS = (
    ...
    'django_auth_qr2auth',
    ...
   )
   ...
   AUTHENTICATION_BACKENDS = (
   'django_auth_qr2auth.backend.QR2AuthBackend',
   ...
   )
   ...
   LOGIN_REDIRECT_URL = '/qrtoauth/'
   ...
   # QRtoAuth passphrase to decrypt the user shared_secrets
   Q2A_PASSPHRASE = 'SomeStrongPassphrase'
   # Q2A_OTP_LENGTH must be in range(6, 10)
   Q2A_OTP_LENGTH = 6
   # Revoke QR2Auth shared secret after 5 failed authentication attempts
   Q2A_MAX_AUTH_TRIES = 5


* Migrate the QR2Auth models to your database with ``python manage.py migrate``
* Finally run ``python manage.py runserver``
