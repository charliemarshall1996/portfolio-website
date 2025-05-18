"""Data models for all CRM-related records.

Data description for contained models:
- Company: a lead, prospect, client or former-client company.
- Contact: a person working for a lead, prospect, client or former-client company.
- Interaction: an interaction had with a lead, prospect, client or former-client company
and/or contact.
"""

from modelcluster.models import ClusterableModel
from django.db import models

# Create your models here.
