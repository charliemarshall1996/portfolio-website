from django.utils import timezone
import pytest

from crm import models


@pytest.mark.django_db
def test_company_model_valid():
    data = {
        'name': "ACME Corp.",
        'industry': 'Software',
        'website': 'https://test.com',
        'status': 'le'
    }

    company = models.Company(**data)

    assert company.name == data['name']
    assert company.industry == data['industry']
    assert company.website == data['website']
    assert company.status == data['status']


@pytest.mark.django_db
def test_contact_model_valid():
    company_data = {
        'name': "ACME Corp.",
        'industry': 'Software',
        'website': 'https://test.com',
        'status': 'le'
    }

    company = models.Company(**company_data)
    company.save()

    contact_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'job_title': 'Owner',
        'company': company
    }

    contact = models.Client(**contact_data)
    assert contact.first_name == contact_data['first_name']
    assert contact.last_name == contact_data['last_name']
    assert contact.job_title == contact_data['job_title']
    assert contact.company == contact_data['company']
