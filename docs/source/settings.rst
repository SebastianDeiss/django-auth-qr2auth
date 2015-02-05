========
Settings
========

Available settings
==================
* Q2A_PASSPHRASE
* LOGIN_URL
* LOGOUT_URL
* LOGIN_REDIRECT_URL

Required settings
=================
* Add :mod:`django_auth_qr2auth` to your `INSTALLED_APPS`...
* Add ``django_auth_qr2auth.backend.QR2AuthBackend`` to the top of your ``AUTHENTICATION_BACKENDS``...
* Save a passphrase for encryption of the user keys in ``Q2A_PASSPHRASE`` in your settings.
* Set ``LOGIN_REDIRECT_URL`` to ``django_auth_qr2auth.views.index``
* Set ``LOGIN_URL`` to ``django_auth_qr2auth.views.auth``
* Set ``LOGOUT_URL`` to ``django.contrib.auth.views.logout``
