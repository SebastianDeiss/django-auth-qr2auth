#
# Copyright (C) 2014-2015 Sebastian Deiss, all rights reserved.
#
# This file is a part of QRtoAuth.
#
# QRtoAuth is free software; you can redistribute it and/or modify it under the
# terms of the MIT licensee. For further information see LICENSE.txt in the
# parent folder.
#

from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils import timezone
from django.conf import settings

from .models import QRtoAuthUser
from .core import QRtoAuthCore, AESCipher
from .backend import QRtoAuthBackend
from StringIO import StringIO

from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

import base64
import logging


logging.basicConfig(level = logging.INFO,
                    format = '%(asctime)s %(levelname)s %(message)s',
                    )
logger = logging.getLogger(__name__)


def index(request):
    if request.user.is_authenticated():
        return render(request, 'qrtoauth/home.html')
    return render(request, 'qrtoauth/index.html')


@sensitive_post_parameters()
@csrf_protect
@never_cache
def auth(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('../showkey')
    username = request.GET.get('username')
    if username is None:
        username = request.POST.get('username')
    otp = request.POST.get('otp')
    challenge = request.POST.get('challenge')
    start = request.POST.get('start')
    end = request.POST.get('end')
    qrtoauth = QRtoAuthCore()
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'qrtoauth/message.html',
                      {'msg': 'Username does not match any records',
                       'redirect_link': 'Index',
                       'redirect_link_text': 'Try again'})
    try:
        qtauser = QRtoAuthUser.objects.get(user=user)
        if otp is None and challenge is None:
            if qtauser.has_valid_key is True:
                challenge, start, end = qrtoauth.get_challenge()
                qtauser.last_issued_challenge = timezone.now()
                qtauser.save()
                qrcode = qrtoauth.qrgen()
                output = StringIO()
                qrcode.save(output)
                qrcode_img = output.getvalue()
                output.close()
                qrcode_img = base64.encodestring(qrcode_img)
                request.challenge = challenge
                return render(request, 'qrtoauth/auth.html',
                              {'qrcode_img': qrcode_img,
                               'challenge': challenge,
                               'start': start,
                               'end': end,
                               'username': username})
            else:
                return render(request, 'qrtoauth/message.html',
                              {'msg': 'Your key has been revoked'})
        else:
            user = QRtoAuthBackend()
            user = user.authenticate(username, otp, challenge, start, end)
            if user is not None:
                login(request, user)
                logger.info('Authenticated user: %s' % username)
                return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
            else:
                return render(request, 'qrtoauth/message.html',
                              {'msg': 'Authentication failed',
                               'redirect_link': 'Index',
                               'redirect_link_text': 'Try again'})
    except QRtoAuthUser.DoesNotExist:
        return render(request, 'qrtoauth/message.html',
                      {'msg': 'Authentication failed',
                       'redirect_link': 'Index',
                       'redirect_link_text': 'Try again'})


@login_required
def keygen(request):
    user = User.objects.get(username=request.user)
    keygen = False  # Generate a key or not
    try:
        qtauser = QRtoAuthUser.objects.get(user=user)
        if not qtauser.has_valid_key:
            keygen = True
    except QRtoAuthUser.DoesNotExist:
        keygen = True

    if keygen is True:
        qta = QRtoAuthCore()
        key = qta.keygen()
        key_img = qta.qrgen(key=True)
        output = StringIO()
        key_img.save(output)
        qrcode_img = output.getvalue()
        output.close()
        qrcode_img = base64.encodestring(qrcode_img)
        qtauser = QRtoAuthUser.objects.get(user=user)
        aes = AESCipher(settings.QTA_PASSPHRASE)
        key_enc = aes.encrypt(key)
        qtauser.shared_secret = key_enc
        qtauser.ss_issue_date = timezone.now()
        qtauser.key_revoked = False
        qtauser.save()
        return render(request, 'qrtoauth/keygen.html',
                      {'qrcode_img': qrcode_img, 'debug_ss': key})
    else:
        return render(request, 'qrtoauth/message.html',
                      {'msg': 'You already have a key',
                       'redirect_link': 'javascript:history.back()',
                       'redirect_link_text': 'Back'})


@login_required
def showkey(request):
    user = User.objects.get(username=request.user)
    try:
        qtauser = QRtoAuthUser.objects.get(user=user)
        if qtauser.has_valid_key:
            aes = AESCipher(settings.QTA_PASSPHRASE)
            _shared_secret = aes.decrypt(qtauser.shared_secret)
            qta = QRtoAuthCore(_shared_secret)
            qrcode = qta.qrgen(key=True)
            output = StringIO()
            qrcode.save(output)
            qrcode_img = output.getvalue()
            output.close()
            qrcode_img = base64.encodestring(qrcode_img)
            return render(request, 'qrtoauth/showkey.html',
                          {'shared_secret': qrcode_img,
                           'debug_ss': _shared_secret})
        else:
            if qtauser.key_revoked is True:
                return render(request, 'qrtoauth/message.html',
                              {'msg': 'Your key has been revoked.',
                               'redirect_link': 'Keygen',
                               'redirect_link_text': 'Get a now one'})
            else:
                return render(request, 'qrtoauth/message.html',
                              {'msg': 'You do not have a QRtoAuth key yet',
                               'redirect_link': 'Keygen',
                               'redirect_link_text': 'Get one'})
    except QRtoAuthUser.DoesNotExist:
        return render(request, 'qrtoauth/message.html',
                      {'msg': 'You do not have a QRtoAuth key yet',
                       'redirect_link': 'Keygen',
                       'redirect_link_text': 'Get one'})


@login_required
def revoke(request):
    user = User.objects.get(username=request.user)
    try:
        qtauser = QRtoAuthUser.objects.get(user=user)
        if qtauser.key_revoked is False:
            qtauser.key_revoked = True
            qtauser.save()
            return render(request, 'qrtoauth/message.html',
                          {'msg': 'Your key has been revoked.',
                           'redirect_link': 'Keygen',
                           'redirect_link_text': 'Get a now one'})
        else:
            return render(request, 'qrtoauth/message.html',
                          {'msg': 'Your key is already revoked.',
                           'redirect_link': 'Keygen',
                           'redirect_link_text': 'Get a now one'})
    except QRtoAuthUser.DoesNotExist:
        return render(request, 'qrtoauth/message.html',
                      {'msg': 'You do not have a QRtoAuth key yet',
                       'redirect_link': 'Keygen',
                       'redirect_link_text': 'Get one'})
