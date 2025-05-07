# website/tasks.py
import logging
from django.conf import settings
from website.services.analyzer import WebsiteAnalyzer
from website import models

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def run():
    if not settings.configured:
        settings.configure()
    print("Starting website analysis...")
    analyzer = WebsiteAnalyzer()
    websites = list(models.Website.objects.all())
    print("N WEBSITES: %s", str(len(websites)))
    anayzed_websites = [a.website.pk for a in models.Analysis.objects.all()]

    for website in websites:
        if website.pk not in anayzed_websites:
            print("Analyzing website %s", website.pk)
            data = analyzer.run(website.url)
            print("Website analyzed: %s", data)
            analysis = models.Analysis.objects.create(
                website=website, data=data)
            analysis.save()
            break
