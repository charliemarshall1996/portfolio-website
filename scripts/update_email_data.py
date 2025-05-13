
import os
import sys
import logging
import csv
from datetime import datetime
from django.utils import timezone

from website.models import Email

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def run():
    file_name = input("Please provide file name: ")
    path = os.path.join(os.path.dirname("../"), "data_imports/")
    path = os.path.join(path, file_name)
    email_records = {}

    with open(path, 'r') as file:
        next(file)  # Skip the media pointer line
        reader = csv.DictReader(file, delimiter='\t')

        for row in reader:
            # Extract email from [email](mailto:...) format
            email_link = row['email']
            start = email_link.find('[') + 1
            end = email_link.find(']', start)

            if start < 1 or end < 0:
                sys.stderr.write(f"Invalid email format: {email_link}")
                continue
            email = email_link[start:end]

            # Parse timestamp
            try:
                naive_time = datetime.strptime(row['ts'], "%d-%m-%Y %H:%M:%S")
                aware_time = timezone.make_aware(naive_time)
            except ValueError as e:
                sys.stderr.write(f"Invalid date {row['ts']}: {e}")
                continue

            # Update latest timestamp
            if email not in email_records or aware_time > email_records[email]:
                email_records[email] = aware_time

    # Update/Create records
    for email, latest in email_records.items():
        Email.objects.update_or_create(
            email=email,
            defaults={'last_emailed': latest}
        )
        sys.stdout.write(f"Processed {email}")
