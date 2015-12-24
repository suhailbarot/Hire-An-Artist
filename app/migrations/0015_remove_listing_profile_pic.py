# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20151224_0939'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='profile_pic',
        ),
    ]
