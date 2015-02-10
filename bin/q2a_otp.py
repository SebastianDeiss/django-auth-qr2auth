#!/usr/bin/env python

#
# Copyright (C) 2014-2015 Sebastian Deiss, all rights reserved.
#
# This file is a part of QR2Auth.
#
# QR2Auth is free software; you can redistribute it and/or modify it under the
# terms of the MIT licensee. For further information see LICENSE.txt in the
# parent folder.
#


from __future__ import print_function
import sys
from Crypto.Hash import HMAC, SHA512


def make_otp(challenge, shared_secret, start, end):
    otp_hash = HMAC.new(shared_secret, challenge, SHA512)
    start = int(start)
    end = int(end)
    if end < start:
        otp = otp_hash.hexdigest()[start:]
        otp += otp_hash.hexdigest()[:end]
        return otp
    else:
        return otp_hash.hexdigest()[start:end]


def banner():
    print('##################################################################')
    print('QR2Auth Tokenizer')
    print('-----------------')
    print('This script creates a QR2Auth one-time-password fron a')
    print('QR2auth challenge')
    print('Note: The QR2Auth key must be set in the variable shared_secret')
    print('##################################################################')


def print_help():
    print('Usage [qr2auth-challenge] [start] [end]')


def main():
    # print the banner
    banner()
    if len(sys.argv) >= 4:
        challenge = sys.argv[1]
        start = sys.argv[2]
        end = sys.argv[3]
    else:
        print('Not enought arguments')
        print_help()
        sys.exit(0)
    # C3POs QR2Auth key
    shared_secret = 'c88c51e6b1150c72d01a6f30daee6edc47471b573e9bde50f9e75c' +\
                    '7704abd6aeed460fa9ac88faf550b8c76da4110b60dbbf27ae73dd' +\
                    '5b8ca5ef88157512c965'
    otp = make_otp(challenge, shared_secret, start, end)

    print('Your QR2Auth OTP is: ' + otp)
    print()


if __name__ == "__main__":
    main()
