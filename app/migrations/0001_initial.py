# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import app.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Function',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('profile_pic', models.ImageField(upload_to=app.models.get_file_path, blank=True)),
                ('name', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('outstation', models.IntegerField(default=1, choices=[(1, b'YES'), (2, b'NO')])),
                ('contact_name', models.CharField(max_length=200)),
                ('contact_email', models.EmailField(default=None, max_length=254, null=True, blank=True)),
                ('contact_number', models.CharField(max_length=12)),
                ('contact_number2', models.CharField(max_length=12, null=True, blank=True)),
                ('contact_number3', models.CharField(max_length=12, null=True, blank=True)),
                ('bio', models.CharField(max_length=2000, blank=True)),
                ('fees', models.IntegerField()),
                ('comments', models.CharField(max_length=1000, null=True, blank=True)),
                ('tech_details', models.CharField(max_length=2000, null=True, blank=True)),
                ('tech_details_file', models.FileField(null=True, upload_to=b'tech_det', blank=True)),
                ('fb_link', models.URLField(null=True, blank=True)),
                ('twitter_link', models.URLField(null=True, blank=True)),
                ('score', models.IntegerField(default=1)),
                ('is_approved', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.IntegerField(default=1)),
                ('functions', models.ManyToManyField(to='app.Function')),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, blank=True)),
                ('caption', models.CharField(max_length=200, blank=True)),
                ('type', models.IntegerField(choices=[(1, b'Image'), (2, b'Youtube'), (3, b'Soundcloud')])),
                ('url', models.URLField()),
                ('order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.IntegerField(default=1)),
                ('listing', models.ForeignKey(to='app.Listing')),
            ],
        ),
        migrations.CreateModel(
            name='PasswordReset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000)),
                ('referral_name', models.CharField(max_length=100, null=True, blank=True)),
                ('referral_email', models.EmailField(max_length=254, null=True, blank=True)),
                ('referral_contact', models.CharField(max_length=12, null=True, blank=True)),
                ('referral_contact_2', models.CharField(max_length=12, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.IntegerField(default=1)),
                ('listing', models.ForeignKey(to='app.Listing')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.IntegerField(default=1)),
                ('listing', models.ForeignKey(to='app.Listing')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=2000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.IntegerField(default=1)),
                ('listing', models.ForeignKey(to='app.Listing')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Talent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=12, null=True, blank=True)),
                ('type', models.IntegerField(default=3, choices=[(1, b'Sub Admin'), (2, b'Artist'), (3, b'Visitor')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.IntegerField(default=1)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='tag',
            name='talent',
            field=models.ForeignKey(to='app.Talent'),
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(to='app.UserProfile'),
        ),
        migrations.AddField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(to='app.UserProfile'),
        ),
        migrations.AddField(
            model_name='listing',
            name='tags',
            field=models.ManyToManyField(to='app.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='talents',
            field=models.ForeignKey(blank=True, to='app.Talent', null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='user',
            field=models.ForeignKey(to='app.UserProfile'),
        ),
    ]
