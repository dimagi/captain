# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0004_deploy_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='deploy',
            name='failure_reason',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
