# Generated by Django 5.1.6 on 2025-04-10 01:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0004_alter_company_industry"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="interaction",
            name="date",
        ),
        migrations.RemoveField(
            model_name="interaction",
            name="time",
        ),
        migrations.AddField(
            model_name="interaction",
            name="timestamp",
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
