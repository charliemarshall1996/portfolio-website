import logging
from datetime import timedelta
from django.apps import apps
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from website.models import Analysis, Email
from crm.utils import get_email_message

Contact = apps.get_model("crm", "Contact")

logger = logging.getLogger(__name__)
