# Generated by Django 5.2 on 2025-05-16 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0011_campaign_location_searchterm_vertical_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="company",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name="Company",
        ),
    ]
