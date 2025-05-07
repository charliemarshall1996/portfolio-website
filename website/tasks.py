# website/tasks.py
import logging
from celery import shared_task
from .services.analyzer import WebsiteAnalyzer
from . import models

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@shared_task
def analyse_website_marketing():
    logger.info("Starting website analysis...")
    analyzer = WebsiteAnalyzer()
    websites = list(models.Website.objects.all())
    logger.debug("N WEBSITES: %s", str(len(websites)))
    anayzed_websites = [a.website.pk for a in models.Analysis.objects.all()]

    for website in websites:
        if website.pk not in anayzed_websites:
            logger.info("Analyzing website %s", website.pk)
            data = analyzer.run(website.url)
            logger.debug("Website analyzed: %s", data)
            analysis = models.Analysis.objects.create(
                website=website, data=data)
            analysis.save()
            break
