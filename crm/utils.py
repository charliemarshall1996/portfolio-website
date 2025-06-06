import logging
from itertools import product
from django.utils import timezone

from . import models

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def sync_campaign_search_parameters(campaign: models.Campaign):
    """Updates CampaignSearchParameters.is_active value campaign values."""
    existing_search_terms = list(models.SearchTerm.objects.filter(
        vertical=campaign.vertical))
    logger.debug("Existing search terms %s", existing_search_terms)
    existing_locations = set(
        campaign.search_locations.values_list("location_id", flat=True)
    )
    logger.debug("Existing locations %s", existing_locations)
    existing_locations = [
        models.SearchLocation.objects.filter(pk=pk).first() for pk in existing_locations
    ]
    existing_params = models.CampaignSearchParameter.objects.filter(
        campaign=campaign)
    params_location_map = {p.location: p for p in existing_params}
    params_search_term_map = {p.search_term: p for p in existing_params}
    logger.debug("Params location map: %s", params_location_map)
    logger.debug("Params search term map: %s", params_search_term_map)
    logger.debug("Iterating over existing locations...")
    for l, st in product(existing_locations, existing_search_terms):
        logger.debug("Checking combo: %s, %s", l, st)
        param, created = models.CampaignSearchParameter.objects.get_or_create(
            campaign=campaign, location=l.name, search_term=st.term, location_pk=l.pk, search_term_pk=st.pk
        )
        param.is_active = True
        param.save(update_fields=["is_active"])

    for l in existing_locations:
        logger.debug("Checking location: %s", l)
        if l.name not in params_location_map.keys():
            logger.debug("Location %s is in location param map", l)
            for st.term in existing_search_terms:
                logger.debug("Search term %s is in search term param map", st)
                param, created = models.CampaignSearchParameter.objects.get_or_create(
                    campaign=campaign, location=l.name, search_term=st.term, location_pk=l.pk, search_term_pk=st.pk
                )
                if created:
                    logger.debug(
                        "Search term created for location: %s, search term: %s", l, st
                    )
                param.is_active = True
                param.save(update_fields=["is_active"])
                logger.debug("Param saved.")

    flattened_search_terms = [st.term for st in existing_search_terms]
    for key, val in params_search_term_map.items():
        if key not in flattened_search_terms and val.is_active:
            val.is_active = False
            val.save(update_fields=["is_active"])

    flattened_locations = [l.name for l in existing_locations]
    for key, val in params_location_map.items():
        if key not in flattened_locations and val.is_active:
            val.is_active = False
            val.save(update_fields=["is_active"])


def sync_search_terms_parameters(search_term: models.SearchTerm):
    params = list(models.CampaignSearchParameter.objects.filter(
        search_term_pk=search_term.pk))
    for p in params:
        p.search_term = search_term.term
        p.save()


def sync_vertical_parameters(vertical: models.Vertical):
    for search_term in list(models.SearchTerm.objects.filter(vertical=vertical)):
        sync_campaign_search_parameters(search_term)


def sync_campaign_is_active_end_date(campaign: models.Campaign):
    """Updates Campaign is_active value based on end_date value."""
    if campaign.end_date:
        if timezone.now() > campaign.end_date and campaign.is_active:
            campaign.is_active = False
            campaign.save(update_fields=["is_active"])


def sync_locations_parameters(location: models.SearchLocation):
    params = list(models.CampaignSearchParameter.objects.filter(
        location_pk=location.pk))
    for p in params:
        p.location = location.name
        p.save()


def normalize_email(email: str):
    return email.strip().lower()


def normalize_url(url: str):
    return (
        url.strip().lower().replace("https://", "").replace("http://", "").rstrip("/")
    )


def get_lead_from_email_obj(email_obj: models.Email) -> models.Lead:
    entity_email = models.EntityEmail.objects.filter(email=email_obj).first()
    entity = models.Entity.objects.get(pk=entity_email.entity.pk)
    return models.Lead.objects.get(entity=entity)


def update_lead_status_from_email_obj(email_obj: models.Email, status: str):
    lead = get_lead_from_email_obj(email_obj)
    lead.status = status
    lead.save()


def create_email_engagement(
    engagement: models.Engagement, email: str, engagement_type: str
):
    models.EmailEngagement.objects.create(
        engagement=engagement, email=email, type=engagement_type
    )


def create_web_engagement(
    engagement: models.Engagement, url: str, engagement_type: str
):
    models.WebEngagement.objects.create(
        engagement=engagement, url=url, type=engagement_type
    )


def opt_out_email_obj(email_obj: models.Email):
    email_obj.opted_out = True
    email_obj.save(update_fields=["opted_out"])


def bounce_email_obj(email_obj: models.Email):
    email_obj.bounced = True
    email_obj.save(update_fields=["bounced"])


def increment_campaign_search_parameter_metric(
    param: models.CampaignSearchParameter, metric: str
):
    param_metric, created = models.CampaignSearchParameterMetric.objects.get_or_create(
        campaign_search_parameter=param, metric=metric
    )
    param_metric.value = param_metric.value + 1
    param_metric.save(update_fields=["value"])


def increment_metric(obj, action: str, owner):
    if owner == "p":
        metric, _ = models.CampaignSearchParameterMetric.objects.get_or_create(
            campaign_search_parameter=obj, action=action
        )
    elif owner == "e":
        metric, _ = models.EmailContentMetric.objects.get_or_create(
            email_content=obj, action=action
        )
    elif owner == "c":
        metric, _ = models.CampaignMetric.objects.get_or_create(
            campaign=obj, action=action
        )

    if metric:
        metric.value = metric.value + 1
        metric.save(update_fields=["value"])


def increment_all_campaign_action_metrics(email_content_pk, param_pk, action, incl_email_content=True):
    params = models.CampaignSearchParameter.objects.get(pk=param_pk)
    campaign = params.campaign
    increment_metric(campaign, action, owner="c")
    increment_metric(params, action, owner="p")
    if incl_email_content:
        content = models.EmailContent.objects.get(pk=email_content_pk)
        increment_metric(content, action, owner="e")


def get_campaign_pk_from_search_param(search_param: models.CampaignSearchParameter):
    return search_param.campaign.pk


def get_search_term_pk_from_search_param(search_param: models.CampaignSearchParameter):
    campaign = search_param.campaign
    vertical = campaign.vertical
    search_term = models.SearchTerm.objects.get(
        vertical=vertical, term=search_param.search_term)
    return search_term.pk


def get_location_pk_from_search_param(search_param: models.CampaignSearchParameter):
    campaign_locations = models.CampaignSearchLocation.objects.filter(
        campaign=search_param.campaign
    )
    name_to_pk = {
        cl.location.name: cl.location.pk for cl in campaign_locations
    }
    return name_to_pk.get(search_param.location, 0)


def get_vertical_pk_from_search_params(search_param: models.CampaignSearchParameter):
    campaign = search_param.campaign
    vertical = campaign.vertical
    return vertical.pk
