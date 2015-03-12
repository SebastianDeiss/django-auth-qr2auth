#
# Copyright (C) 2014-2015 Sebastian Deiss, all rights reserved.
#
# This file is a part of QR2Auth.
#
# QR2Auth is free software; you can redistribute it and/or modify it under the
# terms of the MIT licensee. For further information see LICENSE.txt in the
# parent folder.
#
# This file contains the QR2Auth core implementation.
#


from Crypto.Random.random import StrongRandom, Random
from Crypto.Hash import HMAC, SHA512
from Crypto.Cipher import AES
from django.conf import settings

import logging
import base64
import string
import qrcode.image.svg


logger = logging.getLogger(__name__)


class QR2AuthCore(object):
    '''
    QR2Auth core implementation.
    This class provides the core functionality for the
    challenge response protocol.
    QR2Auth is a challenge response protocol with symmetric
    keys.
    
    TODO: Review required!
    '''
    def __init__(self, shared_secret=None, enc_key=None):
        '''
        Initialize QR2Auth core

        :param str shared_secret: The users shared secret.
        :param str enc_key: The passphrase to decrypt the shared secret.
        '''
        # TODO: make variables private!
        self.challenge = None
        self.start = None
        self.end = None
        if settings.Q2A_OTP_LENGTH in range(6, 11):
            self.otp_length = settings.Q2A_OTP_LENGTH
        else:
            self.otp_length = 8     # default: 8 digest OTP
        # encryption key for shared secret
        self.enc_key = enc_key
        self.shared_secret = shared_secret

    def set_shared_secret(self, shared_secret):
        '''
        Setter for shared secret

        :param str shared_secret: The users shared secret.
        :rtype: void
        '''
        self.shared_secret = shared_secret

    def set_challenge(self, challenge):
        '''
        Setter for the challenge

        :param str challenge: The QR2Auth challenge.
        :rtype: void
        '''
        self.challenge = challenge

    def get_challenge(self):
        '''
        Generate a QR2Auth challenge.
        A QR2Auth challenge consists of 128 random bits generated by PyCrypto
        with StrongRandom.
        These random bits are hashed with SHA512. This hash value represents
        the challenge.

        :return: A tuple containing the QR2Auth challenge as well as the range
                 of the OTP in the response hash value.
        :rtype: tuple
        '''
        random_pool = StrongRandom()
        nonce = random_pool.getrandbits(128)
        nonce_hash = SHA512.new(str(nonce)).hexdigest()
        self.start = int(random_pool.randint(0, 128))
        '''
        Start and end of the range must be between 0 and the length of the hash
        We use Sha512, so in this case start and end must be between
        0 and 128
        '''
        self.end = self.start + self.otp_length
        if self.end > len(nonce_hash):
            self.end = self.end - len(nonce_hash)
        self.challenge = nonce_hash
        return self.challenge, self.start, self.end

    def keygen(self):
        '''
        Generate the secret key for QR2Auth aka shared secret.
        A QR2Auth secret key consists of 256 random bits generated by PyCrypto
        with StrongRandom.
        The random bits are hashed with SHA512. This hash value
        represents the secret key aka. shared secret.

        :return: A QRtoAuth shared secret.
        :rtype: str
        '''
        random_pool = StrongRandom()
        key_seed = random_pool.getrandbits(256)
        key = SHA512.new(str(key_seed))
        self.shared_secret = key.hexdigest()
        return self.shared_secret

    def xor_key(self):
        '''
        Bitwise XOR the shared secret with the QR password.

        :return: A tuple containing the QR password and the XORed
                 shared secret.
        :rtype: tuple
        '''
        # The QR password has 4 digits and we need 128 digits for
        # XOR with the shared secret
        qrpassword = self.__pwgen()
        padded_pwd = qrpassword * 32
        '''
        convert strings to a list of character pair tuples
        go through each tuple, converting them to ASCII code (ord)
        perform exclusive or on the ASCII code
        then convert the result back to ASCII (chr)
        merge the resulting array of characters as a string
        '''
        xored = ''.join(chr(ord(a) ^ ord(b)) for a,  b in zip(padded_pwd,
                                                             self.shared_secret))
        return qrpassword, base64.encodestring(xored)

    def make_otp(self):
        '''
        Create a QR2Auth one-time password

        :raise NotImplementedError: The server will never create an OTP, so
                                    there is no point to implement that.
        '''
        raise NotImplementedError

    def verify_response(self, received_otp, start, end):
        '''
        Verify the One time password (OTP) aka response.
        A QR2Auth Response consists of 8 digests of the HMAC-SHA512 value
        from the challenge with the shared_secret used as key for the HMAC.

        :param str received_otp: The submitted one time password from the
                                 client.
        :param str start: Start of the OTP range
        :param str end: End of the OTP range
        :return: True if the OTP is valid otherwise False
        :rtype: bool
        '''
        # decrypt shared secret
        aes = AESCipher(self.enc_key)
        _shared_secret = aes.decrypt(self.shared_secret.__str__())
        otp_hash = HMAC.new(_shared_secret,
                            self.challenge.__str__(), SHA512)

        # convert the received otp range from string to int
        start = int(start)
        end = int(end)

        # do some logging
        logger.debug('CORE Using shared secret: %s' % _shared_secret)
        logger.debug('CORE Using challenge: %s' % self.challenge)
        logger.debug('CORE HMAC is: %s' % otp_hash.hexdigest())
        logger.debug('CORE OTP range is: (%i, %i)' % (start, end))

        if end < start:
            otp = otp_hash.hexdigest()[start:]
            otp += otp_hash.hexdigest()[:end]
        else:
            otp = otp_hash.hexdigest()[start:end]

        # and log the OTPs
        logger.debug('CORE Received OTP: %s' % received_otp)
        logger.debug('CORE Computed OTP: %s' % otp)

        if otp == received_otp:
            return True
        return False

    def qrgen(self, is_key=False, key=''):
        '''
        Generate an SVG image containing the QR code

        :param bool is_key: True if a shared secret QR code
                            is created otherwise False
        :param str key: The user's shared secret
        :return: An image object containing the SVG image
        :rtype: Object
        '''
        qrfactory = qrcode.image.svg.SvgImage
        # generate the QR code
        if is_key is True:
            '''
            Add a prefix so that another application can distinguish the key
            from the challenge.
            '''
            qr_content = '{key}'
            qr_content += key
            # test vectors
            key_hmac = HMAC.new(self.shared_secret, self.shared_secret, SHA512)
            qr_content += ','
            qr_content += key_hmac.hexdigest()
            # make the QR code
            qrimg = qrcode.make(qr_content,
                                image_factory=qrfactory)
        else:
            qrimg = qrcode.make('{' + str(self.start) + ',' +
                                str(self.end) + '}' +
                                self.challenge, image_factory=qrfactory)
        return qrimg

    #
    # Internals
    #
    def __pwgen(self, size=4, chars=string.digits+string.ascii_lowercase):
        '''
        Generate a password. This password is used as the QR password
        for the bitwise XOR of the shared secret.

        :param str size:  The length of the password
        :param str chars: The characters the password should contain.
                          In this case we want digits and ASCII lowercase
                          letters.
        :return: A generated QR password
        :rtype: string
        '''
        return ''.join(Random.random.choice(chars) for _ in range(size))


