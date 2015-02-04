#
# Copyright (C) 2014-2015 Sebastian Deiss, all rights reserved.
#
# This file is a part of QR2Auth.
#
# QR2Auth is free software; you can redistribute it and/or modify it under the
# terms of the MIT licensee. For further information see LICENSE.txt in the
# parent folder.
#

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import QR2AuthUser


class QR2AuthInline(admin.StackedInline):
    model = QR2AuthUser
    can_delete = False
    verbose_name_plural = 'QR2Auth'


class QR2AuthUserAdmin(UserAdmin):
    inlines = [QR2AuthInline, ]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, QR2AuthUserAdmin)
