# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20151214_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='profile_pic',
            field=models.ImageField(upload_to=b''),
        ),
    ]
