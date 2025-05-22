from django.db import models as django_models
from . import models


def entities_with_url_and_email(website: models.Website, email: models.Email):

    entity_qs = models.Entity.objects.filter(
        django_models.Q(emails__email=email) |
        django_models.Q(websites__website=website)
    ).distinct()
    return entity_qs
