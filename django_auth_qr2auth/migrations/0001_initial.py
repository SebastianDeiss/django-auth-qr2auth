# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='QR2AuthUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shared_secret', models.CharField(default=b'', max_length=236, blank=True)),
                ('ss_issue_date', models.DateField(default=datetime.datetime(2014, 10, 1, 11, 11, 11), verbose_name=b'Key issue date')),
                ('key_revoked', models.BooleanField(default=False)),
                ('last_issued_challenge', models.DateTimeField(default=datetime.datetime(2015, 2, 25, 10, 58, 27, 667477, tzinfo=utc), verbose_name=b'Last issued challenge')),
                ('failed_auths', models.PositiveSmallIntegerField(default=0, verbose_name=b'Failed authentications')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
