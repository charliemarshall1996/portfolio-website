# Generated by Django 5.2 on 2025-05-13 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0011_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="email",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
