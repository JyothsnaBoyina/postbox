# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-13 00:16
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=200)),
                ('c_date', models.DateTimeField(default=datetime.datetime(2016, 7, 13, 5, 46, 17, 982000))),
                ('owner', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(default='', max_length=1000)),
                ('cm_date', models.DateTimeField(default=datetime.datetime(2016, 7, 13, 5, 46, 17, 991000))),
                ('owner', models.ForeignKey(default=' ', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=200)),
                ('status', models.TextField()),
                ('image', models.ImageField(default='', null=True, upload_to='C:/Users/Jyothsna Boyina/PycharmProjects/post/postbox/static/postbox/')),
                ('p_date', models.DateTimeField(default=datetime.datetime(2016, 7, 13, 5, 46, 17, 988000))),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postbox.Categories')),
                ('owner', models.ForeignKey(default=' ', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comments',
            name='pid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postbox.Posts'),
        ),
        migrations.AlterUniqueTogether(
            name='categories',
            unique_together=set([('owner', 'category')]),
        ),
    ]
