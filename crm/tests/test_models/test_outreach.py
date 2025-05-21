import pytest
from django.utils import timezone
from crm.models import (
    Outreach, OutreachEmail, OutreachWebsite,
    Email, Website, CampaignSearchParameter, Vertical, SearchLocation, SearchTerm, Campaign
)


def create_param():
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
    return CampaignSearchParameter.objects.create(
        campaign=campaign, location=location.name, search_term=search_term.term)


@pytest.mark.django_db
def test_outreach_creation():
    param = create_param()
    outreach = Outreach.objects.create(
        campaign_search_parameter=param,
        date=timezone.now(),
        medium="p"
    )
    assert outreach.medium == "p"
    assert outreach.campaign_search_parameter == param


@pytest.mark.django_db
def test_outreach_email_link():
    param = create_param()
    outreach = Outreach.objects.create(
        campaign_search_parameter=param,
        date=timezone.now(),
        medium="e"
    )
    email = Email.objects.create(email="contact@example.com")
    oe = OutreachEmail.objects.create(outreach=outreach, email=email)
    assert oe.outreach == outreach
    assert oe.email == email


@pytest.mark.django_db
def test_outreach_website_link():
    param = create_param()
    outreach = Outreach.objects.create(
        campaign_search_parameter=param,
        date=timezone.now(),
        medium="w"
    )
    website = Website.objects.create(url="https://example.com")
    ow = OutreachWebsite.objects.create(outreach=outreach, website=website)
    assert ow.outreach == outreach
    assert ow.website == website
