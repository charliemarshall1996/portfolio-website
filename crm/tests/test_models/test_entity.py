import pytest
from django.utils.timezone import now
from crm.models import (
    Entity, Company, Contact, Lead,
    EntityEmail, EntityAddress, EntityPhoneNumber, EntityWebsite,
    EntitySearchLocation, EntityVertical, EntityContact,
    Email, Address, PhoneNumber, Website,
    SearchLocation, Vertical
)


@pytest.mark.django_db
def test_entity_creation():
    entity = Entity.objects.create(name="Test Entity")
    assert entity.name == "Test Entity"
    assert isinstance(entity.created_at, type(now()))


@pytest.mark.django_db
def test_company_str():
    entity = Entity.objects.create(name="Company Entity")
    company = Company.objects.create(name="Acme Ltd", entity=entity)
    assert str(company) == "Acme Ltd"


@pytest.mark.django_db
def test_contact_str():
    contact = Contact.objects.create(first_name="Jane", last_name="Doe")
    assert str(contact) == "Jane Doe"


@pytest.mark.django_db
def test_lead_creation():
    entity = Entity.objects.create(name="Lead Entity")
    lead = Lead.objects.create(
        salutation="ms",
        first_name="Alice",
        last_name="Smith",
        job_title="CTO",
        status="interested",
        entity=entity
    )
    assert lead.status == "interested"
    assert lead.entity == entity


@pytest.mark.django_db
def test_entity_email_uniqueness():
    entity = Entity.objects.create(name="Email Entity")
    email = Email.objects.create(email="lead@test.com")
    ee = EntityEmail.objects.create(entity=entity, email=email)
    ee.save()
    with pytest.raises(Exception):
        EntityEmail.objects.create(entity=entity, email=email)


@pytest.mark.django_db
def test_entity_address_uniqueness():
    entity = Entity.objects.create(name="Addr Entity")
    address = Address.objects.create(
        line1="10 Main St", town="Town", postcode="AA1 1AA")
    EntityAddress.objects.create(entity=entity, address=address)
    with pytest.raises(Exception):
        EntityAddress.objects.create(entity=entity, address=address)


@pytest.mark.django_db
def test_entity_phone_number_uniqueness():
    entity = Entity.objects.create(name="Phone Entity")
    phone = PhoneNumber.objects.create(phone_number="01234567890")
    EntityPhoneNumber.objects.create(entity=entity, phone_number=phone)
    with pytest.raises(Exception):
        EntityPhoneNumber.objects.create(entity=entity, phone_number=phone)


@pytest.mark.django_db
def test_entity_website_uniqueness():
    entity = Entity.objects.create(name="Site Entity")
    site = Website.objects.create(url="https://test.com")
    EntityWebsite.objects.create(entity=entity, website=site)
    with pytest.raises(Exception):
        EntityWebsite.objects.create(entity=entity, website=site)


@pytest.mark.django_db
def test_entity_search_location_uniqueness():
    entity = Entity.objects.create(name="Loc Entity")
    loc = SearchLocation.objects.create(type="to", name="Southampton")
    EntitySearchLocation.objects.create(entity=entity, location=loc)
    with pytest.raises(Exception):
        EntitySearchLocation.objects.create(entity=entity, location=loc)


@pytest.mark.django_db
def test_entity_vertical_uniqueness():
    entity = Entity.objects.create(name="Vert Entity")
    vert = Vertical.objects.create(name="Healthcare")
    EntityVertical.objects.create(entity=entity, vertical=vert)
    with pytest.raises(Exception):
        EntityVertical.objects.create(entity=entity, vertical=vert)


@pytest.mark.django_db
def test_entity_contact_uniqueness():
    entity = Entity.objects.create(name="Contacted Entity")
    contact = Contact.objects.create(first_name="John", last_name="Doe")
    EntityContact.objects.create(entity=entity, contact=contact)
    with pytest.raises(Exception):
        EntityContact.objects.create(entity=entity, contact=contact)
