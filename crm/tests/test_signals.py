
from django.utils import timezone
from faker import Faker
import pytest

from crm import models

faker = Faker()


@pytest.mark.django_db
def test_entity_created_on_contact_creation():
    first_name = faker.first_name()
    last_name = faker.last_name()
    entity_name = f"{first_name} {last_name}"
    job_title = faker.job()
    contact = models.Contact.objects.create(
        first_name=first_name, last_name=last_name, job_title=job_title)
    contact.save()
    assert contact.entity
    assert contact.entity.name == entity_name


@pytest.mark.django_db
def test_entity_created_on_company_creation():
    name = faker.company()
    company = models.Company.objects.create(name=name)
    assert company.entity
    assert company.entity.is_company
    assert company.entity.name == name


@pytest.mark.django_db
def test_entity_created_on_lead_creation():
    first_name = faker.first_name()
    last_name = faker.last_name()
    entity_name = f"{first_name} {last_name}"
    job_title = faker.job()
    lead = models.Lead.objects.create(
        first_name=first_name, last_name=last_name, job_title=job_title)
    assert lead.entity
    assert lead.entity.name == entity_name


@pytest.mark.django_db
def test_campaign_search_parameter_updates_on_campaign_save():
    term = "test"
    name = "test"
    vertical = models.Vertical.objects.create(name="test")
    search_term = models.SearchTerm.objects.create(
        term=term, vertical=vertical)
    location = models.SearchLocation.objects.create(name=name)
    campaign = models.Campaign(vertical=vertical)
    campaign_location = models.CampaignSearchLocation(
        campaign=campaign, location=location)
    campaign.save()
    campaign_location.save()
    campaign.save()

    new_params = models.CampaignSearchParameter.objects.filter(
        campaign=campaign, location=name, search_term=term).first()
    assert new_params
    assert new_params.is_active

    campaign_location.delete()
    campaign.save()
    new_params = models.CampaignSearchParameter.objects.filter(
        campaign=campaign, location=name, search_term=term).first()
    assert not new_params.is_active


@pytest.mark.django_db
def test_campaign_is_active_updates_on_campaign_save():
    term = "test"
    name = "test"
    vertical = models.Vertical.objects.create(name="test")
    search_term = models.SearchTerm.objects.create(
        term=term, vertical=vertical)
    location = models.SearchLocation.objects.create(name=name)
    campaign = models.Campaign(vertical=vertical)
    campaign_location = models.CampaignSearchLocation(
        campaign=campaign, location=location)
    campaign.save()
    campaign_location.save()
    campaign.save()

    assert campaign.is_active

    campaign.end_date = (timezone.now() - timezone.timedelta(days=2))
    campaign.save()
    assert not campaign.is_active
