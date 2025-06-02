# crm/signals.py
from datetime import timedelta

from django.apps import apps
from django.core.mail import send_mail
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Client, Website, Lead, Analysis
from .utils import get_email_message
