# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0006_deploy_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='deploy',
            name='stacktrace',
            field=models.TextField(null=True),
        ),
    ]
