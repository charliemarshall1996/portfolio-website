
from crm.models import Contact
from website.models import Email


def run():

    emails = list(Email.objects.all())

    for email in emails:
        contact = Contact.objects.get(email=email.email)

        if contact:
            email.contact_id = contact.pk
