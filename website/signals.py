
import logging

from django.apps import apps
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from website.models import Analysis
from website.utils import get_plain_email_message

Contact = apps.get_model('crm', 'Contact')

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Analysis)
def create_website_for_contact(sender, instance, created, **kwargs):

    if created:
        print("New analysis created.")
        contact = Contact.objects.get(pk=instance.website.contact_id)
        email = contact.email
        if email:
            print("New analysis created. Sending email to %s...", email)
            date = instance.created_at.date()
            first_name = contact.first_name

            data = instance.data

            plain_message, html_message = get_plain_email_message(
                data, first_name, instance.website.url, date)

            try:
                send_mail(subject="I Audited Your Website.", message=plain_message,
                          from_email="charlie@charlie-marshall.dev",
                          recipient_list=[email], html_message=html_message)
            except Exception as e:
                print("ERROR SENDING EMAIL: %s", e)
