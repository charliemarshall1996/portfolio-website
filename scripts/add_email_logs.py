
from django.utils import timezone
import pandas as pd

from crm import models


def run():
    logs_csv = "data/logs/email_logs.csv"
    df = pd.read_csv(logs_csv)
    # Ensure the 'ts' column is a datetime type
    df['ts'] = pd.to_datetime(df['ts'], dayfirst=True)

    # Get the most recent timestamp per duplicate email
    df = df.sort_values('ts', ascending=False).drop_duplicates(
        subset='email', keep='first')

    for i, row in df.iterrows():
        email_obj, created = models.Email.objects.get_or_create(
            email=row.email)
        email_obj.last_emailed = timezone.make_aware(row.ts)
        email_obj.save()