class AESCipher(object):
    '''
    AES cipher for QR2Auth. AES is used to store the users shared_secret
    encrypted in the database.
    
    TODO: Review required!
    '''
    def __init__(self, passphrase):
        '''
        Initialize AESCipher

        :param str passphrase: The passphrase to generate an AES key.
        '''
        self.passphrase = passphrase
        self.mode = AES.MODE_CBC
        self.iv = None
        self.block_size = 32
        self.padding = '@'
        # use the Sha512 hash of the passphrase as AES key
        # TODO: Check if this key generation is strong enough
        self.key = SHA512.new(self.passphrase).digest()[:self.block_size]

    def encrypt(self, plaintext):
        '''
        Encrypt a string with AES

        :param str plaintext: The text to encrypt
        :return: Returns the base64 encoded initialization vector + cipher text
                         of the given plaintext.
        :rtype: str
        '''
        # Initialization vector must be 16 bytes long
        self.iv = Random.new().read(self.block_size)[:16]
        aes = AES.new(self.key, self.mode, self.iv)
        return base64.b64encode(self.iv + aes.encrypt(self._pad(plaintext)))

    def decrypt(self, ciphertext):
        '''
        Decrypt a string encrypted with AES

        :param str ciphertext: The base64 encoded initialization vector +
                               cipher text.
        :return: Returns the plaintext of the given cipher text.
        :rtype: str
        '''
        self.iv = base64.b64decode(ciphertext)[:16]
        ciphertext = base64.b64decode(ciphertext)[16:]
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        return aes.decrypt(ciphertext).rstrip(self.padding)

    #
    # Internals
    #
    def _pad(self, s):
        '''
        Pad the text before encryption, because the length of the text must
        be a multiple of the block size.

        :param str s: The string to add a padding.
        :return: Returns the given string + padding.
        :rtype: str
        '''
        return s + (self.block_size - len(s) % self.block_size) * self.padding
