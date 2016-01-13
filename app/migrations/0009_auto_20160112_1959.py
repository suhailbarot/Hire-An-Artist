# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20160112_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='address',
            field=models.CharField(max_length=2000, blank=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='address_city',
            field=models.CharField(max_length=200, verbose_name=b'City', blank=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='location',
            field=location_field.models.plain.PlainLocationField(default=None, max_length=63, null=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='region',
            field=models.CharField(max_length=200, verbose_name=b'Region', blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='bio',
            field=models.CharField(max_length=2000, blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='city',
            field=models.CharField(max_length=100, verbose_name=b'Which city are you based out of? *'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='comments',
            field=models.CharField(max_length=1000, null=True, verbose_name=b'Additional notes for your fees', blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='contact_email',
            field=models.EmailField(default=None, max_length=254, null=True, verbose_name=b'Contact email *', blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='contact_name',
            field=models.CharField(max_length=200, verbose_name=b'Name of the contact person *'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='contact_number',
            field=models.CharField(max_length=12, verbose_name=b'Contact number *'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='contact_number2',
            field=models.CharField(max_length=12, null=True, verbose_name=b'Additional contact number', blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='contact_number3',
            field=models.CharField(max_length=12, null=True, verbose_name=b'Additional contact number', blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='fb_link',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='fees',
            field=models.IntegerField(verbose_name=b'What are your charges? *'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='functions',
            field=models.ManyToManyField(to='app.Function'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='group_key',
            field=models.CharField(max_length=15, blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='name',
            field=models.CharField(max_length=200, verbose_name=b'Name your listing *'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='outstation',
            field=models.IntegerField(default=1, verbose_name=b'Do you provides services outstation? *', choices=[(1, b'YES'), (2, b'NO')]),
        ),
        migrations.AlterField(
            model_name='listing',
            name='tags',
            field=models.ManyToManyField(to='app.Tag', blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='talents',
            field=models.ForeignKey(blank=True, to='app.Talent', null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='tech_details',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='tech_details_file',
            field=models.FileField(null=True, upload_to=b'tech_det', blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='twitter_link',
            field=models.URLField(null=True, blank=True),
        ),
    ]
