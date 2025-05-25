import logging

from django.conf import settings
from django.utils import timezone

from crm import models, services

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def retrieve_entity_emails(entity):
    entity_emails = models.EntityEmail.objects.filter(
        entity=entity).values_list('email_id', flat=True)
    logger.debug(
        f"Found {len(entity_emails)} emails linked to entity {entity.pk}")
    return entity_emails


def retrieve_email(entity_emails):
    twelve_weeks_ago = timezone.now() - timezone.timedelta(weeks=12)
    return models.Email.objects.filter(
        id__in=entity_emails,
        bounced=False,
        opted_out=False,
        last_emailed__lte=twelve_weeks_ago
    ).order_by("-last_emailed").first()


def retrieve_websites(entity):
    entity_websites = models.EntityWebsite.objects.filter(
        entity=entity).values_list('website_id', flat=True)
    return models.Website.objects.filter(id__in=entity_websites)


def retrieve_lighthouse_analysis(websites):
    return models.LighthouseAnalysis.objects.filter(
        website__in=websites
    ).order_by("-created_at").first()


def map_lighthouse_scores(lighthouse_analysis):

    data = lighthouse_analysis.data
    scores = data.get("scores", {})
    metric_score_map = {}

    for metric, score in scores.items():
        if score <= 50:
            metric_score_map[metric] = "l"
        elif score <= 90:
            metric_score_map[metric] = "m"
        else:
            metric_score_map[metric] = "h"

    return metric_score_map


def run():

    emails_sent = 0

    active_campaign_pks = models.Campaign.objects.filter(
        is_active=True).values_list('pk', flat=True)
    logger.debug(f"Found {len(active_campaign_pks)} active campaigns")

    leads = models.Lead.objects.filter(
        status__in=["a", None], campaign__in=active_campaign_pks)
    logger.debug(
        f"Fetched {leads.count()} leads with status 'a' or None in active campaigns")

    for lead in leads:
        logger.debug(f"Processing lead {lead.pk} for entity {lead.entity_id}")

        if not lead.campaign or not lead.campaign_search_param:
            logger.debug(
                f"Skipping lead {lead.pk} due to missing campaign or search param")
            continue

        entity = lead.entity
        entity_emails = retrieve_entity_emails(entity)
        if not entity_emails:
            continue

        email = retrieve_email(entity_emails)
        if not email:
            logger.debug(
                f"No eligible email found for entity {entity.pk}, skipping lead {lead.pk}")
            continue
        logger.debug(f"Selected email {email.email} for entity {entity.pk}")

        websites = retrieve_websites(entity)
        if not websites.exists():
            logger.debug(
                f"No websites found for entity {entity.pk}, skipping lead {lead.pk}")
            continue
        logger.debug(
            f"Found {websites.count()} websites for entity {entity.pk}")

        lighthouse_analysis = retrieve_lighthouse_analysis(websites)
        if not lighthouse_analysis:
            logger.debug(
                f"No LighthouseAnalysis found for websites of entity {entity.pk}, skipping")
            continue
        logger.debug(
            f"Using LighthouseAnalysis {lighthouse_analysis.pk} for entity {entity.pk}")

        metric_score_map = map_lighthouse_scores(lighthouse_analysis)

        logger.debug(
            f"Metric score map for lead {lead.pk}: {metric_score_map}")

        campaign = models.Campaign.objects.filter(pk=lead.campaign).first()
        if not campaign:
            logger.debug(
                f"Campaign {lead.campaign} not found, skipping lead {lead.pk}")
            continue

        email_content = models.EmailContent.objects.filter(
            campaign=campaign, stage="i").first()
        if not email_content:
            logger.debug(
                f"No email content found for campaign {campaign.pk} at stage 'i', skipping lead {lead.pk}")
            continue

        full_email_html = email_content.get_full_email(
            first_name=lead.first_name,
            metric_score_map=metric_score_map,
            link=lighthouse_analysis.report_url
        )
        logger.debug(f"Constructed full email HTML for lead {lead.pk}")

        search_param = models.CampaignSearchParameter.objects.filter(
            pk=lead.campaign_search_param).first()
        if not search_param:
            logger.debug(
                f"Search param {lead.campaign_search_param} not found, skipping lead {lead.pk}")
            continue
        try:
            response = services.send_email_via_brevo(
                email.email,
                email_content.subject,
                full_email_html,
                tags=[email_content.pk, search_param.pk]
            )
            print(f"RESPONSE: {response}")
            outreach = models.Outreach.objects.create(
                campaign_search_parameter=search_param, medium="e")
            models.OutreachEmail.objects.create(
                outreach=outreach, email=email)
        except Exception as e:
            logger.error("ERROR SENDING EMAIL: %s", e)

        emails_sent += 1
        logger.debug(f"Emails sent so far: {emails_sent}")

        if emails_sent >= 10:
            logger.debug("Reached limit of 10 emails sent, stopping run")
            break
