# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-14 22:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='grad_year',
            field=models.PositiveIntegerField(verbose_name='College graduation year'),
        ),
    ]
