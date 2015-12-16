# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20151214_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='talent',
            field=models.ForeignKey(default=None, to='app.Talent'),
            preserve_default=False,
        ),
    ]
