# Generated by Django 5.1.6 on 2025-04-10 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0003_remove_task_project_remove_task_company_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="industry",
            field=models.CharField(max_length=255),
        ),
    ]
