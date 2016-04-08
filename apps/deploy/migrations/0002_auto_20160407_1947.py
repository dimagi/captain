# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='machine',
            name='deploys',
        ),
        migrations.RemoveField(
            model_name='stage',
            name='deploy',
        ),
        migrations.RemoveField(
            model_name='stage',
            name='machine',
        ),
        migrations.DeleteModel(
            name='Machine',
        ),
        migrations.DeleteModel(
            name='Stage',
        ),
    ]
