# Generated by Django 5.2 on 2025-05-23 04:19

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0041_alter_campaignmetric_action_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="EntityCampaign",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "campaign",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="crm.campaign"
                    ),
                ),
                (
                    "entity",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="campaigns",
                        to="crm.entity",
                    ),
                ),
            ],
            options={
                "unique_together": {("entity", "campaign")},
            },
        ),
        migrations.CreateModel(
            name="EntitySearchTerm",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "entity",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="search_terms",
                        to="crm.entity",
                    ),
                ),
                (
                    "search_term",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="crm.searchterm"
                    ),
                ),
            ],
            options={
                "unique_together": {("entity", "search_term")},
            },
        ),
    ]
