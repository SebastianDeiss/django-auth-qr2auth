#
# Copyright (C) 2014-2015 Sebastian Deiss, all rights reserved.
#
# This file is a part of QRtoAuth.
#
# QRtoAuth is free software; you can redistribute it and/or modify it under the
# terms of the MIT licensee. For further information see LICENSE.txt in the
# parent folder.
#

import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class QRtoAuthUser(models.Model):
    '''
    The QRtoAuth user model.
    It extends Djangos default user model by adding a new model that contains
    the shared secret and information about the status. This model is related
    to the user model.
    It won't be created automaticly. It's created for the user once he requests
    a shared secret to use QRtoAuth.
    '''
    user = models.OneToOneField(User)
    shared_secret = models.CharField(max_length=236, blank=True, default='')
    ss_issue_date = models.DateField("Key issue date",
                                     default=datetime.datetime(2014,10, 1, 11, 11, 11))
    key_revoked = models.BooleanField(default=False)
    last_issued_challenge = models.DateTimeField("Last issued challenge",
                                                 default=timezone.now())

    @property
    def has_valid_key(self):
        if self.key_revoked is False and self.shared_secret != '':
            return True
        return False

    def __unicode__(self):
        return "QRtoAuthUser model"
