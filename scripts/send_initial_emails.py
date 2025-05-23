import logging

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings
from django.utils import timezone
import brevo_python
from brevo_python.rest import ApiException
from pprint import pprint

from crm import models

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def send_email_via_brevo(to_email, subject, html_content, tag=None, from_email=None, from_name=None):

    # Configure API key authorization: api-key
    configuration = brevo_python.Configuration()
    configuration.api_key['api-key'] = settings.BREVO_API_KEY

    # create an instance of the API class
    api_instance = brevo_python.TransactionalEmailsApi(
        brevo_python.ApiClient(configuration))
    send_smtp_email = brevo_python.SendSmtpEmail(to=[{"email": to_email}], subject=subject, html_content=html_content, sender={
                                                 "name": "Charlie Marshall", "email": from_email}, tags=[tag])

    try:
        # Send a transactional email
        api_response = api_instance.send_transac_email(send_smtp_email)
        logger.info("API RESPONSE: %s", api_response)
        return api_response
    except ApiException as e:
        logger.error(
            "Exception when calling TransactionalEmailsApi->send_transac_email: %s\n", e)


def run():
    twelve_weeks_ago = timezone.now() - timezone.timedelta(weeks=12)
    logger.debug(
        f"Emails must have last_emailed <= {twelve_weeks_ago} to be eligible")

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

        entity = lead.entity

        if not lead.campaign or not lead.campaign_search_param:
            logger.debug(
                f"Skipping lead {lead.pk} due to missing campaign or search param")
            continue

        entity_emails = models.EntityEmail.objects.filter(
            entity=entity).values_list('email_id', flat=True)
        logger.debug(
            f"Found {len(entity_emails)} emails linked to entity {entity.pk}")

        email = models.Email.objects.filter(
            id__in=entity_emails,
            bounced=False,
            opted_out=False,
            last_emailed__lte=twelve_weeks_ago
        ).order_by("-last_emailed").first()
        if not email:
            logger.debug(
                f"No eligible email found for entity {entity.pk}, skipping lead {lead.pk}")
            continue
        logger.debug(f"Selected email {email.email} for entity {entity.pk}")

        entity_websites = models.EntityWebsite.objects.filter(
            entity=entity).values_list('website_id', flat=True)
        websites = models.Website.objects.filter(id__in=entity_websites)
        if not websites.exists():
            logger.debug(
                f"No websites found for entity {entity.pk}, skipping lead {lead.pk}")
            continue
        logger.debug(
            f"Found {websites.count()} websites for entity {entity.pk}")

        lighthouse_analysis = models.LighthouseAnalysis.objects.filter(
            website__in=websites
        ).order_by("-created_at").first()
        if not lighthouse_analysis:
            logger.debug(
                f"No LighthouseAnalysis found for websites of entity {entity.pk}, skipping")
            continue
        logger.debug(
            f"Using LighthouseAnalysis {lighthouse_analysis.pk} for entity {entity.pk}")

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
            response = send_email_via_brevo(
                to_email=email.email,
                subject=email_content.subject,
                html_content=full_email_html,
                tag=f"{email_content.pk},{search_param.pk}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                from_name="Charlie Marshall"
            )
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
