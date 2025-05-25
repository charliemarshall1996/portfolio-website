import logging

from django.utils import timezone

from rest_framework import response, authentication, permissions, status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from . import serializers, models, utils, queries

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

EMAIL_OPENS = ["unique_opened", "opened", "proxy_opened"]
EMAIL_BOUNCES = ["hard_bounce", "soft_bounce", "invalid_email"]
EMAIL_OPT_OUTS = ["spam", "unsubscribed", "blocked"]
EMAIL_LINK_CLICKS = ["click"]
EMAIL_SENT = ["request"]
EMAIL_DELIVERED = ["delivered"]


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
    params = (
        models.CampaignSearchParameter.objects.filter(is_active=True)
        .order_by("last_run")
        .first()
    )
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
    location_pk = data.get("location_pk")
    campaign_pk = data.get("campaign_pk")
    search_term_pk = data.get("search_term_pk")
    vertical_pk = data.get("vertical_pk")
    search_param_pk = data.get("id")
    logger.debug("Location PK: %s", location_pk)
    logger.debug("Campaign PK: %s", campaign_pk)
    logger.debug("Search Term PK: %s", search_term_pk)
    logger.debug("Vertical PK: %s", vertical_pk)
    logger.debug("Param PK: %s", search_param_pk)

    email = utils.normalize_email(email_raw)
    url = utils.normalize_url(url)

    email_obj = models.Email.objects.filter(email=email).first()
    website_obj = models.Website.objects.filter(url=url).first()

    entity_qs = queries.entities_with_url_and_email(website_obj, email_obj)
    logger.debug("Entity query count: %s", entity_qs.count())
    if entity_qs.exists():
        entity = entity_qs.first()
        entity_website_objs = [
            w.website.url for w in models.EntityWebsite.objects.filter(entity=entity)
        ]
        entity_email_objs = [
            e.email.email for e in models.EntityEmail.objects.filter(entity=entity)
        ]
        if email_obj.email not in entity_email_objs:
            logger.debug("No email record exists for %s", email)
            models.EntityEmail.objects.get_or_create(
                entity=entity, email=email_obj)

        if website_obj.url not in entity_website_objs:
            logger.debug("No website record exists for %s", url)
            models.EntityWebsite.objects.get_or_create(
                entity=entity, website=website_obj
            )
    else:
        entity = models.Entity.objects.create(
            name=f"{data['first_name']} {data['last_name']}"
        )
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
        entity=entity, first_name=data["first_name"], last_name=data["last_name"]
    ).first()

    if not lead:
        logger.debug("No lead exists for %s %s",
                     data["first_name"], data["last_name"])
        lead = models.Lead.objects.create(
            entity=entity, first_name=data["first_name"], last_name=data["last_name"]
        )
        utils.increment_all_campaign_action_metrics(
            None, search_param_pk, "+", incl_email_content=False)
    lead.campaign = campaign_pk
    lead.campaign_search_param = search_param_pk
    lead.save()
    if location_pk != 0:
        location = models.SearchLocation.objects.get(pk=int(location_pk))
        models.EntitySearchLocation.objects.get_or_create(
            entity=entity, location=location)

    vertical = models.Vertical.objects.get(pk=int(vertical_pk))
    models.EntityVertical.objects.get_or_create(
        entity=entity, vertical=vertical)
    search_term = models.SearchTerm.objects.get(pk=int(search_term_pk))
    models.EntitySearchTerm.objects.get_or_create(
        entity=entity, search_term=search_term)
    campaign = models.Campaign.objects.get(pk=int(campaign_pk))
    models.EntityCampaign.objects.get_or_create(
        entity=entity, campaign=campaign)

    return response.Response({"status": "ok"})


@api_view(["POST"])
@authentication_classes([])  # Disable all authentication
@permission_classes([])  # Disable all permissions
def brevo_webhook_view(request):
    # Example: You could validate expected fields here
    event_type = request.data.get("event")
    email = request.data.get("email")
    tag = request.data.get("tag")
    content_pk, param_pk = tuple(tag.split(","))

    if not event_type or not email:
        logger.warning(
            "Brevo webhook missing expected fields: %s", request.data)
        return response.Response(
            {"detail": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Log or handle the event
    logger.info("Brevo event received: %s for %s", event_type, email)

    email_obj = models.Email.objects.filter(email=email).first()
    if email_obj:
        logger.debug("Email exists for %s", email)
        outreach_email = models.OutreachEmail.objects.filter(
            email=email_obj).first()
        if outreach_email:
            outreach = outreach_email.outreach
            engagement = models.Engagement.objects.create(outreach=outreach)
            if event_type in EMAIL_LINK_CLICKS:
                url = request.data.get("link")
                utils.create_web_engagement(engagement, url, "l")
                utils.update_lead_status_from_email_obj(email_obj, "i")
                utils.increment_all_campaign_action_metrics(
                    content_pk, param_pk, "l")
            elif event_type in EMAIL_OPENS:
                utils.create_email_engagement(engagement, email_obj, "o")
                if event_type == "unique_opened":
                    utils.increment_all_campaign_action_metrics(
                        content_pk, param_pk, "1"
                    )
                utils.increment_all_campaign_action_metrics(
                    content_pk, param_pk, "o")
            elif event_type in EMAIL_OPT_OUTS:
                logger.debug("Email opted out %s", email)
                utils.create_email_engagement(engagement, email_obj, "x")
                utils.opt_out_email_obj(email_obj)
                logger.debug("Email opted out: %s", email_obj.opted_out)
                utils.update_lead_status_from_email_obj(email_obj, "x")
                utils.increment_all_campaign_action_metrics(
                    content_pk, param_pk, "x")
            elif event_type in EMAIL_BOUNCES:
                utils.create_email_engagement(engagement, email_obj, "b")
                utils.bounce_email_obj(email_obj)
                utils.update_lead_status_from_email_obj(email_obj, "x")
                utils.increment_all_campaign_action_metrics(
                    content_pk, param_pk, "b")
            elif event_type in EMAIL_SENT:
                utils.increment_all_campaign_action_metrics(
                    content_pk, param_pk, "s")
            elif event_type in EMAIL_DELIVERED:
                utils.increment_all_campaign_action_metrics(
                    content_pk, param_pk, "d")

    return response.Response({"status": "received"}, status=status.HTTP_200_OK)
