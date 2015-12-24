# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20151224_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='talents',
            field=models.ForeignKey(blank=True, to='app.Talent', null=True),
        ),
    ]
