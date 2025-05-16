from crm.models import Client
from website.models import Email


def run():
    emails = list(Email.objects.all())

    for email in emails:
        contact = Client.objects.get(email=email.email)

        if contact:
            email.contact_id = contact.pk
