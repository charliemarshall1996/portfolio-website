import pytest
from crm.models import (
    Address, Email, Painpoint, PhoneNumber,
    SearchLocation, SearchTerm, Vertical, Website
)
from crm.utils import normalize_url


@pytest.mark.django_db
def test_address_str():
    address = Address.objects.create(
        line1="123 Test St",
        town="Testville",
        postcode="TE5 7ST"
    )
    assert str(address) == "123 Test St, Testville, TE5 7ST"


@pytest.mark.django_db
def test_email_model():
    email = Email.objects.create(email="test@example.com")
    assert str(email) == "test@example.com"
    assert email.opted_out is False
    assert email.bounced is False


@pytest.mark.django_db
def test_painpoint_model():
    vertical = Vertical.objects.create(name="SaaS")
    painpoint = Painpoint.objects.create(
        vertical=vertical, name="Slow onboarding", description="Too many steps"
    )
    assert painpoint.name == "Slow onboarding"
    assert painpoint.vertical == vertical


@pytest.mark.django_db
def test_phone_number_str():
    phone = PhoneNumber.objects.create(phone_number="0123456789", type="work")
    assert str(phone) == "0123456789 (work)"


@pytest.mark.django_db
def test_search_location_str():
    loc = SearchLocation.objects.create(type="to", name="Southampton")
    assert str(loc) == "Southampton"
    assert loc.type == "to"


@pytest.mark.django_db
def test_search_term_model():
    vertical = Vertical.objects.create(name="Fintech")
    term = SearchTerm.objects.create(vertical=vertical, term="payment gateway")
    assert str(term) == "payment gateway"
    assert term.vertical == vertical


@pytest.mark.django_db
def test_vertical_str():
    vertical = Vertical.objects.create(
        name="Health", description="Health sector")
    assert str(vertical) == "Health"


@pytest.mark.django_db
def test_website_str():
    site = Website.objects.create(url="https://example.com")
    assert str(site) == normalize_url("https://example.com")
