#
# Copyright (C) 2014-2015 Sebastian Deiss, all rights reserved.
#
# This file is a part of QR2Auth.
#
# QR2Auth is free software; you can redistribute it and/or modify it under the
# terms of the MIT licensee. For further information see LICENSE.txt in the
# parent folder.
#

from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from StringIO import StringIO

from .models import QR2AuthUser
from .core import QR2AuthCore, AESCipher
from .backend import QR2AuthBackend
from .util import is_ascii, is_integer

from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

import base64
import logging


logger = logging.getLogger(__name__)


def index(request):
    if request.user.is_authenticated():
        return render(request, 'qr2auth/home.html')
    return render(request, 'qr2auth/index.html')


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
    # check if the received POST parameters are valid
    if challenge is not None and start is not None and end is not None:
        if not is_ascii(challenge) or not is_integer(start) or not is_integer(end):
            return render(request, 'qr2auth/message.html',
                          {'issue': 'Authentication failed',
                           'msg': 'Invalid POST parameters submitted',
                           'redirect_link': 'Index',
                           'redirect_link_text': 'Try again'})
    qrtoauth = QR2AuthCore()
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'qr2auth/message.html',
                      {'issue': 'Authentication failed',
                       'msg': 'Username does not match any records',
                       'redirect_link': 'Index',
                       'redirect_link_text': 'Try again'})
    try:
        qtauser = QR2AuthUser.objects.get(user=user)
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
                return render(request, 'qr2auth/auth.html',
                              {'qrcode_img': qrcode_img,
                               'challenge': challenge,
                               'start': start,
                               'end': end,
                               'username': username,
                               'DEBUG': settings.DEBUG})
            else:
                return render(request, 'qr2auth/message.html',
                              {'issue': 'Authentication not possible',
                               'msg': 'Your key has been revoked'})
        else:
            '''
            If the login request does not come within 90 second after the
            challenge was issued to the user it is invalid and the auth will
            fail.
            '''
            challenge_issue_date = qtauser.last_issued_challenge
            if timezone.now() > challenge_issue_date + timedelta(seconds=90):
                logger.info('AUTH: Auth failed! Response timeout!')
                return render(request, 'qr2auth/message.html',
                              {'issue': 'Authentication failed',
                               'msg': 'Response timeout! You did not' +
                                      ' enter the one-time password within' +
                                      ' 90 seconds',
                               'redirect_link': 'Index',
                               'redirect_link_text': 'Try again'})

            user = QR2AuthBackend()
            user = user.authenticate(username, otp.lower(), challenge, start,
                                     end)
            if user is not None:
                login(request, user)
                logger.info('Authenticated user: %s' % username)
                '''
                If authentication was successful and previous authentications
                failed reset failed_auths to 0.
                '''
                if qtauser.failed_auths > 0:
                    qtauser.failed_auths = 0
                    qtauser.save()
                return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
            else:
                # Validate Q2A_MAX_AUTH_TRIES
                if not settings.Q2A_MAX_AUTH_TRIES > 1:
                    logger.error('AUTH: settings.Q2A_MAX_AUTH_TRIES' +
                                 'must be > 1.')
                    settings.Q2A_MAX_AUTH_TRIES = 5     # default: 5 auth tries
                # Count failed authentications
                qtauser.failed_auths += 1
                # Revoke the shared secret after Q2A_MAX_AUTH_TRIES has arrived
                if qtauser.failed_auths == settings.Q2A_MAX_AUTH_TRIES:
                    qtauser.key_revoked = True
                qtauser.save()
                return render(request, 'qr2auth/message.html',
                              {'issue': 'Authentication failed',
                               'msg': 'The one-time password you entered' +
                                      ' is incorrect or the password to' +
                                      ' unlock the key on your phone is' +
                                      ' incorrect',
                               'redirect_link': 'Index',
                               'redirect_link_text': 'Try again'})
    except QR2AuthUser.DoesNotExist:
        return render(request, 'qr2auth/message.html',
                      {'issue': 'Authentication failed',
                       'msg': 'QR2Auth is not yet enabled for your account',
                       'redirect_link': 'Index',
                       'redirect_link_text': 'Try again'})


