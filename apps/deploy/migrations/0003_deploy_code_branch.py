# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0002_auto_20160407_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='deploy',
            name='code_branch',
            field=models.CharField(max_length=255),
            preserve_default=False,
        ),
    ]
