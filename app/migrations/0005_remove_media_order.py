# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20151226_1932'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='order',
        ),
    ]
