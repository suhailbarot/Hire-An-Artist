# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20160209_0954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='rscore',
        ),
    ]
