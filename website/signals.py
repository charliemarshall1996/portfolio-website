
import logging
from datetime import timedelta
from django.apps import apps
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from website.models import Analysis, Email
from website.utils import get_email_message

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
            first_name = contact.first_name.title()

            data = instance.data

            now = timezone.now()
            one_month_ago = now - timedelta(days=30)

            plain_message, html_message = get_email_message(
                data, first_name, instance.website.url, date, contact.search_term)

            email_obj, created = Email.objects.get_or_create(email=email)
            email_obj.contact_id = contact.pk
            email_obj.save()

            last_emailed = None
            if not created:
                last_emailed = email_obj.last_emailed

            try:
                if (not last_emailed or last_emailed >= one_month_ago) and not \
                        email_obj.bounced and not email_obj.opt_out:
                    send_mail(subject="I Audited Your Website.", message=plain_message,
                              from_email="charlie@charlie-marshall.dev",
                              recipient_list=[email], html_message=html_message)
                    email_obj.last_emailed = timezone.now()
                    email_obj.save()
            except Exception as e:
                print("ERROR SENDING EMAIL: %s", e)
