# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-04 05:57
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('itemId', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('userId', models.UUIDField(unique=True)),
                ('title', models.TextField(default='Something')),
                ('description', models.TextField(default='This may or may not be an eggplant')),
                ('image', models.TextField(default='http://i2.kym-cdn.com/entries/icons/original/000/019/068/lgJCmtjW_400x400.jpeg')),
                ('pendingRequests', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'items',
            },
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('tradeId', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('userId', models.UUIDField()),
                ('message', models.TextField(default='I have a proposition for you good sir')),
                ('offeredItem', models.UUIDField()),
                ('requestedItem', models.UUIDField()),
                ('pending', models.BooleanField(default=True)),
                ('accepted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'trades',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userId', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('username', models.TextField(unique=True)),
                ('password', models.TextField()),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]