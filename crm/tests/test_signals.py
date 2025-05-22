
from faker import Faker
import pytest

from crm.models import (Contact, Company, Lead)

faker = Faker()


@pytest.mark.django_db
def test_entity_created_on_contact_creation():
    first_name = faker.first_name()
    last_name = faker.last_name()
    entity_name = f"{first_name} {last_name}"
    job_title = faker.job()
    contact = Contact.objects.create(
        first_name=first_name, last_name=last_name, job_title=job_title)
    contact.save()
    assert contact.entity
    assert contact.entity.name == entity_name


@pytest.mark.django_db
def test_entity_created_on_company_creation():
    name = faker.company()
    company = Company.objects.create(name=name)
    assert company.entity
    assert company.entity.is_company
    assert company.entity.name == name


@pytest.mark.django_db
def test_entity_created_on_lead_creation():
    first_name = faker.first_name()
    last_name = faker.last_name()
    entity_name = f"{first_name} {last_name}"
    job_title = faker.job()
    lead = Lead.objects.create(
        first_name=first_name, last_name=last_name, job_title=job_title)
    assert lead.entity
    assert lead.entity.name == entity_name
