#
# Copyright (C) 2014-2015 Sebastian Deiss, all rights reserved.
#
# This file is a part of QR2Auth.
#
# QR2Auth is free software; you can redistribute it and/or modify it under the
# terms of the MIT licensee. For further information see LICENSE.txt in the
# parent folder.
#


from django.test import TestCase
from .core import QR2AuthCore, AESCipher
from Crypto.Hash import HMAC, SHA512


class QR2AuthCoreTests(TestCase):
    '''
    Test cases to verify that the core of QR2Auth is working.
    '''
    # global test vectors
    shared_secret = '25cfc015a827b4027bfe0dfcf5aa683a5ee48a011a8d349adb4dc129e\
                     b3b3237617854af2396c5865e3ba8dc2520736781805e08e7daea892c2\
                     9bcb1ca953510'
    passphrase = 'QR2Auth'

    def test_aes(self):
        '''
        Test AES cipher
        '''
        # test vectors
        plaintext = 'G\'day Mate!'
        # make the test
        aes = AESCipher(self.passphrase)
        ciphertext = aes.encrypt(plaintext)
        plaintext_decrypted = aes.decrypt(ciphertext)
        self.assertEqual(plaintext, plaintext_decrypted, 'QR2Auth AES cipher')

    def test_response_virification_1(self):
        # test vectors
        start = 123
        end = 3
        # make the test
        q2a = QR2AuthCore(self.shared_secret, self.passphrase)
        challenge, __, __ = q2a.get_challenge()
        otp = self.__make_otp(challenge, self.shared_secret, start, end)
        # encrypt the shared secret, because it is required by verify_response
        aes = AESCipher(self.passphrase)
        shared_secret = aes.encrypt(self.shared_secret)
        q2a.set_shared_secret(shared_secret)
        resp_code = q2a.verify_response(otp, start, end)
        self.assertEqual(resp_code, True, 'QR2Auth test with OTP range 123:3 ')

    def test_response_virification_2(self):
        # test vectors
        start = 90
        end = 98
        # make the test
        q2a = QR2AuthCore(self.shared_secret, self.passphrase)
        challenge, __, __ = q2a.get_challenge()
        otp = self.__make_otp(challenge, self.shared_secret, start, end)
        # encrypt the shared secret, because it is required by verify_response
        aes = AESCipher(self.passphrase)
        shared_secret = aes.encrypt(self.shared_secret)
        q2a.set_shared_secret(shared_secret)
        resp_code = q2a.verify_response(otp, start, end)
        self.assertEqual(resp_code, True, 'QR2Auth test with OTP range 90:98 ')

    #
    # Internal helpers
    #
    def __make_otp(self, challenge, shared_secret, start, end):
        otp_hash = HMAC.new(shared_secret, challenge, SHA512)
        start = int(start)
        end = int(end)
        if end < start:
            otp = otp_hash.hexdigest()[start:]
            otp += otp_hash.hexdigest()[:end]
            return otp
        else:
            return otp_hash.hexdigest()[start:end]
