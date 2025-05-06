# blog/tasks.py
import logging
from celery import shared_task
from services.analyzer import WebsiteAnalyzer
from . import models

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@shared_task
def analyse_website_marketing(self):
    analyzer = WebsiteAnalyzer()
    websites = models.Website.objects.all()
    anayzed_websites = [a.website.pk for a in models.Analysis.objects.all()]

    for website in websites:
        if website.pk not in anayzed_websites:
            data = analyzer.run(website.url)
            analysis = models.Analysis.objects.create(
                website=website, data=data)
            analysis.save()
