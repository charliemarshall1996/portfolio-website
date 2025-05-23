import pytest
from django.utils import timezone
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from faker import Faker
from crm import models

fake = Faker(locale="en_GB")


@pytest.fixture
def email_endpoint_required_data_factory():
    vertical = models.Vertical.objects.create(name="Fintech")
    term = "bank"
    location = models.SearchLocation.objects.create(
        type="to", name=fake.city())
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
    lead = models.Lead.objects.create(
        first_name=fake.file_name(), last_name=fake.last_name())
    email = models.Email.objects.create(
        email=fake.email()
    )
    outreach = models.Outreach.objects.create(
        campaign_search_parameter=param, date=timezone.now())
    email_outreach = models.OutreachEmail.objects.create(
        outreach=outreach, email=email)
    models.EntityEmail.objects.create(
        entity=lead.entity, email=email)
    content = models.EmailContent.objects.create(campaign=campaign)
    return param, lead, email, content, campaign


@pytest.fixture
def auth_client(db):
    user = User.objects.create_user(username="testuser", password="password")
    token = Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return client


@pytest.fixture
def param_factory():
    def factory():
        vertical = models.Vertical.objects.create(name="Fintech")
        term = "bank"
        location = models.SearchLocation.objects.create(
            type="to", name="London")
        search_term = models.SearchTerm.objects.create(
            vertical=vertical, term=term)
        campaign_type = "site_audit"
        campaign_medium = "email"
        campaign_start_date = timezone.now()
        campaign_end_date = campaign_start_date + timezone.timedelta(weeks=12)
        campaign = models.Campaign.objects.create(
            type=campaign_type, medium=campaign_medium, vertical=vertical, start_date=campaign_start_date, end_date=campaign_end_date)
        return models.CampaignSearchParameter.objects.create(
            campaign=campaign, location=location.name, search_term=search_term.term)
    return factory


@pytest.mark.django_db
def test_api_auth_view_returns_user_and_token(auth_client):
    response = auth_client.get("/api/auth/")
    assert response.status_code == 200
    assert "user" in response.data
    assert "auth" in response.data
    assert response.data["user"] == "testuser"
    assert response.data["auth"] is not None


@pytest.mark.django_db
def test_search_parameter_view_returns_data_and_updates_timestamp(auth_client, param_factory):
    param = param_factory()

    old_timestamp = param.last_run

    response = auth_client.get("/api/params/")
    assert response.status_code == 200
    assert response.data["id"] == param.id

    param.refresh_from_db()
    assert param.last_run != old_timestamp


@pytest.fixture
def api_client(db):
    user = User.objects.create_user(username="testuser", password="pass")
    token = Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return client


@pytest.mark.django_db
def test_receive_new_lead_creates_everything(api_client):
    response = api_client.post("/api/lead/", {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "Alice@example.com",
        "url": "https://example.com"
    })
    assert response.status_code == 200
    assert models.Email.objects.filter(email="alice@example.com").exists()
    assert models.Website.objects.filter(url="example.com").exists()
    assert models.Lead.objects.count() == 1
    lead = models.Lead.objects.first()
    assert lead.entity.emails.first().email.email == "alice@example.com"
    assert lead.entity.websites.first().website.url == "example.com"


@pytest.mark.django_db
def test_duplicate_lead_uses_existing_entity(api_client):
    api_client.post("/api/lead/", {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "Alice@example.com",
        "url": "https://example.com"
    })

    response = api_client.post("/api/lead/", {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "Alice@example.com",
        "url": "https://example.com"
    })

    assert response.status_code == 200
    assert models.Email.objects.count() == 1
    assert models.Website.objects.count() == 1
    assert models.Entity.objects.count() == 1
    assert models.Lead.objects.count() == 1


@pytest.mark.django_db
def test_receive_lead_with_existing_email_but_new_url(api_client):
    models.Email.objects.create(email="bob@example.com")

    response = api_client.post("/api/lead/", {
        "first_name": "Bob",
        "last_name": "Jones",
        "email": "bob@example.com",
        "url": "http://newsite.com"
    })

    assert response.status_code == 200
    assert models.Email.objects.count() == 1
    assert models.Website.objects.count() == 1
    assert models.Entity.objects.count() == 1
    assert models.Lead.objects.count() == 1


@pytest.mark.django_db
def test_receive_lead_with_existing_url_but_new_email(api_client):
    models.Website.objects.create(url="mydomain.com")

    response = api_client.post("/api/lead/", {
        "first_name": "Clara",
        "last_name": "Doe",
        "email": "clara@new.com",
        "url": "http://mydomain.com"
    })

    assert response.status_code == 200
    assert models.Email.objects.count() == 1
    assert models.Website.objects.count() == 1
    assert models.Entity.objects.count() == 1
    assert models.Lead.objects.count() == 1


@pytest.mark.django_db
def test_email_link_click(api_client, email_endpoint_required_data_factory):
    param, lead, email, content, campaign = email_endpoint_required_data_factory

    data = {
        "email": email.email,
        "event": "click",
        "tag": f"{param.pk},{content.pk}",
        "link": fake.url()
    }
    response = api_client.post("/api/email/", data)
    assert response.status_code == 200
    lead = models.Lead.objects.get(pk=lead.pk)
    email_content_metric = models.EmailContentMetric.objects.get(
        email_content=content, action="l")
    param_metric = models.CampaignSearchParameterMetric.objects.get(
        campaign_search_parameter=param, action="l"
    )
    campaign_metric = models.CampaignMetric.objects.get(
        campaign=campaign, action="l")
    assert email_content_metric.value == 1
    assert param_metric.value == 1
    assert campaign_metric.value == 1
    assert lead.status == "i"


@pytest.mark.django_db
def test_email_opt_out(api_client, email_endpoint_required_data_factory):
    param, lead, email, content, campaign = email_endpoint_required_data_factory
    data = {
        "email": email.email,
        "event": "spam",
        "tag": f"{param.pk},{content.pk}"
    }
    response = api_client.post("/api/email/", data)
    assert response.status_code == 200
    lead = models.Lead.objects.get(pk=lead.pk)
    email_content_metric = models.EmailContentMetric.objects.get(
        email_content=content, action="x")
    param_metric = models.CampaignSearchParameterMetric.objects.get(
        campaign_search_parameter=param, action="x"
    )
    campaign_metric = models.CampaignMetric.objects.get(
        campaign=campaign, action="x")
    email = email.email
    email_obj = models.Email.objects.get(email=email)
    assert email_content_metric.value == 1
    assert param_metric.value == 1
    assert campaign_metric.value == 1
    assert email_obj.opted_out
    assert lead.status == "x"


@pytest.mark.django_db
def test_email_bounce(api_client, email_endpoint_required_data_factory):
    param, lead, email, content, campaign = email_endpoint_required_data_factory
    data = {
        "email": email.email,
        "event": "hard_bounce",
        "tag": f"{param.pk},{content.pk}"
    }
    response = api_client.post("/api/email/", data)
    assert response.status_code == 200
    lead = models.Lead.objects.get(pk=lead.pk)
    email_content_metric = models.EmailContentMetric.objects.get(
        email_content=content, action="b")
    param_metric = models.CampaignSearchParameterMetric.objects.get(
        campaign_search_parameter=param, action="b"
    )
    campaign_metric = models.CampaignMetric.objects.get(
        campaign=campaign, action="b")
    email = email.email
    email_obj = models.Email.objects.get(email=email)
    assert email_content_metric.value == 1
    assert param_metric.value == 1
    assert campaign_metric.value == 1
    assert email_obj.bounced
    assert lead.status == "x"
