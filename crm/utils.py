
import logging
from itertools import product
from django.utils import timezone

from . import models

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def sync_campaign_search_parameters(campaign: models.Campaign):
    """Updates CampaignSearchParameters.is_active value campaign values."""
    existing_search_terms = models.SearchTerm.objects.filter(
        vertical=campaign.vertical)
    existing_search_terms = [st.term for st in existing_search_terms]
    logger.debug("Existing search terms %s", existing_search_terms)
    existing_locations = set(
        campaign.search_locations.values_list(
            "location_id", flat=True)
    )
    logger.debug("Existing locations %s", existing_locations)
    existing_locations = [models.SearchLocation.objects.filter(
        pk=pk).first() for pk in existing_locations]
    existing_locations = [l.name for l in existing_locations]
    existing_params = models.CampaignSearchParameter.objects.filter(
        campaign=campaign)
    params_location_map = {p.location: p for p in existing_params}
    params_search_term_map = {p.search_term: p for p in existing_params}
    logger.debug("Params location map: %s", params_location_map)
    logger.debug("Params search term map: %s", params_search_term_map)
    logger.debug("Iterating over existing locations...")
    for l, st in product(existing_locations, existing_search_terms):
        logger.debug("Checking combo: %s, %s", l, st)
        param, created = models.CampaignSearchParameter.objects.get_or_create(campaign=campaign,
                                                                              location=l,
                                                                              search_term=st)
        param.is_active = True
        param.save(update_fields=['is_active'])

    for l in existing_locations:
        logger.debug("Checking location: %s", l)
        if l not in params_location_map.keys():
            logger.debug("Location %s is in location param map", l)
            for st in existing_search_terms:
                logger.debug(
                    "Search term %s is in search term param map", st)
                param, created = models.CampaignSearchParameter.objects.get_or_create(
                    location=l, search_term=st, campaign=campaign)
                if created:
                    logger.debug(
                        "Search term created for location: %s, search term: %s", l, st)
                param.is_active = True
                param.save(update_fields=["is_active"])
                logger.debug("Param saved.")

    for key, val in params_search_term_map.items():
        if key not in existing_search_terms and val.is_active:
            val.is_active = False
            val.save(update_fields=["is_active"])

    for key, val in params_location_map.items():
        if key not in existing_locations and val.is_active:
            val.is_active = False
            val.save(update_fields=["is_active"])


def sync_campaign_is_active_end_date(campaign: models.Campaign):
    """Updates Campaign is_active value based on end_date value."""
    if campaign.end_date:
        if timezone.now() > campaign.end_date and campaign.is_active:
            campaign.is_active = False
            campaign.save(update_fields=["is_active"])


def normalize_email(email: str):
    return email.strip().lower()


def normalize_url(url: str):
    return url.strip().lower().replace("https://", "").replace("http://", "").rstrip('/')


def get_lead_from_email_obj(email_obj: models.Email) -> models.Lead:
    entity_email = models.EntityEmail.objects.filter(
        email=email_obj).first()
    entity = models.Entity.objects.get(pk=entity_email.entity.pk)
    return models.Lead.objects.get(entity=entity)


def update_lead_status_from_email_obj(email_obj: models.Email, status: str):
    lead = get_lead_from_email_obj(email_obj)
    lead.status = status
    lead.save()


def create_email_engagement(engagement: models.Engagement, email: str, engagement_type: str):
    models.EmailEngagement.objects.create(
        engagement=engagement, email=email, type=engagement_type
    )


def create_web_engagement(engagement: models.Engagement, url: str, engagement_type: str):
    models.WebEngagement.objects.create(
        engagement=engagement, url=url, type=engagement_type
    )


def opt_out_email_obj(email_obj: models.Email):
    email_obj.opted_out = True
    email_obj.save(update_fields=["opted_out"])


def bounce_email_obj(email_obj: models.Email):
    email_obj.bounced = True
    email_obj.save(update_fields=["bounced"])


def increment_campaign_search_parameter_metric(param: models.CampaignSearchParameter, metric: str):
    param_metric, created = models.CampaignSearchParameterMetric.objects.get_or_create(
        campaign_search_parameter=param, metric=metric)
    param_metric.value = param_metric.value + 1
    param_metric.save(update_fields=["value"])


def increment_metric(obj, action: str, owner):
    if owner == "p":
        metric, _ = models.CampaignSearchParameterMetric.objects.get_or_create(
            campaign_search_parameter=obj, action=action)
    elif owner == "e":
        metric, _ = models.EmailContentMetric.objects.get_or_create(
            email_content=obj, action=action)
    elif owner == "c":
        metric, _ = models.CampaignMetric.objects.get_or_create(
            campaign=obj, action=action
        )

    if metric:
        metric.value = metric.value + 1
        metric.save(update_fields=["value"])


def increment_all_campaign_action_metrics(email_content_pk, param_pk, action):
    params = models.CampaignSearchParameter.objects.get(pk=param_pk)
    content = models.EmailContent.objects.get(pk=email_content_pk)
    campaign = params.campaign
    increment_metric(campaign, action, owner="c")
    increment_metric(params, action, owner="p")
    increment_metric(content, action, owner="e")
