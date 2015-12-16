# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_tag_talent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='tags',
            field=models.ManyToManyField(to='app.Tag', blank=True),
        ),
        migrations.AlterField(
            model_name='media',
            name='caption',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='media',
            name='title',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
