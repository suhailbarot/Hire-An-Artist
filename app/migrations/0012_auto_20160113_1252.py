# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20160112_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='latitude',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='longitude',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='contact_number2',
            field=models.CharField(max_length=12, null=True, verbose_name=b'Additional contact number 1', blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='contact_number3',
            field=models.CharField(max_length=12, null=True, verbose_name=b'Additional contact number 2', blank=True),
        ),
    ]
