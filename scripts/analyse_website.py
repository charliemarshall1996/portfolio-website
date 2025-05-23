# website/tasks.py
import logging
from django.conf import settings
from crm import models
from crm.services import LighthouseAnalysisClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def run():
    if not settings.configured:
        settings.configure()
    logger.info("Starting website analysis...")
    websites = list(models.Website.objects.all())
    logger.info("N WEBSITES: %s", str(len(websites)))
    anayzed_websites = [
        a.website.pk for a in models.LighthouseAnalysis.objects.all()]

    n_analysed = 0
    for website in websites:
        if website.pk not in anayzed_websites:
            client = LighthouseAnalysisClient()
            n_analysed += 1
            logger.info("Analyzing website %s", website.pk)
            data = client.run(website.url)
            logger.info("Website analyzed: %s", data)

            if data:
                analysis = models.LighthouseAnalysis.objects.create(
                    website=website, data=data)
                analysis.save()
                if n_analysed >= 10:
                    break
