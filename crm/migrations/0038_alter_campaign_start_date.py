# Generated by Django 5.2 on 2025-05-23 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0037_alter_campaign_start_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="campaign",
            name="start_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
