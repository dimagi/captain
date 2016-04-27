# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0005_deploy_failure_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='deploy',
            name='duration',
            field=models.IntegerField(null=True),
        ),
    ]
