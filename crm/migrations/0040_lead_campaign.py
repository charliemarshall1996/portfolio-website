# Generated by Django 5.2 on 2025-05-23 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0039_alter_lead_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="lead",
            name="campaign",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
