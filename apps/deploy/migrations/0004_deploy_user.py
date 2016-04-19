# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0003_deploy_code_branch'),
    ]

    operations = [
        migrations.AddField(
            model_name='deploy',
            name='user',
            field=models.CharField(default=b'', max_length=255),
        ),
    ]
