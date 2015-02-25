# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('django_auth_qr2auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qr2authuser',
            name='last_issued_challenge',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 25, 10, 58, 35, 55127, tzinfo=utc), verbose_name=b'Last issued challenge'),
            preserve_default=True,
        ),
    ]
