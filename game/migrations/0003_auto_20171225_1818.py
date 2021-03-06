# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-26 00:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_team_division'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='season',
            name='number_of_weeks',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='teaminfo',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Season'),
        ),
        migrations.AddField(
            model_name='teaminfo',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Team'),
        ),
    ]
