
import logging

from django.utils import timezone

from rest_framework import views, response, authentication, permissions
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from . import serializers, models, utils, queries

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@api_view(["GET"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def api_auth_view(request, format=None):
    content = {
        "user": str(request.user),  # `django.contrib.auth.User` instance.
        "auth": str(request.auth),  # None
    }
    return response.Response(content)


@api_view(["GET"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def search_parameter_view(request, format=None):
    params = models.CampaignSearchParameter.objects.filter(
        is_active=True).order_by("last_run").first()
    serializer = serializers.CampaignSearchParameterSerializer(params)
    params.last_run = timezone.now()
    params.save(update_fields=["last_run"])
    return response.Response(serializer.data)


@api_view(["POST"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def add_lead_view(request):
    data = request.data
    email_raw = data.get("email", "")
    url = data.get("url", "")

    email = utils.normalize_email(email_raw)
    url = utils.normalize_url(url)

    email_obj = models.Email.objects.filter(email=email).first()
    website_obj = models.Website.objects.filter(url=url).first()

    entity_qs = queries.entities_with_url_and_email(website_obj, email_obj)
    logger.debug("Entity query count: %s", entity_qs.count())
    if entity_qs.exists():
        entity = entity_qs.first()
        entity_website_objs = [
            w.website.url for w in models.EntityWebsite.objects.filter(entity=entity)]
        entity_email_objs = [
            e.email.email for e in models.EntityEmail.objects.filter(entity=entity)]
        if email_obj.email not in entity_email_objs:
            logger.debug("No email record exists for %s", email)
            models.EntityEmail.objects.get_or_create(
                entity=entity, email=email_obj)

        if website_obj.url not in entity_website_objs:
            logger.debug("No website record exists for %s", url)
            models.EntityWebsite.objects.get_or_create(
                entity=entity, website=website_obj)
    else:
        entity = models.Entity.objects.create(
            name=f"{data["first_name"]} {data["last_name"]}")
        # Create missing Email/Website
        if not email_obj:
            logger.debug("No email record exists for %s", email)
            email_obj = models.Email.objects.create(email=email)

        if not website_obj:
            logger.debug("No website record exists for %s", url)
            website_obj = models.Website.objects.create(url=url)

        models.EntityEmail.objects.get_or_create(
            entity=entity, email=email_obj)
        models.EntityWebsite.objects.get_or_create(
            entity=entity, website=website_obj)

    # Create Lead
    lead = models.Lead.objects.filter(
        entity=entity,
        first_name=data["first_name"],
        last_name=data["last_name"]
    )

    if not lead:
        logger.debug("No lead exists for %s %s",
                     data["first_name"], data["last_name"])
        models.Lead.objects.create(
            entity=entity,
            first_name=data["first_name"],
            last_name=data["last_name"]
        )

    return response.Response({"status": "ok"})


class EmailAPIView(views.APIView):
    pass
