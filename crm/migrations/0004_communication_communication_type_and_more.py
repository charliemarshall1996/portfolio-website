# Generated by Django 5.2 on 2025-07-25 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0003_alter_vertical_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="communication",
            name="communication_type",
            field=models.CharField(
                choices=[
                    ("cold", "Cold"),
                    ("reply", "Reply"),
                    ("discovery", "Discovery"),
                    ("other", "Other"),
                ],
                default="cold",
                max_length=9,
            ),
        ),
        migrations.AddField(
            model_name="communication",
            name="direction",
            field=models.CharField(
                choices=[("in", "Inbound"), ("out", "Outbound")],
                default="out",
                max_length=3,
            ),
        ),
    ]
