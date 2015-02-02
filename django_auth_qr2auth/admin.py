#
# Copyright (C) 2014-2015 Sebastian Deiss, all rights reserved.
#
# This file is a part of QRtoAuth.
#
# QRtoAuth is free software; you can redistribute it and/or modify it under the
# terms of the MIT licensee. For further information see LICENSE.txt in the
# parent folder.
#

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import QRtoAuthUser


class QRtoAuthInline(admin.StackedInline):
    model = QRtoAuthUser
    can_delete = False
    verbose_name_plural = 'QRtoAuth'


class QRtoAuthUserAdmin(UserAdmin):
    inlines = [QRtoAuthInline, ]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, QRtoAuthUserAdmin)
