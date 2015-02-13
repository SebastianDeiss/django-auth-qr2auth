#
# Copyright (C) 2014-2015 Sebastian Deiss, all rights reserved.
#
# This file is a part of QR2Auth.
#
# QR2Auth is free software; you can redistribute it and/or modify it under the
# terms of the MIT licensee. For further information see LICENSE.txt in the
# parent folder.
#
# This module contains some helper functions
#


def is_ascii(s):
    '''
    Check if a string contains only ASCII characters.

    :param str s: The string to check
    :return: Returns True if the string contains only ASCII characters
             otherwise False
    :rtype: bool
    '''
    return all(ord(c) < 128 for c in s)


def is_integer(s):
    '''
    Check if a string contains only numeric values.

    :param str s: The string to check
    :return: Returns True if the string contains only numeric otherwise False
    :rtype: bool
    '''
    try:
        int(s)
        return True
    except ValueError:
        return False
