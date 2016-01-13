# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20160105_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='talent',
            name='fee_text',
            field=models.CharField(max_length=300, blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='bio',
            field=models.CharField(help_text=b'Some text here', max_length=2000, blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='city',
            field=models.CharField(help_text=b'Some other help text', max_length=100),
        ),
        migrations.AlterField(
            model_name='listing',
            name='comments',
            field=models.CharField(help_text=b'Some text here', max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='contact_email',
            field=models.EmailField(default=None, max_length=254, null=True, help_text=b'Some text here', blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='contact_name',
            field=models.CharField(help_text=b'Some text here', max_length=200),
        ),
        migrations.AlterField(
            model_name='listing',
            name='contact_number',
            field=models.CharField(help_text=b'Some text here', max_length=12),
        ),
        migrations.AlterField(
            model_name='listing',
            name='contact_number2',
            field=models.CharField(help_text=b'Some text here', max_length=12, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='contact_number3',
            field=models.CharField(help_text=b'Some text here', max_length=12, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='fb_link',
            field=models.URLField(help_text=b'Some text here', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='fees',
            field=models.IntegerField(help_text=b'Some text here'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='functions',
            field=models.ManyToManyField(help_text=b'Some text here', to='app.Function'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='group_key',
            field=models.CharField(help_text=b'Some text here', max_length=15, blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='name',
            field=models.CharField(help_text=b'Some text here', max_length=200),
        ),
        migrations.AlterField(
            model_name='listing',
            name='outstation',
            field=models.IntegerField(default=1, help_text=b'Some text here', choices=[(1, b'YES'), (2, b'NO')]),
        ),
        migrations.AlterField(
            model_name='listing',
            name='tags',
            field=models.ManyToManyField(help_text=b'Some text here', to='app.Tag', blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='talents',
            field=models.ForeignKey(blank=True, to='app.Talent', help_text=b'Some text here', null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='tech_details',
            field=models.CharField(help_text=b'Some text here', max_length=2000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='tech_details_file',
            field=models.FileField(help_text=b'Some text here', null=True, upload_to=b'tech_det', blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='twitter_link',
            field=models.URLField(help_text=b'Some text here', null=True, blank=True),
        ),
    ]
