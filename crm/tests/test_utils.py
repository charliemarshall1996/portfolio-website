
import pytest

from faker import Faker

from crm import utils, models

faker = Faker()


def campaign_search_location_factory(campaign: models.Campaign, location: models.SearchLocation):
    campaign_location = models.CampaignSearchLocation(
        campaign=campaign, location=location)
    campaign_location.save()
    campaign.save()


def campaign_factory(vertical):
    campaign = models.Campaign(vertical=vertical)
    campaign.save()
    return campaign


def parameter_factory(vertical=None):
    term = faker.job()
    name = faker.job()
    if not vertical:
        vertical = models.Vertical.objects.create(name=term)

    term = models.SearchTerm.objects.create(
        term=term, vertical=vertical)
    location = models.SearchLocation.objects.create(name=name)

    return vertical, location, term


@pytest.mark.django_db
def test_get_search_param():
    vertical, location1, term1 = parameter_factory()
    vertical, location2, term2 = parameter_factory(vertical=vertical)
    campaign = campaign_factory(vertical)
    campaign_search_location_factory(campaign, location1)
    campaign_search_location_factory(campaign, location2)
    param1 = models.CampaignSearchParameter.objects.filter(
        campaign=campaign, location=location1.name, search_term=term1.term).first()
    param2 = models.CampaignSearchParameter.objects.filter(
        campaign=campaign, location=location2.name, search_term=term2.term).first()
