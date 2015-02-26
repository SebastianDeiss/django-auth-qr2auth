#
# Copyright (C) 2014-2015 Sebastian Deiss, all rights reserved.
#
# This file is a part of QR2Auth.
#
# QR2Auth is free software; you can redistribute it and/or modify it under the
# terms of the MIT licensee. For further information see LICENSE.txt in the
# parent folder.
#
# This file contains the QR2Auth Django authentication backend.
#

import logging
from django.contrib.auth.models import User

from .models import QR2AuthUser
from .core import QR2AuthCore
from django.conf import settings


logger = logging.getLogger(__name__)


class QR2AuthBackend(object):
    '''
    QR2Auth Django authentication backend.
    '''
    def authenticate(self, username=None, otp=None, challenge=None, start=None,
                     end=None):
        '''
        Authenticate against QR2Auth user database.

        :param str username: The name of the user to authenticate
        :param str otp: The generated one time password
        :param str challenge: The challenge used to generate the OTP
        :param str start: Start of the OTP range
        :param str end: End of the OTP range
        :return: Returns a user object if authentication was successful
                 otherwise None.
        :rtype: Object or None
        '''
        try:
            user = User.objects.get(username=username)
            qtauser = QR2AuthUser.objects.get(user=user)
            qta = QR2AuthCore(qtauser.shared_secret, settings.Q2A_PASSPHRASE)
            qta.set_challenge(challenge)
            auth = qta.verify_response(otp, start, end)
            if auth is True:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                logger.info('BACKEND Authenticated user: %s' % username)
                return user
            else:
                logger.info('BACKEND Auth failed for user: %s' % username)
                return None
        except User.DoesNotExist, QR2AuthUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        '''
        Getter for the user object.

        :param str user_id: The user ID.
        :return: Returns the user object to the given user id.
        :rtype: Object
        '''
        try:
            user = User.objects.get(pk=user_id)
            qtauser = QR2AuthUser.objects.get(user=User)
            return user
        except User.DoesNotExist, QR2AuthUser.DoesNotExist:
            return None
