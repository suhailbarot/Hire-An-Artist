# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20151223_2124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name=b'cropping',
        ),
        migrations.AlterField(
            model_name='listing',
            name='profile_pic',
            field=models.ImageField(upload_to=b'profile'),
        ),
    ]
