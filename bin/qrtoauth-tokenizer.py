#!/usr/bin/env python

#
# Copyright (C) 2014-2015 Sebastian Deiss, all rights reserved.
#
# This file is a part of QRtoAuth.
#
# QRtoAuth is free software; you can redistribute it and/or modify it under the
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
	print('###############################################################################')
	print('QR2Auth Tokenizer')
	print('-----------------')
	print('This script creates a QR2Auth one-time-password fron a QR2auth challenge')
	print('The QR2Auth key must be set in the variable shared_secret in main()')
	print('###############################################################################')


def help():
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
		# print help
		help()
		sys.exit(0)
	# C3POs QR2Auth key
	shared_secret = '3008b5d48bd28e46bdae44e4189fdc1847b667000968241f027056de959c53b8c9786207e53a18debfa9e4bcf4d414a2a1dd7d4e0cedc5210a86258f668293e2'
	otp = make_otp(challenge, shared_secret, start, end)
	
	print('Your QR2Auth OTP is: ' + otp)
	print()


if __name__ == "__main__":
	main()
