# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20160112_2000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='location',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='region',
        ),
        migrations.AlterField(
            model_name='listing',
            name='address_city',
            field=models.CharField(max_length=500, verbose_name=b'Locality, City', blank=True),
        ),
    ]
