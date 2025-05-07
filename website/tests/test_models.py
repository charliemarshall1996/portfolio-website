
import pytest

from website import models


@pytest.mark.django_db
def test_website():
    contact_id = 1
    website_id = 1
    url = "https://www.charlie-marshall.dev"
    website = models.Website(contact_id=contact_id,
                             website_id=website_id, url=url)
    website.save()

    assert website.website_id == website_id
    assert website.contact_id == contact_id
    assert website.url == url


@pytest.mark.django_db
def test_analysis():
    contact_id = 1
    website_id = 1
    url = "https://www.charlie-marshall.dev"
    website = models.Website(contact_id=contact_id,
                             website_id=website_id, url=url)
    website.save()

    data = {"test": {}}
    analysis = models.Analysis(website=website, data=data)
    analysis.save()

    assert analysis.data == data
    assert analysis.website == website
