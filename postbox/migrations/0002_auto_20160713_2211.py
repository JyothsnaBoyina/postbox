# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-13 16:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postbox', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='c_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='comments',
            name='cm_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='posts',
            name='image',
            field=models.CharField(default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='posts',
            name='p_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='posts',
            name='status',
            field=models.TextField(default='', null=True),
        ),
    ]