@login_required
def keygen(request):
    user = User.objects.get(username=request.user)
    keygen = False  # Generate a key or not
    try:
        qtauser = QR2AuthUser.objects.get(user=user)
        if not qtauser.has_valid_key:
            keygen = True
    except QR2AuthUser.DoesNotExist:
        keygen = True

    if keygen is True:
        qta = QR2AuthCore()
        __plain_key = qta.keygen()
        # XOR the key with a password
        qrpassword, key = qta.xor_key()
        key_img = qta.qrgen(is_key=True, key=key)
        output = StringIO()
        key_img.save(output)
        qrcode_img = output.getvalue()
        output.close()
        qrcode_img = base64.encodestring(qrcode_img)
        qtauser = QR2AuthUser.objects.get(user=user)
        aes = AESCipher(settings.Q2A_PASSPHRASE)
        key_enc = aes.encrypt(__plain_key)
        qtauser.shared_secret = key_enc
        qtauser.ss_issue_date = timezone.now()
        qtauser.key_revoked = False
        qtauser.failed_auths = 0
        qtauser.save()
        logger.info('New key for user: %s' % request.user)
        return render(request, 'qr2auth/keygen.html',
                      {'qrcode_img': qrcode_img,
                       'qrpassword': qrpassword,
                       'xored_key': key,
                       'plain_key': __plain_key,
                       'DEBUG': settings.DEBUG})
    else:
        return render(request, 'qr2auth/message.html',
                      {'issue': 'You already have a key',
                       'redirect_link': 'Index',
                       'redirect_link_text': 'Back'})


@login_required
def showkey(request):
    user = User.objects.get(username=request.user)
    try:
        qtauser = QR2AuthUser.objects.get(user=user)
        if qtauser.has_valid_key:
            aes = AESCipher(settings.Q2A_PASSPHRASE)
            __plain_key = aes.decrypt(qtauser.shared_secret)
            qta = QR2AuthCore(__plain_key)
            qrpassword, key = qta.xor_key()
            qrcode = qta.qrgen(is_key=True, key=key)
            output = StringIO()
            qrcode.save(output)
            qrcode_img = output.getvalue()
            output.close()
            qrcode_img = base64.encodestring(qrcode_img)
            return render(request, 'qr2auth/showkey.html',
                          {'shared_secret': qrcode_img,
                           'qrpassword': qrpassword,
                           'xored_key': key,
                           'plain_key': __plain_key,
                           'DEBUG': settings.DEBUG})
        else:
            if qtauser.key_revoked is True:
                return render(request, 'qr2auth/message.html',
                              {'issue': 'Your key has been revoked.',
                               'redirect_link': 'Keygen',
                               'redirect_link_text': 'Get a now one'})
            else:
                return render(request, 'qr2auth/message.html',
                              {'issue': 'You do not have a QRtoAuth key yet',
                               'redirect_link': 'Keygen',
                               'redirect_link_text': 'Get one'})
    except QR2AuthUser.DoesNotExist:
        return render(request, 'qr2auth/message.html',
                      {'issue': 'You do not have a QRtoAuth key yet',
                       'redirect_link': 'Keygen',
                       'redirect_link_text': 'Get one'})


@login_required
def revoke(request):
    user = User.objects.get(username=request.user)
    try:
        qtauser = QR2AuthUser.objects.get(user=user)
        if qtauser.key_revoked is False:
            qtauser.key_revoked = True
            qtauser.save()
            logger.info('Revoked key of user: %s' % request.user)
            return render(request, 'qr2auth/message.html',
                          {'issue': 'Your key has been revoked.',
                           'redirect_link': 'Keygen',
                           'redirect_link_text': 'Get a now one'})
        else:
            return render(request, 'qr2auth/message.html',
                          {'issue': 'Your key is already revoked.',
                           'redirect_link': 'Keygen',
                           'redirect_link_text': 'Get a now one'})
    except QR2AuthUser.DoesNotExist:
        return render(request, 'qr2auth/message.html',
                      {'issue': 'You do not have a QRtoAuth key yet',
                       'redirect_link': 'Keygen',
                       'redirect_link_text': 'Get one'})
