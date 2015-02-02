#
# Copyright (C) 2014-2015 Sebastian Deiss, all rights reserved.
#
# This file is a part of QRtoAuth.
#
# QRtoAuth is free software; you can redistribute it and/or modify it under the
# terms of the MIT licensee. For further information see LICENSE.txt in the
# parent folder.
#

from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
                       url(r'^$', view=views.index, name='Index'),
                       url(r'^auth/$', view=views.auth, name='Authenticate'),
                       url(r'^keygen/$', view=views.keygen, name='Keygen'),
                       url(r'^showkey/$', view=views.showkey, name='ShowKey'),
                       url(r'^revoke/$', view=views.revoke, name='RevokeKey'),
                       )
