
import pytest
from django.utils import timezone
from crm.models import (Campaign, CampaignSearchParameter,
                        CampaignSearchLocation, Vertical, SearchLocation, SearchTerm)


@pytest.mark.django_db
def test_campaign_creation():
    vertical = Vertical.objects.create(name="SaaS")
    campaign_type = "site_audit"
    campaign_medium = "email"
    campaign_start_date = timezone.now()
    campaign_end_date = campaign_start_date + timezone.timedelta(weeks=12)
    campaign = Campaign.objects.create(
        type=campaign_type, medium=campaign_medium, vertical=vertical, start_date=campaign_start_date, end_date=campaign_end_date)

    assert campaign.type == campaign_type
    assert campaign.medium == campaign_medium
    assert campaign.start_date == campaign.start_date
    assert campaign.end_date == campaign.end_date
    assert campaign.vertical == vertical


@pytest.mark.django_db
def test_campaign_search_parameter():
    vertical = Vertical.objects.create(name="Fintech")
    term = "bank"
    location = SearchLocation.objects.create(type="to", name="London")
    search_term = SearchTerm.objects.create(vertical=vertical, term=term)
    campaign_type = "site_audit"
    campaign_medium = "email"
    campaign_start_date = timezone.now()
    campaign_end_date = campaign_start_date + timezone.timedelta(weeks=12)
    campaign = Campaign.objects.create(
        type=campaign_type, medium=campaign_medium, vertical=vertical, start_date=campaign_start_date, end_date=campaign_end_date)
    param = CampaignSearchParameter.objects.create(
        campaign=campaign, location=location.name, search_term=search_term.term)
    assert param.campaign == campaign
    assert param.location == location.name
    assert param.search_term == search_term.term


@pytest.mark.django_db
def test_campaign_location():
    vertical = Vertical.objects.create(name="Health")
    campaign_type = "site_audit"
    campaign_medium = "email"
    campaign_start_date = timezone.now()
    campaign_end_date = campaign_start_date + timezone.timedelta(weeks=12)
    campaign = Campaign.objects.create(
        type=campaign_type, medium=campaign_medium, vertical=vertical, start_date=campaign_start_date, end_date=campaign_end_date)
    location = SearchLocation.objects.create(type="to", name="London")
    camp_loc = CampaignSearchLocation.objects.create(
        campaign=campaign, location=location)
    assert camp_loc.location == location
    assert camp_loc.campaign == campaign
