
import pytest
from django.utils import timezone

from crm import services, models


@pytest.mark.django_db
def test_campaign_creation():
    vertical = models.Vertical.objects.create(name="SaaS")
    campaign_type = "site_audit"
    campaign_medium = "email"
    campaign_start_date = timezone.now()
    campaign_end_date = campaign_start_date + timezone.timedelta(weeks=12)
    campaign = models.Campaign.objects.create(
        type=campaign_type, medium=campaign_medium, vertical=vertical, start_date=campaign_start_date, end_date=campaign_end_date)

    assert campaign.type == campaign_type
    assert campaign.medium == campaign_medium
    assert campaign.start_date == campaign.start_date
    assert campaign.end_date == campaign.end_date
    assert campaign.vertical == vertical


@pytest.mark.django_db
def test_campaign_search_parameter():
    vertical = models.Vertical.objects.create(name="Fintech")
    term = "bank"
    location = models.SearchLocation.objects.create(type="to", name="London")
    search_term = models.SearchTerm.objects.create(
        vertical=vertical, term=term)
    campaign_type = "site_audit"
    campaign_medium = "email"
    campaign_start_date = timezone.now()
    campaign_end_date = campaign_start_date + timezone.timedelta(weeks=12)
    campaign = models.Campaign.objects.create(
        type=campaign_type, medium=campaign_medium, vertical=vertical, start_date=campaign_start_date, end_date=campaign_end_date)
    param = models.CampaignSearchParameter.objects.create(
        campaign=campaign, location=location.name, search_term=search_term.term)
    assert param.campaign == campaign
    assert param.location == location.name
    assert param.search_term == search_term.term


@pytest.mark.django_db
def test_campaign_location():
    vertical = models.Vertical.objects.create(name="Health")
    campaign_type = "site_audit"
    campaign_medium = "email"
    campaign_start_date = timezone.now()
    campaign_end_date = campaign_start_date + timezone.timedelta(weeks=12)
    campaign = models.Campaign.objects.create(
        type=campaign_type, medium=campaign_medium, vertical=vertical, start_date=campaign_start_date, end_date=campaign_end_date)
    location = models.SearchLocation.objects.create(type="to", name="London")
    camp_loc = models.CampaignSearchLocation.objects.create(
        campaign=campaign, location=location)
    assert camp_loc.location == location
    assert camp_loc.campaign == campaign


@pytest.mark.django_db
def test_email_content_str():

    vertical = models.Vertical.objects.create(name="Fintech")
    campaign_type = "site_audit"
    campaign_medium = "email"
    campaign_start_date = timezone.now()
    campaign_end_date = campaign_start_date + timezone.timedelta(weeks=12)
    campaign = models.Campaign.objects.create(
        type=campaign_type, medium=campaign_medium, vertical=vertical, start_date=campaign_start_date, end_date=campaign_end_date)

    email_content = models.EmailContent.objects.create(
        campaign=campaign, stage="i", subject="test", intro="test", greeting="test", main="test", closing="test", farewell="test")

    email_content_string = str(email_content)
    assert email_content_string == f"EmailContent for {campaign.pk}"


@pytest.mark.django_db
def test_email_content_get_full_email_initial():

    vertical = models.Vertical.objects.create(name="Fintech")
    campaign_type = "site_audit"
    campaign_medium = "email"
    campaign_start_date = timezone.now()
    campaign_end_date = campaign_start_date + timezone.timedelta(weeks=12)
    campaign = models.Campaign.objects.create(
        type=campaign_type, medium=campaign_medium, vertical=vertical, start_date=campaign_start_date, end_date=campaign_end_date)

    subject = "Test"
    greeting = "Hi"
    intro = "This is a test intro."
    closing = "This is a test close message."
    farewell = "Goodbye,"

    bullet_seo = "seo is great."
    bullet_accessibility = "accessibility is poor."
    bullet_performance = "performance is poor."
    bullet_best_practices = "best practices could be better."

    link_text = "My Website"
    email_content = models.EmailContent.objects.create(
        campaign=campaign, stage="i", subject=subject, intro=intro, greeting=greeting, main="test", closing=closing, farewell=farewell, link_text=link_text)

    b1 = models.BulletContent.objects.create(
        email_content=email_content, metric="seo", score_range="h", content=bullet_seo)
    b2 = models.BulletContent.objects.create(
        email_content=email_content, metric="accessibility", score_range="l", content=bullet_accessibility)
    b3 = models.BulletContent.objects.create(
        email_content=email_content, metric="performance", score_range="l", content=bullet_performance)
    b4 = models.BulletContent.objects.create(
        email_content=email_content, metric="best_practices", score_range="m", content=bullet_best_practices)

    score_map = {"seo": "h", "accessibility": "l",
                 "performance": "l", "best_practices": "m"}
    bullet_items = [b1, b2, b3, b4]
    link = "https://www.charlie-marshall.dev"
    first_name = "Charlie"

    expected_message = services.retrieve_initial_email(
        first_name, link, link_text, bullet_items, greeting, intro, closing, farewell)

    actual_message = email_content.get_full_email(first_name, link, score_map)

    assert expected_message == actual_message
    assert str(b1) == "seo h"
    assert str(b2) == "accessibility l"
    assert str(b3) == "performance l"
    assert str(b4) == "best_practices m"


@pytest.mark.django_db
def test_email_content_get_full_email_follow_up():

    vertical = models.Vertical.objects.create(name="Fintech")
    campaign_type = "site_audit"
    campaign_medium = "email"
    campaign_start_date = timezone.now()
    campaign_end_date = campaign_start_date + timezone.timedelta(weeks=12)
    campaign = models.Campaign.objects.create(
        type=campaign_type, medium=campaign_medium, vertical=vertical, start_date=campaign_start_date, end_date=campaign_end_date)

    subject = "Test"
    greeting = "Hi"
    intro = "This is a test intro."
    main = "This is test content."
    closing = "This is a test close message."
    farewell = "Goodbye,"

    link_text = "My Website"
    email_content = models.EmailContent.objects.create(
        campaign=campaign, stage="f", subject=subject, intro=intro, greeting=greeting, main=main, closing=closing, farewell=farewell, link_text=link_text)

    link = "https://www.charlie-marshall.dev"
    first_name = "Charlie"

    expected_message = services.retrieve_follow_up_email(
        first_name, link, link_text, main, greeting, intro, closing, farewell)

    actual_message = email_content.get_full_email(first_name, link)

    assert expected_message == actual_message
