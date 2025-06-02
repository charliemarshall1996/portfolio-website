import csv

from audit import models


def run():
    file = "./audit_descriptions_cleaned.csv"
    with open(file) as f:
        reader = csv.reader(f)

        for row in reader:
            title = row[0]
            description = row[1]

            score_description, created = models.ScoreDescription.objects.get_or_create(
                {"title": title, "description": description}
            )

            if created:
                score_description.save()
