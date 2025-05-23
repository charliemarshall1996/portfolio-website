import pytest
from faker import Faker
from django.utils import timezone
from crm import models
from scripts.send_initial_emails import run  # Adjust to your actual import path

fake = Faker()


@pytest.mark.django_db
def test_run_sends_emails_and_creates_outreach():
    # 1. Create active campaign
    campaign = models.Campaign.objects.create(is_active=True)

    search_param = models.CampaignSearchParameter.objects.create(
        campaign=campaign, location=fake.city(), search_term="test")

    # 2. Create entity and related objects
    entity = models.Entity.objects.create(name="Test Entity")

    # 3. Create lead linked to campaign and entity, with status "a"
    lead = models.Lead.objects.create(
        entity=entity,
        campaign_search_param=search_param.pk,
        campaign=campaign.pk,
        status="a",
        first_name=fake.first_name(),
        last_name=fake.last_name()
    )

    # 4. Create valid email for the entity with last_emailed > 12 weeks ago
    email = models.Email.objects.create(
        email="subnetix@gmail.com",
        bounced=False,
        opted_out=False,
        last_emailed=timezone.now() - timezone.timedelta(weeks=13)  # > 12 weeks ago
    )
    models.EntityEmail.objects.create(entity=entity, email=email)

    # 5. Create website and EntityWebsite linked to entity
    website = models.Website.objects.create(url="https://test.com")
    models.EntityWebsite.objects.create(entity=entity, website=website)

    # 6. Create LighthouseAnalysis with scores and report_url
    lighthouse_data = {
        "scores": {
            "seo": 40,         # low
            "performance": 85  # medium
        }
    }
    lighthouse_analysis = models.LighthouseAnalysis.objects.create(
        website=website,
        data=lighthouse_data,
        report_url="https://report.url"
    )

    # 7. Create EmailContent with a stub get_full_email method if needed
    email_content = models.EmailContent.objects.create(
        campaign=campaign,
        stage="i"
    )
    # You may need to monkeypatch get_full_email or provide a simple method:

    def dummy_get_full_email(first_name, metric_score_map, link):
        return f"Hello {first_name}, report: {link}"
    email_content.get_full_email = dummy_get_full_email

    # 8. Create CampaignSearchParameter referenced by the lead
    lead.campaign_search_param = search_param.pk
    lead.save()

    # 9. Save default from email in settings or patch it if needed
    # You can do: settings.DEFAULT_FROM_EMAIL = "from@example.com"

    # --- Run your function ---
    run()

    # --- Assertions ---
    # Check that Outreach and OutreachEmail were created
    outreach = models.Outreach.objects.filter(
        campaign_search_parameter=search_param).first()
    assert outreach is not None
    outreach_email = models.OutreachEmail.objects.filter(
        outreach=outreach, email=email).first()
    assert outreach_email is not None

    # Optional: Check that the email was sent (if you have some log or DB record)
    # Since no mocking, you can't assert API call directly.
